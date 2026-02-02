"""
Quahwa Dashboard - Jednostavna Analitička Aplikacija
Fokus: Vremenska analiza, Analiza prodaje, Usporedbe
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Dodavanje src foldera u path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.data_loader import DataLoader

# Konfiguracija
st.set_page_config(
    page_title="Quahwa Analiza",
    page_icon="☕",
    layout="wide"
)

st.markdown("# ☕ Quahwa - Analiza Prodaje")

# Inicijalizacija
if 'df' not in st.session_state:
    st.session_state.df = None

# Sidebar - Učitavanje podataka
with st.sidebar:
    st.header("📂 Učitaj podatke")
    
    uploaded_file = st.file_uploader("Odaberi Excel fajl", type=['xlsx', 'xls'])
    
    if uploaded_file or Path('../data/Računi.xlsx').exists():
        if st.button("Učitaj", type="primary"):
            with st.spinner("Učitavanje..."):
                try:
                    filepath = uploaded_file if uploaded_file else '../data/Računi.xlsx'
                    loader = DataLoader(filepath)
                    st.session_state.df = loader.process_data()
                    st.success(f"✅ Učitano {len(st.session_state.df):,} redova")
                except Exception as e:
                    st.error(f"Greška: {str(e)}")

# Glavni dio
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Sidebar filteri
    with st.sidebar:
        st.divider()
        st.header("🔍 Filteri")
        
        # Period selektor
        min_date = df['Datum i vrijeme'].min().date()
        max_date = df['Datum i vrijeme'].max().date()
        
        date_range = st.date_input(
            "Odaberi period:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[
                (df['Datum i vrijeme'].dt.date >= start_date) &
                (df['Datum i vrijeme'].dt.date <= end_date)
            ]
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Pregled",
        "⏰ Vremenska Analiza", 
        "🛒 Analiza Prodaje",
        "📅 Usporedbe"
    ])
    
    # TAB 1: PREGLED
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Ukupan Promet", f"{df['Ukupno'].sum():,.2f} EUR")
        with col2:
            st.metric("🧾 Broj Računa", f"{df['Fiskalni broj računa'].nunique():,}")
        with col3:
            st.metric("📦 Količina", f"{int(df['Količina'].sum()):,}")
        with col4:
            avg_bill = df.groupby('Fiskalni broj računa')['Ukupno'].sum().mean()
            st.metric("💵 Prosječan Račun", f"{avg_bill:.2f} EUR")
        
        st.divider()
        
        # Dnevni promet
        daily = df.groupby(df['Datum i vrijeme'].dt.date)['Ukupno'].sum().reset_index()
        daily.columns = ['Datum', 'Promet']
        
        fig = px.line(daily, x='Datum', y='Promet', title='Dnevni Promet')
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: VREMENSKA ANALIZA
    with tab2:
        st.subheader("Analiza po Vremenu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Po danima u tjednu
            by_day = df.groupby('Dan_u_tjednu')['Ukupno'].sum().reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            day_names = ['Pon', 'Uto', 'Sri', 'Čet', 'Pet', 'Sub', 'Ned']
            
            fig = go.Figure(data=[go.Bar(x=day_names, y=by_day.values)])
            fig.update_layout(title='Promet po Danima u Tjednu', xaxis_title='Dan', yaxis_title='Promet (EUR)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Po satima
            by_hour = df.groupby('Sat')['Ukupno'].sum()
            
            fig = px.bar(x=by_hour.index, y=by_hour.values, 
                        labels={'x': 'Sat', 'y': 'Promet (EUR)'},
                        title='Promet po Satima')
            st.plotly_chart(fig, use_container_width=True)
        
        # Po mjesecima
        by_month = df.groupby(df['Datum i vrijeme'].dt.to_period('M'))['Ukupno'].sum()
        by_month.index = by_month.index.astype(str)
        
        fig = px.bar(x=by_month.index, y=by_month.values,
                    labels={'x': 'Mjesec', 'y': 'Promet (EUR)'},
                    title='Promet po Mjesecima')
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: ANALIZA PRODAJE
    with tab3:
        st.subheader("Analiza Artikala i Grupa")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top artikli
            top_products = df.groupby('Artikl')['Ukupno'].sum().nlargest(15)
            
            fig = px.bar(y=top_products.index, x=top_products.values, 
                        orientation='h',
                        labels={'x': 'Promet (EUR)', 'y': 'Artikl'},
                        title='Top 15 Artikala po Prometu')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Po prodajnim grupama
            by_group = df.groupby('Prodajna grupa')['Ukupno'].sum().sort_values(ascending=False)
            
            fig = px.pie(values=by_group.values, names=by_group.index,
                        title='Promet po Prodajnim Grupama')
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Detaljna tablica
        st.subheader("Detaljna Tablica - Artikli")
        
        product_stats = df.groupby('Artikl').agg({
            'Ukupno': 'sum',
            'Količina': 'sum',
            'Fiskalni broj računa': 'nunique'
        }).round(2)
        product_stats.columns = ['Promet (EUR)', 'Količina', 'Broj računa']
        product_stats = product_stats.sort_values('Promet (EUR)', ascending=False)
        
        st.dataframe(product_stats, width='stretch')
    
    # TAB 4: USPOREDBE
    with tab4:
        st.subheader("📅 Usporedba Perioda")
        
        # Odabir perioda za usporedbu
        comparison_type = st.radio(
            "Vrsta usporedbe:",
            ["Mjeseci", "Kvartali", "Godine"]
        )
        
        if comparison_type == "Mjeseci":
            # Odabir mjeseci za usporedbu
            available_months = df['Datum i vrijeme'].dt.to_period('M').unique()
            available_months = sorted([str(m) for m in available_months])
            
            if len(available_months) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    month1 = st.selectbox("Prvi mjesec:", available_months, index=0)
                with col2:
                    month2 = st.selectbox("Drugi mjesec:", available_months, 
                                        index=min(1, len(available_months)-1))
                
                # Priprema podataka
                df1 = df[df['Datum i vrijeme'].dt.to_period('M').astype(str) == month1]
                df2 = df[df['Datum i vrijeme'].dt.to_period('M').astype(str) == month2]
                
                # Metrike usporedbe
                col1, col2, col3 = st.columns(3)
                
                promet1 = df1['Ukupno'].sum()
                promet2 = df2['Ukupno'].sum()
                delta_promet = ((promet2 - promet1) / promet1 * 100) if promet1 > 0 else 0
                
                with col1:
                    st.metric(f"💰 Promet {month1}", f"{promet1:,.2f} EUR")
                with col2:
                    st.metric(f"💰 Promet {month2}", f"{promet2:,.2f} EUR", 
                             delta=f"{delta_promet:+.1f}%")
                with col3:
                    racuni1 = df1['Fiskalni broj računa'].nunique()
                    racuni2 = df2['Fiskalni broj računa'].nunique()
                    st.metric(f"🧾 Računi {month1}", f"{racuni1:,}")
                    st.metric(f"🧾 Računi {month2}", f"{racuni2:,}")
                
                # Graf usporedbe top artikala
                st.divider()
                st.subheader("Usporedba Top Artikala")
                
                top1 = df1.groupby('Artikl')['Ukupno'].sum().nlargest(10)
                top2 = df2.groupby('Artikl')['Ukupno'].sum().nlargest(10)
                
                all_products = list(set(top1.index) | set(top2.index))
                
                comparison_data = pd.DataFrame({
                    month1: [top1.get(p, 0) for p in all_products],
                    month2: [top2.get(p, 0) for p in all_products]
                }, index=all_products).sort_values(month1, ascending=False)
                
                fig = go.Figure(data=[
                    go.Bar(name=month1, x=comparison_data.index, y=comparison_data[month1]),
                    go.Bar(name=month2, x=comparison_data.index, y=comparison_data[month2])
                ])
                fig.update_layout(barmode='group', title='Usporedba Top Artikala',
                                xaxis_title='Artikl', yaxis_title='Promet (EUR)')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Potrebno je najmanje 2 mjeseca podataka za usporedbu.")
        
        elif comparison_type == "Godine":
            # Usporedba istih mjeseci u različitim godinama
            st.subheader("Usporedba istog mjeseca u različitim godinama")
            
            available_years = sorted(df['Godina'].unique())
            
            if len(available_years) >= 2:
                # Odabir mjeseca
                month_num = st.selectbox("Odaberi mjesec:", range(1, 13),
                                        format_func=lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 
                                                             'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 
                                                             'Nov', 'Dec'][x-1])
                
                # Podatci za svaku godinu
                yearly_data = {}
                for year in available_years:
                    year_month_df = df[(df['Godina'] == year) & (df['Mjesec'] == month_num)]
                    if not year_month_df.empty:
                        yearly_data[year] = year_month_df
                
                if len(yearly_data) >= 2:
                    # Metrike
                    cols = st.columns(len(yearly_data))
                    for i, (year, year_df) in enumerate(yearly_data.items()):
                        with cols[i]:
                            st.metric(f"💰 {year}", f"{year_df['Ukupno'].sum():,.2f} EUR")
                            st.metric(f"🧾 Računi", f"{year_df['Fiskalni broj računa'].nunique():,}")
                    
                    # Graf usporedbe
                    st.divider()
                    fig = go.Figure()
                    
                    for year, year_df in yearly_data.items():
                        daily = year_df.groupby(year_df['Datum i vrijeme'].dt.day)['Ukupno'].sum()
                        fig.add_trace(go.Scatter(x=daily.index, y=daily.values, 
                                               mode='lines+markers', name=str(year)))
                    
                    fig.update_layout(title=f'Dnevni Promet - Usporedba po Godinama',
                                    xaxis_title='Dan u mjesecu', yaxis_title='Promet (EUR)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Ovaj mjesec ne postoji u više godina za usporedbu.")
            else:
                st.info("Potrebno je najmanje 2 godine podataka.")

else:
    st.info("👈 Učitaj Excel fajl sa podacima o računima koristeći sidebar.")
    st.markdown("""
    ### Očekivana struktura podataka:
    
    Excel fajl treba sadržavati kolone:
    - **Datum i vrijeme** - Datum/vrijeme transakcije
    - **Fiskalni broj računa** - Jedinstveni broj računa
    - **Artikl** - Naziv proizvoda
    - **Prodajna grupa** - Kategorija proizvoda
    - **Količina** - Prodana količina
    - **Ukupno** - Iznos
    """)
