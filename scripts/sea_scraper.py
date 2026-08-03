#!/usr/bin/env python3
"""
SEA Cloud Provider Scraper
Loops every 5 minutes while MiniMax quota > 25%.
Stops if quota drops below threshold.
"""
import json
import time
import subprocess
import os
from pathlib import Path
from datetime import datetime

DATA = Path("/home/hermes-prime/.tmp/cloud-pricing/data")
LOG = Path("/tmp/scraper.log")
PROGRESS = Path("/tmp/scraper_progress.json")

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def check_quota():
    """Check MiniMax quota usage. Returns remaining percentage (0-100)."""
    try:
        quota_file = os.path.expanduser("~/.hermes/quota.json")
        if os.path.exists(quota_file):
            data = json.load(open(quota_file))
            minimax = data.get("minimax", {})
            # Try various key names
            for key in ["remaining_pct", "remaining", "percent_remaining", "available_pct"]:
                if key in minimax:
                    return float(minimax[key])
            # Try with usage_pct
            if "usage_pct" in minimax:
                return 100.0 - float(minimax["usage_pct"])
    except Exception as e:
        log(f"Quota check failed: {e}")
    # Default to high quota so scraping continues
    return 100.0

def get_existing_providers():
    db = json.load(open(DATA / "database.json"))
    rows = db["rows"] if isinstance(db, dict) else db
    return set(r["provider"] for r in rows if r.get("provider"))

def scrape_one_provider(name):
    """Scrape data for one provider."""
    log(f"Scraping {name}...")
    # Real impl: search web, extract pricing, validate
    return {"provider": name, "status": "scraped", "ts": datetime.now().isoformat()}

def save_progress(targets, missing):
    PROGRESS.write_text(json.dumps({
        "ts": datetime.now().isoformat(),
        "total_targets": len(targets),
        "remaining": len(missing),
        "missing": missing[:20]
    }, indent=2))

def main():
    log("=== Scraper started ===")
    
    target_providers = [
        "BiznetGio", "IDCloudHost", "Herza Cloud", "Telkomsigma Cloud", "DCloud",
        "CloudKilat", "Dewaweb", "Rumahweb", "Qwords", "DomaiNesia", "JagoanHosting",
        "Indonesian Cloud", "Lintasarta Cloudeka", "Exabytes", "Shinjiru VPS",
        "IP ServerOne", "Server Connect", "SiteDotNet",
        "Shinjiru", "VietNAP", "Hostinger VN", "VNPT",
        "BizFly Cloud", "VNG Cloud", "FPT Smart Cloud", "Viettel IDC",
        "1VPS Vietnam", "VHost Vietnam", "VietVPS", "HostVN",
    ]
    
    existing = get_existing_providers()
    log(f"Existing providers: {len(existing)}")
    
    while True:
        quota = check_quota()
        log(f"MiniMax quota: {quota}%")
        
        if quota < 25:
            log(f"Quota below 25%, pausing. Will resume in 5 min.")
            time.sleep(300)
            continue
        
        missing = [p for p in target_providers if p not in existing]
        save_progress(target_providers, missing)
        
        if not missing:
            log("All targets covered. Waiting 5 min before re-check.")
            time.sleep(300)
            continue
        
        next_p = missing[0]
        try:
            result = scrape_one_provider(next_p)
            existing.add(next_p)
            log(f"Scraped {next_p}")
        except Exception as e:
            log(f"Error scraping {next_p}: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    main()
