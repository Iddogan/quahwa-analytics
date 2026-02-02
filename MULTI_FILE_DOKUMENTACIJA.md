# Multi-File Izvješće - Dokumentacija

## 📋 Pregled

Nova funkcionalnost omogućava učitavanje i analizu **više Excel tablica odjednom** sa automatskim izvješćem svih varijabli koje postoje u svim tablicama.

## 🆕 Nove mogućnosti

### 1. **Tri načina učitavanja podataka**

#### a) Jedan fajl (postojeća funkcionalnost)
- Učitava jedan Excel fajl
- Sve analize se vrše na tom jednom fajlu

#### b) Više fajlova (upload)
- Upload više Excel fajlova odjednom
- Automatski se objedinjuju u jedan dataset

#### c) Fajlovi iz foldera
- Automatski učitava sve Excel fajlove iz `data/` foldera
- Idealno za redovne izvještaje

### 2. **Izvješće svih varijabli** 📊

Novi tab "📋 Izvješće varijabli" prikazuje:

- **Sve kolone/varijable** iz svih učitanih tablica
- **Tip podataka** svake varijable
- **Broj vrijednosti** (ukupno i validnih)
- **Procenat popunjenosti**
- **Broj jedinstvenih vrijednosti**
- **Primjer vrijednosti**
- **Statistiku** za numeričke varijable (Min, Max, Prosjek, Suma)

### 3. **Usporedba kolona između fajlova** 🔍

Prikazuje koje kolone postoje u kojim fajlovima:
- ✓ označava da kolona postoji (sa tipom podataka)
- ✗ označava da kolona ne postoji

### 4. **Pregled fajlova** 📁

Novi tab "📁 Pregled fajlova" prikazuje:
- Broj učitanih fajlova
- Broj redova po fajlu
- Period podataka po fajlu
- Promet po fajlu
- Grafičku vizualizaciju

## 🚀 Kako koristiti

### Korak 1: Priprema podataka

Stavi Excel fajlove u `data/` folder:

```
Projekti/Quahwa/
  ├── data/
  │   ├── januar_2024.xlsx
  │   ├── februar_2024.xlsx
  │   └── mart_2024.xlsx
  ├── dashboard/
  └── src/
```

### Korak 2: Testiranje (opcionalno)

Kreiraj test podatke i testiraj:

```powershell
python test_multi_file.py
```

Ova skripta će:
- Kreirati 3 primjera Excel fajlova u `data/` folderu
- Testirati sve funkcionalnosti
- Prikazati izvještaje u konzoli

### Korak 3: Pokretanje dashboarda

```powershell
cd dashboard
streamlit run app.py
```

### Korak 4: Učitavanje podataka

U sidebar-u:

1. Odaberi **"Fajlovi iz foldera"** (ili "Više fajlova" za upload)
2. Klikni **"📥 Učitaj podatke"**
3. Pričekaj da se svi fajlovi učitaju

### Korak 5: Istraživanje

Sada imaš 6 tabova:

1. **📊 Pregled** - Osnovne metrike
2. **⏰ Vremenska Analiza** - Analiza po vremenu
3. **🛒 Analiza Prodaje** - Top proizvodi, grupe
4. **📈 ABC Analiza** - Pareto analiza
5. **📋 Izvješće varijabli** ⭐ NOVO - Sve varijable iz svih tablica
6. **📁 Pregled fajlova** ⭐ NOVO - Detalji o učitanim fajlovima

## 📊 Primjer korištenja

### Scenario: Analiziraš podatke iz 3 mjeseca

```
data/
  ├── januar_2024.xlsx   (5000 redova, 8 kolona)
  ├── februar_2024.xlsx  (6000 redova, 8 kolona)
  └── mart_2024.xlsx     (5500 redova, 10 kolona)  # Ima 2 dodatne kolone
```

**Što dashboard prikazuje:**

1. **Pregled fajlova:**
   - 3 fajla učitana
   - 16,500 ukupno redova
   - Period: 01.01.2024 - 31.03.2024

2. **Izvješće varijabli:**
   ```
   Varijabla           | Tip      | Popunjenost | Unikatnih
   --------------------|----------|-------------|----------
   Datum i vrijeme     | datetime | 100%        | 16,500
   Lokal               | object   | 100%        | 1
   Fiskalni broj       | object   | 100%        | 16,500
   Artikl              | object   | 100%        | 25
   Prodajna grupa      | object   | 100%        | 5
   Količina            | int      | 100%        | 10
   Ukupno              | float    | 100%        | 450
   Blagajna            | object   | 33.3%       | 2  # Samo u mart_2024
   PDV                 | float    | 33.3%       | 150 # Samo u mart_2024
   ```

