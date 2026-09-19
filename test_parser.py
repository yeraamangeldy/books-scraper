"""Тесты для parser.py: проверяем разбор HTML без реальных сетевых запросов."""

from parser import parse_page

SAMPLE_HTML = """
<html><body>
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a title="A Light in the Attic" href="a-light-in-the-attic.html">A Light in the Attic</a></h3>
  <div class="product_price">
    <p class="price_color">£51.77</p>
    <p class="instock availability">
        <i class="icon-ok"></i>
        In stock
    </p>
  </div>
</article>
<article class="product_pod">
  <p class="star-rating One"></p>
  <h3><a title="Tipping the Velvet" href="tipping-the-velvet.html">Tipping the Velvet</a></h3>
  <div class="product_price">
    <p class="price_color">£53.74</p>
    <p class="instock availability">
        <i class="icon-ok"></i>
        Out of stock
    </p>
  </div>
</article>
</body></html>
"""


def test_parse_page_returns_all_books():
    rows = parse_page(SAMPLE_HTML)
    assert len(rows) == 2


def test_parse_page_extracts_fields_correctly():
    rows = parse_page(SAMPLE_HTML)
    first = rows[0]
    assert first["title"] == "A Light in the Attic"
    assert first["price"] == 51.77
    assert first["rating"] == 3
    assert first["in_stock"] is True


def test_parse_page_detects_out_of_stock():
    rows = parse_page(SAMPLE_HTML)
    second = rows[1]
    assert second["title"] == "Tipping the Velvet"
    assert second["rating"] == 1
    assert second["in_stock"] is False


def test_parse_page_empty_html_returns_empty_list():
    assert parse_page("<html><body></body></html>") == []
