# 🎯 Brze Upute - Multi-File Dashboard

## ✅ Što je novo?

Sada možeš učitati **više Excel tablica odjednom** i vidjeti **izvješće svih varijabli** koje postoje u svim tablicama!

## 🚀 Kako koristiti (3 koraka)

### 1️⃣ Pokreni dashboard

```powershell
cd C:\Projekti\Quahwa\dashboard
streamlit run app.py
```

### 2️⃣ Odaberi izvor podataka

U sidebar-u imaš 3 opcije:

- **"Jedan fajl"** - Učitaj jedan Excel fajl (stara funkcionalnost)
- **"Više fajlova"** - Upload više Excel fajlova odjednom
- **"Fajlovi iz foldera"** - Automatski učitaj sve iz `data/` foldera ⭐ **PREPORUČENO**

### 3️⃣ Klikni "📥 Učitaj podatke"

Pričekaj da se fajlovi učitaju, onda istraži nove tabove!

## 📊 Novi Tabovi

### 📋 Izvješće varijabli
Prikazuje **SVE varijable (kolone)** iz svih tablica:
- Tip podataka
- Broj vrijednosti
- Procenat popunjenosti
- Jedinstvene vrijednosti
- Statistika za brojeve (min, max, prosjek)

**Primjer:**
```
Varijabla         | Tip      | Popunjenost | Unikatnih
------------------|----------|-------------|----------
Datum i vrijeme   | datetime | 100%        | 429
Lokal             | object   | 100%        | 1
Artikl            | object   | 100%        | 8
Blagajna          | object   | 33.8%       | 2  ← Samo u nekim fajlovima!
```

### 📁 Pregled fajlova
Prikazuje detalje o svakom učitanom fajlu:
- Broj redova
- Period podataka
- Ukupan promet
- Grafovi po fajlovima

## 🧪 Testiranje sa primjer podacima

Ako nemaš svoje podatke, možeš kreirati test podatke:

```powershell
python test_multi_file.py
```

Ova skripta će:
- ✅ Kreirati 3 Excel fajla u `data/` folderu
- ✅ Testirati sve funkcionalnosti
- ✅ Prikazati izvještaje u konzoli

## 📁 Primjer strukture

```
Quahwa/
  ├── data/                    ← Stavi Excel fajlove ovdje!
  │   ├── januar_2024.xlsx
  │   ├── februar_2024.xlsx
  │   └── mart_2024.xlsx
  ├── dashboard/
  │   └── app.py
  └── test_multi_file.py
```

## 💡 Korisni savjeti

1. **Različiti nazivi kolona?** 
   - Nema problema! Sistem automatski prepoznaje slične nazive
   - Npr: "Datum i vrijeme", "Datum/vrijeme", "datetime" → sve se mapiraju na "Datum i vrijeme"

2. **Nedostaju neke kolone u nekim fajlovima?**
   - Također OK! "Izvješće varijabli" će pokazati gdje koja kolona postoji
   - Tabela "Usporedba kolona" pokazuje: ✓ = postoji, ✗ = ne postoji

3. **Previše podataka?**
   - Koristi filtere u sidebar-u da smanjiš period
   - Filtriraj po prodajnoj grupi

## 📥 Download izvještaja

U "📋 Izvješće varijabli" tabu možeš preuzeti:
- `varijable_izvjestaj.csv` - Popis svih varijabli
- `usporedba_kolona.csv` - Koje kolone postoje gdje

## ❓ Česta pitanja

**Q: Mogu li miješati fajlove različitih struktura?**
A: Da! Sistem će objediniti sve kolone. One koje nedostaju bit će `NaN`.

**Q: Koliko fajlova mogu učitati odjednom?**
A: Nema ograničenja, ali pazi na memoriju ako imaš velike fajlove.

**Q: Mogu li vidjeti koja transakcija dolazi iz kojeg fajla?**
A: Da! Svaka transakcija ima internu kolonu `_Izvor_Fajl` sa nazivom fajla.

## 🆘 Pomoć

Ako nešto ne radi:
1. Provjeri da Excel fajlovi imaju kolonu sa datumom (npr. "Datum i vrijeme")
2. Pogledaj error message - često kaže što nedostaje
3. Testiraj sa `python test_multi_file.py`

---

**Verzija:** 2.0
**Zadnja izmjena:** Februar 2026
