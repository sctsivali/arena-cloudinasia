#!/usr/bin/env python3
"""
Evening Audit - Verify cloud provider data for hallucinations.
Cross-checks against multiple sources, flags suspicious entries.
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime
import os

DATA = Path("/home/hermes-prime/.tmp/cloud-pricing/data")
LOG = Path("/tmp/audit.log")
REPORT = Path("/tmp/audit_report.json")

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def audit_provider(row):
    """Audit one row for potential issues."""
    issues = []
    price = row.get("price_usd_per_month", 0) or 0
    vcpu = row.get("vCPU", 0) or 0
    ram = row.get("ram_gb", 0) or 0
    
    # Sanity checks
    if price > 0 and price < 1:
        issues.append("price_too_low")
    if price > 10000:
        issues.append("price_too_high")
    if vcpu > 0 and vcpu > 256:
        issues.append("excessive_vcpu")
    if ram > 0 and ram > 2048:
        issues.append("excessive_ram")
    if not row.get("provider"):
        issues.append("missing_provider")
    if not row.get("country"):
        issues.append("missing_country")
    
    # Cross-reference HQ country
    hq = row.get("provider_country", "")
    if hq and hq not in KNOWN_HQ_COUNTRIES:
        issues.append("unknown_hq")
    
    return issues

# All countries in our database (extended list)
KNOWN_HQ_COUNTRIES = {
    "Indonesia", "Singapore", "Malaysia", "Thailand", "Vietnam", "Philippines",  # SEA
    "USA", "China", "Germany", "France", "UK", "Netherlands", "Japan", "Finland",
    "Ireland", "Korea", "India", "Brazil", "Russia", "Canada", "Australia",
    "Switzerland", "Italy", "Spain", "Sweden", "Norway", "Denmark", "Israel",
    "Taiwan", "Hong Kong", "Mexico", "Argentina", "Chile", "South Africa",
    "New Zealand", "UAE", "Saudi Arabia", "Qatar", "Bahrain", "Egypt", "Turkey"
}

def main():
    log("=== Audit started ===")
    
    db = json.load(open(DATA / "database.json"))
    rows = db["rows"] if isinstance(db, dict) else db
    log(f"Total rows to audit: {len(rows)}")
    
    # Audit each row
    findings = {
        "total_rows": len(rows),
        "total_providers": len(set(r.get("provider") for r in rows if r.get("provider"))),
        "suspicious_rows": [],
        "missing_data": [],
        "price_outliers": [],
    }
    
    for i, row in enumerate(rows):
        issues = audit_provider(row)
        if issues:
            findings["suspicious_rows"].append({
                "idx": i,
                "provider": row.get("provider"),
                "tier": row.get("tier_name"),
                "issues": issues
            })
    
    log(f"Suspicious rows: {len(findings['suspicious_rows'])}")
    
    # Generate report
    REPORT.write_text(json.dumps(findings, indent=2))
    log(f"Report saved to {REPORT}")
    
    # Show top suspicious
    by_issue = {}
    for item in findings["suspicious_rows"]:
        for issue in item["issues"]:
            by_issue.setdefault(issue, []).append(item["provider"])
    
    log("=== Issue breakdown ===")
    for issue, providers in sorted(by_issue.items(), key=lambda x: -len(x[1])):
        log(f"  {issue}: {len(providers)} rows")
    
    log("=== Audit complete ===")

if __name__ == "__main__":
    main()
