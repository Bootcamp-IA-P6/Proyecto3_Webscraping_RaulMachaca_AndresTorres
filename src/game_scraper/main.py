"""Main entrypoint for GAME.es scraper."""

import logging
from pathlib import Path
from .scraper import GameScraper
from .models import GameProduct
from .storage import save_all_formats
from .config import load_config  # Temporal

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Execute complete GAME.es scraping workflow."""
    print("🎮 GAME.es Warhammer 40k Scraper")
    print("=" * 50)
    
    # Inicializar scraper
    scraper = GameScraper()
    
    # Scrapear Warhammer página
    raw_data = scraper.scrape_product()
    
    if raw_data:
        # Validar con Pydantic
        product = GameProduct(
            title=raw_data['title'],
            price=raw_data['price'],
            ratings_count=raw_data['ratings_count'],
            related_products=raw_data['related_products']
        )
        
        # Guardar JSON + CSV
        filenames = save_all_formats(product)
        print(f"\n✅ Scraping COMPLETED!")
        print(f"📄 Files saved: {', '.join(filenames)}")
    else:
        print("❌ Scraping FAILED")

if __name__ == "__main__":
    main()
