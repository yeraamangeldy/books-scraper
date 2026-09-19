# books-scraper

Парсер каталога книг с сайта [books.toscrape.com](https://books.toscrape.com) —
учебного сайта, специально созданного для тренировки веб-скрапинга.
Собирает название, цену, рейтинг и наличие каждой книги и сохраняет
результат в CSV и Excel.

## Что внутри

- `parser.py` — сам парсер (requests + BeautifulSoup + pandas)
- `test_parser.py` — юнит-тесты на разбор HTML (без сетевых запросов)
- `requirements.txt` — зависимости
- `data/` — сюда сохраняются `books.csv` и `books.xlsx` после запуска

## Установка

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python parser.py
```

По умолчанию скачивает все страницы каталога (до 50) с паузой 1 секунда
между запросами и сохраняет результат и в CSV, и в Excel.

Доступные параметры:

```bash
python parser.py --pages 5 --format csv --out data --delay 0.5
```

| Параметр   | По умолчанию | Описание                                  |
|------------|--------------|--------------------------------------------|
| `--pages`  | 50           | сколько страниц каталога скачать           |
| `--format` | both         | `csv`, `excel` или `both`                  |
| `--out`    | data         | папка для результатов                      |
| `--delay`  | 1.0          | пауза между запросами, сек                 |

## Тесты

```bash
pytest -v
```

## Результат

В `data/books.csv` / `data/books.xlsx` — таблица со столбцами:

| title | price | rating | in_stock |
|-------|-------|--------|----------|
| A Light in the Attic | 51.77 | 3 | True |
| ... | ... | ... | ... |

## Про этичный парсинг

Перед парсингом любого другого сайта проверяйте `robots.txt` и условия
использования, делайте паузы между запросами и не собирайте персональные
данные.
