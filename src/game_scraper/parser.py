"""GAME.es specific HTML parsers using CSS selectors."""

from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class GameEsParser:
    """Parser for GAME.es product pages."""
    
    def __init__(self, selectors: Dict[str, str]):
        """Initialize parser with GAME.es CSS selectors."""
        self.selectors = selectors
    
    def parse_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product title using h2.product-title span.cm-txt."""
        title_elem = soup.select_one(self.selectors['title'])
        return title_elem.get_text(strip=True) if title_elem else None
    
    def parse_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and format product price from buy--price structure."""
        int_part = soup.select_one(self.selectors['price_int'])
        dec_part = soup.select_one(self.selectors['price_decimal'])
        currency = soup.select_one(self.selectors['price_currency'])
        
        if all([int_part, dec_part, currency]):
            return f"{int_part.get_text(strip=True)}{dec_part.get_text(strip=True)}{currency.get_text(strip=True)}"
        return None
    
    def parse_ratings(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract ratings count from valoracion link."""
        ratings_elem = soup.select_one(self.selectors['ratings_count'])
        return ratings_elem.get_text(strip=True) if ratings_elem else None
    
    def parse_related_products(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all related products (name + price) from Related_ links."""
        related = []
        name_elements = soup.select(self.selectors['related_names'])
        price_elements = soup.select(self.selectors['related_prices'])
        
        # Zip names and prices (007 First Light, GTA V, etc.)
        for name_elem, price_elem in zip(name_elements, price_elements):
            name = name_elem.get_text(strip=True)
            
            # Same price structure for related products
            int_part = price_elem.select_one('.int')
            dec_part = price_elem.select_one('.decimal')
            currency = price_elem.select_one('.currency')
            
            if int_part and dec_part and currency and name:
                price = f"{int_part.get_text(strip=True)}{dec_part.get_text(strip=True)}{currency.get_text(strip=True)}"
                related.append({"name": name, "price": price})
        
        return related
