#!/usr/bin/env python3
"""
SEA Scraper Supervisor - Runs continuously, auto-restarts scraper on crash.
Replaces the time-limited cron job.
"""
import subprocess
import time
from datetime import datetime
from pathlib import Path

LOG = Path("/tmp/scraper.log")
SUPERVISOR_LOG = Path("/tmp/scraper_supervisor.log")

def log(msg):
    ts = datetime.now().isoformat()
    with open(SUPERVISOR_LOG, "a") as f:
        f.write(f"[SUPERVISOR {ts}] {msg}\n")
    print(f"[SUPERVISOR {ts}] {msg}")

def main():
    log("=== Scraper supervisor started ===")
    log("Will run scraper forever, restarting on crash")
    
    while True:
        try:
            log("Starting scraper subprocess...")
            proc = subprocess.run(
                ["python3", "/home/hermes-prime/.hermes/scripts/sea_scraper.py"],
                capture_output=False,
                timeout=None  # Run forever until killed
            )
            log(f"Scraper exited with code {proc.returncode}")
            time.sleep(10)
        except KeyboardInterrupt:
            log("Supervisor interrupted, exiting")
            break
        except Exception as e:
            log(f"Scraper crashed: {e}, restarting in 30s")
            time.sleep(30)

if __name__ == "__main__":
    main()
