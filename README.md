# ☕ Quahwa Analytics Dashboard

Napredni analitički dashboard sa automatskim učitavanjem podataka, multi-godišnjim analizama i detaljnim BI metrikama.

## 📋 Opis

Quahwa Dashboard je interaktivna aplikacija za kompleksnu analizu prodajnih podataka koja omogućava:
- **Automatsko učitavanje**: Automatski detektuje i učitava sve Excel fajlove iz data foldera
- **Multi-godišnja analiza**: Podrška za analizu više godina istovremeno (2024-2026)
- **10 specijalizovanih tabova**: Executive, Financije, Prodaja, Vremenska analiza, Usporedbe, Lokacije, Kupci, Trendovi, KPI i ABC analiza
- **Napredne metrike**: MoM%, YoY%, statističke mjere (n, μ, σ), trendovi i prognoze
- **Interaktivne vizualizacije**: Plotly grafovi sa zoom, filter i export opcijama

## ✨ Ključne Karakteristike

### Automatizacija
- 🔄 **Auto Data Loading** - Automatski pronalazi i učitava sve račun fajlove
- 📁 **Multi-sheet Support** - Inteligentno prepoznavanje sheet-ova u Excel fajlovima
- 🗓️ **Year-based Filtering** - 3 moda: single year, year comparison, all years
- 🏷️ **Column Mapping** - Automatsko mapiranje različitih naziva kolona

### Analitika
- 📊 **6 Analytics Classes** - FinancialAnalytics, SalesAnalytics, TimeAnalytics, LocationAnalytics, CustomerAnalytics, ProductComparisonAnalytics
- 📈 **Statistical Standards** - Sample size (n), Mean (μ), Std Dev (σ), MoM%, YoY%
- 🎯 **KPI Tracking** - Executive metrike, basket analysis, location performance
- 🔍 **Product Comparison** - Month-by-month usporedbe proizvoda i kategorija

### Vizualizacije
- 📉 **10 Dashboard Tabs** - Svaki tab fokusiran na specifičan aspect poslovanja
- 🎨 **Interactive Charts** - Plotly grafovi sa hover tooltipovima i data labeling
- 📊 **Heatmaps & Trends** - Vremenske distribucije, YoY usporedbe
- 🌈 **Color-coded Tables** - Background gradients za % promjene

## 🚀 Instalacija

### 1. Klonirajte repozitorij:

```bash
git clone <repository-url>
cd Quahwa
```

### 2. Instalirajte zavisnosti:

```bash
pip install -r requirements.txt
```

Potrebne biblioteke:
- streamlit
- pandas
- plotly
- openpyxl
- xlrd
- matplotlib
- numpy
- python-dateutil

### 3. Pripremite podatke:

Stavite Excel fajlove sa računima u `data/` folder. Dashboard će automatski pronaći sve fajlove koji sadrže "račun" ili "racun" u imenu.

## 📁 Struktura Projekta

```
Quahwa/
│
├── dashboard/                 # Streamlit dashboards
│   └── app_complete.py       # Glavni dashboard (10 tabova)
│
├── src/                      # Izvorni kod
│   ├── utils/               # Pomoćne funkcije
│   │   ├── auto_data_loader.py   # Automatsko učitavanje podataka
│   │   └── data_loader.py        # Osnovni data loader
│   │
│   └── analysis/            # Moduli za analizu
│       └── advanced_analytics.py  # 6 analytics klasa
│
├── data/                    # Excel fajlovi sa podacima
│   ├── Excel analiza racuna od 01.01.2024 do 31.12.2024.xlsx
│   ├── Excel analiza racuna od 01.01.2026 do 31.01.2026.xlsx
│   └── Računi.xlsx
│
├── requirements.txt         # Python zavisnosti
├── README.md               # Dokumentacija
└── GIT_SETUP.md           # Git setup instrukcije
```

## 🎯 Kako Koristiti

### Pokretanje Dashboarda

