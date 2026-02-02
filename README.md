# 🎮 GAME.es Warhammer 40k Scraper v2.0

**Scraper profesional** que **cada minuto** extrae datos de **Warhammer 40.000: Space Marine II (PS5)** desde **GAME.es**.

⚠️ **IMPORTANTE – Entorno virtual obligatorio**

Antes de ejecutar el proyecto, **cada usuario debe crear y activar su propio entorno virtual (`venv`)** para evitar conflictos de dependencias.

### 🐍 Crear y activar `venv`

```bash
python -m venv venv
```
### Linux / macOS / WSL
```bash
source venv/bin/activate
```
### Windows (PowerShell)
```bash
venv\Scripts\Activate.ps1
```

## ✨ Funcionalidades

- 💰 Precio + **productos relacionados** (GTA V, 007 First Light)
- 📸 **Screenshots reales** usando Playwright (Chromium)
- 📊 **Dashboard LIVE** auto-actualizado  
  👉 http://localhost:8080/dashboard.html
- 🧪 **Tests automatizados** completos con Pytest
- ⏱️ Ejecución automática **cada 1 minuto** mediante Cron

---

## 🚀 Ejecución rápida (2 minutos)

```bash
git clone <repo>
cd Proyecto3_Webscraping_RaulMachaca

mkdir -p data reports
docker-compose up --build -d

sleep 120

# Abrir en el navegador:
# http://localhost:8080/dashboard.html
```

## 📊 Outputs generados
data/ (cada 1 min)                    reports/
├── products_20260202_231203.json    ├── dashboard.html   ← LIVE Dashboard
├── products_20260202_231204.csv     └── screenshots/
│   ...                                  └── 6da9eeaf.jpg ← Warhammer (24KB+)

## 🧪 Tests (IMPORTANTE)
Ejecutar después de levantar Docker y esperar datos reales

```bash
docker-compose up --build -d
sleep 240   # Esperar 4 minutos
pytest tests/test_scraper.py -v
```

## ✅ Resultado esperado
================== 5 passed ==================
### 🔍 Los tests verifican:
- ✅ JSON y CSV generados (≥ 2 archivos)
- ✅ Screenshots reales (> 5KB)
- ✅ Dashboard funcional sin imágenes embebidas
- ✅ Datos válidos (precio, título, productos relacionados)

## 🌐 Dashboard LIVE
http://localhost:8080/dashboard.html
### Incluye:

- 📈 Gráfico de precios en tiempo real
- 📊 Estadísticas de scrapes y screenshots
- 📋 Productos relacionados
- 🔄 Auto-refresh cada 1 minuto (F5)

## 🐳 Tech Stack
- 🐳 Docker        → Playwright v1.44.0 (jammy) + Cron
- 📱 Playwright   → Chromium + screenshots reales
- 📊 Jinja2       → Renderizado del dashboard
- 📈 Chart.js     → Gráficos interactivos
- 🧪 Pytest       → 5 tests automatizados

## 🔍 Logs en vivo
```bash
docker-compose logs -f game-scraper-cron
```
## Output esperado
- 📸 Screenshot 6da9eeaf... ✅ 24KB
- ✅ JSON: products_20260202_231203.json
- 🌐 LIVE Dashboard: http://localhost:8080

## 🛑 Comandos útiles
```bash
docker-compose up --build -d     # 🚀 Start
docker-compose logs -f          # 📊 Logs
docker-compose down             # 🛑 Stop
pytest tests/test_scraper.py -v # 🧪 Tests
```

## ✅ Estado del proyecto
- ⏱️ Cron: Cada 1 minuto (1440 scrapes/día)
- 📱 LIVE: http://localhost:8080/dashboard.html
- 🧪 Tests: 5/5 automatizados
- 💾 Persistencia: data/ + reports/
- 🐳 Docker: 100% containerizado
- 🚀 Estado: Production Ready