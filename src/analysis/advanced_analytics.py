"""
Advanced Analytics Module - Napredne finansijske i prodajne analize
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class FinancialAnalytics:
    """Financijske analize."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_kpi_metrics(self) -> Dict:
        """Ključni KPI pokazatelji."""
        df = self.df
        
        total_revenue = df['Ukupno'].sum()
        total_invoices = df['Fiskalni broj računa'].nunique()
        avg_invoice = df.groupby('Fiskalni broj računa')['Ukupno'].sum().mean()
        total_items = df['Količina'].sum()
        
        # PDV analiza
        total_pdv = df['PDV'].sum() if 'PDV' in df.columns else 0
        
        # Analiza po načinu plaćanja
        payment_split = df.groupby('Način plaćanja')['Ukupno'].sum() if 'Način plaćanja' in df.columns else {}
        
        return {
            'ukupan_promet': total_revenue,
            'broj_računa': total_invoices,
            'prosječan_račun': avg_invoice,
            'ukupna_količina': total_items,
            'ukupan_pdv': total_pdv,
            'stavki_po_računu': len(df) / total_invoices if total_invoices > 0 else 0,
            'načini_plaćanja': payment_split
        }
    
    def get_daily_metrics(self) -> pd.DataFrame:
        """Dnevne metrike."""
        daily = self.df.groupby('Datum').agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        daily.columns = ['Datum', 'Promet', 'Broj_računa', 'Količina']
        
        # Dodaj moving average
        daily['Promet_MA7'] = daily['Promet'].rolling(window=7, min_periods=1).mean()
        daily['Promet_MA30'] = daily['Promet'].rolling(window=30, min_periods=1).mean()
        
        return daily
    
    def get_monthly_metrics(self) -> pd.DataFrame:
        """Mjesečne metrike."""
        monthly = self.df.groupby(['Godina', 'Mjesec']).agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        monthly.columns = ['Godina', 'Mjesec', 'Promet', 'Broj_računa', 'Količina']
        monthly['Period'] = monthly['Godina'].astype(str) + '-' + monthly['Mjesec'].astype(str).str.zfill(2)
        
        # Growth rates s jasnim opisima
        monthly['Promjena_MoM%'] = monthly['Promet'].pct_change() * 100  # Mjesec vs prethodni mjesec
        monthly['Promjena_YoY%'] = monthly.groupby('Mjesec')['Promet'].pct_change() * 100  # Godina vs prethodna godina (isti mjesec)
        
        # Dodaj broj transakcija za statistiku
        monthly['n_transakcija'] = self.df.groupby(['Godina', 'Mjesec'])['Fiskalni broj računa'].nunique().values
        
        return monthly
    
    def get_revenue_structure(self) -> Dict:
        """Struktura prihoda."""
        df = self.df
        
        total = df['Ukupno'].sum()
        neto = df['Ukupno neto'].sum() if 'Ukupno neto' in df.columns else total
        popusti = df['Ukupno popusta'].sum() if 'Ukupno popusta' in df.columns else 0
        
        # Broj transakcija za statistiku
        n_transakcija = len(df)
        
        return {
            'ukupno': total,
            'neto': neto,
            'popusti': popusti,
            'neto_dio%': (neto / total * 100) if total > 0 else 0,
            'popust%': (popusti / (neto + popusti) * 100) if (neto + popusti) > 0 else 0,
            'n': n_transakcija
        }


