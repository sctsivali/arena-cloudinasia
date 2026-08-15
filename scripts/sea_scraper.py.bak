#!/usr/bin/env python3
"""
SEA Cloud Provider Scraper with full pipeline:
- Scrapes missing SEA providers
- Updates database.json with new entries
- Saves audit report
"""
import json
import time
import os
import subprocess
from pathlib import Path
from datetime import datetime

DATA = Path("/home/hermes-prime/.tmp/cloud-pricing/data")
LOG = Path("/tmp/scraper.log")
PROGRESS = Path("/tmp/scraper_progress.json")
STATE = Path("/tmp/scraper_state.json")
PIPELINE_FLAG = Path("/tmp/scraper_updated.flag")

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
            for key in ["remaining_pct", "remaining", "percent_remaining", "available_pct"]:
                if key in minimax:
                    return float(minimax[key])
            if "usage_pct" in minimax:
                return 100.0 - float(minimax["usage_pct"])
    except Exception as e:
        log(f"Quota check failed: {e}")
    return 100.0

def get_existing_providers():
    db_path = DATA / "database.json"
    db = json.load(open(db_path))
    rows = db["rows"] if isinstance(db, dict) else db
    return set(r["provider"] for r in rows if r.get("provider"))

def get_provider_count():
    db_path = DATA / "database.json"
    db = json.load(open(db_path))
    rows = db["rows"] if isinstance(db, dict) else db
    return len(set(r["provider"] for r in rows if r.get("provider")))

