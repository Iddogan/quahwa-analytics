# ☕ Quahwa Analytics Dashboard

Kompletni analitički dashboard za analizu prodajnih podataka sa Streamlit i Plotly vizualizacijama.

## 📋 Opis

Quahwa Dashboard je interaktivna aplikacija za analizu podataka o prodaji koja omogućava:
- **Vremensku analizu**: Mjeseci, tjedni, dani, sati
- **Analizu prodaje**: Proizvodi, prodajne grupe, promet
- **ABC analizu**: Pareto princip i klasifikacija proizvoda
- **Interaktivne grafove**: Vizualizacija trendova i distribucija
- **Fleksibilno učitavanje**: Podrška za različite Excel formate i nazive kolona

## ✨ Karakteristike

- 📊 **Dinamički grafovi** - Interaktivni Plotly grafovi sa zoom, pan i hover
- 🔍 **Napredni filteri** - Filtriranje po periodu i prodajnim grupama
- 📅 **Vremenska analiza** - Analiza po mjesecima, tjednima, danima i satima
- 🏆 **Top performeri** - Identifikacija najboljih proizvoda i grupa
- 📈 **ABC analiza** - Pareto princip za optimizaciju zaliha
- 🔄 **Automatsko mapiranje** - Prepoznavanje različitih naziva kolona
- ⚠️ **Error handling** - Rad sa nepotpunim podacima

## 🚀 Instalacija

### 1. Instalirajte potrebne biblioteke:

```bash
pip install -r requirements.txt
```

Potrebne biblioteke:
- pandas
- openpyxl
- numpy
- streamlit
- plotly
- python-dateutil

### 2. Pripremite podatke:

Stavite vaš Excel fajl `Računi.xlsx` u root direktorij projekta.

## 📁 Struktura Projekta

```
Quahwa/
│
├── dashboard/              # Streamlit dashboard aplikacija
│   └── app.py             # Glavni fajl dashboarda
│
├── src/                   # Izvorni kod
│   ├── utils/            # Pomoćne funkcije
│   │   └── data_loader.py    # Učitavanje i obrada podataka
│   │
│   └── analysis/         # Moduli za analizu
│       ├── time_analysis.py   # Vremenska analiza
│       └── sales_analysis.py  # Analiza prodaje
│
├── data/                  # Folder za podatke (opciono)
│
├── Računi.xlsx           # Excel fajl s podacima
├── requirements.txt      # Python zavisnosti
└── README.md            # Dokumentacija
```

## 🎯 Kako Koristiti

### Pokretanje Dashboarda

```bash
cd dashboard
streamlit run app.py
```

Dashboard će se otvoriti u vašem web browseru na adresi `http://localhost:8501`

### Korištenje Dashboard-a

1. **Učitavanje podataka**:
   - Kliknite na dugme "📥 Učitaj podatke" u sidebar-u
   - Možete koristiti postojeći fajl ili upload-ovati novi Excel fajl

2. **Filtriranje podataka**:
   - Odaberite vremenski period (Sve, Zadnjih N dana, Custom raspon)
   - Filtrirajte po prodajnim grupama

3. **Istraživanje analiza**:
   - **📊 Pregled**: Osnovne metrike i top proizvodi
   - **⏰ Vremenska Analiza**: Trendovi po mjesecima, danima, satima
   - **🛒 Analiza Prodaje**: Detaljna analiza proizvoda
   - **📈 ABC Analiza**: Pareto princip i klasifikacija

## 📊 Dostupne Analize

### Vremenska Analiza
- Analiza po mjesecima
- Analiza po tjednima
- Analiza po danima u tjednu (Ponedjeljak - Nedjelja)
- Analiza po satima (0-23)
- Analiza po periodu dana (Jutro, Popodne, Večer, Noć)

### Analiza Prodaje
- Top proizvodi po prometu, količini ili broju računa
- Analiza po prodajnim grupama
- Distribucija prometa
- Performanse proizvoda kroz vrijeme

### ABC Analiza
- Klasifikacija proizvoda (A, B, C kategorije)
- Pareto analiza (80/20 pravilo)
- Identifikacija ključnih proizvoda

## 💻 Programski Primjeri

### Osnovno korištenje modula:

