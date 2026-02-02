"""
Auto Data Loader - Automatski učitava i objedinjuje sve račun fajlove
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict
import re


class AutoDataLoader:
    """Automatski učitava sve relevantne Excel fajlove iz data foldera."""
    
    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        self.racuni_df: pd.DataFrame = None
        self.loaded_files: List[str] = []
        
    def load_all_racuni(self) -> pd.DataFrame:
        """
        Automatski pronalazi i učitava sve fajlove sa računima.
        
        Returns:
            DataFrame sa svim objedinjenim računima
        """
        all_dfs = []
        
        # Pronađi sve Excel fajlove
        excel_files = list(self.data_folder.glob('*.xlsx')) + list(self.data_folder.glob('*.xls'))
        
        for file in sorted(excel_files):
            # Provjeri da li je to račun fajl
            if self._is_racuni_file(file):
                print(f"📂 Učitavam: {file.name}")
                
                try:
                    df = self._load_racuni_file(file)
                    if df is not None and len(df) > 0:
                        df['_source_file'] = file.name
                        all_dfs.append(df)
                        self.loaded_files.append(file.name)
                        print(f"   ✅ Učitano {len(df):,} redova")
                except Exception as e:
                    print(f"   ❌ Greška: {str(e)}")
                    continue
        
        if all_dfs:
            self.racuni_df = pd.concat(all_dfs, ignore_index=True)
            self._process_data()
            print(f"\n✅ UKUPNO: {len(self.racuni_df):,} redova iz {len(all_dfs)} fajlova")
            return self.racuni_df
        else:
            raise ValueError("Nema pronađenih račun fajlova!")
    
    def _is_racuni_file(self, file: Path) -> bool:
        """Provjerava da li je fajl račun fajl."""
        name_lower = file.name.lower()
        
        # Ključne riječi za račun fajlove
        racuni_keywords = ['račun', 'racun', 'računi', 'racuni']
        
        # Provjeri naziv fajla
        for keyword in racuni_keywords:
            if keyword in name_lower:
                return True
        
        # Alternativno, provjeri strukturu (ako ima fiskalni broj računa)
        try:
            df_sample = pd.read_excel(file, nrows=1)
            required_cols = ['Fiskalni broj računa', 'Artikl', 'Ukupno']
            return all(col in df_sample.columns for col in required_cols)
        except:
            return False
    
    def _load_racuni_file(self, file: Path) -> pd.DataFrame:
        """Učitava pojedinačni račun fajl."""
        # Provjeri da li ima sheet-ove
        try:
            xls = pd.ExcelFile(file)
            df = None
            
            if len(xls.sheet_names) > 1:
                # Pronađi sheet sa podacima - pokušaj različite varijante
                for sheet in xls.sheet_names:
                    sheet_lower = sheet.lower()
                    # Pokušaj učitati svaki sheet i provjeri ima li podataka
                    if any(keyword in sheet_lower for keyword in ['podaci', 'račun', 'racun', 'stavk']):
                        temp_df = pd.read_excel(file, sheet_name=sheet)
                        if len(temp_df) > 0:
                            df = temp_df
                            break
                
                # Ako nije pronađeno, pokušaj sve sheet-ove dok ne nađemo podatke
                if df is None or len(df) == 0:
                    for sheet in xls.sheet_names:
                        temp_df = pd.read_excel(file, sheet_name=sheet)
                        if len(temp_df) > 0 and 'Fiskalni broj računa' in temp_df.columns:
                            df = temp_df
                            break
            else:
                df = pd.read_excel(file)
        except Exception as e:
            # Fallback - pokušaj učitati default
            try:
                df = pd.read_excel(file)
            except:
                raise e
        
        return df
    
    def _process_data(self):
        """Procesira učitane podatke."""
        if self.racuni_df is None:
            return
        
        df = self.racuni_df
        
        # Konverzija datuma
        date_cols = ['Datum i vrijeme', 'Knjigovodstveni datum']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Dodavanje vremenskih kolona
        if 'Datum i vrijeme' in df.columns:
            df['Godina'] = df['Datum i vrijeme'].dt.year
            df['Mjesec'] = df['Datum i vrijeme'].dt.month
            df['Mjesec_naziv'] = df['Datum i vrijeme'].dt.month_name()
            df['Dan'] = df['Datum i vrijeme'].dt.day
            df['Dan_u_tjednu'] = df['Datum i vrijeme'].dt.day_name()
            df['Dan_u_tjednu_broj'] = df['Datum i vrijeme'].dt.dayofweek
            df['Tjedan'] = df['Datum i vrijeme'].dt.isocalendar().week
            df['Sat'] = df['Datum i vrijeme'].dt.hour
            df['Minuta'] = df['Datum i vrijeme'].dt.minute
            df['Kvartal'] = df['Datum i vrijeme'].dt.quarter
            df['Datum'] = df['Datum i vrijeme'].dt.date
            
            # Period dana
            df['Period_dana'] = df['Sat'].apply(self._get_period_dana)
        
        # Konverzija numeričkih kolona
        numeric_cols = ['Količina', 'Cijena', 'Ukupno', 'PDV', 'PNP', 
                       'Cijena s popustom', 'Ukupno popusta', 'Ukupno neto', 'Ukupno račun']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Čišćenje string kolona
        string_cols = ['Lokal', 'Artikl', 'Prodajna grupa', 'Način plaćanja', 'Izdao']
        for col in string_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        self.racuni_df = df
        print(f"✅ Podaci procesirani")
    
    @staticmethod
    def _get_period_dana(sat: int) -> str:
        """Određuje period dana na osnovu sata."""
        if pd.isna(sat):
            return 'Nepoznato'
        if 6 <= sat < 12:
            return 'Jutro'
        elif 12 <= sat < 18:
            return 'Popodne'
        elif 18 <= sat < 22:
            return 'Večer'
        else:
            return 'Noć'
    
    def get_summary(self) -> Dict:
        """Vraća sažetak učitanih podataka."""
        if self.racuni_df is None:
            return {}
        
        df = self.racuni_df
        
        return {
            'ukupno_redova': len(df),
            'broj_fajlova': len(self.loaded_files),
            'fajlovi': self.loaded_files,
            'datum_od': df['Datum i vrijeme'].min() if 'Datum i vrijeme' in df.columns else None,
            'datum_do': df['Datum i vrijeme'].max() if 'Datum i vrijeme' in df.columns else None,
            'ukupan_promet': df['Ukupno'].sum() if 'Ukupno' in df.columns else 0,
            'broj_računa': df['Fiskalni broj računa'].nunique() if 'Fiskalni broj računa' in df.columns else 0,
            'broj_artikala': df['Artikl'].nunique() if 'Artikl' in df.columns else 0,
            'broj_lokala': df['Lokal'].nunique() if 'Lokal' in df.columns else 0,
        }


# Test
if __name__ == "__main__":
    loader = AutoDataLoader("data")
    df = loader.load_all_racuni()
    
    summary = loader.get_summary()
    print("\n" + "="*60)
    print("SAŽETAK:")
    print("="*60)
    for key, value in summary.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:,}")
        else:
            print(f"{key}: {value}")
