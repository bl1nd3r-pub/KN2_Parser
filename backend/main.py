cd"""
Бэкенд для доски объявлений об аренде жилья.

Endpoints:
  GET  /listings   — вернуть все объявления из src/data/listings.json
  POST /run-parser — запустить Python-парсер kvartirant.ru
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="KN2 Parser Backend")

# CORS для Vue dev-сервера (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пути relative to backend/
BASE_DIR = Path(__file__).resolve().parent.parent
PARSER_PATH = BASE_DIR / "parser.py"
LISTINGS_PATH = BASE_DIR / "src" / "data" / "listings.json"


class RunParserResponse(BaseModel):
    ok: bool
    count: int
    message: str


@app.get("/listings")
async def get_listings() -> list[dict[str, Any]]:
    """Вернуть все объявления из JSON-файла."""
    if not LISTINGS_PATH.exists():
        raise HTTPException(status_code=404, detail="listings.json not found")
    with open(LISTINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@app.post("/run-parser", response_model=RunParserResponse)
async def run_parser() -> RunParserResponse:
    """Запустить Python-парсер и обновить listings.json."""
    if not PARSER_PATH.exists():
        raise HTTPException(status_code=404, detail="parser.py not found")

    try:
        result = subprocess.run(
            [sys.executable, str(PARSER_PATH)],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(BASE_DIR),
        )

        if result.returncode != 0:
            return RunParserResponse(
                ok=False,
                count=0,
                message=f"Парсер завершился с ошибкой: {result.stderr[-500:]}",
            )

        # Читаем обновлённый JSON
        count = 0
        if LISTINGS_PATH.exists():
            with open(LISTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            count = len(data)

        return RunParserResponse(
            ok=True,
            count=count,
            message="Парсер завершён успешно",
        )

    except subprocess.TimeoutExpired:
        return RunParserResponse(
            ok=False,
            count=0,
            message="Парсер превысил лимит времени (5 минут)",
        )
    except Exception as exc:  # noqa: BLE001
        return RunParserResponse(
            ok=False,
            count=0,
            message=f"Ошибка запуска парсера: {exc}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
