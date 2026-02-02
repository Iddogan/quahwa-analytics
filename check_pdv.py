from src.utils.auto_data_loader import AutoDataLoader

loader = AutoDataLoader()
df = loader.load_all_racuni()

print('=== COLUMN CHECK ===')
print('Columns:', list(df.columns))

print('\n=== PDV CHECK ===')
if 'PDV' in df.columns:
    print(df[['PDV', 'PNP', 'Ukupno']].head(10))
    print('\nPDV statistics:')
    print(df['PDV'].describe())
    print(f'\nPDV sum: {df["PDV"].sum():,.2f}')
    print(f'Ukupno sum: {df["Ukupno"].sum():,.2f}')
    print(f'PDV as % of Ukupno: {(df["PDV"].sum() / df["Ukupno"].sum() * 100):.2f}%')
else:
    print('NO PDV column found!')

print('\n=== PNP CHECK ===')
if 'PNP' in df.columns:
    print(f'PNP sum: {df["PNP"].sum():,.2f}')
    print(f'PNP as % of Ukupno: {(df["PNP"].sum() / df["Ukupno"].sum() * 100):.2f}%')
else:
    print('NO PNP column found!')
