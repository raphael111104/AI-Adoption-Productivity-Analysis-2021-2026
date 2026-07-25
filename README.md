# 🤖 AI Adoption & Productivity Analysis (2021–2026)

[![CI Pipeline](https://github.com/raphael111104/AI-Adoption-Productivity-Analysis-2021-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/raphael111104/AI-Adoption-Productivity-Analysis-2021-2026/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](requirements.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data Dictionary](https://img.shields.io/badge/Data_Dictionary-DATA__DICTIONARY.md-green.svg)](DATA_DICTIONARY.md)

> **End-to-End Data Analytics Portfolio Project**  
> Mengukur, menganalisis, dan memvisualisasikan dampak adopsi AI terhadap produktivitas kerja di berbagai industri, profesi, dan wilayah secara global.

> [!IMPORTANT]
> **Synthetic Data Disclosure**:  
> This portfolio project uses synthetic data. Findings demonstrate analytical methods and should not be interpreted as empirical evidence about real-world workers or organizations.

> [!TIP]
> **GitHub Repository Metadata**:  
> - **Description**: End-to-end data analytics and econometric evaluation of global AI adoption and worker productivity metrics (2021-2026) featuring dynamic BI dashboard, OLS regression, and reproducible Python pipelines.  
> - **Topics**: `data-analysis`, `econometrics`, `ols-regression`, `data-science`, `analytics-dashboard`, `python`, `data-analytics`, `statistical-analysis`, `reproducibility`

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

### 📊 Korelasi, Pemodelan Multivariat & Hipotesis
| Hipotesis | Variabel | Pearson r (Naive) | Partial r / Regresi / ANOVA | Kesimpulan |
|:----------|:---------|:-----------------:|:--------------------------:|:-----------|
| H1 | Token Usage → Productivity Gain | **r = 0.88** | **r_partial = 0.71** ($R^2 = 0.81$) | ✅ Korelasi positif kuat, dipengaruhi oleh faktor pembaur (*tool category confounding*) |
| H2 | Tasks Automated → Productivity Gain | **r = 0.55** | **β = +1.99** per task | ✅ Korelasi positif kuat dengan efek langsung yang signifikan |
| H3 | Experience Years → Productivity Gain | **r = −0.01** | **F = 0.69** ($p = 0.554, \eta^2 = 0.00014$) | ✅ Manfaat AI bersifat independen dari senioritas (*overlapping 95% CIs*) |

> [!NOTE]
> **1. Metodologi & Pengontrolan Variabel Pembaur (Confounder Control):**  
> Analisis kritis menggunakan **Regresi Multivariat OLS** ($R^2 = 0.8076$) dan **Partial Correlation** ($r_{\text{partial}} = 0.7070$) menunjukkan bahwa korelasi sederhana $r = 0.88$ sebagian dijelaskan oleh jenis perangkat (*Primary_AI_Tool*). Pengguna perangkat koding spesialis (*GitHub Copilot, DeepSeek*) secara alami mengonsumsi token jauh lebih tinggi (~32.000) dan mencatatkan *productivity gain* tinggi (~40%), sedangkan perangkat teks generalist (*ChatGPT, Claude, Gemini*) beroperasi pada ~8.000 token dengan gain ~10%.

> [!NOTE]
> **2. Metodologi Paritas Senioritas, Dynamic f_oneway & Effect Size Eta-Squared ($\eta^2$):**  
> Pengujian hipotesis menggunakan `scipy.stats.f_oneway()` ($F = 0.6962, p = 0.554241$), **Eta-Squared ($\eta^2 = 0.000139 < 0.01 \implies \text{negligible effect size}$)**, dan 95% Confidence Intervals yang tumpang-tindih (Junior `[10.7%, 11.8%]`, Mid-Level `[11.0%, 11.8%]`, Senior `[10.9%, 11.6%]`, Veteran `[10.8%, 11.4%]`) mengonfirmasi bahwa **manfaat peningkatan produktivitas AI bersifat independen dari tingkat senioritas pekerja**.  
> *Catatan Metodologis*: Tanpa data produktivitas baseline sebelum adopsi (*Pre-AI Baseline*), korelasi $r \approx -0.01$ tidak secara eksplisit membuktikan klaim bahwa AI "menyamakan" kesenjangan produktivitas junior-senior secara absolut, melainkan membuktikan bahwa persentase gain dari AI terdistribusi secara merata di semua tingkat pengalaman.

> [!NOTE]
> **3. Audit Ekonometrika Multicollinearity & Seleksi Model A (Industry) vs Model B (Job_Role):**  
> Hasil audit membuktikan bahwa `Job_Role` bersifat *strictly nested* dalam `Industry`. Memasukkan kedua kelompok dummy menghasilkan *perfect multicollinearity* (*Rank Deficiency = 5*, *Condition Number* $= 1.22 \times 10^{20}$). Model utama yang digunakan adalah **Model A (Industry Model)** yang berstatus *Full Rank* ($k=15$, *Deficiency = 0*, *Condition Number* $= 1.52 \times 10^5$, $\text{VIF} < 3.2$), serta unggul secara parsimoni berdasarkan kriteria informasi (**AIC $= 91.363,57$**, **BIC $= 91.477,80$** dibanding Model B BIC $= 91.614,26$).  
> *Kategori Referensi Eksplisit*: `Primary_AI_Tool`: `ChatGPT (OpenAI)`, `Industry`: `Creative & Design`, `Job_Role`: `Accountant`.

> [!NOTE]
> **4. Hasil Regresi OLS Inferensial (HC3 Robust Standard Errors & Diagnostik Residual):**  
> Menggunakan `statsmodels.formula.api.ols()` dengan **HC3 Robust Standard Errors** ($N=15.000$, $R^2 = 0.8074$, Adjusted $R^2 = 0.8072$, Residual Std Error $= 5.0836$):  
> - `Daily_Token_Usage`: $\beta = +0.001071$, Robust $\text{SE} = 0.000015$, $z = 72.172$, $p < 0.0001$, $95\% \text{ CI} = [0.001042, 0.001100]$.  
> - `Tasks_Automated_Per_Week`: $\beta = +1.9926$, Robust $\text{SE} = 0.0738$, $z = 27.014$, $p < 0.0001$, $95\% \text{ CI} = [1.848, 2.137]$.  
> - `Experience_Years`: $\beta = -0.0115$, Robust $\text{SE} = 0.0056$, $z = -2.033$, $p = 0.042$, $95\% \text{ CI} = [-0.0225, -0.0004]$.  
> - **Uji Heteroskedastisitas Breusch-Pagan**: $\text{LM Stat} = 5183.02 (p < 0.0001) \implies$ Mengonfirmasi heteroskedastisitas signifikan, memvalidasi penggunaan HC3 robust SE.  
> - **Uji Normalitas Residual Jarque-Bera**: $\text{JB Stat} = 11214.40 (p < 0.0001) \implies$ Distribusi residual memanjang ke kanan (*right-skewed / leptokurtic*).

> [!NOTE]
> **5. Evaluasi Model Interaksi (`Experience_Years × Primary_AI_Tool`):**  
> Pengujian model interaksi dilakukan secara eksplisit untuk memeriksa apakah tingkat pengalaman kerja memoderasi dampak jenis perangkat AI terhadap produktivitas. **Joint Hypothesis F-Test** untuk seluruh term interaksi menunjukkan $F(6, 14979) = 0.4951 (p = 0.8125 \implies \text{gagal menolak } H_0)$, mengonfirmasi bahwa tidak ada efek moderasi yang signifikan secara statistik antara senioritas dan perangkat AI. Model aditif tanpa interaksi (Baseline Model A) lebih disukai berdasarkan kriteria parsimoni (**AIC $= 91.363,57$** vs **Interaction AIC $= 91.368,47$**).

### 🛠️ Performa Tools AI
| AI Tool | Avg Productivity Gain | Karakteristik |
|:--------|:---------------------:|:--------------|
| GitHub Copilot | **~40%** | Specialist coding — otomatisasi tinggi, konsumsi token tinggi (~32.3k) |
| DeepSeek | **~43%** | Domain teknis, output terstruktur (~32.8k token) |
| ChatGPT (OpenAI) | **~10%** | Generalist, luas namun tidak spesifik (~8.0k token) |
| Claude (Anthropic) | **~10%** | Generalist text & reasoning (~8.0k token) |
| Gemini (Google) | **~10%** | Generalist multimodal (~8.0k token) |
| Perplexity | **~10%** | Generalist search & text (~8.0k token) |
| Midjourney | **~2%** | Creative/visual — ROI rendah pada task automation (~1.8k token) |

### 🏭 Insight Industri
- **Software Development** & **Finance** mencatatkan productivity gain tertinggi dari seluruh sektor.
- **Konsumsi Token & Otomatisasi Tugas** berkontribusi positif terhadap produktivitas ($r_{\text{partial}} = 0.71$, $+1.07\%$ gain per 1.000 token harian), namun alokasi kuota harus memperhatikan jenis perangkat dan alur kerja.
- Manfaat adopsi AI terbukti **independen dari tingkat pengalaman** — pekerja Junior, Mid-Level, Senior, dan Veteran memperoleh persentase peningkatan produktivitas rata-rata yang seragam (~11.1% – 11.4%).

---

## 📦 Dataset

| File | Skala | Baris | Deskripsi |
|:-----|:------|------:|:----------|
| `data/ai_adoption_productivity_2021_2026.csv` | Makro | 402 | Tren global bulanan: active users, productivity gain per region & tool |
| `data/user_level_ai_adoption.csv` | Mikro | 15.000 | Data individual pengguna AI: industry, role, token usage, productivity gain |
| `data/user_level_ai_adoption_enriched.csv` | Mikro (enriched) | 15.000 | Dataset enriched hasil feature engineering (4 fitur tambahan) |

### 🛡️ Enterprise Data Quality & Integrity Audit Matrix
| Dimensi Audit | Pemeriksaan | Hasil Evaluasi Data Mikro & Makro | Status |
|:--------------|:------------|:-----------------------------------|:------:|
| **1. Missing Values** | Null check | 0 missing values (100% complete across micro & macro datasets) | ✅ |
| **2. Duplicate Primary Keys** | `User_ID` duplication | 0 duplicate IDs (15,000 unique `User_ID` records) | ✅ |
| **3. Temporal Validity** | Date range | `2021-01-01` to `2026-06-30` (0 out-of-bound or invalid dates) | ✅ |
| **4. Vocabulary Integrity** | Category dictionary | 0 unexpected or orphaned category strings | ✅ |
| **5. Value Boundaries** | Range check | `Tokens`: [411, 58,989], `Tasks`: [1, 12], `Gain`: [0.3%, 84.9%], `Exp`: [1.0, 25.0] | ✅ |
| **6. Nesting Integrity** | Crosstab check | 22 valid combinations (Strict 1-to-1 nesting of `Job_Role` in `Industry`) | ✅ |
| **7. Cardinality & Distribution** | `nunique()` count | 15,000 users, 7 AI tools, 6 industries, 22 job roles, 67 monthly periods | ✅ |
| **8. Logical Consistency** | Non-negative logic | 0 negative token values, 0 negative gain values, 0 negative experience values | ✅ |
| **9. Outlier Policy** | Heavy-tail IQR audit | Power-user tail retained (IQR upper = 23,248 tokens); managed via **HC3 Robust SE** | ✅ |
| **10. Macro Dataset Integrity** | Granularity audit | 402 macro rows across 67 monthly timeline points and 6 global sectors | ✅ |

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

## 🚀 Cara Menjalankan Project

### 1. Web Dashboard (Wajib via Local HTTP Server)
> [!IMPORTANT]
> **Catatan Keamanan Browser (CORS restriction)**:  
> Karena dashboard menggunakan fitur `fetch()` dinamis dan parser `PapaParse` untuk membaca dataset CSV, membuka file `index.html` langsung melalui protokol `file://` akan diblokir oleh kebijakan keamanan CORS di mayoritas browser modern.  
> **Wajib** menjalankan aplikasi melalui Local HTTP Server:

```bash
# Jalankan Local HTTP Server dari root folder project:
python -m http.server 8080

# Kemudian buka browser dan akses:
http://localhost:8080
```
*Atau gunakan ekstensi **Live Server** di VS Code (Klik kanan `index.html` → "Open with Live Server").*

### 2. 🌐 Opsi Deployment Publik
Aplikasi web ini bersifat *static & client-side dynamic* yang siap untuk didaftarkan (*zero-config deployment*) ke platform hosting publik:
- **Vercel**: Hubungkan repositori GitHub dan deploy root directory.
- **Netlify**: Drag-and-drop folder project ke Netlify Drop atau hubungkan via Git.
- **GitHub Pages**: Aktifkan GitHub Pages pada tab *Settings → Pages* repositori GitHub (`main` branch / root).

---

### 3. Regenerasi Charts, Model Outputs & Feature Engineering
```bash
# Install dependencies:
pip install -r requirements.txt

# Jalankan pipeline EDA & ekspor model JSON:
python scripts/run_eda.py
```
> Output: memperbarui `data/user_level_ai_adoption_enriched.csv`, `outputs/model_summary.json`, dan semua file `charts/*.png`

### 4. Menjalankan Unit Tests (Pytest)
```bash
# Jalankan unit test suite untuk memverifikasi integritas data & pemodelan:
python -m pytest tests/ -v
```

### 5. Eksekusi Notebook Analisis Reproducible
```bash
# Opsi A: Buka secara interaktif di Jupyter
jupyter notebook notebooks/critical_data_analysis.ipynb

# Opsi B: Eksekusi otomatis secara non-interaktif (CI/CD Automated Execution)
jupyter nbconvert --to notebook --execute notebooks/critical_data_analysis.ipynb --output executed_notebook.ipynb
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

1. **Targeted AI Tooling** — Prioritaskan tools AI terspesialisasi (*Copilot, DeepSeek*) untuk divisi teknis dibanding lisensi generalist semua divisi.
2. **Tata Kelola Kuota Token Berbasis Perangkat & Peran (Role & Tool-Aware Token Governance)** — Hindari asumsi naif bahwa menaikkan kuota token secara umum akan otomatis meningkatkan produktivitas ($r = 0.88$ dipengaruhi oleh kategori perangkat). Kuota token harus dialokasikan secara selektif berdasarkan kebutuhan alur kerja spesifik.
3. **Standardisasi Task Automation** — Dorong penggunaan AI untuk otomatisasi alur kerja berulang, bukan sekadar *Q&A*.
4. **Mitigasi Bias Self-Reporting** — Gabungkan metrik persepsi produktivitas dengan data objektif (*PR completion time, ticket closure rate*) untuk riset lanjutan.

---

*© 2026 · AI Adoption & Productivity Analytics Project · Data Analyst Portfolio*
