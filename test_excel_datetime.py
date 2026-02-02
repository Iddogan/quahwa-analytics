"""
Test skripta za provjeru kako se čita datum i vrijeme iz Excel-a
"""
import pandas as pd

# Učitaj Excel
df = pd.read_excel("Računi.xlsx", nrows=10)

print("=== EXCEL KOLONE ===")
print(df.columns.tolist())
print()

# Pronađi kolonu s datumom i vremenom
datetime_cols = [col for col in df.columns if 'datum' in col.lower() or 'time' in col.lower() or 'vrijeme' in col.lower()]

print(f"=== PRONAĐENE KOLONE S DATUMOM/VREMENOM ===")
print(datetime_cols)
print()

for col in datetime_cols:
    print(f"=== KOLONA: {col} ===")
    print(f"Tip podataka: {df[col].dtype}")
    print(f"Prvi redovi:")
    print(df[col].head())
    print()
    
    # Pokušaj konverziju u datetime
    dt_series = pd.to_datetime(df[col], errors='coerce')
    print(f"Nakon konverzije u datetime:")
    print(f"Tip: {dt_series.dtype}")
    print(f"Primjeri:")
    for i, val in enumerate(dt_series.head()):
        print(f"  Red {i}: {val} -> Sat: {val.hour if pd.notna(val) else 'NaN'}")
    print()
    print("-" * 80)
    print()
