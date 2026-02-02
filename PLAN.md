# 📊 QUAHWA ANALYTICS - PLAN IMPLEMENTACIJE

## 🎯 CILJ
Kreirati kompletan analitički dashboard sa automatskim učitavanjem podataka i detaljnim financijskim/prodajnim analizama.

## 📁 DOSTUPNI PODACI

### Tip 1: Detaljni Računi
- **Računi.xlsx** - 2025 godina (97,654 redova)
- **Excel analiza računa 2026-01** - Januar 2026 (trebaćemo učitati)

**Struktura:** Lokal, Blagajna, Datum i vrijeme, Način plaćanja, Fiskalni broj računa, Artikl, Prodajna grupa, Količina, Cijena, PDV, Ukupno, itd.

### Tip 2: Promet po artiklima
- Fajlovi su složenog formata - preskačemo za sada ili ćemo kreirati poseban loader

## 📈 PLAN ANALIZA (10 TABOVA)

### TAB 1: 📊 Executive Dashboard
**Cilj:** Brzi pregled ključnih metrika za upravu
- KPI kartice: Ukupan promet, Broj računa, Prosječan račun, Rast
- Sparkline grafovi trendova
- Top 5 artikala i grupe
- Promet po lokalu/blagajni

### TAB 2: 💰 Financijska Analiza
**Cilj:** Detaljne financijske metrike
- Dnevni/Mjesečni promet sa trendovima
- PDV analiza
- Analiza načina plaćanja (gotovina vs kartica)
- Struktura prihoda (neto, popusti, PDV)
- Financijske projekcije

### TAB 3: 🛒 Analiza Prodaje
**Cilj:** Prodajne performanse
- Top proizvodi (po prometu i količini)
- Prodajne grupe - pie chart i tabele
- Cross-selling analiza
- Basket analiza (prosječan broj stavki po računu)

### TAB 4: ⏰ Vremenska Analiza
**Cilj:** Vremenski uzorci prodaje
- Po satima (koja sati najbolje)
- Po danima u tjednu
- Po mjesecima
- Heatmap - dan × sat
- Sezonski trendovi

### TAB 5: 📅 Usporedbe Perioda
**Cilj:** Komparativna analiza
- Mjesec vs mjesec (YoY i MoM)
- Kvartal vs kvartal
- Custom period comparison
- Growth rates i delta metrike

### TAB 6: 🏪 Analiza po Lokalu/Blagajni
**Cilj:** Performanse po mjestima prodaje
- Promet po lokalu
- Promet po blagajni
- Usporedba performansi
- Analiza osoblja (Izdao kolona)

### TAB 7: 👥 Analiza Kupaca
**Cilj:** Customer insights
- B2B vs B2C (sa vs bez poreznog broja)
- Najvrjedniji kupci
- Frekvencija kupnje
- Customer segmentacija

### TAB 8: 📈 Trendovi i Prognoze
**Cilj:** Prediktivna analiza
- Trendovi prodaje (moving averages)
- Sezonalnost
- Forecast (jednostavni modeli)
- Growth metrics

### TAB 9: 📋 ABC/XYZ Analiza
**Cilj:** Optimizacija asortimana
- ABC analiza proizvoda (80/20 princip)
- XYZ analiza (volatilnost)
- Portfolio matrica
- Slow-movers identifikacija

### TAB 10: 📊 Izvještaji i Export
**Cilj:** Generiranje izvještaja
- Sažeti izvještaji
- Detaljne tabele sa filterima
- Export u Excel/CSV
- Print-ready izvještaji

## 🔧 TEHNIČKA IMPLEMENTACIJA

### Faza 1: Data Loading Module
- Auto-detekcija fajlova u `data/` folderu
- Grupiranje po tipu (Računi vs Promet)
- Objedinjavanje istog tipa
- Caching podataka

### Faza 2: Analytics Module  
- Klase za različite vrste analiza
- Helper funkcije za kalkulacije
- Statistički moduli

### Faza 3: Visualization Module
- Plotly grafovi
- Custom styling
- Interaktivne komponente

### Faza 4: Streamlit App
- Tab struktura
- Sidebar kontrole
- State management
- Performance optimization

## 📦 PYTHON PAKETI
- pandas, numpy - data manipulation
- plotly - grafovi
- streamlit - UI
- scipy, sklearn - statistika i ML
- openpyxl - Excel export

## 🚀 SLJEDEĆI KORACI
1. ✅ Analiza strukture podataka
2. ⏭️ Kreiranje data loading modula
3. ⏭️ Implementacija analytics klasa
4. ⏭️ Kreiranje Streamlit app-a sa svim tabovima
5. ⏭️ Testiranje i refinement
