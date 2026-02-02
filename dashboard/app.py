"""
Quahwa Dashboard - Analitički Dashboard za Prodaju
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Dodavanje src foldera u path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.data_loader import DataLoader
from utils.multi_file_loader import MultiFileLoader
from analysis.time_analysis import TimeAnalyzer
from analysis.sales_analysis import SalesAnalyzer

# Konfiguracija stranice
st.set_page_config(
    page_title="Quahwa Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E4057;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Inicijalizacija session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df_processed = None
    st.session_state.data_loader = None
    st.session_state.multi_file_loader = None
    st.session_state.use_multi_files = False

# Naslov
st.markdown('<h1 class="main-header">☕ Quahwa Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Postavke")
    
    # Odabir načina učitavanja podataka
    data_source = st.radio(
        "Izvor podataka:",
        ["Jedan fajl", "Više fajlova", "Fajlovi iz foldera"],
        index=0,
        help="Odaberi kako želiš učitati podatke"
    )
    
    uploaded_file = None
    uploaded_files = None
    filepath = None
    
    if data_source == "Jedan fajl":
        # Postojeća funkcionalnost
        uploaded_file = st.file_uploader("Učitaj Excel fajl", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            filepath = uploaded_file
        else:
            filepath = "../Računi.xlsx"
        
        st.session_state.use_multi_files = False
        
    elif data_source == "Više fajlova":
        # Upload više fajlova
        uploaded_files = st.file_uploader(
            "Učitaj Excel fajlove", 
            type=['xlsx', 'xls'],
            accept_multiple_files=True
        )
        st.session_state.use_multi_files = True
        
    else:  # "Fajlovi iz foldera"
        # Učitaj sve iz data foldera
        data_folder = Path(__file__).parent.parent / 'data'
        st.session_state.use_multi_files = True
        st.info(f"📁 Učitavanje fajlova iz: {data_folder}")
    
    # Dugme za učitavanje podataka
    if st.button("📥 Učitaj podatke", type="primary"):
        with st.spinner("Učitavam podatke..."):
            try:
                if st.session_state.use_multi_files:
                    # Učitavanje više fajlova
                    data_folder = Path(__file__).parent.parent / 'data'
                    multi_loader = MultiFileLoader(str(data_folder))
                    
                    if data_source == "Više fajlova" and uploaded_files:
                        # Upload više fajlova
                        multi_loader.load_uploaded_files(uploaded_files)
                    else:
                        # Učitaj iz foldera
                        multi_loader.load_all_files()
                    
                    if not multi_loader.loaded_files:
                        st.error("❌ Nema pronađenih Excel fajlova!")
                    else:
                        df = multi_loader.combine_data()
                        st.session_state.data_loaded = True
                        st.session_state.df_processed = df
                        st.session_state.multi_file_loader = multi_loader
                        
                        # Prikaz sažetka
                        summary = multi_loader.get_summary_report()
                        st.success(f"✅ Učitano {summary['broj_fajlova']} fajlova!")
                        
                        st.info(f"""
                        📊 **Objedinjeni podaci:**
                        - {summary['ukupno_redova']:,} redova
                        - {summary['broj_fajlova']} fajlova
                        - Period: {summary['datum_od'].strftime('%d.%m.%Y')} - {summary['datum_do'].strftime('%d.%m.%Y')}
                        - Ukupan promet: {summary['ukupan_promet']:,.2f} EUR
                        """)
                        
                else:
                    # Postojeća funkcionalnost - jedan fajl
                    loader = DataLoader(filepath)
                    df = loader.process_data()
                    st.session_state.data_loaded = True
                    st.session_state.df_processed = df
                    st.session_state.data_loader = loader
                    
                    # Prikaz informacija o učitanim podacima
                    summary = loader.get_data_summary()
                    st.success("✅ Podaci uspješno učitani!")
                    
                    # Provjera i upozorenje za nedostajuće kolone
                    missing_cols = []
                    important_cols = ['Prodajna grupa', 'Fiskalni broj računa', 'Artikl', 'Količina', 'Ukupno']
                    for col in important_cols:
                        if col not in df.columns:
                            missing_cols.append(col)
                    
                    if missing_cols:
                        st.warning(f"⚠️ Nedostaju kolone: {', '.join(missing_cols)}. Neke analize će biti ograničene.")
                    
                    st.info(f"""
                    📊 **Učitano:**
                    - {summary['ukupno_redova']:,} redova
                    - Period: {summary['datum_od'].strftime('%d.%m.%Y')} - {summary['datum_do'].strftime('%d.%m.%Y')}
                    - Ukupan promet: {summary['ukupni_promet']:,.2f} EUR
                    """)
            except ValueError as e:
                st.error(f"❌ Greška u podacima: {str(e)}")
                st.info("💡 Provjerite da Excel fajl sadrži potrebne kolone (Datum i vrijeme, Količina, Ukupno, itd.)")
            except Exception as e:
                st.error(f"❌ Greška pri učitavanju: {str(e)}")
                st.info("💡 Provjerite da je fajl validan Excel format (.xlsx ili .xls)")
    
    st.divider()
    
    # Filteri - samo ako su podaci učitani
    if st.session_state.data_loaded:
        st.subheader("🔍 Filteri")
        
        df = st.session_state.df_processed
        
        # Filter po periodu
        filter_type = st.radio(
            "Odaberi period:",
            ["Sve", "Zadnjih N dana", "Custom raspon"],
            index=0
        )
        
        df_filtered = df.copy()
        
        if filter_type == "Zadnjih N dana":
            n_days = st.slider("Broj dana:", 1, 365, 30)
            max_date = df['Datum i vrijeme'].max()
            min_date = max_date - pd.Timedelta(days=n_days)
            df_filtered = df[df['Datum i vrijeme'] >= min_date]
        
        elif filter_type == "Custom raspon":
            min_date = df['Datum i vrijeme'].min().date()
            max_date = df['Datum i vrijeme'].max().date()
            
            date_range = st.date_input(
                "Odaberi raspon:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df[
                    (df['Datum i vrijeme'].dt.date >= start_date) &
                    (df['Datum i vrijeme'].dt.date <= end_date)
                ]
        
        st.session_state.df_filtered = df_filtered
        
        # Filter po prodajnoj grupi - samo ako postoji
        if 'Prodajna grupa' in df.columns:
            st.divider()
            all_groups = ["Sve"] + sorted(df['Prodajna grupa'].unique().tolist())
            selected_groups = st.multiselect(
                "Prodajne grupe:",
                all_groups,
                default=["Sve"]
            )
            
            if "Sve" not in selected_groups and selected_groups:
                df_filtered = df_filtered[df_filtered['Prodajna grupa'].isin(selected_groups)]
                st.session_state.df_filtered = df_filtered

# Glavni dio - prikazuje se samo ako su podaci učitani
if st.session_state.data_loaded:
    df_filtered = st.session_state.df_filtered
    
    # Tabs za različite analize - dodaj novi tab za izvješće o varijablama
    if st.session_state.use_multi_files:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Pregled", 
            "⏰ Vremenska Analiza", 
            "🛒 Analiza Prodaje",
            "📈 ABC Analiza",
            "📋 Izvješće varijabli",
            "📁 Pregled fajlova"
        ])
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Pregled", 
            "⏰ Vremenska Analiza", 
            "🛒 Analiza Prodaje",
            "📈 ABC Analiza"
        ])
    
    # TAB 1: PREGLED
    with tab1:
        st.header("Osnovni pregled")
        
        # Metrike
        sales_analyzer = SalesAnalyzer(df_filtered)
        metrics = sales_analyzer.get_sales_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Ukupni Promet",
                f"{metrics['ukupni_promet']:,.2f} EUR"
            )
        
        with col2:
            st.metric(
                "🧾 Broj Računa",
                f"{metrics['broj_računa']:,}"
            )
        
        with col3:
            st.metric(
                "📦 Ukupna Količina",
                f"{int(metrics['ukupna_kolicina']):,}"
            )
        
        with col4:
            st.metric(
                "💵 Prosječan Račun",
                f"{metrics['prosječan_račun']:,.2f} EUR"
            )
        
        st.divider()
        
        # Distribucija po prodajnim grupama
        if 'Prodajna grupa' in df_filtered.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Top 10 Prodajnih Grupa")
                top_groups = sales_analyzer.analyze_by_product_group(top_n=10)
                if not top_groups.empty:
                    st.dataframe(
                        top_groups[['Prodajna_grupa', 'Promet', 'Ukupna_količina', 'Udio_u_prometu']],
                        hide_index=True,
                        width='stretch'
                    )
                else:
                    st.info("Nema podataka o prodajnim grupama.")
            
            with col2:
                st.subheader("🥧 Distribucija Prometa")
                if not top_groups.empty:
                    fig = sales_analyzer.plot_product_group_distribution()
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("Nema podataka za prikaz.")
        else:
            st.info("ℹ️ Excel fajl ne sadrži kolonu 'Prodajna grupa'. Analiza po grupama nije dostupna.")
        
        st.divider()
        
        # Top proizvodi
        st.subheader("🏆 Top 15 Proizvoda")
        
        sort_by = st.selectbox(
            "Sortiraj po:",
            ["promet", "kolicina", "broj_racuna"],
            format_func=lambda x: {
                "promet": "Prometu",
                "kolicina": "Količini",
                "broj_racuna": "Broju računa"
            }[x]
        )
        
        fig = sales_analyzer.plot_top_products(n=15, by=sort_by)
        st.plotly_chart(fig, width='stretch')
    
    # TAB 2: VREMENSKA ANALIZA
    with tab2:
        st.header("Vremenska Analiza")
        
        time_analyzer = TimeAnalyzer(df_filtered)
        
        # Analiza po mjesecima
        st.subheader("📅 Analiza po Mjesecima")
        monthly_data = time_analyzer.analyze_by_month()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = time_analyzer.plot_monthly_trend(metric='Promet')
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            st.dataframe(
                monthly_data[['Mjesec_naziv', 'Promet', 'Broj_računa', 'Prosječan_račun']],
                hide_index=True,
                width='stretch',
                height=400
            )
        
        st.divider()
        
        # Analiza po danima u tjednu
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📆 Analiza po Danima u Tjednu")
            fig = time_analyzer.plot_day_of_week_distribution()
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            st.subheader("🕐 Analiza po Satima")
            # Debug: Detaljni pregled
            with st.expander("🔍 Debug Info", expanded=False):
                st.write("**Dostupne kolone:**", df_filtered.columns.tolist())
                if 'Sat' in df_filtered.columns:
                    st.write(f"**Sat kolona - tip:** {df_filtered['Sat'].dtype}")
                    st.write(f"**Jedinstveni sati:** {sorted(df_filtered['Sat'].dropna().unique().tolist())}")
                    st.write(f"**Broj NaN vrijednosti:** {df_filtered['Sat'].isna().sum()}")
                    st.write(f"**Primjeri Sat vrijednosti:**")
                    st.write(df_filtered[['Datum i vrijeme', 'Sat']].head(10))
                else:
                    st.error("❌ Kolona 'Sat' ne postoji!")
            
            fig = time_analyzer.plot_hourly_distribution()
            st.plotly_chart(fig, width='stretch')
        
        st.divider()
        
        # Detaljna analiza po satima
        st.subheader("📊 Detaljni Pregled po Satima")
        hourly_data = time_analyzer.analyze_by_hour()
        st.dataframe(
            hourly_data,
            hide_index=True,
            width='stretch'
        )
    
    # TAB 3: ANALIZA PRODAJE
    with tab3:
        st.header("Detaljna Analiza Prodaje")
        
        # Top proizvodi tabela
        st.subheader("🏆 Top 20 Proizvoda po Prometu")
        top_products = sales_analyzer.get_top_products(n=20, by='promet')
        st.dataframe(
            top_products,
            hide_index=True,
            width='stretch'
        )
        
        st.divider()
        
        # Performanse po vremenu
        st.subheader("📈 Performanse Prodajnih Grupa kroz Vrijeme")
        
        # Mapiranje naziva za prikaz
        time_dimensions = {
            "Dan_u_tjednu": "Dan u tjednu",
            "Sat": "Sat",
            "Tjedan": "Tjedan",
            "Period_dana": "Period dana",
            "Mjesec_naziv": "Mjesec (naziv)"
        }
        
        time_dim = st.selectbox(
            "Odaberi vremensku dimenziju:",
            list(time_dimensions.keys()),
            format_func=lambda x: time_dimensions[x]
        )
        
        try:
            perf_data = sales_analyzer.analyze_product_performance_by_time(time_dimension=time_dim)
        except ValueError as e:
            st.error(f"Greška: {str(e)}")
            perf_data = pd.DataFrame()
        
        if not perf_data.empty and len(perf_data) > 0:
            import plotly.express as px
            fig = px.bar(
                perf_data,
                x=time_dim,
                y='Promet',
                color='Prodajna_grupa',
                title=f'Promet po {time_dimensions[time_dim]}',
                barmode='stack'
            )
            st.plotly_chart(fig, width='stretch')
            
            # Tabela
            try:
                pivot_data = perf_data.pivot_table(
                    index=time_dim,
                    columns='Prodajna_grupa',
                    values='Promet',
                    fill_value=0
                )
                st.dataframe(pivot_data, width='stretch')
            except Exception as e:
                st.warning(f"Ne mogu kreirati pivot tabelu: {str(e)}")
                st.dataframe(perf_data, width='stretch')
        else:
            st.warning("Nema podataka za prikaz.")
    
    # TAB 4: ABC ANALIZA
    with tab4:
        st.header("ABC Analiza")
        
        st.info("""
        **ABC Analiza** klasificira proizvode u tri kategorije:
        - **A kategorija**: Top proizvodi koji čine 80% prometa
        - **B kategorija**: Srednji proizvodi (80-95% prometa)
        - **C kategorija**: Ostali proizvodi (95-100% prometa)
        """)
        
        try:
            # ABC grafikon
            fig = sales_analyzer.plot_abc_analysis()
            st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.error(f"Greška pri kreiranju ABC grafikona: {str(e)}")
            st.info("Provjerite da li postoje podaci za analizu.")
        
        st.divider()
        
        # ABC tabele
        try:
            abc_data = sales_analyzer.analyze_revenue_distribution()
            
            if not abc_data.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("🥇 A Kategorija")
                    a_products = abc_data[abc_data['ABC_Kategorija'] == 'A']
                    st.metric("Broj proizvoda", len(a_products))
                    st.metric("Udio u prometu", f"{a_products['Udio_u_prometu'].sum():.1f}%")
                
                with col2:
                    st.subheader("🥈 B Kategorija")
                    b_products = abc_data[abc_data['ABC_Kategorija'] == 'B']
                    st.metric("Broj proizvoda", len(b_products))
                    st.metric("Udio u prometu", f"{b_products['Udio_u_prometu'].sum():.1f}%")
                
                with col3:
                    st.subheader("🥉 C Kategorija")
                    c_products = abc_data[abc_data['ABC_Kategorija'] == 'C']
                    st.metric("Broj proizvoda", len(c_products))
                    st.metric("Udio u prometu", f"{c_products['Udio_u_prometu'].sum():.1f}%")
                
                st.divider()
                
                # Tabela po kategorijama
                selected_category = st.selectbox(
                    "Prikaži proizvode kategorije:",
                    ["A", "B", "C", "Sve"]
                )
                
                if selected_category == "Sve":
                    display_data = abc_data
                else:
                    display_data = abc_data[abc_data['ABC_Kategorija'] == selected_category]
                
                st.dataframe(
                    display_data[[
                        'Artikl', 'Prodajna_grupa', 'Promet', 
                        'Ukupna_količina', 'Udio_u_prometu', 
                        'Kumulativni_postotak', 'ABC_Kategorija'
                    ]],
                    hide_index=True,
                    width='stretch',
                    height=400
                )
            else:
                st.warning("Nema podataka za ABC analizu.")
        except Exception as e:
            st.error(f"Greška pri kreiranju ABC analize: {str(e)}")
    
    # TAB 5: IZVJEŠĆE VARIJABLI (samo za multi-file mode)
    if st.session_state.use_multi_files:
        with tab5:
            st.header("📋 Izvješće svih varijabli")
            
            multi_loader = st.session_state.multi_file_loader
            
            if multi_loader:
                st.markdown("""
                Ovaj pregled prikazuje sve varijable (kolone) koje postoje u učitanim Excel tablicama, 
                zajedno sa detaljnim informacijama o svakoj varijabli.
                """)
                
                # Pregled varijabli
                variable_summary = multi_loader.get_variable_summary()
                
                st.subheader("📊 Sve varijable u podacima")
                
                # Filtriraj kolone koje prikazujemo
                display_columns = ['Varijabla', 'Tip_podataka', 'Ukupno_vrijednosti', 
                                 'Validnih_vrijednosti', 'Procenat_popunjenosti', 
                                 'Jedinstvenih_vrijednosti', 'Primjer_vrijednosti']
                
                st.dataframe(
                    variable_summary[display_columns],
                    hide_index=True,
                    use_container_width=True,
                    height=500
                )
                
                st.divider()
                
                # Statistika za numeričke varijable
                numeric_vars = variable_summary[variable_summary['Tip_podataka'].str.contains('int|float')]
                
                if not numeric_vars.empty:
                    st.subheader("📈 Numeričke varijable - statistika")
                    
                    numeric_display = numeric_vars[['Varijabla', 'Min', 'Max', 'Prosjek', 'Suma']].copy()
                    
                    st.dataframe(
                        numeric_display,
                        hide_index=True,
                        use_container_width=True
                    )
                
                st.divider()
                
                # Usporedba kolona između fajlova
                st.subheader("🔍 Usporedba kolona između fajlova")
                
                column_comparison = multi_loader.get_column_comparison()
                
                st.dataframe(
                    column_comparison,
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )
                
                st.info("""
                **Objašnjenje simbola:**
                - ✓ - Kolona postoji u fajlu (tip podataka, broj vrijednosti)
                - ✗ - Kolona ne postoji u fajlu
                """)
                
                # Download opcije
                st.divider()
                st.subheader("💾 Preuzmi izvješća")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_summary = variable_summary.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Preuzmi pregled varijabli (CSV)",
                        data=csv_summary,
                        file_name="varijable_izvjestaj.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    csv_comparison = column_comparison.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Preuzmi usporedbu kolona (CSV)",
                        data=csv_comparison,
                        file_name="usporedba_kolona.csv",
                        mime="text/csv"
                    )
        
        # TAB 6: PREGLED FAJLOVA
        with tab6:
            st.header("📁 Pregled učitanih fajlova")
            
            multi_loader = st.session_state.multi_file_loader
            
            if multi_loader:
                summary = multi_loader.get_summary_report()
                
                # Ukupna statistika
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📁 Broj fajlova", summary['broj_fajlova'])
                
                with col2:
                    st.metric("📊 Ukupno redova", f"{summary['ukupno_redova']:,}")
                
                with col3:
                    st.metric("💰 Ukupan promet", f"{summary['ukupan_promet']:,.2f} EUR")
                
                with col4:
                    st.metric("🧾 Ukupno računa", f"{summary['ukupno_računa']:,}")
                
                st.divider()
                
                # Detalji po fajlovima
                st.subheader("📄 Detalji po fajlovima")
                
                files_overview = multi_loader.get_files_overview()
                
                # Formatiraj datume
                files_overview['datum_od'] = pd.to_datetime(files_overview['datum_od']).dt.strftime('%d.%m.%Y')
                files_overview['datum_do'] = pd.to_datetime(files_overview['datum_do']).dt.strftime('%d.%m.%Y')
                
                st.dataframe(
                    files_overview,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        'naziv': 'Naziv fajla',
                        'redova': st.column_config.NumberColumn('Redova', format="%d"),
                        'kolona': st.column_config.NumberColumn('Kolona', format="%d"),
                        'datum_od': 'Od',
                        'datum_do': 'Do',
                        'ukupan_promet': st.column_config.NumberColumn('Promet (EUR)', format="%.2f"),
                        'broj_računa': st.column_config.NumberColumn('Broj računa', format="%d")
                    }
                )
                
                st.divider()
                
                # Vizualizacija po fajlovima
                st.subheader("📊 Vizualizacija po fajlovima")
                
                import plotly.express as px
                
                # Graf prometa po fajlovima
                fig_revenue = px.bar(
                    files_overview,
                    x='naziv',
                    y='ukupan_promet',
                    title='Promet po fajlovima',
                    labels={'naziv': 'Fajl', 'ukupan_promet': 'Promet (EUR)'}
                )
                st.plotly_chart(fig_revenue, use_container_width=True)
                
                # Graf broja redova
                fig_rows = px.bar(
                    files_overview,
                    x='naziv',
                    y='redova',
                    title='Broj transakcija po fajlovima',
                    labels={'naziv': 'Fajl', 'redova': 'Broj redova'}
                )
                st.plotly_chart(fig_rows, use_container_width=True)

else:
    # Prikaz kada podaci nisu učitani
    st.info("👈 Učitaj podatke koristeći sidebar da započneš analizu!")
    
    st.markdown("""
    ### Dobrodošli u Quahwa Analytics Dashboard! ☕
    
    Ovaj dashboard omogućava detaljnu analizu prodajnih podataka sa fokusom na:
    
    - **Vremensku analizu**: Mjeseci, tjedni, dani, sati
    - **Analizu prodaje**: Proizvodi, prodajne grupe, promet
    - **ABC analizu**: Pareto princip i klasifikacija proizvoda
    - **Interaktivne grafove**: Visualizacija trendova i distribucija
    
    **Kako početi:**
    1. Klikni na "📥 Učitaj podatke" u sidebar-u
    2. Koristi filtere za odabir perioda i prodajnih grupa
    3. Istraži različite tabove za različite tipove analiza
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Quahwa Analytics Dashboard © 2026</p>
</div>
""", unsafe_allow_html=True)