class SalesAnalytics:
    """Prodajne analize."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_top_products(self, n: int = 20) -> pd.DataFrame:
        """Top N proizvoda."""
        top = self.df.groupby('Artikl').agg({
            'Ukupno': 'sum',
            'Količina': 'sum',
            'Fiskalni broj računa': 'nunique'
        }).reset_index()
        
        top.columns = ['Artikl', 'Promet', 'Količina', 'Broj_računa']
        top = top.sort_values('Promet', ascending=False).head(n)
        top['Udio_u_prometu%'] = (top['Promet'] / self.df['Ukupno'].sum() * 100)
        
        return top
    
    def get_product_categories(self) -> pd.DataFrame:
        """Analiza po prodajnim grupama."""
        categories = self.df.groupby('Prodajna grupa').agg({
            'Ukupno': 'sum',
            'Količina': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'nunique'
        }).reset_index()
        
        categories.columns = ['Prodajna_grupa', 'Promet', 'Količina', 'Broj_računa', 'Broj_artikala']
        categories = categories.sort_values('Promet', ascending=False)
        categories['Udio_u_prometu%'] = (categories['Promet'] / self.df['Ukupno'].sum() * 100)
        
        return categories
    
    def get_abc_analysis(self) -> pd.DataFrame:
        """ABC analiza proizvoda."""
        # Promet po proizvodu
        products = self.df.groupby('Artikl').agg({
            'Ukupno': 'sum',
            'Količina': 'sum'
        }).reset_index()
        
        products.columns = ['Artikl', 'Promet', 'Količina']
        products = products.sort_values('Promet', ascending=False)
        
        # Kumulativni postotak
        total_revenue = products['Promet'].sum()
        products['Udio%'] = (products['Promet'] / total_revenue * 100)
        products['Kumulativno%'] = products['Udio%'].cumsum()
        
        # ABC kategorije
        products['ABC'] = products['Kumulativno%'].apply(lambda x:
            'A' if x <= 80 else ('B' if x <= 95 else 'C')
        )
        
        return products
    
    def get_basket_analysis(self) -> Dict:
        """Analiza korpe (basket analysis)."""
        basket = self.df.groupby('Fiskalni broj računa').agg({
            'Artikl': 'count',  # Broj stavki
            'Ukupno': 'sum',
            'Količina': 'sum'
        })
        
        return {
            'prosječan_broj_stavki': basket['Artikl'].mean(),
            'prosječna_vrijednost': basket['Ukupno'].mean(),
            'prosječna_količina': basket['Količina'].mean(),
            'max_stavki_po_računu': basket['Artikl'].max(),
            'min_stavki_po_računu': basket['Artikl'].min()
        }


class TimeAnalytics:
    """Vremenske analize."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_hourly_pattern(self) -> pd.DataFrame:
        """Promet po satima."""
        hourly = self.df.groupby('Sat').agg({
            'Ukupno': ['sum', 'mean', 'count'],
            'Fiskalni broj računa': 'nunique'
        }).reset_index()
        
        hourly.columns = ['Sat', 'Ukupan_promet', 'Prosječan_promet', 'Broj_transakcija', 'Broj_računa']
        return hourly
    
    def get_daily_pattern(self) -> pd.DataFrame:
        """Promet po danima u tjednu."""
        daily = self.df.groupby(['Dan_u_tjednu_broj', 'Dan_u_tjednu']).agg({
            'Ukupno': ['sum', 'mean'],
            'Fiskalni broj računa': 'nunique'
        }).reset_index()
        
        daily.columns = ['Dan_broj', 'Dan', 'Ukupan_promet', 'Prosječan_promet', 'Broj_računa']
        daily = daily.sort_values('Dan_broj')
        
        return daily
    
    def get_heatmap_data(self) -> pd.DataFrame:
        """Podaci za heatmap - dan × sat."""
        heatmap = self.df.groupby(['Dan_u_tjednu_broj', 'Sat'])['Ukupno'].sum().reset_index()
        heatmap_pivot = heatmap.pivot(index='Dan_u_tjednu_broj', columns='Sat', values='Ukupno').fillna(0)
        
        return heatmap_pivot
    
    def get_period_comparison(self, period1: Tuple[str, str], period2: Tuple[str, str]) -> Dict:
        """Usporedba dva perioda."""
        df1 = self.df[(self.df['Datum'] >= period1[0]) & (self.df['Datum'] <= period1[1])]
        df2 = self.df[(self.df['Datum'] >= period2[0]) & (self.df['Datum'] <= period2[1])]
        
        metrics1 = {
            'promet': df1['Ukupno'].sum(),
            'računi': df1['Fiskalni broj računa'].nunique(),
            'količina': df1['Količina'].sum()
        }
        
        metrics2 = {
            'promet': df2['Ukupno'].sum(),
            'računi': df2['Fiskalni broj računa'].nunique(),
            'količina': df2['Količina'].sum()
        }
        
        growth = {
            'promet_%': ((metrics2['promet'] - metrics1['promet']) / metrics1['promet'] * 100) if metrics1['promet'] > 0 else 0,
            'računi_%': ((metrics2['računi'] - metrics1['računi']) / metrics1['računi'] * 100) if metrics1['računi'] > 0 else 0,
            'količina_%': ((metrics2['količina'] - metrics1['količina']) / metrics1['količina'] * 100) if metrics1['količina'] > 0 else 0
        }
        
        return {
            'period1': metrics1,
            'period2': metrics2,
            'growth': growth
        }


