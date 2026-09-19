"""Парсер каталога книг books.toscrape.com с выгрузкой в CSV и Excel."""

import argparse
import re
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(html: str) -> list[dict]:
    """Извлекает книги из HTML одной страницы каталога."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("article.product_pod"):
        price_text = card.select_one("p.price_color").text
        rating_class = card.select_one("p.star-rating")["class"][1]
        rows.append(
            {
                "title": card.h3.a["title"],
                "price": float(re.sub(r"[^\d.]", "", price_text)),
                "rating": RATINGS[rating_class],
                "in_stock": "In stock" in card.select_one("p.availability").text,
            }
        )
    return rows


def fetch_page(session: requests.Session, page: int, retries: int = 3):
    """Скачивает страницу с повторными попытками. Возвращает None, если страницы нет."""
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(BASE_URL.format(page), timeout=10)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as exc:
            print(f"  Ошибка на странице {page} (попытка {attempt}/{retries}): {exc}")
            if attempt == retries:
                raise
            time.sleep(2 * attempt)


def save(rows: list[dict], out_dir: Path, fmt: str) -> None:
    """Сохраняет результат в CSV и/или Excel."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    if fmt in ("csv", "both"):
        df.to_csv(out_dir / "books.csv", index=False, encoding="utf-8-sig")
    if fmt in ("excel", "both"):
        df.to_excel(out_dir / "books.xlsx", index=False)


def main() -> None:
    cli = argparse.ArgumentParser(description="Парсер книг books.toscrape.com")
    cli.add_argument("--pages", type=int, default=50, help="сколько страниц скачать (по умолчанию 50)")
    cli.add_argument("--format", choices=["csv", "excel", "both"], default="both", help="формат выгрузки")
    cli.add_argument("--out", default="data", help="папка для результатов")
    cli.add_argument("--delay", type=float, default=1.0, help="пауза между запросами, сек")
    args = cli.parse_args()

    rows: list[dict] = []
    with requests.Session() as session:
        for page in range(1, args.pages + 1):
            html = fetch_page(session, page)
            if html is None:
                print(f"Страница {page} не найдена, останавливаюсь.")
                break
            rows += parse_page(html)
            print(f"Страница {page}: всего {len(rows)} книг")
            time.sleep(args.delay)

    save(rows, Path(args.out), args.format)
    print(f"Готово: {len(rows)} книг сохранено в папку {args.out}/")


if __name__ == "__main__":
    main()
