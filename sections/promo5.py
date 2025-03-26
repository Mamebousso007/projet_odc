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
search_input = st.sidebar.text_input("Entrez le numéro de téléphone ou l'e-mail :")


filtered_student = df[
    (df['NDETELEPHONE'].astype(str).str.contains(search_input, case=False, na=False)) |
    (df['EMAIL'].str.contains(search_input, case=False, na=False))
]

# Affichage des résultats
if search_input and not filtered_student.empty:
    st.subheader("Informations")
    student_data = filtered_student.iloc[0]  

    st.markdown(
        f"""
        <div style="background-color: #cfe5f1; padding: 15px; border-radius: 8px; border: 1px solid #ddd;">
            <h4 style="color: #001728;"><center>{student_data['NOM']} {student_data['PRENOM']}</center></h4>
            <ul style="color: #001728;">
                <li><strong>Numéro de Téléphone :</strong> {student_data.get('NDETELEPHONE', 'Non spécifié')}</li>
                <li><strong>E-mail :</strong> {student_data.get('EMAIL', 'Non spécifié')}</li>
                <li><strong>Poste occupé :</strong> {student_data.get('INTITULEPOSTE', 'Non spécifié')}</li>
                <li><strong>Entreprise :</strong> {student_data.get('ENTREPRISES', 'Non spécifiée')}</li>
                <li><strong>Type de contrat :</strong> {student_data.get('TYPEDECONTRAT', 'Non spécifié')}</li>
                <li><strong>Rémunération :</strong> {student_data.get('REMUNERATION', 'Non spécifiée')} FCFA</li>
                <li><strong>Durée du contrat :</strong> {student_data.get('DUREEMOIS', 'Non spécifiée')} Mois</li>
                <li><strong>Statut actuel :</strong> {'En poste' if student_data['STATUTACTUELenposteounon'] == 'OUI' else 'Non en poste'}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    if search_input:
        st.error("Aucun étudiant trouvé.")


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

    # Création du diagramme circulaire complet
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

    # Mise en page pour séparer la légende
    fig.update_layout(
        title=dict(
            text="📈 Répartition des types de contrats",
            font=dict(size=14, color="white", family="Arial"),
            x=0.5,
            xanchor="center"
        ),
        showlegend=True, 
        height=400, width=600, 
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=-0.3,  
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(t=50, b=100),  
    )

    
    st.plotly_chart(fig, use_container_width=True) 

with colo2:
    #Durée Moyenne
    contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
    fig = px.bar(
        contract_duration,
        x=contract_duration.index,
        y=contract_duration.values,
        title="Durée moyenne des contrats par type",
        labels={'x': 'Type de contrat', 'y': 'Durée moyenne (mois)'}
    )
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=14), xanchor="center" ),
        
        height=500, width=500,  # 🔹 Uniformisation
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
    )
    st.plotly_chart(fig, use_container_width=True)

with colo3:
    fig = px.histogram(
        filtered_data,
        x='REMUNERATION',
        nbins=20,  
        title="Distribution des rémunérations ",
        labels={'REMUNERATION': 'Rémunération (FCFA)'},
        color_discrete_sequence=['#FF7F0E'],  
        text_auto=True
    )

    fig.update_traces(
        marker_line_color='white',  
        marker_line_width=1.5,  
        opacity=0.9  
    )

    # Personnalisation du layout
    fig.update_layout(
        title=dict(
            text="📈 Distribution des rémunérations ",
            font=dict(size=14, color="white", family="Arial"), 
            x=0.5,  
            xanchor="center" 
        ),
        xaxis=dict(
            title="Rémunération (FCFA)",  
            titlefont=dict(size=14, color="#333"),  
            tickfont=dict(size=14),
            gridcolor="lightgrey"  
        ),
        yaxis=dict(
            title="Nombre d'apprenants",  
            titlefont=dict(size=16, color="#333"),  
            tickfont=dict(size=14),  
            gridcolor="lightgrey"  
        ),
        plot_bgcolor="white", 
        bargap=0.1, 
        height=400, width=500,
    )

    # Affichage du graphique
    st.plotly_chart(fig, use_container_width=True)


st.divider()

colon1, colon2, colon3 = st.columns(3, gap='large')
with colon1:
        
    # Répartition des postes 
    post_count = filtered_data['INTITULEPOSTE'].value_counts().head(10)  
    fig = px.bar(
        post_count, 
        x=post_count.index, 
        y=post_count.values, 
        title="Top 10 des postes occupés ", 
        labels={'x': 'Postes', 'y': 'Nombre'},
        color=post_count.values, 
        color_continuous_scale='Viridis',
        text=post_count
    )

    fig.update_layout(
        height = 500,
        width = 500

    )
    st.plotly_chart(fig, use_container_width=True)

    company_count = filtered_data['ENTREPRISES'].value_counts()


  
with colon2:
    #st.subheader("📈 Évolution temporelle des apprenants en poste")
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
        

        evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y')
        evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR_FR'].str.capitalize()  # Capitaliser la première lettre
        

        evolution_data = evolution_data.sort_values('MONTH_YEAR')

        fig = px.line(
            evolution_data, 
            x='MONTH_YEAR_FR', 
            y='Nombre', 
            title="Évolution insertion au fil du temps",
            labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
            markers=True
        )
        
        fig.update_traces(text=evolution_data['Nombre'], textposition='top center')

        fig.update_layout(
            xaxis=dict(tickangle=45),
            xaxis_title="Mois et Année",
            yaxis_title="Nombre d'apprenants",
            yaxis=dict(tickformat='d'), 
            height = 500,
            width = 500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")

with colon3:
    
    fig = px.bar(
        x=company_count.index,
        y=company_count.values,
        title="Nombre d'étudiants par entreprise",
        labels={'x': 'Entreprise', 'y': 'Nombre d\'étudiants'},
        text=company_count.values,  
        color_discrete_sequence=px.colors.sequential.Viridis 
    )

    fig.update_traces(
        marker_line_color='white',  
        marker_line_width=1.5,  
        opacity=0.9,  
        textposition="outside"  
    )


    fig.update_layout(
        title=dict(
            text="📈Nombre d'étudiants par entreprise",
            font=dict(size=14, color="white", family="Arial"),
            x=0.5,  
            xanchor="center"
        ),
        xaxis=dict(
            title="Entreprise",
            titlefont=dict(size=16, color="black"),
            tickfont=dict(size=14),
            tickangle=-45,  
            gridcolor="lightgrey"
        ),
        yaxis=dict(
            title="Nombre d'étudiants",
            titlefont=dict(size=16, color="#333"),
            tickfont=dict(size=14),
            gridcolor="lightgrey"
        ),
        plot_bgcolor="white",  
        bargap=0.15,
        height = 600,
        width = 800
    )


    st.plotly_chart(fig, use_container_width=True)






print(df.columns)



heatmap_data = filtered_data.pivot_table(
    index='STRUCTUREDIRECTIONPOLE',
    columns='INTITULEPOSTE',
    values='NOM',  
    aggfunc='count',
    fill_value=0
)


st.divider()
st.subheader("Aperçus des données filtrées")
st.dataframe(filtered_data.head())