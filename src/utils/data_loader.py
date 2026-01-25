"""
Modul za učitavanje i pripremu podataka iz Excel fajla.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict


class DataLoader:
    """Klasa za učitavanje i obradu podataka o računima."""
    
    # Mapiranje mogućih naziva kolona
    COLUMN_MAPPINGS = {
        'Lokal': ['lokal', 'lokacija', 'restoran'],
        'Blagajna': ['blagajna', 'kasa', 'pos'],
        'Fiskalni broj računa': ['fiskalni broj', 'fiskalni', 'broj računa', 'račun broj'],
        'Artikl': ['artikl', 'proizvod', 'artikal', 'item'],
        'Prodajna grupa': ['prodajna grupa', 'grupa', 'kategorija', 'category'],
        'Količina': ['količina', 'kolicina', 'qty', 'quantity'],
        'Cijena': ['cijena', 'cena', 'price'],
        'Ukupno': ['ukupno', 'total', 'iznos', 'amount'],
        'PDV': ['pdv', 'vat', 'porez'],
    }
    
    def __init__(self, filepath: str = "Računi.xlsx"):
        """
        Inicijalizacija DataLoader-a.
        
        Args:
            filepath: Putanja do Excel fajla s podacima
        """
        self.filepath = filepath
        self.df = None
        self.df_processed = None
        
    def load_data(self) -> pd.DataFrame:
        """Učitava podatke iz Excel fajla."""
        print(f"Učitavam podatke iz: {self.filepath}")
        self.df = pd.read_excel(self.filepath)
        print(f"Učitano {len(self.df)} redova i {len(self.df.columns)} kolona")
        return self.df
    
    def _find_column(self, possible_names: list) -> Optional[str]:
        """Pronalazi kolonu koja odgovara nekom od mogućih naziva."""
        for col in self.df.columns:
            col_lower = col.lower().strip()
            for name in possible_names:
                if name.lower() in col_lower:
                    return col
        return None
    
    def _standardize_column_names(self):
        """Standardizuje nazive kolona prema mapiranju."""
        for standard_name, possible_names in self.COLUMN_MAPPINGS.items():
            found_col = self._find_column(possible_names)
            if found_col and found_col != standard_name:
                # Preimenuj kolonu samo ako već ne postoji standardni naziv
                if standard_name not in self.df_processed.columns:
                    self.df_processed[standard_name] = self.df_processed[found_col]
    
    def process_data(self) -> pd.DataFrame:
        """
        Obrađuje podatke i dodaje kolone za vremensku analizu.
        """
        if self.df is None:
            self.load_data()
        
        # Kopiranje dataframe-a
        self.df_processed = self.df.copy()
        
        # Pronalaženje kolona za datum/vrijeme
        datetime_col = self._find_column(['datum i vrijeme', 'datum i vreme', 'datum/vrijeme', 'datetime', 'datum', 'date', 'time'])
        if not datetime_col:
            available_cols = ', '.join(self.df.columns.tolist())
            raise ValueError(
                f"Ne mogu pronaći kolonu za datum i vrijeme.\n\n"
                f"Dostupne kolone: {available_cols}\n\n"
                f"Potrebna je kolona koja sadrži datum i vrijeme transakcije."
            )
        
        bookkeeping_col = self._find_column(['knjigovodstveni datum', 'knjig. datum', 'datum knjiženja'])
        
        # Konverzija datumskih kolona
        self.df_processed['Datum i vrijeme'] = pd.to_datetime(
            self.df_processed[datetime_col], errors='coerce'
        )
        
        if bookkeeping_col:
            self.df_processed['Knjigovodstveni datum'] = pd.to_datetime(
                self.df_processed[bookkeeping_col], errors='coerce'
            )
        
        # Provjera da li ima validnih datuma
        if self.df_processed['Datum i vrijeme'].isna().all():
            raise ValueError(f"Kolona '{datetime_col}' ne sadrži validne datume!")
        
        # Mapiranje ostalih kolona na standardne nazive
        self._standardize_column_names()
        
        # Dodavanje kolona za vremensku analizu
        self.df_processed['Godina'] = self.df_processed['Datum i vrijeme'].dt.year
        self.df_processed['Mjesec'] = self.df_processed['Datum i vrijeme'].dt.month
        self.df_processed['Mjesec_naziv'] = self.df_processed['Datum i vrijeme'].dt.strftime('%B')
        self.df_processed['Dan'] = self.df_processed['Datum i vrijeme'].dt.day
        self.df_processed['Dan_u_tjednu'] = self.df_processed['Datum i vrijeme'].dt.day_name()
        self.df_processed['Dan_u_tjednu_broj'] = self.df_processed['Datum i vrijeme'].dt.dayofweek
        self.df_processed['Tjedan'] = self.df_processed['Datum i vrijeme'].dt.isocalendar().week
        self.df_processed['Sat'] = self.df_processed['Datum i vrijeme'].dt.hour
        self.df_processed['Kvartal'] = self.df_processed['Datum i vrijeme'].dt.quarter
        
        # Dodavanje perioda dana
        self.df_processed['Period_dana'] = self.df_processed['Sat'].apply(self._get_period_dana)
        
        print("Podaci su uspješno obrađeni!")
        return self.df_processed
    
    @staticmethod
    def _get_period_dana(sat: int) -> str:
        """Određuje period dana na osnovu sata."""
        if 6 <= sat < 12:
            return 'Jutro'
        elif 12 <= sat < 18:
            return 'Popodne'
        elif 18 <= sat < 22:
            return 'Večer'
        else:
            return 'Noć'
    
    def filter_by_date_range(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        last_n_days: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Filtrira podatke po datumskom opsegu.
        
        Args:
            start_date: Početni datum (format: 'YYYY-MM-DD')
            end_date: Krajnji datum (format: 'YYYY-MM-DD')
            last_n_days: Zadnjih N dana od najnovijeg datuma
            
        Returns:
            Filtrirani DataFrame
        """
        if self.df_processed is None:
            self.process_data()
        
        df_filtered = self.df_processed.copy()
        
        if last_n_days is not None:
            max_date = df_filtered['Datum i vrijeme'].max()
            start_date_calc = max_date - timedelta(days=last_n_days)
            df_filtered = df_filtered[df_filtered['Datum i vrijeme'] >= start_date_calc]
            print(f"Filtrirano na zadnjih {last_n_days} dana")
        else:
            if start_date:
                df_filtered = df_filtered[
                    df_filtered['Datum i vrijeme'] >= pd.to_datetime(start_date)
                ]
            if end_date:
                df_filtered = df_filtered[
                    df_filtered['Datum i vrijeme'] <= pd.to_datetime(end_date)
                ]
            print(f"Filtrirano od {start_date} do {end_date}")
        
        print(f"Broj redova nakon filtriranja: {len(df_filtered)}")
        return df_filtered
    
    def get_data_summary(self) -> dict:
        """Vraća osnovne statistike o podacima."""
        if self.df_processed is None:
            self.process_data()
        
        summary = {
            'ukupno_redova': len(self.df_processed),
            'ukupno_kolona': len(self.df_processed.columns),
            'datum_od': self.df_processed['Datum i vrijeme'].min(),
            'datum_do': self.df_processed['Datum i vrijeme'].max(),
            'ukupni_promet': self.df_processed['Ukupno'].sum(),
            'broj_računa': self.df_processed['Fiskalni broj računa'].nunique(),
            'broj_artikala': self.df_processed['Artikl'].nunique(),
            'broj_prodajnih_grupa': self.df_processed['Prodajna grupa'].nunique(),
        }
        
        return summary
