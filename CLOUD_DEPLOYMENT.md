# 🚀 Quahwa Analytics - Cloud Deployment

Dashboard je spreman za deployment! 

## 📋 Što je urađeno:

✅ **Hybrid Mode** - Radi i lokalno i na cloud-u
- Lokalno: Automatski učitava iz `data/` foldera
- Cloud: Omogućava upload Excel fajlova direktno u browser

✅ **Deployment Files**
- `streamlit_app.py` - Entry point za Streamlit Cloud
- `.streamlit/config.toml` - Tema (kahva boje ☕)
- `requirements.txt` - Sve dependencies

✅ **Sigurnost**
- Podaci nisu na GitHub-u (zaštićeni sa .gitignore)
- Upload se radi direktno na cloud u memoriji

---

## 🌐 Deploy SADA:

### 1️⃣ **Idi na:** https://share.streamlit.io

### 2️⃣ **Login sa GitHub accountom**

### 3️⃣ **Klikni "New app"**

### 4️⃣ **Popuni formu:**
```
Repository:     Iddogan/quahwa-analytics
Branch:         main
Main file:      streamlit_app.py
App URL:        quahwa-analytics (ili bilo šta)
```

### 5️⃣ **Klikni "Deploy!"**

⏱️ Deployment traje 2-3 minute.

---

## 📤 Kako Koristiti na Cloud-u:

1. **Otvori deployed URL** (npr. `quahwa-analytics.streamlit.app`)
2. **Upload Excel fajlove** preko file uploader-a
3. **Analiziraj podatke** - svi tabovi će raditi normalno!

---

## 🏠 Lokalno Pokretanje (kao i prije):

```bash
cd C:\Projekti\Quahwa\dashboard
streamlit run app_complete.py
```

Ili koristi novi entry point:
```bash
cd C:\Projekti\Quahwa
streamlit run streamlit_app.py
```

---

## 🎨 Tema

Dashboard ima custom temu sa kahva bojama:
- Primary: `#8B4513` (seddle brown - kao kafa ☕)
- Secondary: `#F5F5DC` (beige - kao mlijeko)
- Text: `#2F4F4F` (dark slate gray)

---

## ⚙️ Sljedeći Koraci

Samo push-aj ove izmjene i deploy:

```bash
git add .
git commit -m "Add Streamlit Cloud deployment with file upload support"
git push
```

Zatim idi na **share.streamlit.io** i deploy!

---

**URL tvoje app će biti:** 
`https://[tvoj-izbor].streamlit.app`

Npr: `quahwa-analytics.streamlit.app` ☕📊
