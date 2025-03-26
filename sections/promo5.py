import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib as plt
import locale
import plotly.graph_objects as go


#rgement des données

st.set_page_config(
    page_title="Dashboard Suivi Insertion - Sonatel Academy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Couleurs principales */
    :root {
        --primary: #FF6B00;
        --secondary: #001F3F;
        --accent: #4CAF50;
        --background: #f5f5f5;
        --text: #333333;
    }
    
    /* En-tête et styles généraux */
    .main-header {
        background-color: var(--secondary);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        color: white;
    }
    
    /* KPI cards */
    .kpi-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        transition: transform 0.3s;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    
    .kpi-title {
        color: var(--text);
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        color: var(--primary);
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    .kpi-unit {
        color: var(--text);
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    /* Filtres */
    .filter-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .filter-title {
        color: var(--secondary);
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white;
    }
    
    /* Graphiques */
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        height: 100%;
    }
    
    /* Upload section */
    .upload-container {
        background-color: #f8f9fa;
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .upload-container:hover {
        border-color: var(--primary);
    }
    
    /* Tables */
    .dataframe-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Boutons */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #FF8C00;
    }
    
    /* Ajustements divers */
    div[data-testid="stVerticalBlock"] > div:has(.stTabs) {
        gap: 0 !important;
    }
    
    /* Masquer hamburger menu et footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



df = pd.read_excel('SUIVI_GLOBAL_P5.xlsx', engine='openpyxl', skiprows=1)
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Suppression des caractères spéciaux dans les colonnes
    df.columns = df.columns.str.replace('[^a-zA-Z]', '', regex=True)

    # Conversion des colonnes en dates
    df['DATEDENAISSANCE'] = pd.to_datetime(df['DATEDENAISSANCE'], errors='coerce')
    df['DATEDEPRISEDESERVICE'] = pd.to_datetime(df['DATEDEPRISEDESERVICE'], errors='coerce')

    # gerer NaN
    sensitive_columns = [
        'LIEUDENAISSANCE', 
        'SITUATIONSOCIOPROFESSIONNELlinscription', 
        'INTITULEPOSTE', 
        'STRUCTUREDIRECTIONPOLE', 
        'ENTREPRISES', 
        'TYPEDECONTRAT', 
        'STATUTACTUELenposteounon'
    ]
    for col in sensitive_columns:
        if col in df.columns:
            df[col] = df[col]

    columns_fixed = {
        'ADRESSE': 'Non spécifié',
        'CONTACTDURGENCE': 'Non fourni',
        'STATUTMATRIMONIALE': 'Non spécifié',
        'PROFILAGE': 'Non défini',
        'COMMENTAIRE': 'Aucun commentaire',
        'CONTACTENTREPRISE': 'Non précisé'
    }
    for col, value in columns_fixed.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)

    if 'REMUNERATION' in df.columns:
        df['REMUNERATION'] = pd.to_numeric(df['REMUNERATION'], errors='coerce').fillna(0)
    
    if 'DUREEMOIS' in df.columns:
        df['DUREEMOIS'] = df['DUREEMOIS'].fillna(0)

    return df


df = preprocess_data(df)


# st.subheader("📊 SUIVI INSERTION DE LA PROMOTION 5")
px.defaults.template = "plotly_dark"
# En-tête du Dashboard
st.markdown('<div class="main-header"><h1 class="header-title">SUIVI INSERTION DE LA PROMOTION 5</h1><p class="header-subtitle">École du Code - Sonatel Academy</p></div>', unsafe_allow_html=True)


# Utiliser le thème dans vos visualisations
px.defaults.template = "plotly_dark"  

import os

# Chemin relatif pour accéder à styles.css depuis le dossier pages
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown(
    """
    <style>
        .css-18e3th9 {background-color: #1a1a1a;}
        .css-10trblm {color: #ffffff;}
        .css-12ttj6m {color: #ffffff;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Barre de recherche d'étudiant
#st.sidebar.header("Rechercher un étudiant")


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    search_input = st.text_input("🔍 Rechercher", placeholder="Téléphone ou email")

with col2:
    selected_domains = st.multiselect(
            "🎓 Domaine", 
            options=df['DOMAINEFORMATION'].dropna().unique().tolist(),
            default=[]
        )

with col3:
    selected_contracts = st.multiselect(
            "📜 Contrat", 
            options=df['TYPEDECONTRAT'].dropna().unique().tolist(),
            default=[]
        )

with col4:
    selected_companies = st.multiselect(
            "🏢 Entreprise", 
            options=df['ENTREPRISES'].dropna().unique().tolist(),
            default=[]
        )

with col5:
    selected_statuses = st.multiselect(
            "🟢 Statut", 
            options=["En poste", "Non en poste"],
            default=[]
        )

    # Bouton pour appliquer les filtres
st.markdown("<br>", unsafe_allow_html=True)  

# Application des filtres
filtered_data = df.copy()

# Filtre par entreprises
if selected_companies:
    filtered_data = filtered_data[filtered_data['ENTREPRISES'].isin(selected_companies)]

# Filtre par statut
if selected_statuses:
    status_values = ["OUI" if status == "En poste" else "NON" for status in selected_statuses]
    filtered_data = filtered_data[filtered_data['STATUTACTUELenposteounon'].isin(status_values)]

# Filtre par type de contrat
if selected_contracts:
    filtered_data = filtered_data[filtered_data['TYPEDECONTRAT'].isin(selected_contracts)]

# Filtre par domaine de formation
if selected_domains:
    filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'].isin(selected_domains)]
#st.sidebar.image("data/logo.jpg",caption="")



# def kpi():
#     # CSS pour forcer les colonnes à avoir une largeur identique
    
#     # Calcul KPI 
#     avg_salary = filtered_data['REMUNERATION'].mean() if 'REMUNERATION' in filtered_data.columns else 0
#     total_students = len(filtered_data)
#     active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0
#     insertion_rate = (active_students / total_students * 100) if total_students > 0 else 0
#     # Calcul féminisation
#     female_students = len(filtered_data[filtered_data['SEXE'] == 'F']) if 'SEXE' in filtered_data.columns else 0
#     feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0

#     # Configuration de la localisation pour les nombres
#     try:
#         locale.setlocale(locale.LC_ALL, 'French_France.1252')
#     except locale.Error:
#         print("La locale spécifiée n'est pas supportée sur ce système.")

#     # Affichage des KPI avec des colonnes égales
#     col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap='small') 

#     with col1:
#         st.info('Rémunération', icon="💰")
#         avg_salary_formatted = locale.format_string("%.1f", avg_salary, grouping=True)
#         st.metric(label="Moyenne", value=f"{avg_salary_formatted} FCFA")

#     with col2:
#         st.info('Apprenants', icon="🧑‍🎓")
#         st.metric(label="Total", value=f"{total_students:,.0f}")
#     with col3:
#         st.info('En poste', icon="💼")
#         st.metric(label="Total", value=f"{active_students:,.0f}")
#     with col4:
#         st.info('Taux d’insertion', icon="📊")
#         st.metric(label="Taux", value=f"{insertion_rate:.2f} %")
#     with col5:
#         st.info('Taux de féminisation', icon="👩")
#         st.metric(label="Taux", value=f"{feminization_rate:.2f} %")
# # Appliquer le CSS personnalisé
def kpi():
    # CSS pour forcer les colonnes à avoir une largeur identique
    st.markdown(
        """
        <style>
        /* Styles pour les colonnes */
        .stColumns > div {
            width: 100% !important;
            padding: 5px !important;
        }
        
        /* Styles supplémentaires pour les cartes KPI */
        .compact-kpi {
            margin-bottom: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


     # Calcul des KPI 
    avg_salary = filtered_data['REMUNERATION'].mean() if 'REMUNERATION' in filtered_data.columns else 0
    total_students = len(filtered_data)
    active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0
    # insertion_rate = (active_students / total_students * 100) if total_students > 0 else 0

    # Calcul du nombre d'étudiants insérés basé sur la colonne 'STATUT'
    inserted_students = len(filtered_data[filtered_data['STATUT'] == 'Inséré']) if 'STATUT' in filtered_data.columns else 0
    insertion_rate = (inserted_students / total_students * 100) if total_students > 0 else 0

    # Calcul du taux de féminisation
    female_students = len(filtered_data[filtered_data['SEXE'] == 'F']) if 'SEXE' in filtered_data.columns else 0
    feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0

    # Configuration de la localisation pour les nombres
    try:
        locale.setlocale(locale.LC_ALL, 'French_France.1252')
    except locale.Error:
        print("La locale spécifiée n'est pas supportée sur ce système.")

    # Template HTML/CSS pour les KPI
    kpi_template = """
    <div class="compact-kpi" style="
        background-color: {bg_color};
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
        width: 100%;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 14px; font-weight: normal; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 24px; margin-top: 5px;">{value}</div>
    </div>
    """
    
    # Première ligne avec 3 colonnes
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        avg_salary_formatted = locale.format_string("%.2f", avg_salary, grouping=True)
        st.markdown(kpi_template.format(
            bg_color="#F39200", title="Rémunération moyenne", value=f"{avg_salary_formatted} FCFA"),
            unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_template.format(
            bg_color="#005F83", title="Apprenants Suivi", value=total_students),
            unsafe_allow_html=True)

    with col3:
        st.markdown(kpi_template.format(
            bg_color="#00843D", title="Apprenants Inséré", value=inserted_students),
            unsafe_allow_html=True)

    with col4:
        bg_color = "#00843D" if insertion_rate < 50 else "#4CAF50"
        st.markdown(kpi_template.format(
            bg_color=bg_color, title="Taux d'insertion", value=f"{insertion_rate:.2f} %"),
            unsafe_allow_html=True)

    with col5:
        st.markdown(kpi_template.format(
            bg_color="#F39200", title="Taux de féminisation", value=f"{feminization_rate:.2f} %"),
            unsafe_allow_html=True)

#st.subheader("Gestion des apprenants", divider='rainbow')
if "show_form" not in st.session_state:
    st.session_state.show_form = False
    
# if st.button("Ajouter un nouvel apprenant"):
#     st.session_state.show_form = not st.session_state.show_form  # Basculer l'état

if st.session_state.show_form:
    st.write("## Formulaire d'ajout")
    from add_data import *
    add_data() 
kpi()



st.divider()
colo1, colo2, colo3 = st.columns(3, gap="large")

with colo1:
    contract_count = filtered_data['TYPEDECONTRAT'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=contract_count.index,
        values=contract_count.values,
        hole=0,  
        marker=dict(
            colors=px.colors.qualitative.Set2, 
            line=dict(color='white', width=2)
        ),
        textinfo='percent',  
        insidetextorientation='radial',
        hoverinfo='label+percent+value'
    )])

    fig.update_layout(
        title=dict(
            text="📈 Répartition des types de contrats",
            font=dict(size=14, color="white", family="Arial"),
            x=0.5,
            xanchor="center"
        ),
        showlegend=True, 
        height=400, 
        width=700, 
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=-0.3,  
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(t=50, b=100, l=50, r=50),  
    )

    st.plotly_chart(fig, use_container_width=True) 

with colo2:
    contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
    fig = px.bar(
        contract_duration,
        x=contract_duration.index,
        y=contract_duration.values,
        title="📈 Durée moyenne des contrats par type",
        labels={'x': '', 'y': 'Durée moyenne (mois)'}
    )
    fig.update_layout(
        title=dict(
            text="📈 Durée moyenne des contrats par type",
            font=dict(size=14, color="white", family="Arial"),
            x=0.5, 
            xanchor="center"
        ),
        height=500, 
        width=700,  
        xaxis=dict(
            showgrid=False,
            tickangle=-45,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=False,
            title="Durée moyenne (mois)",
            gridcolor="lightgrey"
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

with colo3:
    fig = px.histogram(
        filtered_data,
        x='REMUNERATION',
        nbins=20,  
        title="📈 Distribution des rémunérations",
        labels={'REMUNERATION': 'Rémunération (FCFA)', 'count': "Nombre d'apprenants"},
        color_discrete_sequence=['#FF7F0E'],  
        text_auto=True
    )

    fig.update_traces(
        marker_line_color='white',  
        marker_line_width=1.5,  
        opacity=0.9  
    )

    fig.update_layout(
        title=dict(
            text="📈 Distribution des rémunérations",
            font=dict(size=14, color="white", family="Arial"), 
            x=0.5,  
            xanchor="center" 
        ),
        xaxis=dict(
            title="Rémunération (FCFA)",  
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="Nombre d'apprenants",  
            showgrid=False,
            gridcolor="lightgrey"
        ),
        height=400, 
        width=700,
        margin=dict(l=50, r=50, t=50, b=50),
        bargap=0.1
    )

    st.plotly_chart(fig, use_container_width=True)
st.divider()

# CSS pour uniformiser les styles
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Création des colonnes avec espacement
colon1, colon2, colon3 = st.columns(3, gap='large')

with colon1:
    st.markdown('<p class="title">Top 10 des postes occupés</p>', unsafe_allow_html=True)

    post_count = filtered_data['INTITULEPOSTE'].value_counts().head(10)
    fig = px.bar(
        post_count, 
        x=post_count.index, 
        y=post_count.values, 
        labels={'x': 'Postes', 'y': 'Nombre'},
        color=post_count.values, 
        color_continuous_scale='Viridis',
        text=post_count
    )

    fig.update_layout(
        height=400,
        width=500
    )
    st.plotly_chart(fig, use_container_width=True)

with colon2:
    st.markdown('<p class="title">Évolution insertion au fil du temps</p>', unsafe_allow_html=True)

    if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
        time_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'].notna()]
        time_data = time_data[time_data['STATUTACTUELenposteounon'] == 'OUI']

        time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
        evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
        evolution_data['MONTH_YEAR'] = pd.to_datetime(evolution_data['MONTH_YEAR'].astype(str))

        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8') 
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'fra')  
            except locale.Error:
                st.warning("Impossible de configurer la locale en français. Les mois resteront en anglais.")

        evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y').str.capitalize()

        evolution_data = evolution_data.sort_values('MONTH_YEAR')

        fig = px.line(
            evolution_data, 
            x='MONTH_YEAR_FR', 
            y='Nombre', 
            labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': "Nombre d'apprenants"},
            markers=True
        )
        
        fig.update_traces(text=evolution_data['Nombre'], textposition='top center')

        fig.update_layout(
            xaxis=dict(tickangle=45),
            xaxis_title="Mois et Année",
            yaxis_title="Nombre d'apprenants",
            yaxis=dict(tickformat='d'),
            height=400,
            width=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")

with colon3:
    st.markdown('<p class="title">Données filtrées</p>', unsafe_allow_html=True)
    st.dataframe(filtered_data, height=400, width=700)


st.divider()

print(df.columns)


heatmap_data = filtered_data.pivot_table(
    index='STRUCTUREDIRECTIONPOLE',
    columns='INTITULEPOSTE',
    values='NOM',  
    aggfunc='count',
    fill_value=0
)

# 📌 Disposer les éléments sur la même ligne
col1, col2 = st.columns([1, 1])  # Ajuste les proportions si nécessaire

col1, col2 = st.columns(2)

with col1:
    # 🔽 Slider pour définir le seuil
    seuil = st.slider("", min_value=1, max_value=20, value=2)

if 'ENTREPRISES' in filtered_data.columns:
    structure_count = filtered_data['ENTREPRISES'].value_counts()

    # Séparer les entreprises principales et secondaires
    principales = structure_count[structure_count >= seuil]
    secondaires = structure_count[structure_count < seuil]

    with col1:
        # 📈 Graphique des principales entreprises
        if not principales.empty:
            fig = px.bar(
                x=principales.index,
                y=principales.values,
                title=f"Principales entreprises (≥ {seuil} bénéficiaires)",
                labels={'x': 'Structure', 'y': 'Nombre de bénéficiaires insérés'},
                text=principales.values
            )
            fig.update_traces(marker_color="#FF6600", textposition='outside')
            st.plotly_chart(fig, use_container_width=True)  # Largeur ajustée

    with col2:
        # 📜 Tableau téléchargeable pour les entreprises secondaires
        if not secondaires.empty:
            df_secondaires = pd.DataFrame({
                'Entreprise': secondaires.index,
                'Nombre de bénéficiaires': secondaires.values
            }).sort_values('Nombre de bénéficiaires', ascending=False)

            st.dataframe(df_secondaires, use_container_width=True, height=500)  # Largeur ajustée

            # 📂 Bouton de téléchargement
            # csv = df_secondaires.to_csv(index=False).encode('utf-8')
            # st.download_button(
            #     label="📥 Télécharger le tableau",
            #     data=csv,
            #     file_name="entreprises_secondaires.csv",
            #     mime="text/csv"
            # )

else:
    st.error("❌ La colonne 'ENTREPRISES' est absente des données filtrées.")
st.divider()
