#!/bin/bash
echo "🚀 Starting GAME.es Warhammer Scraper v2.0..."

# Crear logs
touch /var/log/cron/scraper.log /var/log/cron.log
chmod 666 /var/log/cron/scraper.log /var/log/cron.log

echo "📁 Data volume: $(ls -la /app/data || echo 'Vacío')"
echo "⏰ Starting cron cada minuto..."

# Start cron daemon
service cron start

# Debug crontab
echo "📋 Crontab:"
crontab -l

# 🔥 LIVE DASHBOARD: Esperar primer scrape + abrir browser
echo "🌐 Esperando primer scrape (60s)..."
sleep 65 # 1min + 5s margen

echo "✅ Primer scrape completado!"
echo "🌐 Abriendo LIVE Dashboard: http://localhost:8080"

# LIVE SERVER (actualización automática)
python3 -m http.server 8080 --directory /app/reports --bind 0.0.0.0 &
SERVER_PID=$!

# Mantener logs + auto-refresh dashboard
echo "🔄 Dashboard LIVE en: http://localhost:8080/dashboard.html"
echo "📊 Actualización automática cada 1min (F5 o Ctrl+R)"
echo "📈 Logs en tiempo real:"
tail -f /var/log/cron/scraper.log /var/log/cron.log
