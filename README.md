# Arena Cloud in Asia

**Asia Pacific's most complete cloud pricing leaderboard** — 751 tiers across 98 providers, 22 countries.

🌐 **Live**: https://100.65.31.68:8080
🔗 **Repo**: github.com/sctsivali/arena-cloudinasia
📊 **Last updated**: 7 August 2026 (auto-updates every 15 min)

---

## 🎯 What is this?

**Arena Cloud in Asia** is a vendor-neutral, data-driven comparison platform for cloud computing services across Southeast Asia and Asia Pacific. We help buyers, ecosystem builders, and policy makers answer:

- *"Which provider is cheapest per vCPU/RAM/storage?"*
- *"Who has the most data centers in SEA?"*
- *"Which providers are truly sovereign (local HQ + DCs + language support)?"*
- *"What's the open-source / proprietary split?"*

Unlike review sites or affiliate marketing, **every tier is sourced from public pricing pages, normalized to USD/month, and validated** for completeness.

---

## 📊 Database Stats

| Metric | Value |
|--------|------:|
| Total tiers | **751** |
| Unique providers | **98** |
| Countries covered | **22** |
| Sovereign SEA providers | **69** |
| APAC providers | **71** |
| Min price (USD/month) | **$1.09** |
| Avg price (USD/month) | **$958.41** |

### Coverage by Country

| Country | Providers | Notes |
|---------|----------:|-------|
| 🇮🇩 Indonesia | 12 | BiznetGio, CloudKilat, IDCloudHost, Qwords, JagoanHosting, DomaiNesia, Herza Cloud, Rumahweb, Dewaweb, Indonesian Cloud, Lintasarta Cloudeka, Telkomsigma |
| 🇻🇳 Vietnam | 12 | VNG Cloud, FPT Smart Cloud, Viettel IDC, VietNAP, Hostinger VN, VNPT, BizFly Cloud, 1VPS Vietnam, VHost Vietnam, VietVPS, HostVN |
| 🇸🇬 Singapore | 8 | Multi-region presence for AWS, GCP, Azure, Alibaba, Tencent, Huawei, DigitalOcean, Linode |
| 🇲🇾 Malaysia | 6 | Exabytes, Shinjiru, AVM Cloud |
| 🇯🇵 Japan | 6 | GMO Cloud, IDC Frontier, IIJ GIO, KDDI, NTT, Sakura |
| 🇰🇷 South Korea | 9 | NAVER, KT, NHN, Kakao, LG CNS, SK C&C, Samsung SDS, Douzone, Gabia |
| 🇹🇭 Thailand | 4 | INET, True IDC, Bangkok Cloud |
| 🇵🇭 Philippines | 4 | Globe, PLDT, IP Converge |
| 🌍 Global hyperscalers | 25+ | AWS, GCP, Azure, Oracle, IBM, Alibaba, Tencent, Huawei, OVH, Hetzner, DigitalOcean, Linode, Vultr, UpCloud, Kamatera, Contabo |

---

## 🏗️ Architecture

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Vanilla HTML/CSS/JS (no framework) |
| **Data store** | Inline JSON in `index.html` (no server-side DB needed) |
| **Hosting** | Local HTTP server on Tailscale network (100.65.31.68:8080) |
| **Maps** | Leaflet.js + OpenStreetMap |
| **Charts** | D3.js (Voronoi for Open Source panel) |
| **Git workflow** | GitHub Pages-compatible static site |

### Data Pipeline (Cron)

Every 15 minutes, an automated pipeline runs:

```
┌─ STEP 1: Scrape ──────┐
│ Check quota >25%       │
│ Pick missing SEA target│
│ Scrape 1 provider      │
└────────────────────────┘
            ↓
┌─ STEP 2: Update DB ───┐
│ Save to database.json  │
│ (always 100% fields)   │
└────────────────────────┘
            ↓
┌─ STEP 3: Validate ────┐
│ Price >0, <100k        │
│ vCPU >0, <1024         │
│ RAM >0, <8192          │
│ All mandatory filled   │
└────────────────────────┘
            ↓
┌─ STEP 4: Update Site ─┐
│ Rewrite const DATA {}  │
│ in index.html          │
└────────────────────────┘
            ↓
┌─ STEP 5: Git Push ────┐
│ Commit + push if changed│
└────────────────────────┘
```

