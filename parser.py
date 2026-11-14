"""
Парсер объявлений об аренде жилья с kvartirant.ru

Использует: requests + BeautifulSoup4
Сайт: https://www.kvartirant.ru/Moskva/sniat-kvartiru/ (аренда квартир в Москве)

Сайт работает без CAPTCHA и доступен для прямого парсинга.

Принцип работы:
1. Загружаем страницу списка объявлений
2. Собираем уникальные ID объявлений (ссылки вида /23104684/)
3. Для каждого ID загружаем детальную страницу и извлекаем все поля
4. Сохраняем результат в src/data/listings.json
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.kvartirant.ru"
LIST_URL = f"{BASE_URL}/Moskva/sniat-kvartiru/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


@dataclass
class Listing:
    id: str
    title: str
    price: Optional[int]
    district: Optional[str]
    rooms: Optional[int]
    area: Optional[float]
    description: Optional[str]
    photos: list[str]
    source_url: Optional[str]


def fetch_html(url: str) -> Optional[str]:
    """Выполняет GET-запрос и возвращает HTML-текст страницы."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as exc:
        print(f"[!] Ошибка загрузки {url}: {exc}")
        return None


def parse_price(text: Optional[str]) -> Optional[int]:
    """Извлекает цену из строки вида '250 000 ₽' -> 250000."""
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def parse_rooms(text: Optional[str]) -> Optional[int]:
    """Извлекает количество комнат из строки."""
    if not text:
        return None
    text = text.strip().lower()
    if "студия" in text:
        return 1
    # "4-комнатную", "2-комнатную", "комнату"
    match = re.search(r"(\d+)\s*[- ]?комнат", text)
    if match:
        return int(match.group(1))
    if "комнату" in text:
        return 1
    return None


def parse_area(text: Optional[str]) -> Optional[float]:
    """Извлекает площадь из строки вида '140 м2' -> 140.0."""
    if not text:
        return None
    match = re.search(r"([\d]+[.,]?\d*)", text.replace(",", "."))
    return float(match.group(1)) if match else None


def find_element_containing(soup: BeautifulSoup, text_fragment: str) -> Optional[BeautifulSoup]:
    """Находит ближайший блочный элемент (span/div), текст которого содержит фрагмент."""
    for el in soup.find_all(string=lambda s: s and text_fragment in s):
        parent = el.parent
        if not parent:
            continue
        # Поднимаемся выше, пока не найдём span/div с полным текстом
        current = parent
        while current and current.name not in ("span", "div", "td", "li"):
            current = current.parent
        target = current or parent
        if target:
            return target
    return None


def extract_text_after_label(soup: BeautifulSoup, label: str) -> Optional[str]:
    """Извлекает текст после метки вида '<b>Метро:</b>' или '<b>Адрес:</b>'."""
    parent = find_element_containing(soup, label)
    if not parent:
        return None
    text = parent.get_text(" ", strip=True)
    # Убираем саму метку
    text = re.sub(rf"^{re.sub(r'[.*+?^${}()|[\]\\]', r'\\\g<0>', label)}:\s*", "", text, flags=re.IGNORECASE)
    if text.strip():
        return text.strip()
    return None


def collect_listing_ids(html: str) -> list[str]:
    """Собирает уникальные ID объявлений со страницы списка."""
    soup = BeautifulSoup(html, "html.parser")
    ids: list[str] = []
    seen = set()
    # Все ссылки вида /23104684/
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        m = re.fullmatch(r"/(\d+)/?", href)
        if m:
            lid = m.group(1)
            if lid not in seen:
                seen.add(lid)
                ids.append(lid)
    return ids


def parse_detail_page(html: str, listing_id: str) -> Optional[Listing]:
    """Парсит страницу отдельного объявления."""
    soup = BeautifulSoup(html, "html.parser")

    # Заголовок
    title_el = soup.select_one("h3")
    title = title_el.get_text(" ", strip=True) if title_el else "Без названия"

    # Цена из заголовка (span.nowrap.red внутри h3)
    price_el = soup.select_one("h3 span.nowrap.red, h3 span.red")
    price = parse_price(price_el.get_text(strip=True) if price_el else None)

    # Описание — первый <p> с контентом
    desc_el = soup.select_one("p")
    description = desc_el.get_text(" ", strip=True) if desc_el else None
    if description:
        description = re.sub(r"\[подробнее\.\.\.\]", "", description).strip()
        description = re.sub(r"Номер объекта:\s*\d+\.", "", description).strip()

    # Адрес
    address = extract_text_after_label(soup, "Адрес")
    district = None
    if address:
        parts = [p.strip() for p in address.split(",")]
        if len(parts) >= 2:
            district = parts[1]

    # Площадь — из элемента с "Площадь:"
    area_el = find_element_containing(soup, "Площадь:")
    area = None
    if area_el:
        area = parse_area(area_el.get_text(" ", strip=True))

    # Комнаты из заголовка
    rooms = parse_rooms(title)

    # Фото из галереи bxSlider
    photos: list[str] = []
    for img in soup.select("div.bxContainer ul.bxSlider li img, div.bxSlider li img"):
        src = img.get("src", "")
        if src and "no_photo" not in src:
            if not src.startswith("http"):
                src = BASE_URL + src
            if src not in photos:
                photos.append(src)

    return Listing(
        id=listing_id,
        title=title,
        price=price,
        district=district,
        rooms=rooms,
        area=area,
        description=description,
        photos=photos,
        source_url=f"{BASE_URL}/{listing_id}/",
    )


def main() -> None:
    print("=== Парсер объявлений kvartirant.ru ===")

    html = fetch_html(LIST_URL)
    if html is None:
        print("[!] Не удалось загрузить страницу списка.")
        return

    listing_ids = collect_listing_ids(html)
    print(f"[+] Найдено уникальных объявлений: {len(listing_ids)}")

    results: list[Listing] = []
    for i, lid in enumerate(listing_ids, 1):
        url = f"{BASE_URL}/{lid}/"
        detail_html = fetch_html(url)
        if detail_html:
            listing = parse_detail_page(detail_html, lid)
            if listing:
                results.append(listing)
                print(f"  [{i}/{len(listing_ids)}] {lid}: {listing.title[:50]}... price={listing.price}")
        time.sleep(1)

    out_path = Path("src/data/listings.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    data = [asdict(l) for l in results]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[+] Сохранено {len(data)} объявлений в {out_path}")


if __name__ == "__main__":
    main()
