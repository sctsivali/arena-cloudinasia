# Arena CloudinAsia

**Asia Pacific Cloud Infrastructure Leaderboard**

Cheapest VPS, Container, GPU, and Bare Metal servers across Asia Pacific - 506 tiers from 81 providers in 22 countries, normalized to USD/month.

## Brand

Built with CloudinAsia brand:
- **Logo**: from `cloudinasia.com/wp-content/uploads/2023/05/Logo-CIA-Black-no-BG-e1683750700345.png`
- **Font**: Manrope
- **Brand color**: `#60bd91` (CIA green-teal) + `#ffde59` (yellow accent)

## Sections

1. **Overview** - ORCA-style bento grid with 6 stats (tiers, providers, countries, from-price, median, OSS)
2. **Browse by Country** - 22 country cards with tier count + provider count + cheapest
3. **Technology Stack** - virtualization distribution (KVM, Hyper-V, Xen, etc.)
4. **Open Source vs Proprietary** - sovereign vs commercial breakdown
5. **Browse the Full Catalogue** - filterable directory of 506 tiers
6. **Arena Compare** - top 10 providers ranked on 5 dimensions

## Tech Stack

- **HTML5** with inline CSS + JavaScript
- **Manrope** font (Google Fonts CDN)
- **Inline SVG icons** (no external icon library)
- **Bento-grid layout** inspired by Orcahub marketplace
- **Responsive** down to iPhone SE (375px)

## Run

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

## Files

- `index.html` - main leaderboard page (240KB, self-contained)
- `cia-logo.png` - CloudinAsia brand logo (12KB, transparent bg)

## Data Source

Scraped from 81 cloud providers across:
- Indonesia (largest: IDCloudHost, BiznetGio, Dewaweb, JagoanHosting)
- Singapore (DigitalOcean, Vultr, Linode, AWS, Azure)
- Vietnam (Viettel IDC, FPT Smart Cloud, VNG Cloud)
- South Korea (9 providers, full coverage)
- Japan, China, India, Taiwan, Hong Kong
- Australia, New Zealand
- UAE, Saudi Arabia
- South Africa, Kenya, Nigeria
- Malaysia, Thailand, Philippines
- Germany, USA

## License

(C) 2026 Cloud in Asia (Sivali Cloud Technology)
