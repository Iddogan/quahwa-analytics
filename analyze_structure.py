"""
Skripta za detaljnu analizu strukture svih Excel fajlova
"""
import pandas as pd
from pathlib import Path
import re

data_folder = Path('data')

print("="*80)
print("ANALIZA STRUKTURE EXCEL FAJLOVA")
print("="*80)

# Pronađi sve fajlove
racuni_files = []
promet_files = []
analiza_files = []

for file in sorted(data_folder.glob('*.xls*')):
    if 'Računi' in file.name or 'racuni' in file.name.lower():
        racuni_files.append(file)
    elif 'Promet po artiklima' in file.name:
        promet_files.append(file)
    elif 'Excel analiza' in file.name:
        analiza_files.append(file)

print(f"\n📁 Pronađeno {len(racuni_files)} Računi fajlova")
print(f"📁 Pronađeno {len(promet_files)} Promet po artiklima fajlova")
print(f"📁 Pronađeno {len(analiza_files)} Excel analiza fajlova")

# Analiza Računi fajlova
print("\n" + "="*80)
print("1. RAČUNI FAJLOVI")
print("="*80)

for file in racuni_files:
    print(f"\n📄 {file.name}")
    try:
        df = pd.read_excel(file, nrows=3)
        print(f"   Redova (sample): {len(df)}")
        print(f"   Kolona: {len(df.columns)}")
        print(f"   Kolone: {list(df.columns)}")
        
        # Provjeri period
        df_full = pd.read_excel(file)
        if 'Datum i vrijeme' in df_full.columns:
            dates = pd.to_datetime(df_full['Datum i vrijeme'])
            print(f"   Period: {dates.min()} do {dates.max()}")
            print(f"   Ukupno redova: {len(df_full):,}")
    except Exception as e:
        print(f"   ❌ Greška: {str(e)}")

# Analiza Promet po artiklima fajlova
print("\n" + "="*80)
print("2. PROMET PO ARTIKLIMA FAJLOVI")
print("="*80)

for file in promet_files:
    print(f"\n📄 {file.name}")
    try:
        # Pokušaj sa različitim opcijama
        df = pd.read_excel(file, nrows=10)
        print(f"   Redova (sample): {len(df)}")
        print(f"   Kolona: {len(df.columns)}")
        print(f"   Kolone (prvih 5): {list(df.columns)[:5]}")
        
        # Provjeri da li ima header u nekim redovima
        print("\n   Prvih par redova:")
        print(df.head())
        
    except Exception as e:
        print(f"   ❌ Greška: {str(e)}")

# Analiza Excel analiza fajlova
print("\n" + "="*80)
print("3. EXCEL ANALIZA FAJLOVI")
print("="*80)

for file in analiza_files:
    print(f"\n📄 {file.name}")
    try:
        # Pročitaj sve sheet-ove
        xls = pd.ExcelFile(file)
        print(f"   Sheet-ova: {len(xls.sheet_names)}")
        print(f"   Nazivi: {xls.sheet_names}")
        
        for sheet in xls.sheet_names[:3]:  # Prvih 3 sheet-a
            df = pd.read_excel(file, sheet_name=sheet, nrows=5)
            print(f"\n   Sheet '{sheet}':")
            print(f"     Redova (sample): {len(df)}")
            print(f"     Kolona: {len(df.columns)}")
            if len(df.columns) <= 10:
                print(f"     Kolone: {list(df.columns)}")
            else:
                print(f"     Kolone (prvih 5): {list(df.columns)[:5]}")
    except Exception as e:
        print(f"   ❌ Greška: {str(e)}")

print("\n" + "="*80)
print("ZAVRŠENO")
print("="*80)
