"""
Modul za analizu prodaje i artikala.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional


class SalesAnalyzer:
    """Klasa za analizu prodaje artikala i prodajnih grupa."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: Obrađeni DataFrame
        """
        self.df = df
    
    def analyze_by_product_group(self, top_n: Optional[int] = None) -> pd.DataFrame:
        """
        Analiza po prodajnim grupama.
        
        Args:
            top_n: Broj top prodajnih grupa (None = sve)
        """
        # Provjera da li postoji kolona
        if 'Prodajna grupa' not in self.df.columns:
            return pd.DataFrame()
        
        groups = self.df.groupby('Prodajna grupa').agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Fiskalni broj računa': 'nunique',
            'Artikl': 'nunique'
        }).reset_index()
        
        groups.columns = [
            'Prodajna_grupa', 
            'Ukupna_količina', 'Promet', 'Broj_računa', 'Broj_različitih_artikala'
        ]
        
        groups['Prosječna_cijena'] = groups['Promet'] / groups['Ukupna_količina']
        groups['Udio_u_prometu'] = (groups['Promet'] / groups['Promet'].sum() * 100).round(2)
        
        groups = groups.sort_values('Promet', ascending=False)
        
        if top_n:
            groups = groups.head(top_n)
        
        return groups
    
    def analyze_by_article(self, top_n: Optional[int] = None) -> pd.DataFrame:
        """
        Analiza po artiklima.
        
        Args:
            top_n: Broj top artikala (None = svi)
        """
        # Odabir kolona za grupiranje - sa ili bez prodajne grupe
        group_cols = ['Artikl']
        if 'Prodajna grupa' in self.df.columns:
            group_cols.append('Prodajna grupa')
        
        articles = self.df.groupby(group_cols).agg({
            'Količina': 'sum',
            'Ukupno': 'sum',
            'Cijena': 'mean',
            'Fiskalni broj računa': 'nunique'
        }).reset_index()
        
        # Postavljanje naziva kolona zavisno od grupiranja
        if 'Prodajna grupa' in self.df.columns:
            articles.columns = [
                'Artikl', 'Prodajna_grupa',
                'Ukupna_količina', 'Promet', 'Prosječna_cijena', 'Broj_računa'
            ]
        else:
            articles.columns = [
                'Artikl',
                'Ukupna_količina', 'Promet', 'Prosječna_cijena', 'Broj_računa'
            ]
            articles['Prodajna_grupa'] = 'N/A'  # Dodaj placeholder kolonu
        
        articles['Udio_u_prometu'] = (articles['Promet'] / articles['Promet'].sum() * 100).round(2)
        
        articles = articles.sort_values('Promet', ascending=False)
        
        if top_n:
            articles = articles.head(top_n)
        
        return articles
    
    def get_top_products(self, n: int = 10, by: str = 'promet') -> pd.DataFrame:
        """
        Vraća top N proizvoda.
        
        Args:
            n: Broj proizvoda
            by: Kriterij sortiranja ('promet', 'kolicina', 'broj_racuna')
        """
        articles = self.analyze_by_article()
        
        if by == 'promet':
            return articles.head(n)
        elif by == 'kolicina':
            return articles.sort_values('Ukupna_količina', ascending=False).head(n)
        elif by == 'broj_racuna':
            return articles.sort_values('Broj_računa', ascending=False).head(n)
        else:
            raise ValueError("by mora biti 'promet', 'kolicina', ili 'broj_racuna'")
    
    def analyze_revenue_distribution(self) -> pd.DataFrame:
        """ABC analiza proizvoda (Pareto princip)."""
        articles = self.analyze_by_article()
        
        # Provjera praznih podataka
        if articles.empty or len(articles) == 0:
            return pd.DataFrame()
        
        # Sortiranje po prometu
        articles = articles.sort_values('Promet', ascending=False).reset_index(drop=True)
        
        # Kumulativni promet
        articles['Kumulativni_promet'] = articles['Promet'].cumsum()
        articles['Kumulativni_postotak'] = (
            articles['Kumulativni_promet'] / articles['Promet'].sum() * 100
        ).round(2)
        
        # ABC klasifikacija
        def classify_abc(cum_pct):
            if cum_pct <= 80:
                return 'A'
            elif cum_pct <= 95:
                return 'B'
            else:
                return 'C'
        
        articles['ABC_Kategorija'] = articles['Kumulativni_postotak'].apply(classify_abc)
        
        return articles
    
    def analyze_product_performance_by_time(
        self, 
        time_dimension: str = 'Dan_u_tjednu'
    ) -> pd.DataFrame:
        """
        Analiza performansi proizvoda kroz vrijeme.
        
        Args:
            time_dimension: Vremenska dimenzija ('Dan_u_tjednu', 'Sat', 'Mjesec', itd.)
        """
        # Validacija da kolona postoji
        if time_dimension not in self.df.columns:
            available_cols = [col for col in self.df.columns if any(x in col.lower() for x in ['dan', 'sat', 'mjesec', 'tjedan', 'period'])]
            raise ValueError(
                f"Kolona {time_dimension} ne postoji u podacima. "
                f"Dostupne kolone: {', '.join(available_cols)}"
            )
        
        # Odabir kolona za grupiranje
        group_cols = [time_dimension]
        if 'Prodajna grupa' in self.df.columns:
            group_cols.append('Prodajna grupa')
        else:
            # Ako nema prodajne grupe, grupiši samo po vremenskoj dimenziji
            group_cols.append('Artikl')  # Koristi artikl kao alternativu
        
        performance = self.df.groupby(group_cols).agg({
            'Količina': 'sum',
            'Ukupno': 'sum'
        }).reset_index()
        
        # Postavljanje naziva kolona
        if 'Prodajna grupa' in self.df.columns:
            performance.columns = [time_dimension, 'Prodajna_grupa', 'Količina', 'Promet']
        else:
            performance.columns = [time_dimension, 'Artikl', 'Količina', 'Promet']
            # Preimenuj Artikl u Prodajna_grupa za kompatibilnost
            performance = performance.rename(columns={'Artikl': 'Prodajna_grupa'})
        
        return performance
    
    def get_sales_metrics(self) -> dict:
        """Vraća ključne metrike prodaje."""
        metrics = {
            'ukupni_promet': self.df['Ukupno'].sum(),
            'ukupna_kolicina': self.df['Količina'].sum(),
            'prosječan_račun': self.df.groupby('Fiskalni broj računa')['Ukupno'].sum().mean(),
            'prosječna_stavka': self.df['Ukupno'].mean(),
            'broj_transakcija': len(self.df),
            'broj_računa': self.df['Fiskalni broj računa'].nunique(),
            'broj_artikala': self.df['Artikl'].nunique(),
            'broj_prodajnih_grupa': self.df['Prodajna grupa'].nunique(),
            'prosječna_količina_po_transakciji': self.df['Količina'].mean(),
        }
        
        return metrics
    
    def plot_top_products(self, n: int = 10, by: str = 'promet') -> go.Figure:
        """Kreira grafikon top proizvoda."""
        top = self.get_top_products(n=n, by=by)
        
        metric_map = {
            'promet': 'Promet',
            'kolicina': 'Ukupna_količina',
            'broj_racuna': 'Broj_računa'
        }
        
        metric_col = metric_map[by]
        
        fig = px.bar(
            top,
            y='Artikl',
            x=metric_col,
            orientation='h',
            title=f'Top {n} proizvoda po {by}',
            color='Prodajna_grupa',
            labels={metric_col: by.capitalize(), 'Artikl': 'Proizvod'}
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=max(400, n * 40)
        )
        
        return fig
    
    def plot_product_group_distribution(self) -> go.Figure:
        """Kreira pie chart distribucije po prodajnim grupama."""
        groups = self.analyze_by_product_group()
        
        fig = px.pie(
            groups,
            values='Promet',
            names='Prodajna_grupa',
            title='Distribucija prometa po prodajnim grupama',
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        return fig
    
    def plot_abc_analysis(self) -> go.Figure:
        """Kreira grafikon ABC analize."""
        abc = self.analyze_revenue_distribution()
        
        fig = go.Figure()
        
        # Provjera da ima podataka
        if abc.empty or len(abc) == 0:
            fig.add_annotation(
                text="Nema podataka za ABC analizu",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
            return fig
        
        # Bar chart za promet
        fig.add_trace(go.Bar(
            x=list(range(len(abc))),
            y=abc['Promet'],
            name='Promet po artiklu',
            marker_color='lightblue',
            yaxis='y'
        ))
        
        # Line chart za kumulativni postotak
        fig.add_trace(go.Scatter(
            x=list(range(len(abc))),
            y=abc['Kumulativni_postotak'],
            name='Kumulativni %',
            line=dict(color='red', width=2),
            yaxis='y2'
        ))
        
        # ABC granice - koristi add_shape umjesto add_hline za dva y-osa
        if len(abc) > 0:
            fig.add_shape(
                type='line',
                x0=0,
                x1=len(abc)-1,
                y0=80,
                y1=80,
                yref='y2',
                line=dict(color='green', width=2, dash='dash')
            )
            
            fig.add_shape(
                type='line',
                x0=0,
                x1=len(abc)-1,
                y0=95,
                y1=95,
                yref='y2',
                line=dict(color='orange', width=2, dash='dash')
            )
        
        fig.update_layout(
            title='ABC Analiza proizvoda',
            xaxis_title='Artikl (sortirano po prometu)',
            yaxis=dict(title='Promet', side='left'),
            yaxis2=dict(title='Kumulativni %', overlaying='y', side='right', range=[0, 105]),
            hovermode='x unified'
        )
        
        return fig