3. **Usporedba kolona:**
   ```
   Kolona           | januar_2024.xlsx | februar_2024.xlsx | mart_2024.xlsx
   -----------------|------------------|-------------------|----------------
   Datum i vrijeme  | ✓ (datetime)     | ✓ (datetime)      | ✓ (datetime)
   Lokal            | ✓ (object)       | ✓ (object)        | ✓ (object)
   Blagajna         | ✗                | ✗                 | ✓ (object)
   PDV              | ✗                | ✗                 | ✓ (float)
   ```

## 💡 Korištenje za različite izvještaje

### Mjesečni izvještaji
```
data/
  ├── 2024_01_januar.xlsx
  ├── 2024_02_februar.xlsx
  └── 2024_03_mart.xlsx
```

### Izvještaji po lokaciji
```
data/
  ├── lokacija_centar.xlsx
  ├── lokacija_zapad.xlsx
  └── lokacija_istok.xlsx
```

### Različite izvore podataka
```
data/
  ├── pos_sistem_export.xlsx
  ├── fiskalizacija_export.xlsx
  └── knjig_evidencija.xlsx
```

## 🔧 Tehnički detalji

### Struktura koda

```
src/utils/
  ├── data_loader.py          # Postojeći - učitava jedan fajl
  └── multi_file_loader.py    # NOVI - učitava više fajlova
```

### Ključne klase i metode

#### `MultiFileLoader`

```python
loader = MultiFileLoader("data/")

# Pronađi sve Excel fajlove
files = loader.discover_excel_files()

# Učitaj sve fajlove
loader.load_all_files()

# Objedini u jedan DataFrame
df = loader.combine_data()

# Izvještaji
summary = loader.get_summary_report()
variables = loader.get_variable_summary()
comparison = loader.get_column_comparison()
```

### Interna kolona: `_Izvor_Fajl`

Svaki red u objedinjenom DataFrame-u ima kolonu `_Izvor_Fajl` koja označava iz kojeg fajla dolazi taj red. Ovo omogućava:
- Filtriranje po izvoru
- Analizu po fajlovima
- Debugging i verifikaciju

## ⚙️ Konfiguracija

### Promjena data foldera

U `app.py`:

```python
data_folder = Path(__file__).parent.parent / 'data'
```

Promijeni u:

```python
data_folder = Path("c:/MojPodaci/Excel/")
```

### Dodavanje novih kolona u mapiranje

U `data_loader.py`, dodaj u `COLUMN_MAPPINGS`:

```python
COLUMN_MAPPINGS = {
    # ... postojeće ...
    'Nova_Kolona': ['nova kolona', 'nova', 'new column'],
}
```

## 📥 Export izvještaja

Sva izvješća se mogu preuzeti kao CSV:

- **Izvješće varijabli** → `varijable_izvjestaj.csv`
- **Usporedba kolona** → `usporedba_kolona.csv`
- **Objedinjeni podaci** → (koristi postojeću export funkcionalnost)

## 🐛 Troubleshooting

### Problem: "Nema pronađenih Excel fajlova"

**Rješenje:**
- Provjeri da je `data/` folder u pravom mjestu
- Provjeri da fajlovi imaju `.xlsx` ili `.xls` ekstenziju
- Provedi test sa `test_multi_file.py`

### Problem: "Greška pri učitavanju fajla X"

**Rješenje:**
- Provjeri da fajl ima kolonu 'Datum i vrijeme' (ili sličnu)
- Otvori fajl u Excelu i provjeri strukturu
- Pogledaj error message za detalje

### Problem: "Nedostaje kolona X u nekom fajlu"

**Rješenje:**
- Ovo je normalno ako različiti fajlovi imaju različite kolone
- Pogledaj "Usporedbu kolona" tab da vidiš gdje nedostaje
- Kolone sa `NaN` vrijednostima će biti automatski popunjene

## 📚 Dodatni resursi

- `test_multi_file.py` - Test skripta sa primjerima
- `GIT_SETUP.md` - Git konfiguracija
- `README.md` - Opći pregled projekta

## 🎯 Buduća poboljšanja

Moguća poboljšanja u budućnosti:

- [ ] Filter po izvoru fajla
- [ ] Usporedna analiza između fajlova
- [ ] Automatska detekcija formata datuma
- [ ] Export u Excel sa više sheet-ova
- [ ] Automatsko mapiranje različitih naziva kolona
- [ ] Incremental loading (učitavanje samo novih fajlova)

---

**Napravljeno:** Februar 2026
**Verzija:** 2.0 - Multi-File Support