```python
from src.utils.data_loader import DataLoader
from src.analysis.time_analysis import TimeAnalyzer
from src.analysis.sales_analysis import SalesAnalyzer

# Učitavanje podataka
loader = DataLoader("Računi.xlsx")
df = loader.process_data()

# Filtriranje zadnjih 30 dana
df_filtered = loader.filter_by_date_range(last_n_days=30)

# Vremenska analiza
time_analyzer = TimeAnalyzer(df_filtered)
monthly_stats = time_analyzer.analyze_by_month()
hourly_stats = time_analyzer.analyze_by_hour()

# Analiza prodaje
sales_analyzer = SalesAnalyzer(df_filtered)
top_products = sales_analyzer.get_top_products(n=10, by='promet')
abc_analysis = sales_analyzer.analyze_revenue_distribution()

# Metrike
metrics = sales_analyzer.get_sales_metrics()
print(f"Ukupni promet: {metrics['ukupni_promet']:.2f} EUR")
```

## 📈 Varijable u Podacima

Dataset sadrži sljedeće varijable (kolone):

1. **Lokal** - Naziv lokala
2. **Blagajna** - Identifikator blagajne
3. **Knjigovodstveni datum** - Datum za knjiženje
4. **Datum i vrijeme** - Tačno vrijeme transakcije
5. **Način plaćanja** - Metoda plaćanja
6. **Način prodaje** - Tip prodaje
7. **Fiskalni broj računa** - Jedinstveni broj računa
8. **Izdao** - Ko je izdao račun
9. **Kupac** - Informacije o kupcu
10. **Porezni broj kupca** - PIB kupca
11. **PDV** - Iznos PDV-a
12. **PNP** - Porez na potrošnju
13. **Ukupno račun** - Ukupan iznos računa
14. **Šifra** - Šifra artikla
15. **Artikl** - Naziv artikla
16. **Prodajna grupa** - Kategorija proizvoda
17. **Količina** - Prodata količina
18. **Cijena** - Cijena po jedinici
19. **Cijena s popustom** - Cijena nakon popusta
20. **Ukupno popusta** - Ukupan popust
21. **Ukupno neto** - Neto iznos
22. **Ukupno** - Ukupan iznos stavke

## 🔧 Dodatne Funkcionalnosti

### DataLoader klasa:
- `load_data()` - Učitava podatke
- `process_data()` - Dodaje vremenske kolone
- `filter_by_date_range()` - Filtrira po datumu
- `get_data_summary()` - Vraća osnovne statistike

### TimeAnalyzer klasa:
- `analyze_by_month()` - Mjesečna analiza
- `analyze_by_week()` - Tjedno analiza
- `analyze_by_day_of_week()` - Analiza po danima
- `analyze_by_hour()` - Satna analiza
- `plot_monthly_trend()` - Graf mjesečnog trenda
- `plot_hourly_distribution()` - Graf satne distribucije

### SalesAnalyzer klasa:
- `analyze_by_product_group()` - Analiza po grupama
- `analyze_by_article()` - Analiza po artiklima
- `get_top_products()` - Top proizvodi
- `analyze_revenue_distribution()` - ABC analiza
- `get_sales_metrics()` - Ključne metrike
- `plot_top_products()` - Graf top proizvoda
- `plot_abc_analysis()` - ABC graf

## 🎨 Customizacija

Dashboard možete prilagoditi:
- Promijenite boje u grafovima (plotly color schemes)
- Dodajte nove metrike u `get_sales_metrics()`
- Kreirajte nove tipove analiza
- Dodajte export funkcionalnost (PDF, Excel)

## 📝 Napomene

- Podatke automatski formatira i dodaje vremenske kolone
- Svi iznosi su u EUR (Euro)
- Dashboard je optimizovan za velike količine podataka
- Interaktivni grafovi omogućavaju zoom, pan i hover

## 🐛 Rješavanje Problema

**Problem**: Podaci se ne učitavaju
- Provjerite da li je putanja do Excel fajla ispravna
- Provjerite format Excel fajla (.xlsx)

**Problem**: Grafovi se ne prikazuju
- Osvježite stranicu (F5)
- Provjerite internet konekciju (za plotly CDN)

**Problem**: Spor dashboard
- Filtrirajte podatke na manji period
- Koristite manje proizvoda u top listama

## 📧 Podrška

Za pitanja i podršku kontaktirajte autora projekta.

---

**Verzija**: 1.0  
**Datum**: Januar 2026  
**Autor**: Quahwa Analytics Team