```bash
# Iz root direktorija
streamlit run dashboard/app_complete.py --server.port 8510

# Ili iz dashboard foldera
cd dashboard
streamlit run app_complete.py
```

Dashboard će se otvoriti u browseru (npr. `http://localhost:8510`)

### Dashboard Tabovi

1. **📊 Executive Dashboard**
   - Osnovni KPI-jevi (promet, broj računa, prosječan račun)
   - Year-over-year usporedbe sa YoY% promjenama
   - Mjesečni trendovi kroz sve godine
   - Top 5 artikala i distribucija po prodajnim grupama

2. **💰 Financijska Analiza**
   - Revenue struktura (Ukupno, Neto, Popusti)
   - Mjesečni promet sa MoM% i YoY% promjenama
   - Statistički opisi (n, μ, σ)
   - Načini plaćanja

3. **🛒 Analiza Prodaje**
   - Basket analytics (prosječna vrijednost korpe, količina po računu)
   - Top 20 proizvoda sa % udjela
   - Prodajne grupe sa distribucijom prometa

4. **⏰ Vremenska Analiza**
   - Promet po danima u tjednu
   - Promet po satima
   - Heatmap (Dan × Sat)

5. **📈 Usporedbe Proizvoda i Kategorija**
   - Month-by-month trendovi po kategorijama
   - % Promjena MoM sa color-coded tablicama
   - Multi-product usporedbe
   - Top growers/decliners

6. **🏪 Analiza po Lokalu**
   - Performance po lokalu
   - Performance po blagajni
   - Geografska distribucija prometa

7. **👥 Analiza Kupaca**
   - Segmentacija kupaca
   - Ponašanje kupaca kroz vrijeme

8. **📉 Trendovi i Predikcije**
   - Mjesečni trendovi sa prognozama
   - Seasonality analiza

9. **🎯 KPI Praćenje**
   - Month-over-Month rast grafovi
   - Year-over-Year rast grafovi
   - Ključni poslovni pokazatelji

10. **📊 ABC Analiza**
    - Pareto princip (80/20 pravilo)
    - Klasifikacija proizvoda (A, B, C)
    - Identifikacija ključnih proizvoda

### Filteri u Sidebaru

- **Year Selection**: Odabir jedne ili više godina
  - Single year mode: Fokus na jednu godinu
  - Year comparison: Usporedba 2-3 godine
  - All years: Prikaz svih podataka

- **Month Filter**: Filtriraj po mjesecima (opciono)
- **Location Filter**: Filtriraj po lokalu (opciono)

## 💻 Programski Primjeri

### Automatsko učitavanje svih podataka:

```python
from src.utils.auto_data_loader import AutoDataLoader

# Učitaj sve račun fajlove iz data foldera
loader = AutoDataLoader("data")
df = loader.load_all_racuni()

# Pregledaj summary
summary = loader.get_summary()
print(f"Učitano {summary['total_rows']} redova iz {summary['file_count']} fajlova")
print(f"Period: {summary['date_range']['start']} - {summary['date_range']['end']}")
```

### Financial Analytics:

```python
from src.analysis.advanced_analytics import FinancialAnalytics

# Kreiraj analytics objekat
fin = FinancialAnalytics(df)

# KPI metrike
kpis = fin.get_kpi_metrics()
print(f"Ukupan promet: {kpis['ukupan_promet']:,.2f} EUR")
print(f"Broj računa: {kpis['broj_računa']:,}")
print(f"Prosječan račun: {kpis['prosječan_račun']:.2f} EUR")

# Mjesečne metrike sa MoM% i YoY%
monthly = fin.get_monthly_metrics()
print(monthly[['Period', 'Promet', 'Promjena_MoM%', 'Promjena_YoY%']])

# Revenue struktura
revenue = fin.get_revenue_structure()
print(f"Ukupno: {revenue['ukupno']:,.2f} EUR")
print(f"Neto: {revenue['neto']:,.2f} EUR ({revenue['neto_dio%']:.1f}%)")
```