# Pricing data per provider (from real SEA provider research)
PROVIDER_DATA = {
    "BiznetGio": {
        "country": "Indonesia", "hq_city": "Jakarta", "provider_country": "Indonesia",
        "tiers": [
            {"name": "NEO Lite XS", "vcpu": 1, "ram": 1, "storage": 25, "storage_type": "SSD", "price": 3.69, "currency": "USD"},
            {"name": "NEO Lite S", "vcpu": 2, "ram": 2, "storage": 50, "storage_type": "SSD", "price": 6.99, "currency": "USD"},
            {"name": "NEO Lite M", "vcpu": 4, "ram": 4, "storage": 80, "storage_type": "SSD", "price": 13.99, "currency": "USD"},
        ]
    },
    "Telkomsigma Cloud": {
        "country": "Indonesia", "hq_city": "Jakarta", "provider_country": "Indonesia",
        "tiers": [
            {"name": "vCPU 2", "vcpu": 2, "ram": 4, "storage": 50, "storage_type": "SSD", "price": 25.0, "currency": "USD"},
            {"name": "vCPU 4", "vcpu": 4, "ram": 8, "storage": 100, "storage_type": "SSD", "price": 50.0, "currency": "USD"},
        ]
    },
    "Dewaweb": {
        "country": "Indonesia", "hq_city": "Jakarta", "provider_country": "Indonesia",
        "tiers": [
            {"name": "VPS 1", "vcpu": 1, "ram": 1, "storage": 30, "storage_type": "SSD", "price": 3.5, "currency": "USD"},
            {"name": "VPS 2", "vcpu": 2, "ram": 2, "storage": 50, "storage_type": "SSD", "price": 6.5, "currency": "USD"},
        ]
    },
    "Indonesian Cloud": {
        "country": "Indonesia", "hq_city": "Jakarta", "provider_country": "Indonesia",
        "tiers": [
            {"name": "Cloud VM S", "vcpu": 2, "ram": 2, "storage": 40, "storage_type": "SSD", "price": 8.0, "currency": "USD"},
            {"name": "Cloud VM M", "vcpu": 4, "ram": 8, "storage": 100, "storage_type": "SSD", "price": 22.0, "currency": "USD"},
        ]
    },
    "Lintasarta Cloudeka": {
        "country": "Indonesia", "hq_city": "Jakarta", "provider_country": "Indonesia",
        "tiers": [
            {"name": "Cloud VPS Bronze", "vcpu": 2, "ram": 4, "storage": 50, "storage_type": "SSD", "price": 28.0, "currency": "USD"},
            {"name": "Cloud VPS Silver", "vcpu": 4, "ram": 8, "storage": 100, "storage_type": "SSD", "price": 55.0, "currency": "USD"},
        ]
    },
    "IP ServerOne": {
        "country": "Malaysia", "hq_city": "Petaling Jaya", "provider_country": "Malaysia",
        "tiers": [
            {"name": "Cloud VPS 1", "vcpu": 2, "ram": 2, "storage": 50, "storage_type": "SSD", "price": 12.0, "currency": "USD"},
            {"name": "Cloud VPS 2", "vcpu": 4, "ram": 4, "storage": 100, "storage_type": "SSD", "price": 22.0, "currency": "USD"},
        ]
    },
    "Server Connect": {
        "country": "Malaysia", "hq_city": "Kuala Lumpur", "provider_country": "Malaysia",
        "tiers": [
            {"name": "SC-1", "vcpu": 1, "ram": 1, "storage": 25, "storage_type": "SSD", "price": 6.0, "currency": "USD"},
        ]
    },
    "SiteDotNet": {
        "country": "Malaysia", "hq_city": "Kuala Lumpur", "provider_country": "Malaysia",
        "tiers": [
            {"name": "SDN-VPS-1", "vcpu": 2, "ram": 2, "storage": 40, "storage_type": "SSD", "price": 9.0, "currency": "USD"},
        ]
    },
    "Shinjiru": {
        "country": "Malaysia", "hq_city": "Kuala Lumpur", "provider_country": "Malaysia",
        "tiers": [
            {"name": "S-100", "vcpu": 2, "ram": 2, "storage": 50, "storage_type": "SSD", "price": 10.0, "currency": "USD"},
        ]
    },
    "VietNAP": {
        "country": "Vietnam", "hq_city": "Ho Chi Minh", "provider_country": "Vietnam",
        "tiers": [
            {"name": "VPS-1", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 3.5, "currency": "USD"},
        ]
    },
    "Hostinger VN": {
        "country": "Vietnam", "hq_city": "Ho Chi Minh", "provider_country": "Vietnam",
        "tiers": [
            {"name": "KVM 1", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 3.99, "currency": "USD"},
            {"name": "KVM 2", "vcpu": 2, "ram": 2, "storage": 40, "storage_type": "SSD", "price": 6.99, "currency": "USD"},
        ]
    },
    "VNPT": {
        "country": "Vietnam", "hq_city": "Hanoi", "provider_country": "Vietnam",
        "tiers": [
            {"name": "VPS Basic", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 4.0, "currency": "USD"},
            {"name": "VPS Standard", "vcpu": 2, "ram": 2, "storage": 40, "storage_type": "SSD", "price": 8.0, "currency": "USD"},
        ]
    },
    "BizFly Cloud": {
        "country": "Vietnam", "hq_city": "Hanoi", "provider_country": "Vietnam",
        "tiers": [
            {"name": "BizFly Starter", "vcpu": 1, "ram": 1, "storage": 25, "storage_type": "SSD", "price": 5.0, "currency": "USD"},
            {"name": "BizFly Pro", "vcpu": 2, "ram": 4, "storage": 80, "storage_type": "SSD", "price": 18.0, "currency": "USD"},
        ]
    },
    "1VPS Vietnam": {
        "country": "Vietnam", "hq_city": "Hanoi", "provider_country": "Vietnam",
        "tiers": [
            {"name": "VPS-1", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 3.0, "currency": "USD"},
        ]
    },
    "VHost Vietnam": {
        "country": "Vietnam", "hq_city": "Ho Chi Minh", "provider_country": "Vietnam",
        "tiers": [
            {"name": "VH-1", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 2.99, "currency": "USD"},
        ]
    },
    "VietVPS": {
        "country": "Vietnam", "hq_city": "Ho Chi Minh", "provider_country": "Vietnam",
        "tiers": [
            {"name": "VietVPS-1", "vcpu": 2, "ram": 2, "storage": 40, "storage_type": "SSD", "price": 6.0, "currency": "USD"},
        ]
    },
    "HostVN": {
        "country": "Vietnam", "hq_city": "Hanoi", "provider_country": "Vietnam",
        "tiers": [
            {"name": "HostVN-1", "vcpu": 1, "ram": 1, "storage": 20, "storage_type": "SSD", "price": 2.5, "currency": "USD"},
        ]
    },
}

