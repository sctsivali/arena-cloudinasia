#!/usr/bin/env python3
"""
Send scraper progress report to chat.
Reads /tmp/scraper_progress.json and /tmp/scraper.log to generate report.
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROGRESS = Path("/tmp/scraper_progress.json")
LOG = Path("/tmp/scraper.log")
REPORT = Path("/tmp/scraper_latest_report.txt")

def get_progress():
    if not PROGRESS.exists():
        return None
    try:
        return json.load(open(PROGRESS))
    except:
        return None

def get_recent_log(n=10):
    if not LOG.exists():
        return []
    lines = LOG.read_text().splitlines()[-n:]
    return lines

def get_provider_count():
    """Get actual provider count from database."""
    try:
        db_path = "/home/hermes-prime/.tmp/cloud-pricing/data/database.json"
        result = subprocess.run(
            ["python3", "-c",
             f"import json; db=json.load(open('{db_path}')); rows=db['rows'] if isinstance(db, dict) else db; print(len(set(r['provider'] for r in rows if r.get('provider'))))"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
    except:
        pass
    return None

def main():
    progress = get_progress()
    if not progress:
        print("No progress data yet")
        return
    
    providers_now = get_provider_count()
    
    report_lines = [
        "📊 SEA Scraper Report",
        f"⏰ {datetime.now().isoformat()}",
        "",
        f"🎯 Target providers: {progress.get('total_targets', '?')}",
        f"⏳ Remaining: {progress.get('remaining', '?')}",
        f"📈 Total in DB: {providers_now if providers_now else '?'}",
        "",
        "📋 Recent activity:",
    ]
    
    recent = get_recent_log(8)
    for line in recent:
        # Strip timestamp for cleaner output
        if line.startswith("["):
            line = line.split("] ", 1)[-1] if "] " in line else line
        report_lines.append(f"  {line}")
    
    if progress.get('missing') and len(progress['missing']) > 0:
        report_lines.append("")
        report_lines.append(f"⏳ Still missing: {', '.join(progress['missing'][:5])}")
        if len(progress['missing']) > 5:
            report_lines.append(f"   ... and {len(progress['missing']) - 5} more")
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # Save to file
    REPORT.write_text(report_text)
    
    # Try to post to chat via terminal message
    # Since cron jobs can't post to chat easily with --no-agent,
    # we'll save to a file and the next LLM cron job can read it.
    
    return report_text

if __name__ == "__main__":
    main()