### Product Comparison:

```python
from src.analysis.advanced_analytics import ProductComparisonAnalytics

comp = ProductComparisonAnalytics(df)

# Usporedi kategorije mjesečno
cat_comp = comp.compare_categories_monthly()
monthly_revenue = cat_comp['mjesecni_promet']  # DataFrame sa prometo

m po kategorijama
pct_change = cat_comp['promjena_promet_%']  # MoM% promjene

# Top growers and decliners
growers = comp.top_growers_and_decliners(period='M')
print("Top 10 proizvoda sa najvećim rastom:")
print(growers['najveci_rast'])
```

## 📊 Analytics Classes

### 1. FinancialAnalytics
- `get_kpi_metrics()` - Osnovni KPI-jevi (promet, računi, količina)
- `get_monthly_metrics()` - Mjesečne metrike sa MoM% i YoY%
- `get_revenue_structure()` - Revenue breakdown (Ukupno, Neto, Popusti)
- `get_daily_metrics()` - Dnevne metrike

### 2. SalesAnalytics
- `get_top_products(n)` - Top N proizvoda po prometu
- `get_product_categories()` - Analiza po prodajnim grupama
- `get_basket_analysis()` - Basket metrics (prosječna vrijednost, količina)
- `get_sales_metrics()` - Ključne sales metrike

### 3. TimeAnalytics
- `get_daily_pattern()` - Analiza po danima u tjednu
- `get_hourly_pattern()` - Analiza po satima
- `get_heatmap_data()` - Dan × Sat heatmap data
- `get_time_period_analysis()` - Period dana analiza (jutro, popodne, večer)

### 4. LocationAnalytics
- `get_location_performance()` - Performance po lokalu
- `get_cashier_performance()` - Performance po blagajni
- `compare_locations()` - Usporedba lokacija

### 5. CustomerAnalytics
- `get_customer_segments()` - Segmentacija kupaca
- `get_customer_behavior()` - Analiza ponašanja
- `get_top_customers()` - Top kupci

### 6. ProductComparisonAnalytics
- `compare_categories_monthly()` - Month-by-month usporedba kategorija
- `compare_products_monthly(products)` - Usporedba odabranih proizvoda
- `year_over_year_comparison(month)` - YoY usporedba za specifičan mjesec
- `top_growers_and_decliners(period)` - Top rast/pad proizvoda

## 📈 Statistički Standardi

Dashboard koristi statističke standarde za sve metrike:

- **n** - Sample size (broj opažanja, transakcija, mjeseci)
- **μ** (mu) - Aritmetička sredina (mean)
- **σ** (sigma) - Standardna devijacija (standard deviation)
- **MoM%** - Month-over-Month promjena (mjesec vs prethodni mjesec)
- **YoY%** - Year-over-Year promjena (godina vs prethodna godina za isti mjesec)

Primjer:
```
Mjesečni Promet | n=36 mjeseci, μ=22,055 EUR, σ=5,234 EUR
```

## 📈 Varijable u Podacima

Dataset sadrži sljedeće kolone:

**Osnovne informacije:**
- Lokal - Naziv lokala
- Blagajna - Identifikator blagajne  
- Knjigovodstveni datum - Datum za knjiženje
- Datum i vrijeme - Tačno vrijeme transakcije

**Transakcija:**
- Način plaćanja - Metoda plaćanja
- Način prodaje - Tip prodaje
- Fiskalni broj računa - Jedinstveni broj računa
- Izdao - Ko je izdao račun

**Kupac:**
- Kupac - Informacije o kupcu
- Porezni broj kupca - PIB kupca

**Finansije:**
- Ukupno račun - Ukupan iznos računa
- Ukupno neto - Neto iznos (bez PDV)
- Ukupno popusta - Ukupan popust
- Ukupno - Ukupan iznos stavke

