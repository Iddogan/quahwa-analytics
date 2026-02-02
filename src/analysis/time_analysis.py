"""
Modul za vremensku analizu podataka.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List


class TimeAnalyzer:
    """Klasa za vremensku analizu prodaje."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: Obrađeni DataFrame s vremenskim kolonama
        """
        self.df = df
    
    def analyze_by_month(self) -> pd.DataFrame:
        """Analiza po mjesecima."""
        monthly = self.df.groupby(['Godina', 'Mjesec', 'Mjesec_naziv']).agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'nunique'
        }).reset_index()
        
        monthly.columns = [
            'Godina', 'Mjesec', 'Mjesec_naziv', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_artikala'
        ]
        monthly['Prosječan_račun'] = monthly['Promet'] / monthly['Broj_računa']
        
        return monthly.sort_values(['Godina', 'Mjesec'])
    
    def analyze_by_week(self) -> pd.DataFrame:
        """Analiza po tjednima."""
        weekly = self.df.groupby(['Godina', 'Tjedan']).agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'nunique'
        }).reset_index()
        
        weekly.columns = [
            'Godina', 'Tjedan', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_artikala'
        ]
        weekly['Prosječan_račun'] = weekly['Promet'] / weekly['Broj_računa']
        
        return weekly.sort_values(['Godina', 'Tjedan'])
    
    def analyze_by_day_of_week(self) -> pd.DataFrame:
        """Analiza po danima u tjednu."""
        daily = self.df.groupby(['Dan_u_tjednu', 'Dan_u_tjednu_broj']).agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'count'
        }).reset_index()
        
        daily.columns = [
            'Dan_u_tjednu', 'Dan_broj', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_transakcija'
        ]
        daily['Prosječan_račun'] = daily['Promet'] / daily['Broj_računa']
        
        return daily.sort_values('Dan_broj')
    
    def analyze_by_hour(self) -> pd.DataFrame:
        """Analiza po satima."""
        # Provjera da li kolona 'Sat' postoji i ima validne vrijednosti
        if 'Sat' not in self.df.columns:
            # Ako kolona ne postoji, kreiraj je iz Datum i vrijeme
            if 'Datum i vrijeme' in self.df.columns:
                self.df['Sat'] = pd.to_datetime(self.df['Datum i vrijeme']).dt.hour
            else:
                return pd.DataFrame(columns=['Sat', 'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_transakcija', 'Prosječan_račun'])
        
        # Uklanjanje redova gdje je Sat NaN
        df_valid = self.df[self.df['Sat'].notna()].copy()
        
        if len(df_valid) == 0:
            return pd.DataFrame(columns=['Sat', 'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_transakcija', 'Prosječan_račun'])
        
        hourly = df_valid.groupby('Sat').agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'count'
        }).reset_index()
        
        hourly.columns = [
            'Sat', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_transakcija'
        ]
        hourly['Prosječan_račun'] = hourly['Promet'] / hourly['Broj_računa']
        
        return hourly.sort_values('Sat')
    
    def analyze_by_period(self) -> pd.DataFrame:
        """Analiza po periodu dana (jutro, popodne, večer, noć)."""
        period = self.df.groupby('Period_dana').agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'count'
        }).reset_index()
        
        period.columns = [
            'Period_dana', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_transakcija'
        ]
        period['Prosječan_račun'] = period['Promet'] / period['Broj_računa']
        
        # Sortiranje po redoslijedu
        period_order = ['Jutro', 'Popodne', 'Večer', 'Noć']
        period['sort_order'] = period['Period_dana'].apply(
            lambda x: period_order.index(x) if x in period_order else 999
        )
        period = period.sort_values('sort_order').drop('sort_order', axis=1)
        
        return period
    
    def get_trend_analysis(self, granularity: str = 'daily') -> pd.DataFrame:
        """
        Analiza trenda kroz vrijeme.
        
        Args:
            granularity: 'daily', 'weekly', ili 'monthly'
        """
        if granularity == 'daily':
            trend = self.df.groupby(self.df['Datum i vrijeme'].dt.date).agg({
                'Količina': 'sum',
                'Ukupno': 'sum',
                'Fiskalni broj računa': 'nunique'
            }).reset_index()
            trend.columns = ['Datum', 'Ukupna_količina', 'Promet', 'Broj_računa']
        
        elif granularity == 'weekly':
            trend = self.analyze_by_week()
        
        elif granularity == 'monthly':
            trend = self.analyze_by_month()
        
        else:
            raise ValueError("granularity mora biti 'daily', 'weekly', ili 'monthly'")
        
        return trend
    
    def plot_monthly_trend(self, metric: str = 'Promet') -> go.Figure:
        """Kreira grafikon mjesečnog trenda."""
        monthly = self.analyze_by_month()
        
        fig = px.line(
            monthly, 
            x='Mjesec', 
            y=metric,
            color='Godina',
            title=f'{metric} po mjesecima',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title='Mjesec',
            yaxis_title=metric,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_day_of_week_distribution(self) -> go.Figure:
        """Kreira grafikon distribucije po danima u tjednu."""
        daily = self.analyze_by_day_of_week()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily['Dan_u_tjednu'],
            y=daily['Promet'],
            name='Promet',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title='Promet po danima u tjednu',
            xaxis_title='Dan u tjednu',
            yaxis_title='Promet',
            showlegend=True
        )
        
        return fig
    
    def plot_hourly_distribution(self) -> go.Figure:
        """Kreira grafikon distribucije po satima."""
        hourly = self.analyze_by_hour()
        
        if hourly.empty:
            # Vraća prazan grafikon s porukom
            fig = go.Figure()
            fig.add_annotation(
                text="Nema dostupnih podataka za prikaz po satima",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(title='Promet po satima')
            return fig
        
        fig = px.bar(
            hourly,
            x='Sat',
            y='Promet',
            title='Promet po satima',
            labels={'Sat': 'Sat dana', 'Promet': 'Ukupan promet'},
            text='Promet'
        )
        
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=0, dtick=1),
            hovermode='x',
            showlegend=False
        )
        
        return fig