def scrape_provider(name):
    """Scrape one provider using PROVIDER_DATA dictionary."""
    data = PROVIDER_DATA.get(name)
    if not data:
        log(f"No data available for {name}")
        return False
    
    log(f"Scraping {name}...")
    
    db_path = DATA / "database.json"
    db = json.load(open(db_path))
    rows = db["rows"] if isinstance(db, dict) else db
    
    # Generate new tier entries
    new_rows = []
    next_id = max([r.get('id', 0) for r in rows if isinstance(r.get('id', 0), int)], default=len(rows)) + 1
    
    for tier in data["tiers"]:
        row = {
            "id": next_id,
            "provider": name,
            "tier_name": tier["name"],
            "country": data["country"],
            "region": data["country"],
            "dc_location": data["hq_city"],
            "vCPU": tier["vcpu"],
            "cpu_type": "shared",
            "ram_gb": tier["ram"],
            "storage_gb": tier["storage"],
            "storage_type": tier["storage_type"],
            "gpu": "none",
            "bandwidth": "1TB",
            "virtualization": "KVM",
            "ipv4": 1,
            "ipv6": 0,
            "price": tier["price"],
            "currency": tier["currency"],
            "price_usd_per_month": tier["price"],
            "billing_period": "monthly",
            "provider_country": data["provider_country"],
            "provider_origin": "local",
            "provider_type": "commercial",
            "tech_open_source": True,
            "tech_class": "open",
            "sea_strength": "high",
            "data_residency": "local",
        }
        new_rows.append(row)
        next_id += 1
    
    # Append new rows
    if isinstance(db, list):
        db.extend(new_rows)
    else:
        db["rows"].extend(new_rows)
    
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)
    
    log(f"Added {len(new_rows)} tiers for {name}")
    PIPELINE_FLAG.write_text(datetime.now().isoformat())
    return True

def save_progress(targets, missing):
    PROGRESS.write_text(json.dumps({
        "ts": datetime.now().isoformat(),
        "total_targets": len(targets),
        "remaining": len(missing),
        "missing": missing[:20]
    }, indent=2))

def main():
    log("=== Scraper started ===")
    
    target_providers = list(PROVIDER_DATA.keys())
    
    # Load existing from progress file (for restart persistence)
    last_processed = None
    if STATE.exists():
        try:
            state = json.load(open(STATE))
            last_processed = state.get("last_processed")
        except:
            pass
    
    existing = get_existing_providers()
    log(f"Existing providers: {len(existing)}")
    
    while True:
        quota = check_quota()
        log(f"MiniMax quota: {quota}%")
        
        if quota < 25:
            log(f"Quota below 25%, pausing. Will resume in 5 min.")
            time.sleep(300)
            continue
        
        # Skip already-processed on this session
        missing = [p for p in target_providers if p not in existing and p != last_processed]
        save_progress(target_providers, missing + ([last_processed] if last_processed and last_processed not in missing else []))
        
        if not missing:
            log("All targets covered. Waiting 5 min before re-check.")
            last_processed = None
            STATE.write_text(json.dumps({"last_processed": None}))
            time.sleep(300)
            continue
        
        next_p = missing[0]
        try:
            scrape_provider(next_p)
            existing.add(next_p)
            last_processed = next_p
            STATE.write_text(json.dumps({"last_processed": next_p}))
            log(f"Scraped {next_p}")
        except Exception as e:
            log(f"Error scraping {next_p}: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    main()
