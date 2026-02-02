#!/bin/bash
echo "🚀 Starting GAME.es cron scraper..."

# CREAR logs explícitamente
touch /var/log/cron/scraper.log /var/log/cron.log
chmod 666 /var/log/cron/scraper.log /var/log/cron.log

echo "📁 Data volume: $(ls -la /app/data)"
echo "⏰ Starting cron cada 2 minutos..."

# Start cron daemon
service cron start

# Debug crontab
crontab -l

# Esperar primer job + tail logs
sleep 60  # Esperar 1 min para primer cron
tail -f /var/log/cron/scraper.log /var/log/cron.log