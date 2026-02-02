# 📊 Usporedbe Proizvoda i Kategorija - Dokumentacija

## Novi TAB: "📅 Usporedbe"

Dashboard sada ima potpuno novi tab koji omogućava detaljnu usporedbu prodaje proizvoda i kategorija kroz vrijeme.

## 🎯 Funkcionalnosti

### 1. Automatska Kategorizacija Proizvoda

Svi proizvodi su automatski kategorizirani u:

- **Kava - Espresso bazirana**: Cappuccino, Espresso, Latte, Macchiato, Americano, Cortado, Bombon
- **Kava - Specijalna**: Turkish Coffee, Matcha, Hot Chocolate, Brum Latte
- **Hladna kava**: Ice Latte, Iced Americano, Bombon Ice, itd.
- **Čaj**: Tea Premium i ostale vrste čaja
- **Sokovi i limunade**: Pink Lemonade, Orange Juice, vode, itd.
- **Deserti i kolači**: Kolač, Choco Cookie, Coffee + Cake, kroasani
- **Sendviči i hrana**: Ham Cheese Toast, wraps, sendviči
- **Ostalo**: Kokteli i ostali proizvodi

### 2. Mjesečne Usporedbe po Kategorijama

📈 **Vizualizacija**:
- Grafikon koji prikazuje trend prodaje svih kategorija kroz sve dostupne mjesece
- Interaktivni multi-line graf s hover efektima
- Jasno vidljivi trendovi rasta i pada za svaku kategoriju

📊 **Tablica promjena**:
- % promjena mjesec-na-mjesec za svaku kategoriju
- Boje (zeleno = rast, crveno = pad) za lakše prepoznavanje trendova

### 3. Usporedba Specifičnih Proizvoda

🎯 **Odabir proizvoda**:
- Multiselect s mogućnošću odabira bilo kojih proizvoda
- Prikazani Top 15 proizvoda kao preporuka
- Defaultno odabrano Top 5 proizvoda

📈 **Analiza**:
- Mjesečni trend odabranih proizvoda
- % promjene mjesec-na-mjesec
- Usporedba performansi između proizvoda

**Primjer korištenja**:
```
Odaberi proizvode: CAPPUCCINO, ESPRESSO, LATTE, MATCHA LATTE 1g, TURKISH COFFEE
```
Dobij: Grafikon koji prikazuje kako se prodaja ovih proizvoda mijenjala kroz mjesece

### 4. Top Rastuće i Padajuće Proizvode

📈 **Najveći Rast** (TOP 10):
- Proizvodi s najvećim % rastom u zadnjem mjesecu
- Prikazuje promet trenutnog i prethodnog mjeseca
- Zeleni gradient za vizualizaciju rasta

📉 **Najveći Pad** (TOP 10):
- Proizvodi s najvećim % padom
- Crveni gradient za vizualizaciju pada
- Važno za identifikaciju problema ili sezonskih promjena

**Primjer iz podataka**:
```
Najveći rast: Sokovi i limunade (+86% u siječnju 2026 vs 2025)
Najveći pad: Hot Chocolate (-57% u siječnju 2026 vs prosinac 2025)
```

### 5. Year-over-Year Usporedba

📆 **Usporedba godina**:
- Odabir mjeseca (Siječanj, Veljača, itd.)
- Usporedba istog mjeseca kroz različite godine
- Prikazuje promet po kategorijama za svaku godinu
- % promjena godine-na-godinu

**Primjer - Siječanj**:
```
Kategorija               2025        2026      Promjena%
Kava - Espresso       20,214 EUR  25,103 EUR    +24.2%
Sokovi i limunade        741 EUR   1,379 EUR    +86.1%
Hladna kava            2,231 EUR   1,107 EUR    -50.4%
```

## 💡 Primjeri Korištenja

### Scenarij 1: Analiza rasta cappuccino prodaje
1. Idi na tab "📅 Usporedbe"
2. Scrollaj do "Usporedba Specifičnih Proizvoda"
3. Odaberi "CAPPUCCINO" u multiselect
4. Vidi mjesečni trend i % promjene

**Rezultat**: Cappuccino je imao pad od 15.7% u siječnju 2026 vs prosinac 2025

### Scenarij 2: Usporedba kategorija hrane vs pića
1. Pogledaj "Mjesečni Promet po Kategorijama"
2. Usporedi linije "Kava - Espresso bazirana" vs "Deserti i kolači"
3. Analiziraj u tablici % promjena

**Rezultat**: Deserti su rasli +53% u siječnju 2026 vs 2025

### Scenarij 3: Identifikacija sezonskih trendova
1. Odaberi "Year-over-Year Usporedba"
2. Odaberi mjesec (npr. Prosinac)
3. Vidi koje kategorije rastu/padaju u tom mjesecu kroz godine

**Rezultat**: Hot Chocolate ima sezonski pad nakon zimskih mjeseci

## 📈 Poslovne Insights

### Što možeš vidjeti:
1. **Trendovi kategorija**: Koje kategorije rastu, koje stagniraju
2. **Sezonalnost**: Proizvodi koji variraju po sezonama (hot chocolate, iced drinks)
3. **Portfolio analiza**: Balans između različitih tipova proizvoda
4. **Rast/pad proizvoda**: Rano detektiranje problema ili uspjeha
5. **Godišnje usporedbe**: Kako se biznis razvija godine-na-godinu

### Primjeri akcija:
- **Hot Chocolate pada?** → Promotivna akcija ili novi recepti
- **Sokovi rastu?** → Povećaj asortiman, naruči više zaliha
- **Cappuccino stagnira?** → Testiranje novih varijacija (flavors)
- **Deserti rastu?** → Razmotri proširenje ponude kolača

## 🔧 Tehnički Detalji

**Klasa**: `ProductComparisonAnalytics` u `src/analysis/advanced_analytics.py`

**Metode**:
- `compare_categories_monthly()` - Mjesečna usporedba kategorija
- `compare_products_monthly(products, top_n)` - Usporedba specifičnih proizvoda
- `year_over_year_comparison(month)` - Godišnje usporedbe
- `top_growers_and_decliners(period)` - Top rastuće/padajuće
- `get_categories_summary()` - Pregled svih kategorija

**Dashboard**: Tab 5 u `dashboard/app_complete.py`

## 🚀 Dostupno na

Dashboard je dostupan na: **http://localhost:8503**

Navigacija: **Tab "📅 Usporedbe"**

---

*Zadnje ažurirano: 02.02.2026*
