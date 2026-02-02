"""
Test skripta za MultiFileLoader funkcionalnost
"""
import sys
from pathlib import Path

# Dodaj src u path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.multi_file_loader import MultiFileLoader
import pandas as pd

def create_sample_data():
    """Kreira primjer Excel fajlova za testiranje."""
    data_folder = Path(__file__).parent / 'data'
    data_folder.mkdir(exist_ok=True)
    
    print("Kreiram primjer podataka...")
    
    # Fajl 1 - Januar 2024
    dates1 = pd.date_range('2024-01-01', '2024-01-31', freq='6H')
    n1 = len(dates1)
    df1 = pd.DataFrame({
        'Datum i vrijeme': dates1,
        'Lokal': ['Kafić Quahwa'] * n1,
        'Fiskalni broj računa': [f'F-{i:04d}' for i in range(1, n1+1)],
        'Artikl': (['Kafa', 'Čaj', 'Sok', 'Sendvič'] * (n1//4 + 1))[:n1],
        'Prodajna grupa': (['Pića', 'Pića', 'Pića', 'Hrana'] * (n1//4 + 1))[:n1],
        'Količina': ([1, 2, 1, 1] * (n1//4 + 1))[:n1],
        'Cijena': ([2.5, 1.5, 3.0, 5.0] * (n1//4 + 1))[:n1],
        'Ukupno': ([2.5, 3.0, 3.0, 5.0] * (n1//4 + 1))[:n1],
    })
    df1.to_excel(data_folder / 'januar_2024.xlsx', index=False)
    print(f"  ✓ Kreirano: januar_2024.xlsx ({len(df1)} redova)")
    
    # Fajl 2 - Februar 2024
    dates2 = pd.date_range('2024-02-01', '2024-02-28', freq='4H')
    n2 = len(dates2)
    df2 = pd.DataFrame({
        'Datum i vrijeme': dates2,
        'Lokal': ['Kafić Quahwa'] * n2,
        'Fiskalni broj računa': [f'F-{i:04d}' for i in range(200, 200+n2)],
        'Artikl': (['Kafa', 'Espresso', 'Kapućino', 'Sendvič', 'Palačinke'] * (n2//5 + 1))[:n2],
        'Prodajna grupa': (['Pića', 'Pića', 'Pića', 'Hrana', 'Hrana'] * (n2//5 + 1))[:n2],
        'Količina': ([1, 1, 1, 2, 3] * (n2//5 + 1))[:n2],
        'Cijena': ([2.5, 2.0, 3.0, 5.0, 4.5] * (n2//5 + 1))[:n2],
        'Ukupno': ([2.5, 2.0, 3.0, 10.0, 13.5] * (n2//5 + 1))[:n2],
    })
    df2.to_excel(data_folder / 'februar_2024.xlsx', index=False)
    print(f"  ✓ Kreirano: februar_2024.xlsx ({len(df2)} redova)")
    
    # Fajl 3 - Mart 2024 (sa dodatnim kolonama)
    dates3 = pd.date_range('2024-03-01', '2024-03-31', freq='5H')
    n3 = len(dates3)
    df3 = pd.DataFrame({
        'Datum i vrijeme': dates3,
        'Lokal': ['Kafić Quahwa'] * n3,
        'Blagajna': (['Kasa 1', 'Kasa 2'] * (n3//2 + 1))[:n3],
        'Fiskalni broj računa': [f'F-{i:04d}' for i in range(500, 500+n3)],
        'Artikl': (['Kafa', 'Čaj', 'Sok', 'Sendvič', 'Torta'] * (n3//5 + 1))[:n3],
        'Prodajna grupa': (['Pića', 'Pića', 'Pića', 'Hrana', 'Desrti'] * (n3//5 + 1))[:n3],
        'Količina': ([1, 1, 2, 1, 1] * (n3//5 + 1))[:n3],
        'Cijena': ([2.5, 1.5, 3.0, 5.0, 4.0] * (n3//5 + 1))[:n3],
        'Ukupno': ([2.5, 1.5, 6.0, 5.0, 4.0] * (n3//5 + 1))[:n3],
        'PDV': ([0.5, 0.3, 1.2, 1.0, 0.8] * (n3//5 + 1))[:n3],
    })
    df3.to_excel(data_folder / 'mart_2024.xlsx', index=False)
    print(f"  ✓ Kreirano: mart_2024.xlsx ({len(df3)} redova)")
    
    print(f"\n✅ Kreirano 3 test Excel fajla u folderu: {data_folder}")
    return data_folder


def test_multi_file_loader():
    """Testira MultiFileLoader funkcionalnost."""
    print("\n" + "="*60)
    print("TEST: MultiFileLoader")
    print("="*60 + "\n")
    
    # Kreiraj test podatke
    data_folder = create_sample_data()
    
    # Inicijalizuj loader
    print("\n1. Inicijalizacija MultiFileLoader...")
    loader = MultiFileLoader(str(data_folder))
    
    # Pronađi fajlove
    print("\n2. Pronalaženje Excel fajlova...")
    files = loader.discover_excel_files()
    print(f"   Pronađeno {len(files)} fajlova:")
    for f in files:
        print(f"   - {f.name}")
    
    # Učitaj sve fajlove
    print("\n3. Učitavanje svih fajlova...")
    loaded = loader.load_all_files()
    print(f"   ✓ Učitano {len(loaded)} fajlova")
    
    # Objedini podatke
    print("\n4. Objedinjavanje podataka...")
    combined_df = loader.combine_data()
    print(f"   ✓ Objedinjeni DataFrame ima {len(combined_df)} redova")
    
    # Sažeti izvještaj
    print("\n5. Sažeti izvještaj:")
    summary = loader.get_summary_report()
    print(f"   - Broj fajlova: {summary['broj_fajlova']}")
    print(f"   - Ukupno redova: {summary['ukupno_redova']}")
    print(f"   - Ukupan promet: {summary['ukupan_promet']:.2f} EUR")
    print(f"   - Period: {summary['datum_od'].strftime('%d.%m.%Y')} - {summary['datum_do'].strftime('%d.%m.%Y')}")
    
    # Pregled varijabli
    print("\n6. Pregled varijabli:")
    var_summary = loader.get_variable_summary()
    print(f"   Ukupno varijabli: {len(var_summary)}")
    print("\n   Prvih 10 varijabli:")
    print(var_summary[['Varijabla', 'Tip_podataka', 'Procenat_popunjenosti', 'Jedinstvenih_vrijednosti']].head(10).to_string(index=False))
    
    # Usporedba kolona
    print("\n7. Usporedba kolona između fajlova:")
    column_comp = loader.get_column_comparison()
    print(column_comp.to_string(index=False))
    
    # Pregled fajlova
    print("\n8. Pregled učitanih fajlova:")
    files_overview = loader.get_files_overview()
    print(files_overview[['naziv', 'redova', 'kolona', 'ukupan_promet', 'broj_računa']].to_string(index=False))
    
    print("\n" + "="*60)
    print("✅ TEST USPJEŠNO ZAVRŠEN!")
    print("="*60 + "\n")
    
    return loader


if __name__ == "__main__":
    try:
        loader = test_multi_file_loader()
        
        print("\n💡 UPUTE ZA KORIŠTENJE:")
        print("-" * 60)
        print("1. Pokreni dashboard: streamlit run dashboard/app.py")
        print("2. U sidebar-u odaberi: 'Fajlovi iz foldera'")
        print("3. Klikni '📥 Učitaj podatke'")
        print("4. Istraži nove tabove:")
        print("   - 📋 Izvješće varijabli - sve varijable iz svih tablica")
        print("   - 📁 Pregled fajlova - detalji o učitanim fajlovima")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Greška: {str(e)}")
        import traceback
        traceback.print_exc()
