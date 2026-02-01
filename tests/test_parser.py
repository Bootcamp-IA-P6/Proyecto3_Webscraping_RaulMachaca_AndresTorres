"""Pytest tests for GAME.es parser using real HTML samples."""

import pytest
from bs4 import BeautifulSoup
from src.game_scraper.parser import GameEsParser
from src.game_scraper.models import GameProduct, RelatedProduct


@pytest.fixture
def sample_html():
    """Real HTML sample from Warhammer 40k GAME.es page."""
    return """
    <h2 class="product-title">
        <span class="cm-txt">Warhammer 40.000 Space Marine II</span>
    </h2>
    <div class="buy--price">
        <span class="int">34</span>
        <span class="decimal">'99</span>
        <span class="currency">€</span>
    </div>
    <a href="#valoracion" class="cm-txt u-txt_secondary">208 Valoraciones</a>
    <a id="Related_227743_246786" class="item">
        <div class="thumb-title">
            <span class="cm-txt w-100">007 First Light</span>
        </div>
        <div class="buy--price">
            <span class="int">69</span><span class="decimal">'99</span><span class="currency">€</span>
        </div>
    </a>
    """


@pytest.fixture
def game_es_selectors():
    """GAME.es CSS selectors from config.toml."""
    return {
        'title': 'h2.product-title span.cm-txt',
        'price_int': '.buy--price .int',
        'price_decimal': '.buy--price .decimal',
        'price_currency': '.buy--price .currency',
        'ratings_count': 'a[href="#valoracion"]',
        'related_names': 'a[id^="Related_"] .thumb-title span.cm-txt',
        'related_prices': 'a[id^="Related_"] .buy--price'
    }


@pytest.fixture
def parser(game_es_selectors):
    """GameEsParser with production selectors."""
    return GameEsParser(game_es_selectors)


class TestGameEsParser:
    """Tests for GAME.es specific parser."""

    def test_parse_title(self, parser, sample_html):
        """Test title extraction: Warhammer 40.000 Space Marine II."""
        soup = BeautifulSoup(sample_html, 'html.parser')
        assert parser.parse_title(soup) == "Warhammer 40.000 Space Marine II"

    def test_parse_price(self, parser, sample_html):
        """Test price extraction: 34'99€."""
        soup = BeautifulSoup(sample_html, 'html.parser')
        assert parser.parse_price(soup) == "34'99€"

    def test_parse_ratings(self, parser, sample_html):
        """Test ratings extraction: 208 Valoraciones."""
        soup = BeautifulSoup(sample_html, 'html.parser')
        assert parser.parse_ratings(soup) == "208 Valoraciones"

    def test_parse_related_products(self, parser, sample_html):
        """Test related products extraction."""
        soup = BeautifulSoup(sample_html, 'html.parser')
        related = parser.parse_related_products(soup)
        assert len(related) == 1
        assert related[0]["name"] == "007 First Light"
        assert related[0]["price"] == "69'99€"


class TestPydanticModels:
    """Tests for Pydantic data validation."""

    def test_game_product_validation(self):
        """Test complete GameProduct model validation."""
        product = GameProduct(
            title="Warhammer 40k",
            price="34,99€",
            ratings_count="208 Valoraciones",
            related_products=[
                RelatedProduct(name="007 First Light", price="69,99€")
            ]
        )
        assert product.title == "Warhammer 40k"
        assert len(product.related_products) == 1

    def test_model_serialization(self):
        """Test model_dump() for JSON/CSV export."""
        product = GameProduct(title="Test", price="€10", ratings_count="100")
        dumped = product.model_dump()
        assert "title" in dumped
        assert "scraped_at" in dumped
