#!/bin/bash
echo "[$(date)] Stopping SEA scraper..."
pkill -f sea_scraper.py 2>/dev/null && echo "Scraper stopped" || echo "No active scraper"
