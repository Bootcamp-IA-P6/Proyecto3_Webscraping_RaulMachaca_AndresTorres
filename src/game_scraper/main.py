"""Main entrypoint for GAME.es scraper."""

import logging
from pathlib import Path
from .scraper import GameScraper
from .models import GameProduct
from .storage import save_all_formats
from .config import load_config  # Temporal
from playwright.sync_api import sync_playwright
import os
from pathlib import Path

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

def generate_report():
    """Generate HTML dashboard after scraping."""
    from .reports import HtmlReportGenerator
    generator = HtmlReportGenerator()
    report_path = generator.generate_dashboard()
    print(f"📊 HTML Report: {report_path}")


def capture_product_screenshot(product_url: str, product_id: str, base_path: Path) -> str:
    """Captura screenshot de producto Warhammer"""
    screenshot_path = base_path / "screenshots" / f"{product_id}.jpg"
    screenshot_path.parent.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(product_url, wait_until="networkidle")
        
        # Screenshot del elemento producto (selector GAME.es)
        page.locator(".product-detail").screenshot(path=screenshot_path)
        browser.close()
    
    return str(screenshot_path)

if __name__ == "__main__":
    main()
    generate_report()  # Auto-generate after scrape
