# Arena Cloud in Asia

**Asia Tenggara's most complete cloud pricing & digital sovereignty leaderboard** — fokus pada ASEAN dengan prioritas kedaulatan digital.

🌐 **Live**: http://100.65.31.68:8080  
🔗 **Repo**: github.com/sctsivali/arena-cloudinasia  
📊 **Last updated**: 16 August 2026 (auto-updates every 15 min)

---

## 🎯 What is this?

**Cloud in Asia** adalah platform perbandingan vendor-neutral yang membantu pembeli, ecosystem builder, dan policy maker di **ASEAN** menjawab pertanyaan-pertanyaan strategis:

- "Cloud lokal mana yang paling kompetitif harganya?"
- "Siapa yang benar-benar mendukung kedaulatan digital ASEAN?"
- "Berapa banyak DC fisik di Indonesia/Vietnam/Malaysia?"
- "Mana yang open source vs proprietary?"
- "Bagaimana kita mengurangi ketergantungan hyperscaler asing?"

Berbeda dengan review site atau affiliate marketing, **setiap tier diambil dari pricing page publik, dinormalisasi ke USD/bulan, dan divalidasi ketat** dengan fokus kedaulatan digital ASEAN.

**Scope Data (Batasan Ketat – ASEAN First):**
- Prioritas utama: Provider lokal ASEAN (HQ di Indonesia, Vietnam, Malaysia, Thailand, Singapore, Philippines)
- Sekunder: Hyperscalers yang punya DC signifikan di ASEAN (sebagai pembanding saja)
- Pure European providers (Hetzner, Scaleway, OVH Europe-only, IONOS Europe) **tidak masuk** kecuali memiliki komitmen serius di ASEAN (DC lokal + entitas legal lokal)
- Filter default website: **Local ASEAN** vs Global

---

## 📊 Database Stats (saat ini sedang di-update dengan scoring baru)

| Metric | Value |
|--------|-------|
| Total tiers | **~750+** |
| Unique providers | **~100** |
| Countries covered (ASEAN focus) | **6** (ID, VN, MY, TH, SG, PH) |
| Local ASEAN providers | Prioritas tinggi |
| Digital Sovereignty focus | ✅ |

---

## 🏆 Arena Categories (Cloud in Asia – ASEAN Digital Sovereignty Focus)

Leaderboard menggunakan **5 kategori** dengan bobot yang mendukung kampanye **kedaulatan digital ASEAN**:

### 1. Cost Champion 💰
Harga termurah per vCPU, RAM, storage (prioritas harga lokal dalam IDR/VND/MYR/THB/SGD).

### 2. Coverage Leader 🌍
Jumlah DC di ASEAN + negara ASEAN yang dilayani (bobot lebih tinggi untuk DC di Indonesia dan Vietnam).

### 3. Performance Champion ⚡
Ketersediaan GPU, max RAM, NVMe, CPU terbaru, dengan catatan performa di region ASEAN.

### 4. Digital Sovereignty (ASEAN) 🛡️ (**Bobot tertinggi**)
- HQ dan legal entity di salah satu negara ASEAN
- DC fisik mayoritas di ASEAN (bukan hanya hub Singapore)
- Support bahasa lokal + billing mata uang lokal
- Compliance dengan regulasi data ASEAN (UU PDP, PDPA, dll)
- Penggunaan stack open source dan kontrol data yang tinggi
- Skor 0-100 dengan formula transparan (lihat **Methodology** di bawah)

### 5. Open Source Cloud Native (ASEAN) 🐧
- Hypervisor open source (KVM, Xen) bukan proprietary
- Container & Orchestration berbasis open source
- Storage open (Ceph, OpenEBS, Longhorn)
- Bebas vendor lock-in dan mendukung interoperabilitas antar cloud ASEAN
- Skor 0-100 dengan formula transparan

Setiap kategori menampilkan **top 3 dengan medali emas/perak/perunggu** + ranking lengkap seluruh provider. **Default view** adalah Local ASEAN providers.

---

## 📋 Data Validation & Scoring Methodology (Transparan)

Semua data divalidasi dengan aturan ketat:

**Mandatory Fields (100% required):**
- `provider`, `tier_name`, `country`, `dc_location`, `vCPU`, `cpu_family` (harus specific, bukan "shared" atau "Intel Xeon")
- `ram_gb`, `storage_gb`, `storage_type`, `price_usd_per_month`
- `billing_period` ("monthly" atau "hourly → monthly")
- `provider_country`, `data_residency` ("local" preferred)

**Scoring Formula (baru di-update):**
- **Digital Sovereignty Score (0-100)**: HQ ASEAN (35), DC di ASEAN (25), local billing+language (10), regulatory compliance (15), open control plane (15)
- **Open Source Score (0-100)**: Open hypervisor (30), container/orchestration (20), open storage (20), no lock-in (15), control plane (15)
- **Local vs Global**: `is_local_provider` = true jika HQ + operasi utama di ASEAN

**Last-updated timestamp** selalu ditampilkan di footer.

Metodologi lengkap tersedia di modal **"Our Methodology"** di website.

---

## 🛠️ Automation & Pipeline

Pipeline dijalankan setiap 15 menit:
1. Scrape dengan fokus ASEAN + real web tools
2. Update database dengan scoring baru
3. Validate semua existing rows (termasuk sovereignty & open source)
4. Rebuild `index.html` dengan toggle Local ASEAN vs Global
5. Git commit + push jika ada perubahan

Hourly report dikirim ke chat.

---

## 🔗 Related Projects

- **cloudin.asia** — News & ecosystem events
- **ORCA** — Open Reliable Cloud Access (federated sovereign cloud marketplace)
- **Sivali Cloud Technology** — Penyelenggara utama

---

*Built with ❤️ for ASEAN digital sovereignty and open cloud ecosystem.*  
**Last updated**: 16 August 2026