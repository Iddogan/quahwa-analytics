# 🎉 QUAHWA ANALYTICS - GOTOVO!

## ✅ ŠTO JE NAPRAVLJENO

Kreiran je **kompletan analitički dashboard** sa **10 detaljnih tabova** i **automatskim učitavanjem podataka**.

### 📊 **10 ANALITIČKIH TABOVA:**

#### 1. 📊 **Executive Dashboard**
- KPI kartice (Promet, Računi, Prosječan račun, Količina)
- Top 5 artikala
- Promet po prodajnim grupama
- Dnevni trend sa MA7 i MA30

#### 2. 💰 **Financijska Analiza**
- Struktura prihoda (Neto, PDV, Popusti)
- Mjesečni promet sa MoM% rastom
- Analiza načina plaćanja
- Detaljne mjesečne metrike

#### 3. 🛒 **Analiza Prodaje**
- Basket analysis (stavki po računu, vrijednost korpe)
- Top 20 proizvoda
- Prodajne grupe
- Detaljna tablica svih proizvoda

#### 4. ⏰ **Vremenska Analiza**
- Promet po danima u tjednu
- Promet po satima
- Heatmap (Dan × Sat)

#### 5. 📅 **Usporedbe Perioda**
- Usporedba mjeseci (MoM)
- Custom period comparison
- Delta metrike i growth rates
- Usporedba top artikala

#### 6. 🏪 **Analiza po Lokalu/Blagajni**
- Performanse po lokalu
- Performanse po blagajni
- Performanse osoblja (top 20)

#### 7. 👥 **Analiza Kupaca**
- B2B vs B2C segmentacija
- Top 20 kupaca
- Pie chart distribucija

#### 8. 📈 **Trendovi i Prognoze**
- Dnevni trend sa moving averages (MA7, MA30)
- Month-over-Month rast
- Year-over-Year rast (ako dostupno)

#### 9. 📋 **ABC/Pareto Analiza**
- ABC kategorije (80/15/5 princip)
- Pareto dijagram
- Tabele po kategorijama
- Kumulativni postoci

#### 10. 📄 **Izvještaji i Export**
- Sažeti izvještaj
- Export dnevnog prometa (CSV)
- Export top proizvoda (CSV)
- Export ABC analize (CSV)

---

## 🚀 KAKO POKRENUTI

### 1. Otvori Terminal

```powershell
cd C:\Projekti\Quahwa\dashboard
```

### 2. Pokreni Dashboard

```powershell
streamlit run app_complete.py
```

Dashboard će se otvoriti na: **http://localhost:8503**

---

## 📁 PODACI

Dashboard **AUTOMATSKI** učitava sve Excel fajlove sa računima iz `data/` foldera!

### Trenutno učitani podaci:
- **Računi.xlsx** - Cijela 2025 godina (97,654 redova)
- **Excel analiza računa 2026-01** - Januar 2026 (9,597 redova)
- **UKUPNO: 107,251 redova**
- **Period: 02.01.2025 - 31.01.2026**

### Dodavanje novih podataka:
1. Stavi Excel fajl u `data/` folder
2. Fajl mora imati kolone: `Datum i vrijeme`, `Fiskalni broj računa`, `Artikl`, `Ukupno`
3. Refresh dashboard (F5)

---

## 🔍 GLAVNI FEATURES

### ✅ Automatsko učitavanje
- Skenira `data/` folder
- Automatski detektira račun fajlove
- Objedinjuje sve u jedan dataset
- Procesira i priprema podatke

### ✅ Napredne analize
- **Financijske**: PDV, popusti, načini plaćanja, mjesečni trendovi
- **Prodajne**: Top proizvodi, kategorije, basket analysis, ABC
- **Vremenske**: Heatmap, dani, sati, sezonalnost
- **Usporedbe**: MoM, YoY, custom periodi
- **Kupci**: B2B/B2C, top kupci, segmentacija

### ✅ Interaktivni grafovi
- Plotly interaktivni grafovi
- Hover tooltips
- Zoom, pan, export
- Profesionalni dizajn

### ✅ Export funkcionalnost
- CSV export svih izvještaja
- Print-ready format
- Detaljne tabele

### ✅ Filteri
- Globalni period filter u sidebar-u
- Automatsko ponovno računanje

---

## 📊 DODATNE ANALIZE DOSTUPNE

### Finansijske Metrike
- Ukupan promet, PDV, Neto
- Prosječan račun
- Moving averages (7-dana, 30-dana)
- MoM i YoY rast
- PDV stopa, postotak popusta

### Prodajne Metrike
- Top N proizvoda (po prometu i količini)
- Udio u prometu po proizvodima/grupama
- ABC kategorije
- Basket size i vrijednost
- Cross-selling potencijal

### Vremenske Metrike
- Peak hours i peak days
- Heatmap aktivnosti
- Dnevni/Mjesečni/Kvartalni trendovi
- Sezonalnost

### Customer Insights
- B2B vs B2C raspodjela
- Top kupci
- Frekvencija kupnje

---

## 📂 STRUKTURA PROJEKTA

```
Quahwa/
├── data/                          ← Stavi Excel fajlove ovdje
│   ├── Računi.xlsx
│   └── Excel analiza...xlsx
├── dashboard/
│   ├── app_complete.py           ← NOVI KOMPLETAN DASHBOARD ⭐
│   ├── app_simple.py             
│   └── app.py                    
├── src/
│   ├── utils/
│   │   ├── auto_data_loader.py   ← Automatsko učitavanje ⭐
│   │   ├── data_loader.py
│   │   └── multi_file_loader.py
│   └── analysis/
│       ├── advanced_analytics.py  ← Sve analitičke klase ⭐
│       ├── sales_analysis.py
│       └── time_analysis.py
├── PLAN.md                        ← Detaljan plan implementacije
└── README.md
```

---

## 💡 TIPS & TRICKS

### Brže učitavanje
- Dashboard cache-ira podatke
- Promjena perioda u sidebar-u je instant
- Refresh samo ako dodaješ nove fajlove

### Best Practices
- Koristi period filter za fokusirane analize
- Export CSV za detaljne analize u Excelu
- ABC analiza pomaže u optimizaciji asortimana
- Heatmap pokazuje peak hours za planiranje smjena

### Interpretacija
- **A proizvodi** = 80% prometa, fokusiraj se na njih
- **Peak hours** = najbolje vrijeme za promocije
- **MoM rast** = prati mjesečni napredak
- **B2B vs B2C** = različite strategije za segmente

---

## 🎯 KORIŠTENJE ZA PREZENTACIJU UPRAVI

### Executive Summary (Tab 1)
- Brzi pregled ključnih metrika
- Top 5 proizvoda i grupe
- Dnevni trend

### Financijski Izvještaj (Tab 2)
- Mjesečni promet sa rastom
- PDV analiza
- Načini plaćanja

### Prodajne Performanse (Tab 3)
- Top proizvodi
- Basket analysis
- Detaljne tabele

### Planiranje (Tab 4 + 8)
- Vremenska analiza za optimizaciju smjena
- Trendovi za forecast
- Sezonski uzorci

### ABC Optimizacija (Tab 9)
- Identifikacija key proizvoda
- Slow-movers
- Portfolio optimizacija

---

## 📞 DODATNE MOGUĆNOSTI

Ako trebaš dodatne analize, lako se mogu dodati:
- Inventory turnover
- Customer lifetime value
- Forecast modeli
- Cohort analysis
- Geo analysis (ako dodamo lokacije)
- itd.

---

**Dashboard je spreman za korištenje! 🎉**

Otvori: **http://localhost:8503**