class LocationAnalytics:
    """Analiza po lokalu/blagajni."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_location_performance(self) -> pd.DataFrame:
        """Performanse po lokalu."""
        if 'Lokal' not in self.df.columns:
            return pd.DataFrame()
        
        location = self.df.groupby('Lokal').agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        location.columns = ['Lokal', 'Promet', 'Broj_računa', 'Količina']
        location['Prosječan_račun'] = location['Promet'] / location['Broj_računa']
        
        return location
    
    def get_cashier_performance(self) -> pd.DataFrame:
        """Performanse po blagajnama."""
        if 'Blagajna' not in self.df.columns:
            return pd.DataFrame()
        
        cashier = self.df.groupby('Blagajna').agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        cashier.columns = ['Blagajna', 'Promet', 'Broj_računa', 'Količina']
        cashier['Prosječan_račun'] = cashier['Promet'] / cashier['Broj_računa']
        
        return cashier
    
    def get_staff_performance(self) -> pd.DataFrame:
        """Performanse osoblja."""
        if 'Izdao' not in self.df.columns:
            return pd.DataFrame()
        
        staff = self.df.groupby('Izdao').agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        staff.columns = ['Osoblje', 'Promet', 'Broj_računa', 'Količina']
        staff = staff.sort_values('Promet', ascending=False)
        staff['Prosječan_račun'] = staff['Promet'] / staff['Broj_računa']
        
        return staff


class CustomerAnalytics:
    """Analiza kupaca."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_customer_segmentation(self) -> Dict:
        """Segmentacija kupaca (B2B vs B2C)."""
        if 'Porezni broj kupca' not in self.df.columns:
            return {}
        
        # B2B = ima porezni broj
        b2b = self.df[self.df['Porezni broj kupca'].notna()]
        b2c = self.df[self.df['Porezni broj kupca'].isna()]
        
        return {
            'b2b': {
                'promet': b2b['Ukupno'].sum(),
                'računi': b2b['Fiskalni broj računa'].nunique(),
                'udio%': b2b['Ukupno'].sum() / self.df['Ukupno'].sum() * 100
            },
            'b2c': {
                'promet': b2c['Ukupno'].sum(),
                'računi': b2c['Fiskalni broj računa'].nunique(),
                'udio%': b2c['Ukupno'].sum() / self.df['Ukupno'].sum() * 100
            }
        }
    
    def get_top_customers(self, n: int = 20) -> pd.DataFrame:
        """Top kupci."""
        if 'Kupac' not in self.df.columns:
            return pd.DataFrame()
        
        # Filtriraj samo named customers
        named = self.df[self.df['Kupac'].notna() & (self.df['Kupac'] != 'nan')]
        
        if len(named) == 0:
            return pd.DataFrame()
        
        top = named.groupby('Kupac').agg({
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Količina': 'sum'
        }).reset_index()
        
        top.columns = ['Kupac', 'Promet', 'Broj_računa', 'Količina']
        top = top.sort_values('Promet', ascending=False).head(n)
        top['Prosječan_račun'] = top['Promet'] / top['Broj_računa']
        
        return top


