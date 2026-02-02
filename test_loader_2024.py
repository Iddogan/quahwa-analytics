from src.utils.auto_data_loader import AutoDataLoader

loader = AutoDataLoader()
df = loader.load_all_racuni()

print(f'\n📊 Period: {df["Datum i vrijeme"].min()} to {df["Datum i vrijeme"].max()}')
print(f'📈 Total rows: {len(df):,}')
print(f'📁 Files loaded: {loader.loaded_files}')
print(f'\n✅ All years loaded successfully!')
