import logging
from pathlib import Path
from datetime import datetime
from .scraper import GameScraper
from .models import GameProduct
from .storage import save_all_formats
from .config import load_config
from playwright.sync_api import sync_playwright
import hashlib
import json
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def capture_screenshot(product: dict, base_path: Path, max_retries: int = 2) -> str:
    """#22 Captura screenshot producto Warhammer - DOCKER OPTIMIZADO."""
    product_id = hashlib.md5(product['url'].encode()).hexdigest()[:8]
    screenshot_path = base_path / "screenshots" / f"{product_id}.jpg"
    
    # Si ya existe, retornar
    if screenshot_path.exists():
        print(f"📸 Screenshot exists: {screenshot_path}")
        return str(screenshot_path)
    
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    
    for attempt in range(max_retries):
        try:
            print(f"📸 Capturando screenshot {product_id} (attempt {attempt+1})...")
            
            # ✅ DOCKER FLAGS ESPECÍFICOS
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--no-first-run',
                        '--no-zygote',
                        '--single-process',  # ✅ Docker critical
                        '--disable-extensions'
                    ]
                )
                page = browser.new_page(
                    viewport={'width': 1280, 'height': 720},
                    user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                # ✅ MÁS RÁPIDO: domcontentloaded vs networkidle
                page.goto(product['url'], wait_until="domcontentloaded", timeout=30000)
                
                # ✅ Esperar SOLO elemento crítico (no falla si no existe)
                try:
                    page.wait_for_selector(".product-detail, .product-main, article, .product-tile", timeout=5000)
                except:
                    print("⚠️ Product selector timeout - screenshot anyway")
                
                # ✅ Screenshot COMPLETO de la página
                page.screenshot(path=screenshot_path, full_page=True)
                browser.close()
                
            # ✅ Verificar archivo creado
            if screenshot_path.exists() and screenshot_path.stat().st_size > 1000:
                print(f"✅ Screenshot guardado: {screenshot_path} ({screenshot_path.stat().st_size} bytes)")
                return str(screenshot_path)
            else:
                print(f"⚠️ Screenshot vacío: {screenshot_path}")
                
        except Exception as e:
            print(f"❌ Screenshot attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                # ✅ FALLBACK: Placeholder image
                placeholder_path = screenshot_path.parent / f"{product_id}_placeholder.txt"
                placeholder_path.write_text(f"No screenshot available for {product['url']}")
                print(f"📝 Placeholder creado: {placeholder_path}")
                return str(screenshot_path)
    
    return ""

def main():
    """Execute complete GAME.es scraping workflow + screenshots."""
    print("🎮 GAME.es Warhammer 40k Scraper v2.0 (#22)")
    print("=" * 60)
    
    # Paths
    DATA_PATH = Path("data")
    REPORTS_PATH = Path("reports")
    DATA_PATH.mkdir(exist_ok=True)
    REPORTS_PATH.mkdir(exist_ok=True)
    
    # Inicializar scraper
    scraper = GameScraper()
    
    # Scrapear Warhammer página
    raw_data = scraper.scrape_product()
    
    if raw_data:
        # ✅ URL requerida para screenshot
        if 'url' not in raw_data:
            raw_data['url'] = "https://www.game.es/videojuegos/accion/playstation-5/warhammer-40000-space-marine-ii/227743"
        
        # ✅ #22: Capturar screenshot
        print("📸 Capturando screenshot del producto principal...")
        raw_data['screenshot'] = capture_screenshot(raw_data, REPORTS_PATH)
        
        # Validar Pydantic (sin screenshot field - solo datos)
        product = GameProduct(
            title=raw_data['title'],
            price=raw_data['price'],
            ratings_count=raw_data['ratings_count'],
            related_products=raw_data['related_products']
        )
        
        # ✅ Guardar JSON + CSV (SIN timestamp)
        filenames = save_all_formats(product)
        
        print(f"\n✅ Scraping + Screenshot COMPLETED!")
        print(f"📄 Files: {', '.join(filenames)}")
        print(f"📸 Screenshot: {raw_data.get('screenshot', 'N/A')}")
        
        # ✅ reports.py genera dashboard con screenshot path
        try:
            from .reports import HtmlReportGenerator
            generator = HtmlReportGenerator(data_dir="data")
            report_path = generator.generate_dashboard()
            print(f"📊 HTML Dashboard: {report_path}")
        except Exception as e:
            print(f"⚠️ Report generation failed: {e}")
        
    else:
        print("❌ Scraping FAILED - No screenshots")

if __name__ == "__main__":
    main()