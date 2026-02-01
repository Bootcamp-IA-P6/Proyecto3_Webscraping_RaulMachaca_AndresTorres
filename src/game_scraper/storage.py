"""JSON and CSV storage with timestamped filenames for GAME.es data."""

import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from .models import GameProduct, RelatedProduct


def generate_filename(base_dir: str, timestamp: str, extension: str) -> str:
    """Generate timestamped filename: products_20260201_224644.json."""
    path = Path(base_dir) / f"products_{timestamp}.{extension}"
    return str(path)


def save_json(data: GameProduct, output_dir: str = "data") -> str:
    """Save validated Pydantic data to JSON file."""
    timestamp = data.scraped_at.strftime("%Y%m%d_%H%M%S")
    filename = generate_filename(output_dir, timestamp, "json")
    
    Path(output_dir).mkdir(exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data.model_dump(exclude={"scraped_at"}), f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON saved: {filename}")
    return filename


def save_csv(data: GameProduct, output_dir: str = "data") -> str:
    """Save data to CSV (flattened for easy analysis)."""
    timestamp = data.scraped_at.strftime("%Y%m%d_%H%M%S")
    filename = generate_filename(output_dir, timestamp, "csv")
    
    Path(output_dir).mkdir(exist_ok=True)
    
    # Crear todas las columnas posibles primero
    all_fields = set(["title", "price", "ratings_count"])
    
    max_related = max(len(data.related_products), 1)
    for i in range(max_related):
        all_fields.add(f"related_name_{i}")
        all_fields.add(f"related_price_{i}")
    
    # Preparar filas
    rows = []
    main_row = data.model_dump(exclude={'related_products', 'scraped_at'})
    
    if data.related_products:
        for i, related in enumerate(data.related_products):
            row = main_row.copy()
            row[f"related_name_{i}"] = related.name
            row[f"related_price_{i}"] = related.price
            rows.append(row)
    else:
        rows.append(main_row)
    
    # Escribir CSV con TODOS los campos
    if rows:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(all_fields))
            writer.writeheader()
            writer.writerows(rows)
    
    print(f"✅ CSV saved: {filename}")
    return filename


def save_all_formats(data: GameProduct, output_dir: str = "data") -> List[str]:
    """Save in all configured formats (JSON + CSV)."""
    filenames = []
    filenames.append(save_json(data, output_dir))
    filenames.append(save_csv(data, output_dir))
    return filenames