class ProductComparisonAnalytics:
    """Analiza usporedbe prodaje proizvoda i kategorija kroz vrijeme."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Kategorizacija proizvoda
        self.product_categories = self._create_product_categories()
    
    def _create_product_categories(self) -> Dict[str, List[str]]:
        """Kreiranje kategorija proizvoda na osnovu naziva."""
        categories = {
            'Kava - Espresso bazirana': [],
            'Kava - Specijalna': [],
            'Hladna kava': [],
            'Čaj': [],
            'Sokovi i limunade': [],
            'Deserti i kolači': [],
            'Sendviči i hrana': [],
            'Ostalo': []
        }
        
        espresso_keywords = ['CAPPUCCINO', 'ESPRESSO', 'LATTE', 'MACCHIATO', 'AMERICANO', 'CORTADO', 'BOMBON']
        special_coffee_keywords = ['TURKISH', 'MATCHA', 'HOT CHOCOLATE', 'BRUM']
        iced_keywords = ['ICE', 'ICED']
        tea_keywords = ['TEA']
        drinks_keywords = ['LEMONADE', 'JUICE', 'VODA', 'WATER']
        dessert_keywords = ['KOLAČ', 'CAKE', 'COKKIE', 'Kroasan']
        food_keywords = ['Toast', 'Ham', 'WRAP', 'SANDWICH']
        
        for product in self.df['Artikl'].unique():
            product_upper = str(product).upper()
            categorized = False
            
            # Check iced first (može biti i espresso i ice)
            if any(keyword in product_upper for keyword in iced_keywords):
                categories['Hladna kava'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in espresso_keywords):
                categories['Kava - Espresso bazirana'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in special_coffee_keywords):
                categories['Kava - Specijalna'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in tea_keywords):
                categories['Čaj'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in drinks_keywords):
                categories['Sokovi i limunade'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in dessert_keywords):
                categories['Deserti i kolači'].append(product)
                categorized = True
            elif any(keyword in product_upper for keyword in food_keywords):
                categories['Sendviči i hrana'].append(product)
                categorized = True
            
            if not categorized:
                categories['Ostalo'].append(product)
        
        return categories
    
    def get_categories_summary(self) -> pd.DataFrame:
        """Vraća sažetak svih kategorija sa brojem proizvoda."""
        summary = []
        for cat, products in self.product_categories.items():
            summary.append({
                'Kategorija': cat,
                'Broj_proizvoda': len(products),
                'Primjer_proizvoda': ', '.join(products[:3]) if products else ''
            })
        return pd.DataFrame(summary)
    
    def get_product_category(self, product: str) -> str:
        """Vraća kategoriju za određeni proizvod."""
        for category, products in self.product_categories.items():
            if product in products:
                return category
        return 'Ostalo'
    
    def compare_products_monthly(self, products: Optional[List[str]] = None, top_n: int = 10) -> pd.DataFrame:
        """
        Uspoređuje prodaju proizvoda mjesec po mjesec.
        
        Args:
            products: Lista proizvoda za usporedbu. Ako je None, uzima top N proizvoda.
            top_n: Broj top proizvoda ako products nije zadan
            
        Returns:
            DataFrame sa mjesečnom prodajom i postotnim promjenama
        """
        df = self.df.copy()
        
        # Ako nisu zadani proizvodi, uzmi top N
        if products is None:
            top_products = df.groupby('Artikl')['Ukupno'].sum().nlargest(top_n).index.tolist()
            products = top_products
        
        # Filter podatke
        df_filtered = df[df['Artikl'].isin(products)].copy()
        
        # Grupiranje po mjesecu i proizvodu
        monthly = df_filtered.groupby([
            df_filtered['Datum i vrijeme'].dt.to_period('M'), 
            'Artikl'
        ]).agg({
            'Ukupno': 'sum',
            'Količina': 'sum'
        }).reset_index()
        
        monthly.columns = ['Mjesec', 'Artikl', 'Promet', 'Količina']
        monthly['Mjesec'] = monthly['Mjesec'].astype(str)
        
        # Pivot za lakšu usporedbu
        pivot_revenue = monthly.pivot(index='Mjesec', columns='Artikl', values='Promet').fillna(0)
        pivot_quantity = monthly.pivot(index='Mjesec', columns='Artikl', values='Količina').fillna(0)
        
        # Izračunaj % promjene
        pct_change_revenue = pivot_revenue.pct_change() * 100
        pct_change_quantity = pivot_quantity.pct_change() * 100
        
        return {
            'mjesecni_promet': pivot_revenue,
            'mjesecna_kolicina': pivot_quantity,
            'promjena_promet_%': pct_change_revenue,
            'promjena_kolicina_%': pct_change_quantity
        }
    
    def compare_categories_monthly(self) -> pd.DataFrame:
        """Uspoređuje prodaju kategorija proizvoda mjesec po mjesec."""
        df = self.df.copy()
        
        # Dodaj kategoriju svakom proizvodu
        df['Kategorija'] = df['Artikl'].apply(self.get_product_category)
        
        # Grupiranje po mjesecu i kategoriji
        monthly = df.groupby([
            df['Datum i vrijeme'].dt.to_period('M'),
            'Kategorija'
        ]).agg({
            'Ukupno': 'sum',
            'Količina': 'sum'
        }).reset_index()
        
        monthly.columns = ['Mjesec', 'Kategorija', 'Promet', 'Količina']
        monthly['Mjesec'] = monthly['Mjesec'].astype(str)
        
        # Pivot za lakšu usporedbu
        pivot_revenue = monthly.pivot(index='Mjesec', columns='Kategorija', values='Promet').fillna(0)
        pivot_quantity = monthly.pivot(index='Mjesec', columns='Kategorija', values='Količina').fillna(0)
        
        # Izračunaj % promjene
        pct_change_revenue = pivot_revenue.pct_change() * 100
        pct_change_quantity = pivot_quantity.pct_change() * 100
        
        return {
            'mjesecni_promet': pivot_revenue,
            'mjesecna_kolicina': pivot_quantity,
            'promjena_promet_%': pct_change_revenue,
            'promjena_kolicina_%': pct_change_quantity
        }
    
    def year_over_year_comparison(self, month: int) -> pd.DataFrame:
        """
        Uspoređuje isti mjesec kroz različite godine (npr. siječanj 2025 vs siječanj 2026).
        
        Args:
            month: Broj mjeseca (1-12)
            
        Returns:
            DataFrame sa usporedbom po godinama
        """
        df = self.df.copy()
        df['Kategorija'] = df['Artikl'].apply(self.get_product_category)
        
        # Filtriraj samo zadani mjesec
        df_month = df[df['Mjesec'] == month].copy()
        
        # Grupiranje po godini i kategoriji
        yearly = df_month.groupby(['Godina', 'Kategorija']).agg({
            'Ukupno': 'sum',
            'Količina': 'sum'
        }).reset_index()
        
        # Pivot
        pivot_revenue = yearly.pivot(index='Kategorija', columns='Godina', values='Ukupno').fillna(0)
        pivot_quantity = yearly.pivot(index='Kategorija', columns='Godina', values='Količina').fillna(0)
        
        # Izračunaj promjene ako imamo više godina
        if len(pivot_revenue.columns) >= 2:
            years = sorted(pivot_revenue.columns)
            latest_year = years[-1]
            previous_year = years[-2]
            
            pivot_revenue['Promjena_%'] = ((pivot_revenue[latest_year] - pivot_revenue[previous_year]) / 
                                           pivot_revenue[previous_year] * 100).replace([np.inf, -np.inf], 0)
            pivot_quantity['Promjena_%'] = ((pivot_quantity[latest_year] - pivot_quantity[previous_year]) / 
                                            pivot_quantity[previous_year] * 100).replace([np.inf, -np.inf], 0)
        
        return {
            'promet_po_godinama': pivot_revenue,
            'kolicina_po_godinama': pivot_quantity
        }
    
    def top_growers_and_decliners(self, period: str = 'M') -> Dict:
        """
        Identificira proizvode s najvećim rastom i padom.
        
        Args:
            period: Vremenski period ('M' za mjesec, 'Q' za kvartal)
            
        Returns:
            Dictionary s top rastom i padom proizvoda
        """
        df = self.df.copy()
        
        # Grupiranje po periodu i proizvodu
        periodic = df.groupby([
            df['Datum i vrijeme'].dt.to_period(period),
            'Artikl'
        ])['Ukupno'].sum().reset_index()
        
        periodic.columns = ['Period', 'Artikl', 'Promet']
        periodic['Period'] = periodic['Period'].astype(str)
        
        # Pivot
        pivot = periodic.pivot(index='Artikl', columns='Period', values='Promet').fillna(0)
        
        # Zadnji i predzadnji period
        if len(pivot.columns) >= 2:
            latest = pivot.columns[-1]
            previous = pivot.columns[-2]
            
            # Izračunaj % promjenu
            pivot['Promjena_%'] = ((pivot[latest] - pivot[previous]) / 
                                   pivot[previous] * 100).replace([np.inf, -np.inf], 0)
            
            # Filtriraj proizvode koji imaju dovoljno prometa
            min_revenue = 1000  # Minimum promet da bi bio relevantan
            significant = pivot[(pivot[latest] >= min_revenue) | (pivot[previous] >= min_revenue)]
            
            top_growers = significant.nlargest(10, 'Promjena_%')[['Promjena_%', latest, previous]]
            top_decliners = significant.nsmallest(10, 'Promjena_%')[['Promjena_%', latest, previous]]
            
            top_growers.columns = ['Promjena_%', f'Promet_{latest}', f'Promet_{previous}']
            top_decliners.columns = ['Promjena_%', f'Promet_{latest}', f'Promet_{previous}']
            
            return {
                'najveci_rast': top_growers,
                'najveci_pad': top_decliners
            }
        
        return {'najveci_rast': pd.DataFrame(), 'najveci_pad': pd.DataFrame()}
