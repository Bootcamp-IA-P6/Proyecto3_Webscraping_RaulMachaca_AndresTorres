import os
import pytest
from pathlib import Path
import json
import re
from datetime import datetime

@pytest.fixture(scope="session")
def data_dir():
    return Path("data")

@pytest.fixture(scope="session")
def reports_dir():
    return Path("reports")

def test_json_files_generated(data_dir):
    """✅ Verifica JSON generados cada 2min."""
    json_files = list(data_dir.glob("products_*.json"))
    assert len(json_files) >= 2, f"Se esperan al menos 2 JSONs, encontrados: {len(json_files)}"
    
    # ✅ FIX: Parseo timestamp correcto
    recent_files = []
    for f in json_files:
        match = re.search(r'products_(\d{8})_(\d{6})\.json', f.name)
        if match:
            timestamp_str = f"{match.group(1)}T{match.group(2)}"
            try:
                file_time = datetime.strptime(timestamp_str, '%Y%m%dT%H%M%S')
                if (datetime.now() - file_time).seconds < 21600:  # 6h
                    recent_files.append(f)
            except ValueError:
                continue
    assert recent_files, "No hay JSONs recientes (últimas 6h)"

def test_csv_files_generated(data_dir):
    csv_files = list(data_dir.glob("products_*.csv"))
    assert len(csv_files) >= 2

def test_screenshots_generated(reports_dir):
    screenshots_dir = reports_dir / "screenshots"
    assert screenshots_dir.exists()
    jpg_files = list(screenshots_dir.glob("*.jpg"))
    assert len(jpg_files) >= 1
    valid_screenshots = [f for f in jpg_files if f.stat().st_size > 5000]
    assert valid_screenshots, "No hay screenshots válidos (>5KB)"

def test_dashboard_generated(reports_dir):
    dashboard = reports_dir / "dashboard.html"
    assert dashboard.exists()
    with open(dashboard) as f:
        content = f.read()
        assert '<img' not in content, "Dashboard contiene tags <img> ❌"
        assert 'screenshot' in content.lower()

def test_data_content(data_dir):
    """✅ Verifica contenido JSON válido."""
    json_files = list(data_dir.glob("products_*.json"))
    if not json_files:
        pytest.skip("No hay JSONs generados")
    
    latest = json_files[-1]
    with open(latest) as f:
        data = json.load(f)
    
    assert 'title' in data
    assert 'price' in data
    
    # ✅ FIX: Precio español "49'99€" → 49.99
    price_str = data['price'].replace('€', '').replace("'", '.').replace(',', '.')
    price_float = float(re.sub(r'[^\d.]', '', price_str))
    assert price_float > 0, f"Precio inválido: {data['price']}"
