"""HTML dashboard generator from GAME.es scraped data."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class HtmlReportGenerator:
    """Generate professional HTML dashboard from JSON scrapes."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def load_recent_data(self, max_files: int = 50) -> List[Dict]:
        """Load last N JSON files."""
        json_files = sorted(
            self.data_dir.glob("products_*.json"),
            reverse=True
        )[:max_files]
        
        products = []
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['scraped_file'] = file_path.name
                data['scraped_time'] = file_path.name[8:14]  # YYYYMMDD_HHMMSS
                products.append(data)
            except (json.JSONDecodeError, KeyError):
                continue
        
        return products
    
    def generate_dashboard(self, output_path: str = "reports/dashboard.html") -> str:
        """Generate complete HTML dashboard."""
        products = self.load_recent_data()
        
        # Extract price trends
        prices = []
        titles = []
        for product in products[:24]:  # Last 24 scrapes (~48 min)
            try:
                price_str = product['price'].replace('\'', '.').replace('€', '').strip()
                price = float(price_str.replace(',', '.'))
                prices.append(price)
                titles.append(product['title'][:30] + '...')
            except:
                continue
        
        context = {
            'products': products[:12],  # Latest 12
            'price_trend': prices[-7:],  # Last 7 scrapes
            'titles': titles[-7:],
            'total_scrapes': len(products),
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        template = self.env.get_template('dashboard.html')
        html_content = template.render(context)
        
        Path(output_path).parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
