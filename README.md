# 🤖 AI Adoption & Productivity Analysis (2021–2026)

> **End-to-End Data Analytics Portfolio Project**  
> Mengukur, menganalisis, dan memvisualisasikan dampak adopsi AI terhadap produktivitas kerja di berbagai industri, profesi, dan wilayah secara global.

---

## 📌 Latar Belakang

Penggunaan kecerdasan buatan (*Artificial Intelligence*) dalam dunia kerja telah berkembang pesat sejak dekade 2020-an. Pertanyaan kritis bagi para pimpinan bisnis dan organisasi adalah:

> **"Seberapa besar dampak nyata penggunaan AI terhadap produktivitas kerja di berbagai industri, profesi, dan wilayah?"**

Project ini memanfaatkan **2 dataset komprehensif** — Tren Makro Bulanan & Micro User-Level 15.000 Pengguna — untuk mengukur, menganalisis, dan memodelkan dampak adopsi AI terhadap efisiensi dan produktivitas kerja.

> **📦 Dataset Credit & Attribution:**  
> [Global AI Usage and Productivity · Kaggle](https://www.kaggle.com/datasets/ashyou09/global-ai-usage-and-productivity)

---

## 🎯 Goals Utama Project

| # | Goal | Deskripsi |
|:--|:-----|:----------|
| 1 | **Data-Driven Insights** | Identifikasi tren pertumbuhan adopsi AI, industri paling adaptif, dan tools AI dengan produktivitas tertinggi |
| 2 | **Hypothesis Testing** | Uji statistik korelasi antara token usage, task automation, experience, dan productivity gain |
| 3 | **User Segmentation** | Kelompokkan pengguna berdasarkan pola adopsi (*Heavy, Moderate, Light Users*) via Clustering |
| 4 | **Interactive BI Dashboard** | Dashboard interaktif dark-theme untuk presentasi temuan kepada stakeholder bisnis |
| 5 | **Executive Storytelling** | Laporan eksekutif & dokumentasi teknis standar industri sebagai portofolio Data Analyst |

---

## 🔑 Key Findings (Temuan Utama)

Berdasarkan analisis statistik terhadap 15.000 data pengguna:

### 📊 Korelasi & Hipotesis
| Hipotesis | Variabel | Pearson r | Kesimpulan |
|:----------|:---------|:---------:|:-----------|
| H1 | Token Usage → Productivity Gain | **r = 0.88** | ✅ Korelasi positif sangat kuat |
| H2 | Tasks Automated → Productivity Gain | **r = 0.74** | ✅ Korelasi positif kuat |
| H3 | Experience Years → Productivity Gain | **r = −0.01** | ✅ Tidak ada korelasi (AI = Great Equalizer) |

### 🛠️ Performa Tools AI
| AI Tool | Avg Productivity Gain | Karakteristik |
|:--------|:---------------------:|:--------------|
| GitHub Copilot | **~42%** | Specialist coding — otomatisasi tinggi |
| DeepSeek | **~41%** | Domain teknis, output terstruktur |
| ChatGPT (OpenAI) | **~11%** | Generalist, luas namun tidak spesifik |
| Claude (Anthropic) | **~10%** | Generalist text & reasoning |
| Gemini (Google) | **~10%** | Generalist multimodal |
| Midjourney | **~2%** | Creative/visual — ROI rendah pada task automation |

### 🏭 Insight Industri
- **Software Development** & **Finance** mencatatkan productivity gain tertinggi dari seluruh sektor.
- **Token Usage** adalah prediktor terkuat produktivitas — semakin tinggi kuota token, semakin besar efisiensi kerja.
- AI terbukti sebagai **"productivity equalizer"** — pekerja Junior mendapat manfaat setara dengan pekerja Senior/Veteran.

---

## 📦 Dataset

| File | Skala | Baris | Deskripsi |
|:-----|:------|------:|:----------|
| `data/ai_adoption_productivity_2021_2026.csv` | Makro | 402 | Tren global bulanan: active users, productivity gain per region & tool |
| `data/user_level_ai_adoption.csv` | Mikro | 15.000 | Data individual pengguna AI: industry, role, token usage, productivity gain |
| `data/user_level_ai_adoption_enriched.csv` | Mikro (enriched) | 15.000 | Dataset enriched hasil feature engineering (4 fitur tambahan) |

---

## 🗂️ Struktur Repositori

```
ai adoption & productivity/
│
├── index.html                                  ← Web Dashboard (Interactive BI)
├── app.js                                      ← Dashboard Logic & Data Engine
├── styles.css                                  ← Dashboard Styling (Dark Theme)
├── README.md                                   ← Dokumentasi project (file ini)
│
├── data/                                       ← Dataset CSV
│   ├── ai_adoption_productivity_2021_2026.csv  ← Dataset Makro Tren Global (402 baris)
│   ├── user_level_ai_adoption.csv              ← Dataset Mikro User Level (15.000 baris)
│   └── user_level_ai_adoption_enriched.csv     ← Dataset Enriched (output Feature Engineering)
│
├── notebooks/                                  ← Jupyter Notebooks
│   └── critical_data_analysis.ipynb            ← Notebook Analisis Kritis & Hipotesis
│
├── scripts/                                    ← Python Scripts
│   └── run_eda.py                              ← EDA, Feature Engineering & Chart Generation
│
└── charts/                                     ← Visualisasi output EDA (PNG)
    ├── chart1_ai_tools_adoption.png
    ├── chart2_token_vs_productivity.png
    ├── chart3_productivity_by_industry.png
    └── chart4_macro_trend.png
```

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|:------|:----------|
| **Web Dashboard** | HTML5, Vanilla CSS, JavaScript (ES6+) |
| **Charting** | [Chart.js](https://www.chartjs.org/) |
| **Data Analysis** | Python 3.x — `pandas`, `numpy`, `matplotlib` |
| **Notebook** | Jupyter Notebook (`.ipynb`) |
| **Fonts** | Inter (Google Fonts) |

---

## 🚀 Cara Menjalankan

### 1. Web Dashboard
Buka `index.html` langsung di browser **atau** jalankan via local server:
```bash
# Opsi A: Python built-in server (dari root folder project)
python -m http.server 8080
# Akses: http://localhost:8080

# Opsi B: VS Code Live Server Extension
# Klik kanan index.html → "Open with Live Server"
```

### 2. Regenerasi Charts & Enriched Dataset
```bash
# Jalankan dari folder scripts/
cd scripts
python run_eda.py
```
> Output: memperbarui `data/user_level_ai_adoption_enriched.csv` dan semua file `charts/*.png`

### 3. Notebook Analisis
```bash
cd notebooks
jupyter notebook critical_data_analysis.ipynb
```

---

## 📋 Status Deliverables

| # | Deliverable | Status |
|:--|:------------|:------:|
| 1 | Data Understanding & Profiling | ✅ Selesai |
| 2 | Exploratory Data Analysis (EDA) & Hypothesis Testing | ✅ Selesai |
| 3 | Feature Engineering (`Token_Per_Task`, `Experience_Group`, `Productivity_Tier`, `Adoption_Year`) | ✅ Selesai |
| 4 | Interactive Web Dashboard (Dark Theme, Filter Dinamis) | ✅ Selesai |
| 5 | Predictive Modeling & User Clustering (K-Means) | ⏳ Planned |
| 6 | Executive Summary & Final Portfolio Report | ⏳ Planned |

---

## ❓ Pertanyaan Bisnis yang Dijawab

1. **Tools Performance:** Tools AI manakah yang memberikan *productivity gain* tertinggi pada tiap-tiap industri?
2. **Workforce Equity:** Apakah AI membantu menyejajarkan produktivitas pekerja junior dengan pekerja senior?
3. **Efficiency Bottleneck:** Apakah makin tinggi token usage selalu berarti makin banyak tugas yang terotomatisasi?
4. **Macro vs Micro Trend:** Bagaimana tren adopsi global 2021–2026 berdampak pada performa individu?

---

## 🔬 Rekomendasi Strategis

1. **Targeted AI Tooling** — Prioritaskan tools AI terspealisasi (*Copilot, DeepSeek*) untuk divisi teknis dibanding lisensi generalist semua divisi.
2. **Optimasi Kuota Token** — Karena korelasi token–produktivitas sangat tinggi (`r = 0.88`), sediakan batas token harian yang memadai agar tidak jadi bottleneck efisiensi.
3. **Standardisasi Task Automation** — Dorong penggunaan AI untuk otomatisasi alur kerja berulang, bukan sekadar *Q&A*.
4. **Mitigasi Bias Self-Reporting** — Gabungkan metrik persepsi produktivitas dengan data objektif (*PR completion time, ticket closure rate*) untuk riset lanjutan.

---

*© 2026 · AI Adoption & Productivity Analytics Project · Data Analyst Portfolio*
