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
```
## Antes que nada, despues de importar tendremos que cambiar el CRLF del archivo entrypoint.sh, lo pondremos a LF, clickando encima de este.
<img width="527" height="299" alt="image" src="https://github.com/user-attachments/assets/588e9403-dc83-48a4-bfdb-d7fb72ebf5d1" />

## Lo cambiamos
<img width="872" height="137" alt="image" src="https://github.com/user-attachments/assets/37f338d9-de68-4530-88d2-f38018f3b14a" />

## Deberia estar asi, y no te olvides de guardar:
<img width="506" height="286" alt="image" src="https://github.com/user-attachments/assets/655da4ca-0b6b-4459-af09-050be6e70d09" />

```bash
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