Hourly report delivers to chat with cycle stats.

---

## 📂 Repository Structure

```
arena-cloudinasia/
├── index.html                  # Main site (1.3MB)
│   ├── const DATA = {rows: [...]}  # 751 tiers inline
│   ├── buildOSLeaderboard()       # OS detect by tech_stack
│   ├── buildArena()               # 5 ranking categories
│   ├── buildTechStackBlocks()     # 29 tech cards
│   ├── buildOSSPanel()            # OSS vs proprietary split
│   ├── buildCountryCards()        # 23 country cards
│   ├── buildProviderTechCards()   # provider detail modal
│   └── buildLeafletMap()          # DC coverage map
│
├── scripts/                    # Automation
│   ├── pipeline_15min.py        # Main pipeline (cron)
│   ├── pipeline_report.py       # Hourly status report
│   ├── sea_scraper.py           # LLM-driven scraper (stub)
│   ├── sea_audit.py             # Data integrity audit
│   ├── scraper_supervisor.py    # Auto-restart wrapper
│   ├── scraper_report.py        # Scraper progress
│   └── stop_scraper.sh          # 6pm shutdown script
│
├── data/                       # Database exports
│   └── database.json           # Master 751-tier DB
│
└── docs/                       # Documentation
    ├── VALIDATION_RULES.md     # What tiers can enter
    ├── SCRAPING_GUIDE.md       # How scraping works
    └── CONTRIBUTING.md         # Adding new providers
```

---

## 📋 Data Validation Rules

Every tier must pass these checks to enter the database:

### ✅ Mandatory Fields (100% required)

| Field | Type | Example |
|-------|------|---------|
| `id` | string | `"biznetgio_6"` |
| `provider` | string | `"BiznetGio"` |
| `tier_name` | string | `"NEO Lite XS 1.1"` |
| `country` | string | `"Indonesia"` |
| `dc_location` | string | `"Jakarta"` |
| `vCPU` | int | `1` |
| `cpu_family` | string | `"AMD EPYC 7402P"` (specific) |
| `ram_gb` | float | `1.0` |
| `storage_gb` | float | `60.0` |
| `storage_type` | string | `"SSD"`, `"NVMe"` |
| `price_usd_per_month` | float | `3.69` |
| `billing_period` | string | `"monthly"` |
| `currency` | string | `"USD"`, `"IDR"` |
| `provider_country` | string | HQ country |
| `data_residency` | string | `"local"` / `"regional"` / `"global"` |
| `tech_class` | string | `"standard"` / `"premium"` / `"open"` |
| `provider_type` | string | `"IaaS"` / `"GPU Cloud"` / `"Serverless"` / `"Container"` |

### ✅ Allowed Product Categories

| Category | Allowed |
|----------|:-------:|
| VPS / Cloud Server | ✅ |
| GPU Cloud (NVIDIA H100/A100/V100/etc) | ✅ |
| Bare Metal / Dedicated | ✅ |
| Container-as-a-Service | ✅ |
| Serverless Compute | ✅ |
| Web Hosting (shared) | ❌ |
| Domain Registration | ❌ |
| Email Hosting | ❌ |
| SaaS apps | ❌ |
| CDN/DNS only | ❌ |
| Object storage only (no compute) | ❌ |
| Colocation | ❌ |

### ✅ Quality Rules

- **No "unknown" fields** — 0% unknowns allowed
- **CPU model specific** — "AMD EPYC 7402P", not generic "Intel Xeon"
- **Hourly prices** converted to monthly (× 730), flagged `"hourly (-> monthly)"`
- **Price always > 0** and < $100,000
- **DC location filled** — no empty DC
- **HQ country filled** — provider's legal HQ

### ❌ Outlier Detection

