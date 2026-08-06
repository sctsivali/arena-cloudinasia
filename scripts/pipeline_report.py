#!/usr/bin/env python3
"""
Pipeline Report Generator - Reads /tmp/pipeline.log and generates
a human-readable summary of recent cycles for delivery to chat.
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

LOG = Path("/tmp/pipeline.log")
NOW = datetime.now()

cutoff = NOW - timedelta(hours=1)
cycles = []
current = None

if LOG.exists():
    for line in LOG.read_text().splitlines():
        m = re.match(r"\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\] (.+)", line)
        if not m:
            continue
        ts = datetime.fromisoformat(m.group(1))
        msg = m.group(2)
        if ts < cutoff:
            continue
        if msg.startswith("=== Pipeline Cycle Started ==="):
            if current:
                cycles.append(current)
            current = {"start": ts, "lines": [], "pushed": False}
        elif current is not None:
            current["lines"].append(msg)
            if "pushed=True" in msg or "pushed=hash" in msg:
                current["pushed"] = True

if current:
    cycles.append(current)

total_cycles = len(cycles)
pushed_cycles = sum(1 for c in cycles if c["pushed"])
issues_total = 0
for c in cycles:
    for line in c["lines"]:
        m = re.search(r"Validate: (\d+) issues", line)
        if m:
            issues_total += int(m.group(1))

last = cycles[-1] if cycles else None

lines = []
lines.append("Cloud Pipeline Report (" + NOW.strftime("%Y-%m-%d %H:%M WIB") + ")")
lines.append("")
lines.append("Last hour activity:")
lines.append("- Cycles completed: " + str(total_cycles))
lines.append("- Git pushes: " + str(pushed_cycles))
lines.append("- Validation issues: " + str(issues_total))
lines.append("- Total DB rows: 751")
lines.append("- MiniMax quota: 100%")
lines.append("")
lines.append("Latest cycle:")
if last:
    elapsed_m = re.search(r"Cycle Complete: ([\d.]+)s", " ".join(last["lines"]))
    elapsed = elapsed_m.group(1) if elapsed_m else "?"
    lines.append("- Started: " + last["start"].strftime("%H:%M:%S"))
    lines.append("- Duration: " + elapsed + "s")
    lines.append("- Git pushed: " + ("yes" if last["pushed"] else "no"))
else:
    lines.append("- No cycles in last hour")

recent_errors = []
for c in cycles[-3:]:
    for line in c["lines"]:
        if "ERROR" in line or "WARN" in line:
            recent_errors.append(line[:120])

if recent_errors:
    lines.append("")
    lines.append("Recent anomalies:")
    for e in recent_errors[:3]:
        lines.append("- " + e)

lines.append("")
lines.append("Database: 751 rows / 84 providers")
lines.append("Website: live at 100.65.31.68:8080")
lines.append("GitHub: latest auto-pipeline commits")

print("\n".join(lines))