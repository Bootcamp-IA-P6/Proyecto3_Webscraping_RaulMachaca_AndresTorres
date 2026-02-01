"""Configuration loader for GAME.es scraper."""

import tomli
from pathlib import Path
from typing import Dict

def load_config(config_path: str = "config.toml") -> Dict:
    """Load configuration from TOML file."""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file, 'rb') as f:
        return tomli.load(f)

if __name__ == "__main__":
    print(load_config())
