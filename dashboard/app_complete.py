"""
Quahwa Analytics - Kompletan Dashboard
Automatski učitava sve podatke i prikazuje 10 tabova sa detaljnim analizama
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Dodavanje src foldera u path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.auto_data_loader import AutoDataLoader
from analysis.advanced_analytics import (
    FinancialAnalytics, SalesAnalytics, TimeAnalytics,
    LocationAnalytics, CustomerAnalytics, ProductComparisonAnalytics
)

# Konfiguracija stranice
st.set_page_config(
    page_title="Quahwa Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E4057;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# Inicijalizacija session state
@st.cache_data
def load_data_from_folder():
    """Učitava sve podatke sa cachingom iz data/ foldera."""
    # Pronađi data folder relativno od ovog fajla
    data_path = Path(__file__).parent.parent / 'data'
    loader = AutoDataLoader(str(data_path))
    df = loader.load_all_racuni()
    summary = loader.get_summary()
    return df, summary

def load_data_from_upload(uploaded_files):
    """Učitava podatke iz upload-ovanih fajlova."""
    dfs = []
    for uploaded_file in uploaded_files:
        df_temp = pd.read_excel(uploaded_file)
        dfs.append(df_temp)
    
    df = pd.concat(dfs, ignore_index=True)
    
    # Konverzija datuma
    df['Datum i Vrijeme'] = pd.to_datetime(df['Datum i Vrijeme'])
    df['Datum'] = df['Datum i Vrijeme'].dt.date
    df['Mjesec'] = df['Datum i Vrijeme'].dt.to_period('M')
    df['Godina'] = df['Datum i Vrijeme'].dt.year
    
    summary = {
        'ukupno_redova': len(df),
        'broj_fajlova': len(uploaded_files),
        'datum_od': df['Datum i Vrijeme'].min(),
        'datum_do': df['Datum i Vrijeme'].max(),
        'fajlovi': [f.name for f in uploaded_files]
    }
    
    return df, summary

# Naslov
st.markdown('<div class="main-header">☕ QUAHWA ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

# Učitavanje podataka - uvijek pokušaj učitati iz data/ foldera
with st.spinner('📂 Učitavam podatke...'):
    try:
        df, data_summary = load_data_from_folder()
        data_loaded = True
    except Exception as e:
        st.error(f"❌ Greška pri učitavanju: {str(e)}")
        data_loaded = False

if data_loaded:
    # Sidebar info i filteri
    with st.sidebar:
        st.header("ℹ️ Informacije o Podacima")
        st.success(f"✅ Učitano {data_summary['ukupno_redova']:,} redova")
        st.info(f"""
        **Period:** {data_summary['datum_od'].strftime('%d.%m.%Y')} - {data_summary['datum_do'].strftime('%d.%m.%Y')}
        
        **Fajlovi:** {data_summary['broj_fajlova']}
        """)
        
        for file in data_summary['fajlovi']:
            st.text(f"  • {file}")
        
        st.divider()
        st.header("🔍 Globalni Filteri")
        
        # GODINE - glavni filter
        available_years = sorted(df['Godina'].unique())
        
        st.subheader("📅 Godina/Godine")
        
        # Odabir jedne ili više godina
        year_mode = st.radio(
            "Način prikaza:",
            ["Pojedinačna godina", "Usporedba godina", "Sve godine"],
            horizontal=True
        )
        
        if year_mode == "Pojedinačna godina":
            selected_years = [st.selectbox("Odaberi godinu:", available_years, index=len(available_years)-1)]
            comparison_mode = False
        elif year_mode == "Usporedba godina":
            selected_years = st.multiselect(
                "Odaberi godine za usporedbu:",
                available_years,
                default=available_years[-2:] if len(available_years) >= 2 else available_years
            )
            comparison_mode = True
        else:  # Sve godine
            selected_years = available_years
            comparison_mode = False
        
        # Filtriraj podatke po godinama
        df_filtered = df[df['Godina'].isin(selected_years)]
        
        st.divider()
        
        # Dodatni filteri
        st.subheader("🎯 Dodatni Filteri")
        
        # Mjesec filter (opciono)
        if st.checkbox("Filtriraj po mjesecu", value=False):
            selected_months = st.multiselect(
                "Odaberi mjesece:",
                range(1, 13),
                format_func=lambda x: ['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj', 'Lipanj',
                                       'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac'][x-1]
            )
            if selected_months:
                df_filtered = df_filtered[df_filtered['Mjesec'].isin(selected_months)]
        
        # Lokal filter (opciono)
        if 'Lokal' in df_filtered.columns and df_filtered['Lokal'].nunique() > 1:
            if st.checkbox("Filtriraj po lokalu", value=False):
                selected_locations = st.multiselect(
                    "Odaberi lokale:",
                    df_filtered['Lokal'].unique()
                )
                if selected_locations:
                    df_filtered = df_filtered[df_filtered['Lokal'].isin(selected_locations)]
        
        st.divider()
        st.caption(f"📊 Prikazano: **{len(df_filtered):,}** redova")
        st.caption(f"🗓️ Godine: **{', '.join(map(str, selected_years))}**")
    
    # Inicijalizacija analytics objekata
    fin_analytics = FinancialAnalytics(df_filtered)
    sales_analytics = SalesAnalytics(df_filtered)
    time_analytics = TimeAnalytics(df_filtered)
    loc_analytics = LocationAnalytics(df_filtered)
    cust_analytics = CustomerAnalytics(df_filtered)
    comp_analytics = ProductComparisonAnalytics(df_filtered)
    
    # TABS
    tabs = st.tabs([
        "📊 Executive",
        "💰 Financije",
        "🛒 Prodaja",
        "⏰ Vrijeme",
        "📅 Usporedbe",
        "🏪 Lokacije",
        "👥 Kupci",
        "📈 Trendovi",
        "📋 ABC Analiza",
        "📄 Izvještaji"
    ])
    
    # TAB 1: EXECUTIVE DASHBOARD
    with tabs[0]:
        st.header("📊 Executive Dashboard")
        
        # Ako je odabrana više godina, prikaži usporedbu
        if len(selected_years) > 1 and comparison_mode:
            st.subheader("📊 Usporedba Godina - Ključni Pokazatelji")
            
            # KPI usporedba po godinama
            yearly_kpis = []
            for year in selected_years:
                df_year = df_filtered[df_filtered['Godina'] == year]
                year_analytics = FinancialAnalytics(df_year)
                year_kpis = year_analytics.get_kpi_metrics()
                year_kpis['Godina'] = year
                yearly_kpis.append(year_kpis)
            
            # Prikaz u kolonama
            cols = st.columns(len(selected_years))
            for idx, year_data in enumerate(yearly_kpis):
                with cols[idx]:
                    st.markdown(f"### {year_data['Godina']}")
                    st.metric("💰 Promet", f"{year_data['ukupan_promet']:,.0f} EUR")
                    st.metric("🧾 Računi", f"{year_data['broj_računa']:,}")
                    st.metric("💵 Pros. Račun", f"{year_data['prosječan_račun']:.2f} EUR")
                    st.metric("📦 Količina", f"{year_data['ukupna_količina']:,.0f}")
            
            # Grafikon usporedbe prometa po godinama
            st.divider()
            yearly_revenue = df_filtered.groupby('Godina')['Ukupno'].sum().reset_index()
            yearly_revenue.columns = ['Godina', 'Promet']
            yearly_revenue = yearly_revenue.sort_values('Godina')
            
            # Izračunaj YoY promjene
            yearly_revenue['YoY_promjena%'] = yearly_revenue['Promet'].pct_change() * 100
            
            n_godina = len(yearly_revenue)
            total_all = yearly_revenue['Promet'].sum()
            
            fig = go.Figure(data=[
                go.Bar(x=yearly_revenue['Godina'].astype(str), 
                      y=yearly_revenue['Promet'],
                      text=yearly_revenue.apply(
                          lambda x: f"{x['Promet']:,.0f} EUR<br>({x['YoY_promjena%']:+.1f}% YoY)" 
                          if pd.notna(x['YoY_promjena%']) else f"{x['Promet']:,.0f} EUR",
                          axis=1
                      ),
                      textposition='outside',
                      marker_color='lightblue')
            ])
            fig.update_layout(
                title=f'Usporedba Ukupnog Prometa po Godinama | n={n_godina} god., Ukupno={total_all:,.0f} EUR',
                xaxis_title='Godina',
                yaxis_title='Promet (EUR)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Mjesečni trend kroz godine
            st.subheader("📈 Mjesečni Trend - Usporedba Godina")
            monthly_data = df_filtered.groupby(['Godina', 'Mjesec'])['Ukupno'].sum().reset_index()
            
            # Dodaj statistiku
            mjesec_names = {1:'Siječanj', 2:'Veljača', 3:'Ožujak', 4:'Travanj', 5:'Svibanj', 6:'Lipanj',
                          7:'Srpanj', 8:'Kolovoz', 9:'Rujan', 10:'Listopad', 11:'Studeni', 12:'Prosinac'}
            
            fig = go.Figure()
            for year in selected_years:
                year_data = monthly_data[monthly_data['Godina'] == year]
                fig.add_trace(go.Scatter(
                    x=year_data['Mjesec'],
                    y=year_data['Ukupno'],
                    name=str(year),
                    mode='lines+markers',
                    text=year_data['Ukupno'].apply(lambda x: f'{x/1000:.0f}k EUR'),
                    textposition='top center'
                ))
            
            fig.update_layout(
                title='Mjesečni Promet - Usporedba po Godinama (svi mjeseci od 1-12)',
                xaxis_title='Mjesec',
                yaxis_title='Promet (EUR)',
                height=450,
                hovermode='x unified',
                xaxis=dict(tickmode='linear', tick0=1, dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            
        else:
            # Pojedinačna godina ili sve godine zajedno
            selected_year = selected_years[0] if len(selected_years) == 1 else "Sve"
            st.subheader(f"📊 Pregled - Godina {selected_year}")
            
            kpis = fin_analytics.get_kpi_metrics()
            
            # KPI Metrike
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Ukupan Promet", f"{kpis['ukupan_promet']:,.2f} EUR")
            with col2:
                st.metric("🧾 Broj Računa", f"{kpis['broj_računa']:,}")
            with col3:
                st.metric("💵 Prosječan Račun", f"{kpis['prosječan_račun']:.2f} EUR")
            with col4:
                st.metric("📦 Ukupna Količina", f"{kpis['ukupna_količina']:,.0f}")
            
            st.divider()
            
            # Mjesečni trend za odabranu godinu/godine
            if len(selected_years) == 1:
                st.subheader(f"📈 Mjesečni Trend - {selected_years[0]}")
                monthly_metrics = fin_analytics.get_monthly_metrics()
                
                # Dodaj imena mjeseci
                month_names = ['Sij', 'Velj', 'Ožu', 'Tra', 'Svi', 'Lip', 
                              'Srp', 'Kol', 'Ruj', 'Lis', 'Stu', 'Pro']
                monthly_metrics['Mjesec_naziv'] = monthly_metrics['Mjesec'].apply(
                    lambda x: month_names[x-1] if 1 <= x <= 12 else str(x)
                )
                
                n_mj = len(monthly_metrics)
                promet_avg = monthly_metrics['Promet'].mean()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=monthly_metrics['Mjesec_naziv'],
                    y=monthly_metrics['Promet'],
                    mode='lines+markers',
                    name='Promet',
                    line=dict(color='blue', width=3),
                    text=monthly_metrics['Promet'].apply(lambda x: f'{x/1000:.0f}k'),
                    textposition='top center'
                ))
                
                # Dodaj prosječnu liniju
                fig.add_hline(y=promet_avg, line_dash="dash", line_color="gray",
                             annotation_text=f"Prosjek: {promet_avg:,.0f} EUR",
                             annotation_position="right")
                
                fig.update_layout(
                    title=f'Mjesečni Promet - {selected_years[0]} | n={n_mj} mj., μ={promet_avg:,.0f} EUR',
                    xaxis_title='Mjesec',
                    yaxis_title='Promet (EUR)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top 5 artikala
                st.subheader("🏆 Top 5 Artikala po Prometu")
                top5 = sales_analytics.get_top_products(5)
                
                total_top5 = top5['Promet'].sum()
                total_all_prod = df_filtered['Ukupno'].sum()
                top5_share = (total_top5 / total_all_prod * 100) if total_all_prod > 0 else 0
                
                fig = go.Figure(data=[
                    go.Bar(x=top5['Artikl'], y=top5['Promet'],
                          text=top5['Promet'].apply(lambda x: f'{x:,.0f} EUR'),
                          textposition='outside')
                ])
                fig.update_layout(
                    title=f"Top 5 = {top5_share:.1f}% ukupnog prometa",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Promet po prodajnim grupama
                st.subheader("📊 Po Prodajnim Grupama")
                categories = sales_analytics.get_product_categories()
                
                n_cat = len(categories)
                
                fig = px.pie(categories, values='Promet', names='Prodajna_grupa',
                            title=f"Distribucija Prometa | n={n_cat} grupa")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

    
    # TAB 2: FINANCIJSKA ANALIZA
    with tabs[1]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"💰 Financijska Analiza - {year_text}")
        
        # Dohvati KPIs za ovaj tab
        kpis = fin_analytics.get_kpi_metrics()
        
        # Struktura prihoda
        revenue_struct = fin_analytics.get_revenue_structure()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ukupan Promet", f"{revenue_struct['ukupno']:,.2f} EUR",
                     help=f"Ukupan promet. n={revenue_struct['n']:,} transakcija")
        with col2:
            st.metric("Neto Promet", f"{revenue_struct['neto']:,.2f} EUR",
                     delta=f"{revenue_struct['neto_dio%']:.1f}% od Ukupno",
                     help=f"Neto promet = {revenue_struct['neto_dio%']:.1f}% ukupnog prometa")
        with col3:
            st.metric("Popusti", f"{revenue_struct['popusti']:,.2f} EUR",
                     delta=f"-{revenue_struct['popust%']:.1f}%",
                     help=f"Popusti kao postotak od Neto+Popusti")

        
        st.divider()
        
        # Mjesečni promet
        st.subheader("📊 Mjesečni Promet")
        monthly = fin_analytics.get_monthly_metrics()
        
        # Dodaj statistiku
        promet_mean = monthly['Promet'].mean()
        promet_std = monthly['Promet'].std()
        n_mjeseci = len(monthly)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=monthly['Period'], y=monthly['Promet'], name="Promet (EUR)",
                  text=monthly['Promet'].apply(lambda x: f'{x/1000:.0f}k'),
                  textposition='outside'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=monthly['Period'], y=monthly['Promjena_MoM%'],
                      mode='lines+markers', name="Promjena MoM% (vs prethodni mjesec)", 
                      line=dict(color='red'),
                      text=monthly['Promjena_MoM%'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else ''),
                      textposition='top center'),
            secondary_y=True
        )
        
        fig.update_layout(
            title=f"Mjesečni Promet i Rast (MoM%) | n={n_mjeseci} mjeseci, μ={promet_mean:,.0f} EUR, σ={promet_std:,.0f} EUR",
            height=450
        )
        fig.update_yaxes(title_text="Promet (EUR)", secondary_y=False)
        fig.update_yaxes(title_text="Promjena MoM% (mjesec vs prethodni)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Prikaži tablicu s jasnim oznakama
        st.dataframe(
            monthly[['Period', 'Promet', 'Broj_računa', 'Količina', 'Promjena_MoM%', 'Promjena_YoY%', 'n_transakcija']].style.format({
                'Promet': '{:,.2f} EUR',
                'Broj_računa': '{:,.0f}',
                'Količina': '{:,.0f}',
                'Promjena_MoM%': '{:.1f}%',
                'Promjena_YoY%': '{:.1f}%',
                'n_transakcija': '{:,.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # Načini plaćanja
        if 'načini_plaćanja' in kpis and len(kpis['načini_plaćanja']) > 0:
            st.subheader("💳 Načini Plaćanja")
            payment_df = pd.DataFrame(kpis['načini_plaćanja'].items(),
                                     columns=['Način', 'Promet'])
            
            n_payment = payment_df['Promet'].sum()
            
            fig = px.bar(payment_df, x='Način', y='Promet',
                        text=payment_df['Promet'].apply(lambda x: f'{x:,.0f} EUR'))
            fig.update_traces(textposition='outside')
            fig.update_layout(
                title=f"Promet po Načinu Plaćanja | Ukupno: {n_payment:,.0f} EUR",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela mjesečnih metrika
        st.subheader("📋 Detaljne Mjesečne Metrike")
        st.caption("MoM% = Promjena mjesec vs prethodni mjesec | YoY% = Promjena godina vs prethodna godina (isti mjesec)")
        st.dataframe(
            monthly[['Period', 'Promet', 'Broj_računa', 'Količina', 'Promjena_MoM%', 'Promjena_YoY%', 'n_transakcija']].style.format({
                'Promet': '{:,.2f} EUR',
                'Promjena_MoM%': '{:.1f}%',
                'Promjena_YoY%': '{:.1f}%',
                'Broj_računa': '{:,.0f}',
                'Količina': '{:,.0f}',
                'n_transakcija': '{:,.0f}'
            }),
            hide_index=True,
            use_container_width=True
        )
    
    # TAB 3: ANALIZA PRODAJE
    with tabs[2]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"🛒 Analiza Prodaje - {year_text}")
        
        # Basket metrics
        basket = sales_analytics.get_basket_analysis()
        
        n_racuna = df_filtered['Fiskalni broj računa'].nunique()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Prosječno Stavki po Računu", f"{basket['prosječan_broj_stavki']:.1f}",
                     help=f"n={n_racuna:,} računa")
        with col2:
            st.metric("Prosječna Vrijednost Korpe", f"{basket['prosječna_vrijednost']:.2f} EUR",
                     help=f"Promet / Broj računa | n={n_racuna:,}")
        with col3:
            st.metric("Prosječna Količina po Računu", f"{basket['prosječna_količina']:.1f}",
                     help=f"Ukupna količina / Broj računa")
        
        st.divider()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🏆 Top 20 Proizvoda po Prometu")
            top20 = sales_analytics.get_top_products(20)
            
            total_top20 = top20['Promet'].sum()
            total_promet = df_filtered['Ukupno'].sum()
            share_top20 = (total_top20 / total_promet * 100) if total_promet > 0 else 0
            
            fig = px.bar(top20, y='Artikl', x='Promet', orientation='h',
                        text=top20['Promet'].apply(lambda x: f'{x:,.0f}'),
                        title=f"Top 20 = {share_top20:.1f}% ukupnog prometa")
            fig.update_traces(textposition='outside')
            fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Prodajne Grupe")
            categories = sales_analytics.get_product_categories()
            
            st.dataframe(
                categories[['Prodajna_grupa', 'Promet', 'Udio_u_prometu%']].round(2),
                hide_index=True,
                height=600
            )
        
        st.divider()
        
        # Detaljna tablica svih proizvoda
        st.subheader("📋 Svi Proizvodi - Detaljna Tablica")
        all_products = sales_analytics.get_top_products(1000)  # Svi proizvodi
        st.dataframe(
            all_products.round(2),
            hide_index=True,
            width='stretch',
            height=400
        )
    
    # TAB 4: VREMENSKA ANALIZA
    with tabs[3]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"⏰ Vremenska Analiza - {year_text}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Promet po danima u tjednu
            st.subheader("📅 Promet po Danima u Tjednu")
            daily_pattern = time_analytics.get_daily_pattern()
            
            total_week = daily_pattern['Ukupan_promet'].sum()
            avg_day = daily_pattern['Ukupan_promet'].mean()
            
            fig = px.bar(daily_pattern, x='Dan', y='Ukupan_promet',
                        text=daily_pattern['Ukupan_promet'].apply(lambda x: f'{x:,.0f}'),
                        title=f"Tjedni promet={total_week:,.0f} EUR | μ={avg_day:,.0f} EUR/dan")
            fig.update_traces(textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Promet po satima
            st.subheader("🕐 Promet po Satima")
            hourly_pattern = time_analytics.get_hourly_pattern()
            
            avg_hour = hourly_pattern['Ukupan_promet'].mean()
            peak_hour = hourly_pattern.loc[hourly_pattern['Ukupan_promet'].idxmax(), 'Sat']
            peak_value = hourly_pattern['Ukupan_promet'].max()
            
            fig = px.line(hourly_pattern, x='Sat', y='Ukupan_promet',
                         markers=True,
                         title=f"Peak sat: {peak_hour}h ({peak_value:,.0f} EUR) | μ={avg_hour:,.0f} EUR/h")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap
        st.subheader("🔥 Heatmap - Dan × Sat (Promet u EUR)")
        heatmap_data = time_analytics.get_heatmap_data()
        
        day_names = ['Pon', 'Uto', 'Sri', 'Čet', 'Pet', 'Sub', 'Ned']
        
        total_heatmap = heatmap_data.values.sum()
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=day_names,
            colorscale='Blues',
            text=heatmap_data.values.round(0),
            texttemplate='%{text} EUR',
            textfont={"size":9},
            colorbar=dict(title="Promet (EUR)")
        ))
        fig.update_layout(
            title=f'Promet po Danu i Satu | Ukupno={total_heatmap:,.0f} EUR',
            height=450,
            xaxis_title='Sat',
            yaxis_title='Dan u Tjednu'
        )
        st.plotly_chart(fig, use_container_width=True)

    
    # TAB 5: USPOREDBE PROIZVODA I KATEGORIJA
    with tabs[4]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"📅 Usporedbe Prodaje - {year_text}")
        
        st.markdown("### 📊 Usporedba po Kategorijama Proizvoda")
        
        # Usporedba kategorija mjesečno
        cat_comparison = comp_analytics.compare_categories_monthly()
        
        # Prikaži promet po kategorijama
        st.subheader("Mjesečni Promet po Kategorijama")
        revenue_df = cat_comparison['mjesecni_promet']
        
        # Graf - sve kategorije kroz vrijeme
        n_cat = len(revenue_df.columns)
        
        fig = go.Figure()
        for col in revenue_df.columns:
            fig.add_trace(go.Scatter(
                x=revenue_df.index,
                y=revenue_df[col],
                name=col,
                mode='lines+markers'
            ))
        fig.update_layout(
            title=f'Trend Prodaje po Kategorijama | n={n_cat} kategorija',
            xaxis_title='Mjesec (Period)',
            yaxis_title='Promet (EUR)',
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tablica sa % promjenama
        st.subheader("% Promjena Prometa Mjesec-na-Mjesec (MoM%)")
        st.caption("Pozitivne vrijednosti (zeleno) = rast, negativne (crveno) = pad prometa u odnosu na prethodni mjesec")
        pct_change_df = cat_comparison['promjena_promet_%']
        
        # Formatiraj za prikaz
        styled_df = pct_change_df.style.format("{:.1f}%")\
            .background_gradient(cmap='RdYlGn', axis=None, vmin=-50, vmax=50)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        st.markdown("---")
        st.markdown("### 🎯 Usporedba Specifičnih Proizvoda")
        
        # Odabir proizvoda za usporedbu
        all_products = sorted(df_filtered['Artikl'].unique())
        
        # Prikaz top proizvoda kao preporučenih
        top_products_list = df_filtered.groupby('Artikl')['Ukupno'].sum().nlargest(15).index.tolist()
        
        st.write("**Top 15 proizvoda:**", ", ".join(top_products_list[:10]) + "...")
        
        selected_products = st.multiselect(
            "Odaberi proizvode za usporedbu:",
            options=all_products,
            default=top_products_list[:5]
        )
        
        if selected_products:
            prod_comparison = comp_analytics.compare_products_monthly(products=selected_products)
            
            # Graf prometa odabranih proizvoda
            st.subheader(f"Mjesečni Promet - Odabrani Proizvodi (n={len(selected_products)})")
            prod_revenue = prod_comparison['mjesecni_promet']
            
            total_selected = prod_revenue.sum().sum()
            
            fig = go.Figure()
            for col in prod_revenue.columns:
                fig.add_trace(go.Scatter(
                    x=prod_revenue.index,
                    y=prod_revenue[col],
                    name=col,
                    mode='lines+markers'
                ))
            fig.update_layout(
                title=f'Mjesečni Trend | Ukupno={total_selected:,.0f} EUR',
                xaxis_title='Period (Godina-Mjesec)',
                yaxis_title='Promet (EUR)',
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # % promjene MoM
            st.subheader("% Promjena MoM (Mjesec vs Prethodni Mjesec)")
            prod_pct_change = prod_comparison['promjena_promet_%']
            
            styled_prod = prod_pct_change.style.format("{:.1f}%")\
                .background_gradient(cmap='RdYlGn', axis=None, vmin=-50, vmax=50)
            st.dataframe(styled_prod, use_container_width=True, height=400)
        
        st.markdown("---")
        st.markdown("### 🚀 Proizvodi s Najvećim Rastom i Padom")
        
        growers_decliners = comp_analytics.top_growers_and_decliners(period='M')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 TOP 10 - Najveći Rast (MoM%)")
            st.caption("Proizvodi s najvećim postotnim rastom mjesec-na-mjesec")
            if not growers_decliners['najveci_rast'].empty:
                growth_df = growers_decliners['najveci_rast']
                # Formatiranje
                styled_growth = growth_df.style.format({
                    'Promjena_%': '{:.1f}%',
                    growth_df.columns[1]: '{:,.0f} EUR',
                    growth_df.columns[2]: '{:,.0f} EUR'
                }).background_gradient(subset=['Promjena_%'], cmap='Greens')
                st.dataframe(styled_growth, use_container_width=True, height=400)
        
        with col2:
            st.subheader("📉 TOP 10 - Najveći Pad (MoM%)")
            st.caption("Proizvodi s najvećim postotnim padom mjesec-na-mjesec")
            if not growers_decliners['najveci_pad'].empty:
                decline_df = growers_decliners['najveci_pad']
                styled_decline = decline_df.style.format({
                    'Promjena_%': '{:.1f}%',
                    decline_df.columns[1]: '{:,.0f} EUR',
                    decline_df.columns[2]: '{:,.0f} EUR'
                }).background_gradient(subset=['Promjena_%'], cmap='Reds_r')
                st.dataframe(styled_decline, use_container_width=True, height=400)
        
        st.markdown("---")
        st.markdown("### 📆 Usporedba Godina (Year-over-Year - isti mjesec)")
        st.caption("Usporedit ćemo isti mjesec kroz različite godine da vidimo YoY promjene")
        
        # Odabir mjeseca za year-over-year usporedbu
        month_names = ['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj', 'Lipanj',
                      'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac']
        
        selected_month_name = st.selectbox("Odaberi mjesec za usporedbu:", month_names, index=0)
        selected_month_num = month_names.index(selected_month_name) + 1
        
        yoy_comparison = comp_analytics.year_over_year_comparison(selected_month_num)
        
        if not yoy_comparison['promet_po_godinama'].empty:
            st.subheader(f"Promet po Kategorijama - {selected_month_name} (svih godina)")
            yoy_revenue = yoy_comparison['promet_po_godinama']
            
            n_years_yoy = len(yoy_revenue.columns)
            
            # Bar chart usporedbe
            fig = go.Figure()
            for col in [c for c in yoy_revenue.columns if c != 'Promjena_%']:
                fig.add_trace(go.Bar(
                    name=str(col),
                    x=yoy_revenue.index,
                    y=yoy_revenue[col]
                ))
            fig.update_layout(
                barmode='group',
                title=f'Usporedba {selected_month_name} kroz n={n_years_yoy} godina',
                xaxis_title='Kategorija',
                yaxis_title='Promet (EUR)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tablica s promjenama
            if 'Promjena_%' in yoy_revenue.columns:
                st.subheader("% Promjena YoY (Year-over-Year)")
                st.caption("Promjena između najnovije i prethodne godine za isti mjesec")
                styled_yoy = yoy_revenue.style.format({
                    col: '{:,.0f} EUR' for col in yoy_revenue.columns if col != 'Promjena_%'
                } | {'Promjena_%': '{:.1f}%'})\
                    .background_gradient(subset=['Promjena_%'], cmap='RdYlGn', vmin=-50, vmax=50)
                st.dataframe(styled_yoy, use_container_width=True)
    
    # TAB 6: LOKACIJE
    with tabs[5]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"🏪 Analiza po Lokalu - {year_text}")
        
        # Performanse po lokalu
        loc_perf = loc_analytics.get_location_performance()
        if not loc_perf.empty:
            st.subheader("📍 Performanse po Lokalu")
            st.dataframe(loc_perf.round(2), hide_index=True, width='stretch')
        
        # Performanse po blagajni
        cashier_perf = loc_analytics.get_cashier_performance()
        if not cashier_perf.empty:
            st.subheader("🖥️ Performanse po Blagajni")
            
            fig = px.bar(cashier_perf, x='Blagajna', y='Promet',
                        text=cashier_perf['Promet'].apply(lambda x: f'{x:,.0f}'))
            fig.update_traces(textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(cashier_perf.round(2), hide_index=True, width='stretch')
        
        # Performanse osoblja
        staff_perf = loc_analytics.get_staff_performance()
        if not staff_perf.empty:
            st.subheader("👤 Performanse Osoblja")
            st.dataframe(staff_perf.head(20).round(2), hide_index=True, width='stretch', height=400)
    
    # TAB 7: KUPCI
    with tabs[6]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"👥 Analiza Kupaca - {year_text}")
        
        # B2B vs B2C
        segmentation = cust_analytics.get_customer_segmentation()
        
        if segmentation:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏢 B2B (Pravne osobe)")
                st.metric("Promet", f"{segmentation['b2b']['promet']:,.2f} EUR")
                st.metric("Računi", f"{segmentation['b2b']['računi']:,}")
                st.metric("Udio u prometu", f"{segmentation['b2b']['udio%']:.1f}%")
            
            with col2:
                st.subheader("🛍️ B2C (Fizičke osobe)")
                st.metric("Promet", f"{segmentation['b2c']['promet']:,.2f} EUR")
                st.metric("Računi", f"{segmentation['b2c']['računi']:,}")
                st.metric("Udio u prometu", f"{segmentation['b2c']['udio%']:.1f}%")
            
            # Pie chart
            seg_data = pd.DataFrame({
                'Segment': ['B2B', 'B2C'],
                'Promet': [segmentation['b2b']['promet'], segmentation['b2c']['promet']]
            })
            
            fig = px.pie(seg_data, values='Promet', names='Segment',
                        title='Distribucija B2B vs B2C')
            st.plotly_chart(fig, use_container_width=True)
        
        # Top kupci
        top_customers = cust_analytics.get_top_customers(20)
        if not top_customers.empty:
            st.subheader("🏆 Top 20 Kupaca")
            st.dataframe(top_customers.round(2), hide_index=True, width='stretch')
    
    # TAB 8: TRENDOVI
    with tabs[7]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"📈 Trendovi i Prognoze - {year_text}")
        
        daily = fin_analytics.get_daily_metrics()
        
        # Trend sa moving averages
        st.subheader("📊 Dnevni Promet sa Trendovima")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily['Datum'], y=daily['Promet'],
                                mode='lines', name='Dnevni Promet',
                                line=dict(color='lightblue', width=1)))
        fig.add_trace(go.Scatter(x=daily['Datum'], y=daily['Promet_MA7'],
                                mode='lines', name='MA7',
                                line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=daily['Datum'], y=daily['Promet_MA30'],
                                mode='lines', name='MA30',
                                line=dict(color='red', width=2, dash='dash')))
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth metrics
        st.subheader("📊 Growth Metrics")
        monthly = fin_analytics.get_monthly_metrics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(monthly, x='Period', y='Promjena_MoM%',
                        title='Month-over-Month Rast (% promjena mjesec vs prethodni)',
                        color='Promjena_MoM%',
                        color_continuous_scale=['red', 'yellow', 'green'])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Promjena_YoY%' in monthly.columns:
                fig = px.bar(monthly, x='Period', y='Promjena_YoY%',
                            title='Year-over-Year Rast (% promjena godina vs prethodna)',
                            color='Promjena_YoY%',
                            color_continuous_scale=['red', 'yellow', 'green'])
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

    
    # TAB 9: ABC ANALIZA
    with tabs[8]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"📋 ABC/Pareto Analiza - {year_text}")
        
        abc_data = sales_analytics.get_abc_analysis()
        
        # Sažetak
        abc_summary = abc_data.groupby('ABC').agg({
            'Artikl': 'count',
            'Promet': 'sum',
            'Udio%': 'sum'
        }).reset_index()
        abc_summary.columns = ['Kategorija', 'Broj_proizvoda', 'Promet', 'Udio%']
        
        col1, col2, col3 = st.columns(3)
        
        a_cat = abc_summary[abc_summary['Kategorija'] == 'A'].iloc[0] if len(abc_summary[abc_summary['Kategorija'] == 'A']) > 0 else None
        b_cat = abc_summary[abc_summary['Kategorija'] == 'B'].iloc[0] if len(abc_summary[abc_summary['Kategorija'] == 'B']) > 0 else None
        c_cat = abc_summary[abc_summary['Kategorija'] == 'C'].iloc[0] if len(abc_summary[abc_summary['Kategorija'] == 'C']) > 0 else None
        
        with col1:
            if a_cat is not None:
                st.metric("🥇 A Kategorija",
                         f"{int(a_cat['Broj_proizvoda'])} proizvoda",
                         delta=f"{a_cat['Udio%']:.1f}% prometa")
        
        with col2:
            if b_cat is not None:
                st.metric("🥈 B Kategorija",
                         f"{int(b_cat['Broj_proizvoda'])} proizvoda",
                         delta=f"{b_cat['Udio%']:.1f}% prometa")
        
        with col3:
            if c_cat is not None:
                st.metric("🥉 C Kategorija",
                         f"{int(c_cat['Broj_proizvoda'])} proizvoda",
                         delta=f"{c_cat['Udio%']:.1f}% prometa")
        
        # Pareto graf
        st.subheader("📊 Pareto Dijagram")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=abc_data.index[:50], y=abc_data['Promet'][:50], name="Promet"),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=abc_data.index[:50], y=abc_data['Kumulativno%'][:50],
                      mode='lines+markers', name="Kumulativno %",
                      line=dict(color='red', width=2)),
            secondary_y=True
        )
        
        fig.update_layout(title="Pareto Analiza - Top 50 Proizvoda", height=500)
        fig.update_yaxes(title_text="Promet", secondary_y=False)
        fig.update_yaxes(title_text="Kumulativno %", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabele po kategorijama
        selected_cat = st.selectbox("Prikaži kategoriju:", ["A", "B", "C", "Sve"])
        
        if selected_cat == "Sve":
            display_data = abc_data
        else:
            display_data = abc_data[abc_data['ABC'] == selected_cat]
        
        st.dataframe(
            display_data[['Artikl', 'Promet', 'Količina', 'Udio%', 'Kumulativno%', 'ABC']].round(2),
            hide_index=True,
            width='stretch',
            height=400
        )
    
    # TAB 10: IZVJEŠTAJI
    with tabs[9]:
        year_text = ', '.join(map(str, selected_years)) if len(selected_years) <= 3 else f"{len(selected_years)} godina"
        st.header(f"📄 Izvještaji i Export - {year_text}")
        
        st.subheader("📊 Sažeti Izvještaj")
        
        # Generiraj sažetak
        summary_data = {
            'Metrika': [
                'Ukupan Promet',
                'Broj Računa',
                'Prosječan Račun',
                'Ukupna Količina',
                'Broj Artikala',
                'Broj Prodajnih Grupa',
                'Period (dana)'
            ],
            'Vrijednost': [
                f"{kpis['ukupan_promet']:,.2f} EUR",
                f"{kpis['broj_računa']:,}",
                f"{kpis['prosječan_račun']:.2f} EUR",
                f"{kpis['ukupna_količina']:,.0f}",
                f"{data_summary['broj_artikala']:,}",
                f"{df_filtered['Prodajna grupa'].nunique():,}",
                f"{(df_filtered['Datum'].max() - df_filtered['Datum'].min()).days} dana"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df)
        
        st.divider()
        
        # Export opcije
        st.subheader("💾 Export Podataka")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export dnevnih podataka
            daily_export = fin_analytics.get_daily_metrics()
            csv_daily = daily_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Dnevni Promet (CSV)",
                data=csv_daily,
                file_name="dnevni_promet.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export top proizvoda
            top_products_export = sales_analytics.get_top_products(100)
            csv_products = top_products_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Top Proizvodi (CSV)",
                data=csv_products,
                file_name="top_proizvodi.csv",
                mime="text/csv"
            )
        
        with col3:
            # Export ABC analize
            abc_export = sales_analytics.get_abc_analysis()
            csv_abc = abc_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 ABC Analiza (CSV)",
                data=csv_abc,
                file_name="abc_analiza.csv",
                mime="text/csv"
            )

else:
    st.info("📂 Nema pronađenih podataka u data folderu.")
    st.markdown("""
    ### Upute:
    1. Stavi Excel fajlove sa računima u `data/` folder
    2. Fajlovi trebaju imati kolone: Datum i vrijeme, Fiskalni broj računa, Artikl, Ukupno
    3. Refresh stranicu
    """)
