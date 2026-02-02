# Game Scraper

Professional **GAME.es** web scraper that extracts **Warhammer 40k** product data:

- Title, price, ratings, **related products** (007 First Light, GTA V)
- **JSON + CSV** output with timestamps
- **Pydantic** validation + **pytest** coverage
- **uv** modern tooling

---

## 🎮 Demo Output

**data/products_20260201_221200.json**
```json
{
  "title": "Warhammer 40.000 Space Marine II",
  "price": "34'99€",
  "ratings_count": "208 Valoraciones",
  "related_products": [
    { "name": "007 First Light", "price": "69'99€" },
    { "name": "Grand Theft Auto V", "price": "19'99€" }
  ]
}
```
---

## 🚀 Quick Start
## Clone & Virtual Environment

git clone <repo> game-scraper
cd game-scraper
python -m venv venv
source venv/bin/activate   # Linux / Mac
.# venv\Scripts\activate    # Windows

## uv setup (IMPORTANT)

pip install uv
uv sync --dev
uv pip install -e .

## Run scraper

uv run python -m src.game_scraper.main

## Run tests

uv run pytest tests/ -v

# 📁 Project Structure

src/game_scraper/     # Core scraper + parser
tests/               # pytest + HTML samples
data/                # JSON + CSV output
config.toml          # GAME.es selectors

## 🧪 Tests & Coverage

uv run pytest --cov=src/game_scraper/ tests/

# 🔧 Troubleshooting (uv / pytest)

## Error:
ModuleNotFoundError: No module named 'src'

## Solution:
uv pip install -e .

## Alternative (run tests from ROOT):
PYTHONPATH=src pytest

# 🧠 Main Entrypoint

src/game_scraper/main.py

## 🐳 Docker
```bash
### Quick Docker Run

docker-compose up --build
# Files saved → data/products_*.json (persistent volume)
```

### Single Run
```bash
docker-compose run --rm game-scraper
```

### Verify Data Persistence
```bash
ls -la data/  # JSON + CSV files locally!
```

### Docker Compose Services
```bash
game-scraper:
  ✅ Image: python:3.12-slim (~150MB)
  ✅ Volume: ./data:/app/data (persistent)
  ✅ pip deps: requests + beautifulsoup4
  ✅ CMD: python -m src.game_scraper.main
```

### ⏰ CRONJOB PRODUCTION (cada 2 minutos)

Cronjob configurado para ejecutar el scraper automáticamente en entorno de producción, generando archivos persistentes cada 2 minutos mediante Docker.

- Ejecución automática cada 2 minutos

- Generación de archivos JSON + CSV con timestamp

- Logs accesibles desde Docker y dentro del contenedor

- Compatible con Windows + Git Bash usando MSYS_NO_PATHCONV=1

### 🎯 Step 3 – Resumen

✅ Cron ejecuta el scraper cada 2 minutos

✅ Archivos generados:
data/products_YYYYMMDD_HHMMSS.json
data/products_YYYYMMDD_HHMMSS.csv

✅ Logs disponibles en:

docker-compose logs -f

/var/log/cron/scraper.log

✅ Volumen persistente en Windows (Git Bash compatible)

### 🚀 Comandos Git Bash (Windows)
## Inicio (cron automático)
MSYS_NO_PATHCONV=1 docker-compose up -d --build

## Ver logs en vivo (ejecución cada 2 minutos)
MSYS_NO_PATHCONV=1 docker-compose logs -f

## Detener el servicio
MSYS_NO_PATHCONV=1 docker-compose down

## Ver archivos generados localmente
ls -la data/      # En Windows: dir data\

### 📁 docker-compose.yml
```bash
services:
  game-scraper:
    build: .
    container_name: game-scraper-cron
    volumes:
      - type: bind
        source: "./data"
        target: "/app/data"
    restart: unless-stopped
```

### ✅ Output Esperado
data/products_20260202_013000.json
data/products_20260202_013000.csv
data/products_20260202_013200.json
data/products_20260202_013200.csv


Todos los archivos se generan localmente en la carpeta data/ cada 2 minutos.

### 🔧 Troubleshooting (Windows / Git Bash)
## Problema

Se crea una carpeta incorrecta llamada data;C.

### Solución

#### Usar siempre:
```bash
MSYS_NO_PATHCONV=1 docker-compose up -d
```

### Alternativa directa con Docker:
```bash
docker run -v "$(pwd)/data:/app/data"
```
### 📊 Métricas Step 3

- Cron frequency: */2 * * * * (cada 2 minutos)

- Archivos generados: 720 por día (JSON + CSV)

- Tamaño estimado: ~50 KB por ejecución

- Uso diario: ~36 MB / día

- Almacenamiento: volumen local persistente (data/)
