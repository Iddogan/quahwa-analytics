"""
Modul za učitavanje i objedinjavanje podataka iz više Excel fajlova.
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import glob
from .data_loader import DataLoader


class MultiFileLoader:
    """Klasa za učitavanje i objedinjeavanje podataka iz više Excel fajlova."""
    
    def __init__(self, data_folder: str = "data"):
        """
        Inicijalizacija MultiFileLoader-a.
        
        Args:
            data_folder: Putanja do foldera sa Excel fajlovima
        """
        self.data_folder = Path(data_folder)
        self.loaded_files: Dict[str, pd.DataFrame] = {}
        self.combined_df: Optional[pd.DataFrame] = None
        self.file_info: List[Dict] = []
        
    def discover_excel_files(self) -> List[Path]:
        """Pronalazi sve Excel fajlove u data folderu."""
        excel_files = []
        
        if self.data_folder.exists():
            # Pronađi sve .xlsx i .xls fajlove
            for pattern in ['*.xlsx', '*.xls']:
                excel_files.extend(list(self.data_folder.glob(pattern)))
        
        return sorted(excel_files)
    
    def load_all_files(self, file_paths: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """
        Učitava sve Excel fajlove.
        
        Args:
            file_paths: Lista putanja do fajlova. Ako nije navedeno, učitava sve iz data foldera.
            
        Returns:
            Dictionary sa ključevima: naziv fajla, vrijednosti: DataFrame
        """
        if file_paths is None:
            files = self.discover_excel_files()
        else:
            files = [Path(f) for f in file_paths]
        
        self.loaded_files = {}
        self.file_info = []
        
        for file_path in files:
            try:
                print(f"Učitavam: {file_path.name}")
                
                # Koristi postojeći DataLoader za konzistentnost
                loader = DataLoader(str(file_path))
                df = loader.process_data()
                
                # Dodaj kolonu sa izvorom podataka
                df['_Izvor_Fajl'] = file_path.name
                
                self.loaded_files[file_path.name] = df
                
                # Sačuvaj informacije o fajlu
                self.file_info.append({
                    'naziv': file_path.name,
                    'putanja': str(file_path),
                    'redova': len(df),
                    'kolona': len(df.columns),
                    'datum_od': df['Datum i vrijeme'].min(),
                    'datum_do': df['Datum i vrijeme'].max(),
                    'ukupan_promet': df['Ukupno'].sum() if 'Ukupno' in df.columns else 0,
                    'broj_računa': df['Fiskalni broj računa'].nunique() if 'Fiskalni broj računa' in df.columns else 0
                })
                
                print(f"  ✓ Učitano {len(df)} redova")
                
            except Exception as e:
                print(f"  ✗ Greška pri učitavanju {file_path.name}: {str(e)}")
                continue
        
        return self.loaded_files
    
    def load_uploaded_files(self, uploaded_files: List) -> Dict[str, pd.DataFrame]:
        """
        Učitava fajlove iz Streamlit file_uploader-a.
        
        Args:
            uploaded_files: Lista Streamlit UploadedFile objekata
            
        Returns:
            Dictionary sa učitanim podacima
        """
        self.loaded_files = {}
        self.file_info = []
        
        for uploaded_file in uploaded_files:
            try:
                print(f"Učitavam: {uploaded_file.name}")
                
                loader = DataLoader(uploaded_file)
                df = loader.process_data()
                
                df['_Izvor_Fajl'] = uploaded_file.name
                
                self.loaded_files[uploaded_file.name] = df
                
                self.file_info.append({
                    'naziv': uploaded_file.name,
                    'putanja': uploaded_file.name,
                    'redova': len(df),
                    'kolona': len(df.columns),
                    'datum_od': df['Datum i vrijeme'].min(),
                    'datum_do': df['Datum i vrijeme'].max(),
                    'ukupan_promet': df['Ukupno'].sum() if 'Ukupno' in df.columns else 0,
                    'broj_računa': df['Fiskalni broj računa'].nunique() if 'Fiskalni broj računa' in df.columns else 0
                })
                
                print(f"  ✓ Učitano {len(df)} redova")
                
            except Exception as e:
                print(f"  ✗ Greška pri učitavanju {uploaded_file.name}: {str(e)}")
                continue
        
        return self.loaded_files
    
    def combine_data(self) -> pd.DataFrame:
        """
        Objedinjava sve učitane fajlove u jedan DataFrame.
        
        Returns:
            Objedinjeni DataFrame sa svim podacima
        """
        if not self.loaded_files:
            raise ValueError("Nema učitanih fajlova za objedinjavanje")
        
        # Spoji sve DataFrame-ove
        all_dfs = list(self.loaded_files.values())
        self.combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)
        
        print(f"Objedinjeno {len(self.loaded_files)} fajlova:")
        print(f"  - Ukupno redova: {len(self.combined_df)}")
        print(f"  - Ukupno kolona: {len(self.combined_df.columns)}")
        
        return self.combined_df
    
    def get_column_comparison(self) -> pd.DataFrame:
        """
        Vraća usporedbu kolona između različitih fajlova.
        
        Returns:
            DataFrame sa informacijama o kolonama u svakom fajlu
        """
        if not self.loaded_files:
            raise ValueError("Nema učitanih fajlova")
        
        # Skupi sve kolone
        all_columns = set()
        for df in self.loaded_files.values():
            all_columns.update(df.columns)
        
        # Izgradi usporednu tablicu
        comparison_data = []
        
        for col in sorted(all_columns):
            row = {'Kolona': col}
            
            for file_name, df in self.loaded_files.items():
                if col in df.columns:
                    # Provjeri tip podataka i broj ne-null vrijednosti
                    non_null_count = df[col].notna().sum()
                    dtype = str(df[col].dtype)
                    row[file_name] = f"✓ ({dtype}, {non_null_count})"
                else:
                    row[file_name] = "✗"
            
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def get_summary_report(self) -> Dict:
        """
        Vraća sažeti izvještaj o svim učitanim fajlovima.
        
        Returns:
            Dictionary sa sažetim informacijama
        """
        if not self.loaded_files:
            return {}
        
        # Osnovne statistike
        total_rows = sum(info['redova'] for info in self.file_info)
        total_revenue = sum(info['ukupan_promet'] for info in self.file_info)
        total_invoices = sum(info['broj_računa'] for info in self.file_info)
        
        # Datumski raspon
        all_dates_min = min(info['datum_od'] for info in self.file_info)
        all_dates_max = max(info['datum_do'] for info in self.file_info)
        
        return {
            'broj_fajlova': len(self.loaded_files),
            'ukupno_redova': total_rows,
            'ukupan_promet': total_revenue,
            'ukupno_računa': total_invoices,
            'datum_od': all_dates_min,
            'datum_do': all_dates_max,
            'fajlovi': self.file_info
        }
    
    def get_variable_summary(self) -> pd.DataFrame:
        """
        Vraća pregled svih varijabli (kolona) u svim učitanim fajlovima.
        
        Returns:
            DataFrame sa informacijama o svakoj varijabli
        """
        if self.combined_df is None:
            self.combine_data()
        
        variable_info = []
        
        for col in self.combined_df.columns:
            # Preskači internu kolonu _Izvor_Fajl
            if col.startswith('_'):
                continue
            
            col_data = self.combined_df[col]
            
            info = {
                'Varijabla': col,
                'Tip_podataka': str(col_data.dtype),
                'Ukupno_vrijednosti': len(col_data),
                'Validnih_vrijednosti': col_data.notna().sum(),
                'Nedostaje_vrijednosti': col_data.isna().sum(),
                'Procenat_popunjenosti': f"{(col_data.notna().sum() / len(col_data) * 100):.1f}%",
                'Jedinstvenih_vrijednosti': col_data.nunique(),
            }
            
            # Dodaj primjer vrijednosti
            if col_data.notna().any():
                info['Primjer_vrijednosti'] = str(col_data.dropna().iloc[0])
            else:
                info['Primjer_vrijednosti'] = 'N/A'
            
            # Za numeričke kolone dodaj statistiku
            if pd.api.types.is_numeric_dtype(col_data):
                info['Min'] = col_data.min()
                info['Max'] = col_data.max()
                info['Prosjek'] = col_data.mean()
                info['Suma'] = col_data.sum()
            
            variable_info.append(info)
        
        return pd.DataFrame(variable_info)
    
    def get_files_overview(self) -> pd.DataFrame:
        """Vraća pregled svih učitanih fajlova."""
        return pd.DataFrame(self.file_info)