- `price_usd_per_month`: 0 < x < 100,000
- `vCPU`: 0 < x < 1,024
- `ram_gb`: 0 < x < 8,192

Anything outside these ranges is flagged for manual review.

---

## 🏆 Arena Categories

The leaderboard ranks providers in **5 categories**:

### 1. Cost Champion 💰
Cheapest compute per vCPU, RAM, storage — averaged across all tiers.

### 2. Coverage Leader 🌍
Most data centers + most countries served.

### 3. Performance Champion ⚡
GPU availability, max RAM, NVMe storage, latest CPUs.

### 4. Digital Sovereignty 🛡️
HQ in SEA + DCs in HQ country + local language support + UU PDP/GDPR-style compliance.

### 5. Open Source Cloud Native 🐧
KVM/Xen/OpenStack (not proprietary hypervisor) + Docker/Kubernetes + Ceph/OpenEBS (not proprietary storage) + free from vendor lock-in.

Each category shows **top 3 with luxury gold/silver/bronze medals** + full ranking with `#1-#N` numbers.

---

## 🛠️ Automation

### Cron Jobs

| Job ID | Schedule | Purpose |
|--------|----------|---------|
| `15a82a1f9960` | every 15m | Content Update Pipeline |
| `5507ed4878b4` | every 60m | Pipeline Status Report (delivered to chat) |

### Scripts

**`scripts/pipeline_15min.py`** — Main pipeline:
1. Scrapes SEA providers (1 per cycle if quota >25%)
2. Updates `database.json` (saves any new rows)
3. Validates existing data (outlier check)
4. Rewrites `const DATA = {...}` block in `index.html`
5. Commits + pushes to GitHub if changes

**`scripts/pipeline_report.py`** — Status report:
- Reads `/tmp/pipeline.log`
- Generates hourly summary: cycles, pushes, issues, DB stats
- Delivered to origin chat

---

## 🔗 Related Projects

| Project | Domain | Purpose |
|---------|--------|---------|
| [cloudprovider.id](https://cloudprovider.id) | Pricing leaderboard | This project |
| cloudin.asia | News & events | SEA cloud ecosystem news |
| Mautic | mautic.cloudinasia.com | Marketing automation |
| ORCA | Open Reliable Cloud Access | Federated cloud marketplace |

---

## 👥 Team

- **Ryo Ardian** — Founder, Cloud in Asia / Sivali Cloud Technology
- **Wong Sui Jan** — President Director, Sivali
- **Safira Zahira** — CTO, Engineer Sivali team
- **Mutiara Sukma Adilla** — Reports to Ryo
- **Hendra Permana / Amanda M.S / Nabilla Sarwadan** — Reports to Mutiara

---

## 📜 License

Data sourced from public pricing pages of each provider. Tier-level pricing is informational only and may not reflect negotiated enterprise rates.

---

## 🆕 Recent Updates

### 2026-08-07
- Hero stats dynamic: 98 providers, 751 tiers, 22 countries
- "666 Plans / 82 providers" hardcoded references replaced with dynamic values
- Top-3 luxury medals + ranking numbers in Arena
- Last-updated timestamp in footer

### 2026-08-05
- 15-minute content update pipeline deployed
- Sovereign SEA providers count: 69
- Coverage expanded: Vietnam 12 providers, Malaysia 6

### 2026-08-01
- Initial database: 1,201 consolidated tiers across 44 providers
- Tech stack metadata: hypervisor, container runtime, orchestration, storage, network

---

## 🤝 Contributing

To add a new provider:

1. **Research** the provider's public pricing page
2. **Create tiers** with ALL mandatory fields (see Validation Rules above)
3. **Convert hourly** to monthly where applicable
4. **Add to database.json** with `provider_type` set correctly
5. **Test** the website locally before pushing

For LLM-assisted research, use the existing `sea_scraper.py` pattern (requires quota).

---

## 📬 Contact

Questions or feedback?
- Telegram: @ryoardian (DM)
- Email: via cloudin.asia contact form

---

*Built with ❤️ for the Asia Pacific cloud ecosystem.*