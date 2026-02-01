"""Core web scraping engine with requests + BeautifulSoup integration."""

import requests
import logging
from typing import Dict, Optional
from pathlib import Path
from bs4 import BeautifulSoup

from .parser import GameEsParser
from .config import load_config  # Will create in next commit

logger = logging.getLogger(__name__)

class GameScraper:
    """Main scraper engine for GAME.es product pages."""
    
    def __init__(self, config_path: str = "config.toml"):
        """Initialize scraper with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.parser = GameEsParser(self.config["selectors"]["game_es"])
        
        # Session con headers GAME.es
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config["scraper"]["user_agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        })
    
    def _load_config(self) -> Dict:
        """Load configuration from config.toml."""
        # Temporal - usaremos config.py en commit siguiente
        return {
            "scraper": {
                "target_url": "https://www.game.es/videojuegos/accion/playstation-5/warhammer-40000-space-marine-ii/227743",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "selectors": {
                "game_es": {
                    "title": "h2.product-title span.cm-txt",
                    "price_int": ".buy--price .int",
                    "price_decimal": ".buy--price .decimal",
                    "price_currency": ".buy--price .currency",
                    "ratings_count": 'a[href="#valoracion"]',
                    "related_names": 'a[id^="Related_"] .thumb-title span.cm-txt',
                    "related_prices": 'a[id^="Related_"] .buy--price'
                }
            }
        }
    
    def scrape_product(self, url: Optional[str] = None) -> Optional[Dict]:
        """Scrape single GAME.es product page."""
        url = url or self.config["scraper"]["target_url"]
        
        try:
            logger.info(f"🔍 Scraping: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer datos con parser específico
            data = {
                "title": self.parser.parse_title(soup),
                "price": self.parser.parse_price(soup),
                "ratings_count": self.parser.parse_ratings(soup),
                "related_products": self.parser.parse_related_products(soup)
            }
            
            logger.info(f"✅ Scraped: {data['title'][:50]}...")
            return data
            
        except requests.RequestException as e:
            logger.error(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Parse Error: {e}")
            return None
