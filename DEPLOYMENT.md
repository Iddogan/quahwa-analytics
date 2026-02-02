# Streamlit Deployment za Quahwa Analytics ☕

## Koraci za Deployment na Streamlit Community Cloud

### 1. **Pripremi GitHub Repository** ✅
Repository je već pushovan na: `https://github.com/Iddogan/quahwa-analytics.git`

### 2. **Konfiguracija Fajlovi** ✅
- ✅ `requirements.txt` - sve dependencies
- ✅ `.streamlit/config.toml` - tema i server postavke
- ✅ `streamlit_app.py` - glavni entry point

### 3. **Deploy na Streamlit Cloud**

#### 3.1. Idi na [share.streamlit.io](https://share.streamlit.io)

#### 3.2. Klikni "New app"

#### 3.3. Popuni deployment formu:
- **Repository:** `Iddogan/quahwa-analytics`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`

#### 3.4. Advanced settings (opcionalno):
- **Python version:** 3.11 ili 3.12
- **Secrets:** Dodaj ako imaš API ključeve (nije potrebno za ovaj projekt)

#### 3.5. Klikni "Deploy!"

### 4. **Čekaj Deployment** ⏱️
Deployment traje 2-5 minuta. Streamlit će:
- Instalirati sve pakete iz `requirements.txt`
- Pokrenuti aplikaciju
- Dodijeliti javni URL (npr. `quahwa-analytics.streamlit.app`)

---

## Važne Napomene za Deployment

### ⚠️ **PROBLEM: Data Files**
**Dashboard trenutno traži Excel fajlove u `/data` folderu.**

Imate 2 opcije:

#### **OPCIJA A: Upload Data na GitHub** (NE PREPORUČLJIVO za osjetljive podatke)
```bash
git add data/*.xlsx
git commit -m "Add data files for deployment"
git push
```
⚠️ **UPOZORENJE:** Podaci će biti javno vidljivi na GitHub-u!

#### **OPCIJA B: Koristiti Streamlit Secrets za Data** (PREPORUČLJIVO)
Umjesto da čitaš Excel fajlove, prebaci ih u online storage:
1. Google Drive
2. AWS S3
3. Azure Blob Storage
4. Ili koristi API za real-time podatke

---

## Trenutna Struktura

```
quahwa-analytics/
├── streamlit_app.py          ← Entry point za Streamlit Cloud
├── requirements.txt          ← Dependencies
├── .streamlit/
│   ├── config.toml          ← Tema i server config
│   └── secrets.toml         ← Secrets (prazan)
├── dashboard/
│   └── app_complete.py      ← Glavni dashboard
├── src/
│   ├── analysis/
│   │   └── advanced_analytics.py
│   └── utils/
│       └── auto_data_loader.py
└── data/                    ← ⚠️ NIJE na GitHubu (gitignored)
    ├── Excel analiza racuna od 02.01.2024 do 31.12.2024.xlsx
    ├── Excel analiza racuna od 01.01.2025 do 31.12.2025.xlsx
    └── Excel analiza racuna od 01.01.2026 do 31.01.2026.xlsx
```

---

## 🎯 Sljedeći Koraci

### Ako želiš deploy ODMAH sa podacima:
```bash
# 1. Provjeri .gitignore
cat .gitignore

# 2. Ako data/ je u .gitignore, makni ga
# nano .gitignore (ukloni liniju "data/")

# 3. Upload data
git add data/*.xlsx
git commit -m "Add data files for cloud deployment"
git push

# 4. Deploy na share.streamlit.io
```

### Ako želiš deploy BEZ podataka (demo mode):
Moram modifikovati `app_complete.py` da prikaže demo poruku ako nema podataka.

---

## 📝 Deployment Checklist

- ✅ GitHub repository pushovan
- ✅ `requirements.txt` kreiran
- ✅ `.streamlit/config.toml` kreiran
- ✅ `streamlit_app.py` entry point kreiran
- ❌ **Data fajlovi na GitHub** (odluči hoćeš li ih upload-ati)
- ⏳ **Deployment na share.streamlit.io** (čeka na tvoju akciju)

---

## 🚀 Alternative: Local Deployment

Ako ne želiš javni deployment, možeš pokrenuti lokalno:

```bash
cd C:\Projekti\Quahwa\dashboard
streamlit run app_complete.py --server.port 8501
```

Ili share lokalno sa ngrok:
```bash
# Install ngrok
# Pokreni dashboard
streamlit run app_complete.py

# U drugom terminalu
ngrok http 8501
```

---

**Šta želiš da uradim?**
1. Upload podatke na GitHub i deploy javno?
2. Kreiraj demo mode bez podataka?
3. Nešto drugo?