**Proizvod:**
- Šifra - Šifra artikla
- Artikl - Naziv artikla
- Prodajna grupa - Kategorija proizvoda
- Količina - Prodata količina
- Cijena - Cijena po jedinici
- Cijena s popustom - Cijena nakon popusta

**Generirane kolone** (dodaje AutoDataLoader):
- Godina - Ekstrahovana godina
- Mjesec - Ekstrahovani mjesec (1-12)
- Dan - Ekstrahovani dan
- Sat - Ekstrahovani sat (0-23)
- Dan_u_tjednu - Dan u tjednu (0=Ponedjeljak, 6=Nedjelja)

## 🔧 Napredne Funkcionalnosti

### AutoDataLoader
```python
loader = AutoDataLoader("data")

# Učitaj sve fajlove
df = loader.load_all_racuni()

# Summary informacije
summary = loader.get_summary()
# {
#   'total_rows': 204987,
#   'file_count': 3,
#   'files': [...],
#   'date_range': {'start': '2024-01-02', 'end': '2026-01-31'},
#   'columns': [...]
# }
```

### Multi-sheet Excel Support
AutoDataLoader automatski:
- Detektuje sve sheet-ove u Excel fajlu
- Pronalazi sheet sa kolonom "Fiskalni broj računa"
- Učitava podatke iz ispravnog sheet-a

### Year-based Filtering
```python
# U dashboard-u: sidebar multiselect za godine
selected_years = st.multiselect("Odaberi godine", [2024, 2025, 2026])

# Dashboard automatski filtrira podatke
df_filtered = df[df['Godina'].isin(selected_years)]
```

## 🎨 Customizacija

### Dodavanje novih analiza:

1. Kreiraj novu metodu u odgovarajućoj analytics klasi
2. Dodaj novi tab u dashboard-u
3. Pozovi metodu i prikažI rezultate

Primjer:
```python
# U advanced_analytics.py
class SalesAnalytics:
    def get_product_velocity(self):
        """Brzina prodaje proizvoda."""
        return self.df.groupby(['Artikl', 'Mjesec']).agg({
            'Količina': 'sum'
        }).reset_index()

# U app_complete.py
with tabs[X]:
    st.header("Brzina Prodaje")
    velocity = sales_analytics.get_product_velocity()
    st.dataframe(velocity)
```

## 📝 Napomene

- **Automatsko učitavanje**: Dashboard automatski detektuje sve račun fajlove u data folderu
- **Multi-godina support**: Podrška za analizu podataka kroz više godina
- **Statistički standardi**: Sve metrike prate znanstvene standarde (n, μ, σ, MoM%, YoY%)
- **Optimizovano**: Cache mehanizam za brže učitavanje
- **Responsive**: Dashboard se prilagođava veličini ekrana

## 🐛 Rješavanje Problema

**Problem**: "Nema pronađenih račun fajlova"
```bash
# Provjeri da li su fajlovi u data/ folderu
ls data/

# Imena fajlova moraju sadržavati "račun" ili "racun"
# Primjer: "Excel analiza racuna 2024.xlsx"
```

**Problem**: ValueError sa kolonama
```bash
# Provjeri da Excel fajl sadrži potrebne kolone
# Minimalno potrebne: 'Fiskalni broj računa', 'Datum i vrijeme', 'Ukupno', 'Artikl'
```

**Problem**: Dashboard se sporo učitava
```bash
# Očisti cache
streamlit cache clear

# Restartuj dashboard
```

**Problem**: Grafovi prikazuju stare podatke
```bash
# Refresh stranicu (F5) ili klikni "Rerun" u dashboard-u
# Cache se automatski očisti kad se podaci promijene
```

## 📧 Podrška

Za pitanja i podršku:
- Pregledajte [GIT_SETUP.md](GIT_SETUP.md) za Git setup
- Provjerite Issues na GitHub repozitoriju

---

**Verzija**: 2.0  
**Datum**: Februar 2026  
**Status**: Production Ready  
**Dataset**: 204,987 redova (2024-2026)
