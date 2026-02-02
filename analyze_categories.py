from src.utils.auto_data_loader import AutoDataLoader
import pandas as pd

loader = AutoDataLoader()
df = loader.load_all_racuni()

print('Columns:', list(df.columns))
print('\nSample products (top 30):')
print(df['Artikl'].value_counts().head(30))
print('\nDate range:')
print(df['Datum i vrijeme'].min(), 'to', df['Datum i vrijeme'].max())
print('\nUnique months:')
df['year_month'] = df['Datum i vrijeme'].dt.to_period('M')
print(df['year_month'].value_counts().sort_index())
