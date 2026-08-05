#!/usr/bin/env python3
"""
Full Deploy Pipeline:
1. Run scraper (or detect recent scrape)
2. Update database.json
3. Regenerate website data files
4. Push to GitHub
"""
import json
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

DATA = Path("/home/hermes-prime/.tmp/cloud-pricing/data")
WEBROOT = Path("/home/hermes-prime/cloudprovider-id")
REPO = Path("/home/hermes-prime/arena-cloudinasia")
LOG = Path("/tmp/pipeline.log")
PIPELINE_FLAG = Path("/tmp/scraper_updated.flag")
LOCK_FILE = Path("/tmp/pipeline.lock")

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def acquire_lock():
    if LOCK_FILE.exists():
        age = time.time() - LOCK_FILE.stat().st_mtime
        if age < 600:  # 10 min lock
            log("Pipeline lock held by another run, skipping")
            return False
    LOCK_FILE.write_text(str(time.time()))
    return True

def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

def has_recent_update():
    if not PIPELINE_FLAG.exists():
        return False
    age = time.time() - PIPELINE_FLAG.stat().st_mtime
    return age < 3600  # 1 hour

def get_db():
    db_path = DATA / "database.json"
    db = json.load(open(db_path))
    rows = db["rows"] if isinstance(db, dict) else db
    return rows

def get_provider_count():
    rows = get_db()
    return len(set(r["provider"] for r in rows if r.get("provider")))

def regenerate_data_files():
    """Regenerate tech_usage.json, sovereignty_scores.json, arena_*.json."""
    log("Regenerating data files...")
    
    rows = get_db()
    
    # Generate tech_usage.json
    tech_usage = {}
    for row in rows:
        if not row.get('provider'):
            continue
        p = row['provider']
        if p not in tech_usage:
            tech_usage[p] = {
                "provider": p,
                "provider_count": 1,
                "tier_count": 0,
                "providers": []
            }
        tech_usage[p]["tier_count"] += 1
        if p not in tech_usage[p]["providers"]:
            tech_usage[p]["providers"].append(p)
    
    # Write to both data dir and webroot
    with open(DATA / "tech_usage.json", 'w') as f:
        json.dump(tech_usage, f, indent=2)
    with open(WEBROOT / "tech_usage.json", 'w') as f:
        json.dump(tech_usage, f, indent=2)
    log(f"tech_usage.json: {len(tech_usage)} providers")

def regenerate_website_data():
    """Regenerate DATA const in index.html from latest database."""
    log("Regenerating website DATA block...")
    
    rows = get_db()
    
    # Build smaller DATA object for HTML (avoid huge file)
    # Keep essential fields
    slim_rows = []
    for r in rows:
        slim = {k: r[k] for k in [
            'id', 'provider', 'tier_name', 'country', 'region', 'dc_location',
            'vCPU', 'cpu_type', 'cpu_family', 'ram_gb', 'storage_gb', 'storage_type',
            'gpu', 'gpu_count', 'gpu_memory_gb', 'bandwidth', 'virtualization',
            'ipv4', 'ipv6', 'price', 'currency', 'price_usd_per_month',
            'billing_period', 'provider_country', 'provider_origin',
            'provider_type', 'tech_open_source', 'tech_class', 'sea_strength',
            'data_residency'
        ] if k in r}
        slim_rows.append(slim)
    
    data_json = json.dumps({"rows": slim_rows}, separators=(',', ':'))
    data_js = f"const DATA = {data_json};"
    
    # Update index.html
    index_path = WEBROOT / "index.html"
    content = index_path.read_text()
    
    # First remove any existing DATA blocks (safety against duplicates)
    while True:
        idx = content.find("const DATA = {")
        if idx == -1:
            break
        # Find matching close
        depth = 0
        in_string = False
        escape_next = False
        i = idx + len("const DATA = ")
        while i < len(content):
            c = content[i]
            if escape_next:
                escape_next = False
                i += 1
                continue
            if c == "\\":
                escape_next = True
                i += 1
                continue
            if c == '"':
                in_string = not in_string
            if not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
            i += 1
        # Find semicolon
        if i < len(content) and content[i] == ";":
            i += 1
        content = content[:idx] + content[i:].lstrip()
    
    # Now find clean insertion point
    start_marker = "const DATA = {"
    start_idx = content.find(start_marker)
    if start_idx >= 0:
        # Find matching closing brace - need to count braces
        depth = 0
        in_string = False
        escape_next = False
        i = start_idx + len(start_marker)
        while i < len(content):
            c = content[i]
            if escape_next:
                escape_next = False
                i += 1
                continue
            if c == "\\":
                escape_next = True
                i += 1
                continue
            if c == '"':
                in_string = not in_string
            if not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
            i += 1
        end_idx = i
        # DATA block is content[start_idx:end_idx] which ends with }
        # We need to add semicolon after
        # Find the semicolon
        if content[end_idx] == ";":
            new_content = content[:start_idx] + data_js + content[end_idx+1:]
        else:
            new_content = content[:start_idx] + data_js + content[end_idx:]
        n = 1
    else:
        new_content = content
        n = 0
    
    if n > 0:
        index_path.write_text(new_content)
        log(f"Updated index.html with {len(slim_rows)} tiers")
    else:
        log("WARNING: Could not find DATA pattern in index.html")

def git_push():
    """Commit and push to GitHub."""
    log("Git push...")
    
    os.chdir(REPO)
    
    # Copy latest index.html
    subprocess.run(['cp', str(WEBROOT / 'index.html'), 'index.html'], check=True)
    
    # Copy tech_usage.json
    subprocess.run(['cp', str(DATA / 'tech_usage.json'), 'tech_usage.json'], check=True)
    
    # Copy arena data files
    for f in ['arena_cost.json', 'arena_coverage.json', 'arena_performance.json', 'arena_opensource.json', 'sovereignty_audit.json', 'sovereignty_scores.json']:
        src = DATA / f
        if src.exists():
            subprocess.run(['cp', str(src), f], check=True)
    
    # Git status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if not result.stdout.strip():
        log("No changes to commit")
        return False
    
    # Add and commit
    subprocess.run(['git', 'add', '-A'], check=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M WIB")
    msg = f"auto: pipeline update {ts}"
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    
    # Push
    result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        log(f"Pushed: {result.stdout[:200]}")
        return True
    else:
        log(f"Push failed: {result.stderr[:200]}")
        return False

def main():
    log("=== Deploy Pipeline Started ===")
    
    if not acquire_lock():
        return
    
    try:
        # Check if there's a recent scraper update
        if has_recent_update():
            log("Recent scraper update detected")
        else:
            log("No recent scraper update, but running pipeline anyway")
        
        # Step 1: Regenerate data files
        regenerate_data_files()
        
        # Step 2: Regenerate website
        regenerate_website_data()
        
        # Step 3: Push to GitHub
        git_push()
        
        log("=== Pipeline Complete ===")
    finally:
        release_lock()

if __name__ == "__main__":
    main()
