# KN2_Parser — Доска объявлений об аренде жилья

Одностраничное приложение на Vue 3 для просмотра объявлений об аренде жилья с собственным парсером на Python. Взаимодействие фронтенда и парсера реализовано через HTTP API (FastAPI).

## ✅ Итоговая реализация

### 1. Парсер (`parser.py`)

- **Сайт:** `kvartirant.ru` — доска аренды недвижимости без CAPTCHA, доступна для прямого парсинга
- **Язык:** Python 3 + `requests` + `BeautifulSoup4`
- **Принцип работы:** загружает страницу списка `/Moskva/sniat-kvartiru/`, собирает уникальные ID объявлений, затем для каждого ID парсит детальную страницу (фото, описание, адрес, метро, площадь, комнаты)
- **Результат:** `src/data/listings.json` — 30 реальных объявлений с ценами от 33 000 до 250 000 ₽, все с описаниями, 29 с фотографиями, все с районами и площадями, адресом и метро
- **CLI-опции:** `python parser.py --limit 5` (спарсить только первые N), `python parser.py --out test.json` (сохранить в другой файл)

### 2. Бэкенд (`backend/main.py`, FastAPI)

Промежуточный сервис между фронтендом и парсером:

| Endpoint | Метод | Описание |
|---|---|---|
| `/listings` | `GET` | Возвращает все объявления из `src/data/listings.json` |
| `/run-parser` | `POST` | Запускает Python-парсер `parser.py` и обновляет `listings.json` |

CORS настроен на `http://localhost:5173` (Vue dev-сервер).

### 3. Vue-приложение (одна страница, без роутера)

- **Стек:** Vue 3 (Composition API), TypeScript, Pinia, Vite
- **Управление состоянием:** Pinia — стор объявлений (`listings.ts`) и стор избранного (`favorites.ts` с `localStorage`)
- **Переключение видов** (список / избранное / детальный просмотр) через флаг `view` в Pinia, без `vue-router`
- **Взаимодействие с бэкендом:** кнопка «Запустить парсер» в навигационной панели отправляет `POST` на `http://localhost:8000/run-parser`; после завершения свежие данные подтягиваются через `GET /listings` и обновляются в сторе **без перезагрузки страницы**. Если бэкенд не запущен — приложение работает со статическим `listings.json` из сборки

### 4. Реализованный функционал

| Возможность | Где реализовано |
|---|---|
| Поиск по названию | `SearchBar.vue` + фильтрация в `listings.ts` |
| Фильтрация по цене (от/до) | `FilterPanel.vue` |
| Фильтрация по комнатам | `FilterPanel.vue` |
| Фильтрация по району | `FilterPanel.vue` (выпадающий список из данных) |
| Счётчик найденных объявлений | `App.vue` — `{{ store.filteredListings.length }}` |
| Избранное (добавление/удаление) | `favorites.ts`, кнопка ♥ на карточках |
| Страница избранного | Переключение во вкладке навигации |
| Подробный просмотр | `ListingDetail.vue` со всеми полями и галереей фото |
| Сообщение при пустом результате | `EmptyState.vue` |
| Устойчивость к missing fields | `MissingField.vue` — "Цена не указана", "Описание отсутствует" и т.п. |
| Запуск парсера со страницы | Кнопка «Запустить парсер» в `App.vue` → FastAPI `/run-parser` |

### 5. Структура файлов

```
src/
├── main.ts              # Точка входа, инициализация Pinia + загрузка избранного из localStorage
├── App.vue              # Одна страница: навигация + переключение видов + кнопка запуска парсера
├── types/listing.ts     # TS-интерфейсы Listing, Filters
├── stores/
│   ├── listings.ts      # Все объявления, поиск, фильтры, счётчик, детальный просмотр
│   └── favorites.ts     # Избранное с localStorage
├── components/
│   ├── SearchBar.vue
│   ├── FilterPanel.vue
│   ├── ListingCard.vue
│   ├── ListingDetail.vue
│   ├── PhotoGallery.vue
│   ├── EmptyState.vue
│   └── MissingField.vue
├── data/
│   └── listings.json    # 30 реальных объявлений из kvartirant.ru
backend/
├── main.py              # FastAPI бэкенд: /listings (GET), /run-parser (POST)
parser.py                # Python-парсер (запускается бэкендом или отдельно)
requirements.txt         # Python-зависимости (requests, beautifulsoup4, fastapi, uvicorn)
```

### 6. Как запустить

Нужно запустить **два сервиса**:

**Терминал 0 — Python-зависимости (один раз):**
```bash
pip install -r requirements.txt
```

**Терминал 1 — бэкенд (FastAPI):**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
# Бэкенд будет доступен на http://localhost:8000
```

**Терминал 2 — фронтенд (Vue):**
```bash
npm run dev
# Приложение откроется на http://localhost:5173
```

После этого на странице появится кнопка **«Запустить парсер»**, которая инициирует сбор новых объявлений через бэкенд.

**Запуск парсера отдельно (без бэкенда):**
```bash
python parser.py
```

## Требования

- Node.js >= 22.18.0 (для Vite)
- Python 3 (для парсера и бэкенда)
- Python-пакеты: `requests`, `beautifulsoup4`, `fastapi`, `uvicorn`
