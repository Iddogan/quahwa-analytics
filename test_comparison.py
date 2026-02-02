"""Test ProductComparisonAnalytics"""
from src.utils.auto_data_loader import AutoDataLoader
from src.analysis.advanced_analytics import ProductComparisonAnalytics
import pandas as pd

# Load data
loader = AutoDataLoader()
df = loader.load_all_racuni()

print(f"✅ Loaded {len(df):,} rows")

# Create analytics
comp = ProductComparisonAnalytics(df)

print("\n📋 Categories Summary:")
cat_summary = comp.get_categories_summary()
print(cat_summary)

print("\n📊 Monthly Category Comparison:")
cat_comp = comp.compare_categories_monthly()
print("\nRevenue by category (last 3 months):")
print(cat_comp['mjesecni_promet'].tail(3))

print("\n🎯 Top Products Monthly:")
top_comp = comp.compare_products_monthly(top_n=5)
print("\nRevenue (last 3 months):")
print(top_comp['mjesecni_promet'].tail(3))

print("\n🚀 Top Growers and Decliners:")
growth = comp.top_growers_and_decliners()
print("\nTop 5 Growers:")
print(growth['najveci_rast'].head())
print("\nTop 5 Decliners:")
print(growth['najveci_pad'].head())

print("\n📆 Year-over-Year (January):")
yoy = comp.year_over_year_comparison(1)
print(yoy['promet_po_godinama'])

print("\n✅ All tests passed!")
