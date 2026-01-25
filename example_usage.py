"""
Primjer korištenja modula za analizu podataka
"""
from src.utils.data_loader import DataLoader
from src.analysis.time_analysis import TimeAnalyzer
from src.analysis.sales_analysis import SalesAnalyzer
import pandas as pd

def main():
    # 1. Učitavanje i obrada podataka
    print("=" * 60)
    print("UČITAVANJE PODATAKA")
    print("=" * 60)
    
    loader = DataLoader("Računi.xlsx")
    df = loader.process_data()
    
    # Prikaz osnovnih informacija
    summary = loader.get_data_summary()
    print(f"\n📊 Osnovne informacije:")
    print(f"   - Ukupno redova: {summary['ukupno_redova']:,}")
    print(f"   - Datum od: {summary['datum_od']}")
    print(f"   - Datum do: {summary['datum_do']}")
    print(f"   - Ukupni promet: {summary['ukupni_promet']:,.2f} EUR")
    print(f"   - Broj računa: {summary['broj_računa']:,}")
    print(f"   - Broj artikala: {summary['broj_artikala']:,}")
    
    # 2. Filtriranje podataka - zadnjih 30 dana
    print("\n" + "=" * 60)
    print("FILTRIRANJE NA ZADNJIH 30 DANA")
    print("=" * 60)
    
    df_30_days = loader.filter_by_date_range(last_n_days=30)
    
    # 3. VREMENSKA ANALIZA
    print("\n" + "=" * 60)
    print("VREMENSKA ANALIZA")
    print("=" * 60)
    
    time_analyzer = TimeAnalyzer(df_30_days)
    
    # Analiza po mjesecima
    print("\n📅 Top 3 mjeseca po prometu:")
    monthly = time_analyzer.analyze_by_month()
    print(monthly.nlargest(3, 'Promet')[['Mjesec_naziv', 'Promet', 'Broj_računa']])
    
    # Analiza po danima u tjednu
    print("\n📆 Promet po danima u tjednu:")
    daily = time_analyzer.analyze_by_day_of_week()
    print(daily[['Dan_u_tjednu', 'Promet', 'Broj_računa', 'Prosječan_račun']])
    
    # Analiza po satima
    print("\n🕐 Top 5 sati po prometu:")
    hourly = time_analyzer.analyze_by_hour()
    print(hourly.nlargest(5, 'Promet')[['Sat', 'Promet', 'Broj_računa']])
    
    # 4. ANALIZA PRODAJE
    print("\n" + "=" * 60)
    print("ANALIZA PRODAJE")
    print("=" * 60)
    
    sales_analyzer = SalesAnalyzer(df_30_days)
    
    # Osnovne metrike
    metrics = sales_analyzer.get_sales_metrics()
    print("\n📊 Ključne metrike:")
    print(f"   - Ukupni promet: {metrics['ukupni_promet']:,.2f} EUR")
    print(f"   - Ukupna količina: {metrics['ukupna_kolicina']:,.0f}")
    print(f"   - Prosječan račun: {metrics['prosječan_račun']:,.2f} EUR")
    print(f"   - Broj transakcija: {metrics['broj_transakcija']:,}")
    
    # Top proizvodi
    print("\n🏆 Top 10 proizvoda po prometu:")
    top_products = sales_analyzer.get_top_products(n=10, by='promet')
    print(top_products[['Artikl', 'Prodajna_grupa', 'Promet', 'Ukupna_količina']])
    
    # Prodajne grupe
    print("\n📦 Top 5 prodajnih grupa:")
    product_groups = sales_analyzer.analyze_by_product_group(top_n=5)
    print(product_groups[['Prodajna_grupa', 'Promet', 'Ukupna_količina', 'Udio_u_prometu']])
    
    # 5. ABC ANALIZA
    print("\n" + "=" * 60)
    print("ABC ANALIZA")
    print("=" * 60)
    
    abc = sales_analyzer.analyze_revenue_distribution()
    
    a_products = abc[abc['ABC_Kategorija'] == 'A']
    b_products = abc[abc['ABC_Kategorija'] == 'B']
    c_products = abc[abc['ABC_Kategorija'] == 'C']
    
    print(f"\n🥇 A Kategorija (Top proizvodi - do 80% prometa):")
    print(f"   - Broj proizvoda: {len(a_products)}")
    print(f"   - Udio u prometu: {a_products['Udio_u_prometu'].sum():.1f}%")
    
    print(f"\n🥈 B Kategorija (Srednji proizvodi - 80-95% prometa):")
    print(f"   - Broj proizvoda: {len(b_products)}")
    print(f"   - Udio u prometu: {b_products['Udio_u_prometu'].sum():.1f}%")
    
    print(f"\n🥉 C Kategorija (Ostali proizvodi - 95-100% prometa):")
    print(f"   - Broj proizvoda: {len(c_products)}")
    print(f"   - Udio u prometu: {c_products['Udio_u_prometu'].sum():.1f}%")
    
    print("\n" + "=" * 60)
    print("ANALIZA ZAVRŠENA!")
    print("=" * 60)
    print("\n💡 Savjet: Pokrenite Streamlit dashboard za interaktivnu vizualizaciju:")
    print("   cd dashboard")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main()
