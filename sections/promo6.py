import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale
import gspread
from google.oauth2.service_account import Credentials
import os
import sys
from google.oauth2 import service_account


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

def error_callback():
    _, exc, tb = sys.exc_info()
    st.error(f"Une erreur s'est produite: {exc}")
    st.code(str(exc))


SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# SERVICE_ACCOUNT_FILE = "eighth-jigsaw-446022-r0-638d8f86d788.json"
# SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1oNQc5xQO4bRj72v50po6Qg95jZzXp3VhBxyi7edx_ZY"
credentials = Credentials.from_service_account_info(st.secrets["google"], scopes=SCOPE)

#SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/your_spreadsheet_id/edit#gid=0"
#SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1oNQc5xQO4bRj72v50po6Qg95jZzXp3VhBxyi7edx_ZY"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1T-EWMgcFa74OrLFFlFL_eyoQpRDLtoDMeYNyocDBdZg"

# Modified to use a lower TTL and add a last_refreshed attribute
@st.cache_data(ttl=5) 
def load_data_from_excel(uploaded_file, promo_name):
    try:
        df = pd.read_excel(uploaded_file)
        df = preprocess_data(df)
        st.session_state.promos_data[promo_name] = df
        st.session_state.current_promo = promo_name
        return True
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier: {e}")
        return False 
def charger_donnees():
    try:
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(SPREADSHEET_URL).worksheet("GLOBAL")
        data = sheet.get_all_records(head=3)
        
        if not data:
            st.warning("Aucune donnée trouvée dans la feuille Google Sheets.")
            return pd.DataFrame()

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return pd.DataFrame()
    
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
        
    try:
        # Filtrage des domaines HACKEUSE et AWS
        if 'DOMAINEFORMATION' in df.columns:
            df['DOMAINEFORMATION'] = df['DOMAINEFORMATION'].astype(str).str.strip().str.upper()
            df = df[~df['DOMAINEFORMATION'].isin(['HACKEUSE', 'AWS'])]
        
        # Suppression des caractères spéciaux dans les noms de colonnes
        df.columns = df.columns.str.replace(r'[^a-zA-Z]', '', regex=True)

        # Colonnes à convertir en chaîne
        columns_str = {'CIN', 'NDETELEPHONE', 'EMAIL'} & set(df.columns)
        for col in columns_str:
            df[col] = df[col].astype(str)

        # Fonction pour traiter les dates au format texte français
        def preprocess_date(date_val):
            if pd.isna(date_val):
                return date_val
                
            # Convertir en chaîne si ce n'est pas déjà le cas
            date_str = str(date_val)
            
            # Dictionnaire de conversion des mois en français vers des nombres
            mois_fr_to_num = {
                'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
                'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
                'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
            }
            
            # Convertir le mois en texte en nombre
            date_parts = date_str.lower().split()
            if len(date_parts) == 3:
                try:
                    jour = date_parts[0].zfill(2)
                    mois = mois_fr_to_num.get(date_parts[1], '01')
                    annee = date_parts[2]
                    return f"{jour}/{mois}/{annee}"
                except:
                    return date_str
            
            return date_str

        # Colonnes à convertir en dates
        columns_date = {'DATEDENAISSANCE', 'DATEDEPRISEDESERVICE'} & set(df.columns)
        for col in columns_date:
            # Prétraiter les dates au format texte français
            df[f"{col}_TEMP"] = df[col].apply(preprocess_date)
            
            # Essayer différents formats de date
            df[col] = pd.to_datetime(df[f"{col}_TEMP"], format='%d/%m/%Y', errors='coerce')
            
            # Si certaines dates n'ont pas été converties, essayer d'autres formats
            if df[col].isna().any():
                mask_nat = df[col].isna()
                try:
                    # Format JJ/MM/YY
                    temp_dates = pd.to_datetime(df.loc[mask_nat, f"{col}_TEMP"], format='%d/%m/%y', errors='coerce')
                    df.loc[mask_nat, col] = temp_dates
                except:
                    pass
            
            # Supprimer la colonne temporaire
            df = df.drop(f"{col}_TEMP", axis=1, errors='ignore')
            
            # Appliquer la correction d'année si nécessaire
            df[col] = df[col].apply(lambda x: correct_year(x) if not pd.isna(x) else x)
            df[col] = df[col].fillna(pd.NaT)

        # Colonnes sensibles (ne pas remplacer les valeurs manquantes)
        sensitive_columns = {
            'INTITULEPOSTE', 'LIEUDENAISSANCE', 'SITUATIONSOCIOPROFESSIONNELlinscription',
            'STRUCTUREDIRECTIONPOLE', 'ENTREPRISES', 'TYPEDECONTRAT', 'STATUTACTUELenposteounon'
        } & set(df.columns)
        # Pas de remplissage des NaN pour ces colonnes

        # Colonnes avec valeurs par défaut
        columns_fixed = {
            'ADRESSE': 'Non spécifié', 'CONTACTDURGENCE': 'Non fourni', 
            'STATUTMATRIMONIALE': 'Non spécifié', 'PROFILAGE': 'Non défini', 
            'COMMENTAIRE': 'Aucun commentaire', 'CONTACTENTREPRISE': 'Non précisé'
        }
        for col, value in columns_fixed.items():
            if col in df.columns:
                df[col] = df[col].fillna(value)

        # Colonnes numériques : conversion et remplissage avec 0
        columns_numeric = {'REMUNERATION', 'DUREEMOIS'} & set(df.columns)
        for col in columns_numeric:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du prétraitement des données : {e}")
        return df  # Retour du DataFrame original en cas d'erreur


# Fonction pour corriger les années incorrectes
def correct_year(date):
    """Corrige les années incorrectes (ex: 25 devient 2025 au lieu de 1925)"""
    if pd.isna(date):
        return date
    if date.year < 2000:
        return date.replace(year=date.year + 100)
    return date

# Fonction pour ajouter un nouvel étudiant
def add_student(new_data):
    try:
        # Charger les identifiants depuis st.secrets et se connecter à Google Sheets
        credentials = Credentials.from_service_account_info(st.secrets["google"], scopes=SCOPE)
        
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(SPREADSHEET_URL).worksheet("GLOBAL")
        
        # Ajouter une nouvelle ligne
        sheet.append_row(list(new_data.values()))
        
        st.success("Étudiant ajouté avec succès!")
        # Actualiser les données explicitement
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'ajout de l'étudiant: {e}")
        return False
    
# Fonction pour le formulaire d'ajout d'étudiant
def add_data():
    with st.form("new_student_form"):
        st.write("Entrez les informations de l'étudiant")
        
        # Informations personnelles
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            sexe = st.selectbox("Sexe", options=["F", "M"])
            date_naissance = st.date_input("Date de naissance")
            telephone = st.text_input("Numéro de téléphone")
        
        with col2:
            email = st.text_input("Email")
            cin = st.text_input("CIN")
            domaine_formation = st.text_input("Domaine de formation")
            adresse = st.text_input("Adresse")
        
        # Informations professionnelles
        st.write("Informations professionnelles")
        col3, col4 = st.columns(2)
        with col3:
            entreprise = st.text_input("Entreprise")
            poste = st.text_input("Intitulé du poste")
            type_contrat = st.selectbox("Type de contrat", options=["CDI", "CDD", "Stage", "Freelance", "Autre"])
            date_service = st.date_input("Date de prise de service")
        
        with col4:
            remuneration = st.number_input("Rémunération (FCFA)", min_value=0)
            duree_mois = st.number_input("Durée (mois)", min_value=0)
            statut = st.selectbox("Statut", options=["INSERE", "NON INSERE"])
            statut_poste = st.selectbox("En poste actuellement ?", options=["OUI", "NON"])
            structure = st.text_input("Structure/Direction/Pôle")
        
        submitted = st.form_submit_button("Ajouter l'étudiant")
        
        if submitted:
            # Créer un dictionnaire avec les données
            new_student = {
                "NOM": nom,
                "PRENOM": prenom,
                "SEXE": sexe,
                "DATEDENAISSANCE": date_naissance.strftime("%Y-%m-%d"),
                "NDETELEPHONE": telephone,
                "EMAIL": email,
                "CIN": cin,
                "DOMAINEFORMATION": domaine_formation,
                "ADRESSE": adresse,
                "ENTREPRISES": entreprise,
                "INTITULEPOSTE": poste,
                "TYPEDECONTRAT": type_contrat,
                "DATEDEPRISEDESERVICE": date_service.strftime("%Y-%m-%d"),
                "REMUNERATION": remuneration,
                "DUREEMOIS": duree_mois,
                "STATUT": statut,
                "STATUTACTUELenposteounon": statut_poste,
                "STRUCTUREDIRECTIONPOLE": structure
            }
            
            # Ajouter l'étudiant
            success = add_student(new_student)
            if success:
                # Vider les champs après l'ajout
                st.experimental_rerun()

# Fonction pour les KPIs


def kpi(filtered_data):
    # Vérifier si le DataFrame est vide
    if filtered_data.empty:
        st.warning("Aucune donnée disponible pour afficher les KPI.")
        return
        
    # CSS pour les colonnes et les cartes KPI
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
    inserted_students_data = filtered_data[filtered_data['STATUT'] == 'INSERE'] if 'STATUT' in filtered_data.columns else pd.DataFrame()

    # Calculer la rémunération moyenne uniquement pour les étudiants insérés
    avg_salary = inserted_students_data['REMUNERATION'].mean() if not inserted_students_data.empty else 0

    total_students = len(filtered_data)
    active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0

    # nombre d'étudiants insérés 
    inserted_students = len(filtered_data[filtered_data['STATUT'] == 'INSERE']) if 'STATUT' in filtered_data.columns else 0
    insertion_rate = (inserted_students / total_students * 100) if total_students > 0 else 0

    # Calcul du taux de féminisation
    female_students = len(filtered_data[filtered_data['SEXE'] == 'F']) if 'SEXE' in filtered_data.columns else 0
    feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0

    # Configuration de la localisation pour les nombres
    try:
        locale.setlocale(locale.LC_ALL, 'French_France.1252')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        except locale.Error:
            print("La locale spécifiée n'est pas supportée sur ce système.")

    # Template HTML/CSS pour les KPI (version compacte)
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
    
    # Disposition en deux lignes avec 3 colonnes chacune
    # Première ligne avec 3 KPIs
    # Disposition en une seule ligne avec 6 colonnes
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

    # with col6:
    #     active_rate = (active_students / total_students * 100) if total_students > 0 else 0
    #     st.markdown(kpi_template.format(
    #         bg_color="#F39200", title="Taux en poste", value=f"{active_rate:.2f} %"),
    #         unsafe_allow_html=True)

# Main application 
#st.subheader("📊 SUIVI INSERTION DE LA PROMOTION 6")
px.defaults.template = "plotly_dark"
# En-tête du Dashboard
st.markdown('<div class="main-header"><h1 class="header-title">SUIVI INSERTION DE LA PROMOTION 6</h1><p class="header-subtitle">École du Code - Sonatel Academy</p></div>', unsafe_allow_html=True)


# # refresh button
# if st.button("🔄 Rafraîchir"):
#     st.cache_data.clear()

# Load data
df = charger_donnees()
df = preprocess_data(df)











































































































































































































































































































































































df = df.convert_dtypes()
# print(df.dtypes)
# print(df.head())  
# print(df.info())

import datetime
#st.caption(f"Dernière actualisation: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

print(df.columns)
# Conversion des types de données
df = df.convert_dtypes()


if 'DOMAINEFORMATION' in df.columns:
    # Normaliser les valeurs de la colonne DOMAINEFORMATION
    df['DOMAINEFORMATION'] = df['DOMAINEFORMATION'].astype(str).str.strip().str.upper()
    
    # Filtrer les domaines exclus
    df = df[~df['DOMAINEFORMATION'].isin(['HACKEUSE', 'AWS'])]

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


# Section de filtres sur la page principale
    #st.markdown('<div class="filter-container"><p class="filter-title">Filtres</p>', unsafe_allow_html=True)

    # Organisation des filtres sur une seule ligne
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
st.markdown("<br>", unsafe_allow_html=True)  # Espacement
    # if st.button("✅ Appliquer les filtres"):
    #     st.success("Filtres appliqués avec succès!")

    # Application des filtres
filtered_data = df.copy()

if selected_domains:
    filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'].isin(selected_domains)]

if selected_companies:
    filtered_data = filtered_data[filtered_data['ENTREPRISES'].isin(selected_companies)]

if selected_statuses:
    status_values = ["OUI" if status == "En poste" else "NON" for status in selected_statuses]
    filtered_data = filtered_data[filtered_data['STATUTACTUELenposteounon'].isin(status_values)]

if selected_contracts:
    filtered_data = filtered_data[filtered_data['TYPEDECONTRAT'].isin(selected_contracts)]

    # Recherche par téléphone ou email
if search_input:
    filtered_students = filtered_data[
            (filtered_data['NDETELEPHONE'].astype(str).str.contains(search_input, case=False, na=False)) |
            (filtered_data['EMAIL'].str.contains(search_input, case=False, na=False))
        ]

        # Affichage des résultats de recherche
    if not filtered_students.empty:
        st.subheader("📌 Informations Apprenant")

            # Parcourir les étudiants trouvés et afficher leurs informations
        for _, student_data in filtered_students.iterrows():
            student_data = student_data.fillna("Non spécifié")

            st.markdown(
                    f"""
                    <div style="background-color: #cfe5f1; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px;">
                        <h4 style="color: #001728;"><center>{student_data['NOM']} {student_data['PRENOM']}</center></h4>
                        <ul style="color: #001728;">
                            <li><strong>📞 Téléphone :</strong> {student_data['NDETELEPHONE']}</li>
                            <li><strong>📧 E-mail :</strong> {student_data['EMAIL']}</li>
                            <li><strong>💼 Poste :</strong> {student_data['INTITULEPOSTE']}</li>
                            <li><strong>🏢 Entreprise :</strong> {student_data['ENTREPRISES']}</li>
                            <li><strong>📜 Type de contrat :</strong> {student_data['TYPEDECONTRAT']}</li>
                            <li><strong>💰 Rémunération :</strong> {student_data['REMUNERATION']} FCFA</li>
                            <li><strong>⏳ Durée du contrat :</strong> {student_data['DUREEMOIS']} Mois</li>
                            <li><strong>🟢 Statut :</strong> {'En poste' if student_data['STATUTACTUELenposteounon'] == 'OUI' else 'Non en poste'}</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    elif search_input:
        st.warning("⚠️ Aucun étudiant trouvé avec ces critères de recherche.")



st.sidebar.image("data/logo.jpg", caption="")
#st.subheader("Gestion des apprenants", divider='rainbow')
# if "show_form" not in st.session_state:
#     st.session_state.show_form = False
    
# if st.button("➕"):
#     st.session_state.show_form = not st.session_state.show_form  # Basculer l'état

# if st.session_state.show_form:
#     st.write("## Formulaire d'ajout")
#     add_data() 

kpi(filtered_data)


st.divider()

colo1, colo2, colo3 = st.columns(3, gap="large")

# 🔹 Graphe 1 : Répartition des types de contrats
with colo1:
    filtered_data['TYPEDECONTRAT'] = filtered_data['TYPEDECONTRAT'].fillna('Sans emploi')
    filtered_data.loc[filtered_data['TYPEDECONTRAT'] == '', 'TYPEDECONTRAT'] = 'Sans emploi'
    contract_count = filtered_data['TYPEDECONTRAT'].value_counts()

    fig1 = go.Figure(data=[go.Pie(
        labels=contract_count.index,
        values=contract_count.values,
        hole=0.3,  # Ajout d'un trou pour un meilleur rendu
        marker=dict(colors=px.colors.qualitative.Set2, line=dict(color='white', width=2)),
        textinfo='percent',
        hoverinfo='label+percent+value'
    )])

    fig1.update_layout(
         title=dict(
            text="📊 Répartition des types de contrats",
            font=dict(size=14, color="white", family="Arial"),
            x=0.5,  
            xanchor="center" 
        ),
        showlegend=True,
        legend=dict(orientation="h", y=-0.3, x=0.5),
        height=400, width=600  
    )

    st.plotly_chart(fig1, use_container_width=True)

# 🔹 Graphe 2 : Durée moyenne des contrats
with colo2:
    contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
    
    fig2 = px.bar(
        x=contract_duration.index, y=contract_duration.values,
        title="📅 Durée moyenne des contrats",
        labels={'x': 'Type de contrat', 'y': 'Durée (mois)'},
        color_discrete_sequence=['#00843D']
    )
    
    fig2.update_layout(
        
        title=dict(x=0.5, font=dict(size=14), xanchor="center" ),
        
        height=400, width=500,  # 🔹 Uniformisation
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        #plot_bgcolor="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

# 🔹 Graphe 3 : Distribution des rémunérations
with colo3:
    filtered_data_inseres = filtered_data[filtered_data['REMUNERATION'].notna() & (filtered_data['REMUNERATION'] > 0)]

    fig3 = px.histogram(
        filtered_data_inseres, x='REMUNERATION', nbins=8,
        title="💰 Distribution des rémunérations",
        labels={'REMUNERATION': 'Rémunération (FCFA)'},
        color_discrete_sequence=['#FF7F0E']
    )

    fig3.update_traces(marker_line_color='white', marker_line_width=1.5, opacity=0.9)

    fig3.update_layout(
        title=dict(x=0.5, font=dict(size=14), xanchor="center" ),
        height=400, width=500,  # 🔹 Alignement
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        #plot_bgcolor="white",
        bargap=0.2
    )

    st.plotly_chart(fig3, use_container_width=True)



st.divider()

#colon1, colon2, colon3 = st.columns(3, gap='large')
colon1, colon2, colon3 = st.columns([1, 1, 1], gap='large')


with colon1:
    if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
        filtered_data = filtered_data.dropna(subset=['DATEDEPRISEDESERVICE'])
        
        # Nous ne modifions pas ici le format des dates car c'est déjà fait dans preprocess_data()
        # Si besoin, on peut ajouter une vérification supplémentaire
        if filtered_data['DATEDEPRISEDESERVICE'].dtype != 'datetime64[ns]':
            st.warning("La colonne DATEDEPRISEDESERVICE n'est pas au format datetime. Vérifiez le prétraitement.")
            
            # Tentative de conversion au cas où
            filtered_data['DATEDEPRISEDESERVICE'] = pd.to_datetime(
                filtered_data['DATEDEPRISEDESERVICE'], 
                errors='coerce'
            )
        
        time_data = filtered_data[filtered_data['STATUT'] == 'INSERE'].copy()

        if not time_data.empty:
            time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
            time_data = time_data.drop_duplicates(subset=['DATEDEPRISEDESERVICE', 'STATUT'])
            evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
            evolution_data['MONTH_YEAR'] = evolution_data['MONTH_YEAR'].dt.to_timestamp()

            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            except:
                try:
                    locale.setlocale(locale.LC_TIME, 'fr_FR')
                except:
                    pass

            evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y').str.capitalize()
            today = pd.Timestamp.today()
            evolution_data = evolution_data[evolution_data['MONTH_YEAR'] <= today]
            evolution_data = evolution_data.sort_values('MONTH_YEAR')

            fig = px.line(
                evolution_data,
                x='MONTH_YEAR_FR',
                y='Nombre',
                title="📈 Évolution des apprenants insérés",
                labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': "Nombre d'apprenants"},
                markers=True,
                color_discrete_sequence=['#00843D']  # Couleur verte
            )

            fig.update_traces(
                mode='lines+markers',
                line=dict(width=3),
                marker=dict(size=8)
            )

            fig.update_layout(
                title=dict(
                    text="📈 Évolution des apprenants insérés",
                    font=dict(size=16, color="white", family="Arial"),
                    x=0.5,
                    xanchor="center"
                ),
                xaxis=dict(
                    showgrid=False,
                    title=dict(text="Mois et Année", font=dict(size=14, color="#333")),
                    tickangle=45,
                    tickfont=dict(size=12),
                    categoryorder='array',
                    categoryarray=evolution_data['MONTH_YEAR_FR'].tolist()
                ),
                yaxis=dict(
                    showgrid=False,
                    title=dict(text="Nombre d'apprenants", font=dict(size=14, color="white")),
                    tickfont=dict(size=14),
                    tickformat='d',
                    gridcolor="lightgrey"
                ),
                height=500,
                width=700
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée valide trouvée après filtrage des dates.")
    else:
        st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible.")

with colon2:

    filtered_data_inseres = filtered_data[filtered_data['STATUT'] == 'INSERE']

        # Répartition des postes
    filtered_data_inseres = filtered_data_inseres[filtered_data_inseres['INTITULEPOSTE'].notna()]


    post_count = filtered_data_inseres['INTITULEPOSTE'].value_counts().head(10)

        # Créer le graphique
    fig = px.bar(
            post_count, 
            x=post_count.index, 
            y=post_count.values, 
    
            labels={'x': 'Postes', 'y': 'Nombre'},
            color=post_count.values, 
            color_continuous_scale='Viridis',
            text=post_count.values  
        )

        # Personnalisation du layout pour les postes
    fig.update_layout(
            title=dict(
                
                text="📈 Top 10 des postes occupés ",
                font=dict(size=14, color="white", family="Arial"),
                x=0.5,  
                xanchor="center"
            ),
            xaxis=dict(
                showgrid = False,
                title="Postes",
                tickangle=-45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                showgrid = False,
                title="Nombre d'apprenants insérés",
                gridcolor="lightgrey"
            ),

            bargap=0.2,
            height=500,
            width=700
        )

        # Personnalisation des barres et des textes
    fig.update_traces(
            textposition="outside",  
            textfont=dict(color="white", size=14),  
            hovertemplate="<b>Poste occupé:</b> %{x}<br><b>Nombre:</b> %{y}<extra></extra>"
        )

        # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)


  # Définition du seuil (fixe ou interactif)

with colon3:
    st.subheader("Données filtrées")
    st.dataframe(filtered_data)
    height=500,
    width=700


st.divider()
# 📌 Disposer les éléments sur la même ligne
col1, col2 = st.columns([1, 1])  # Ajuste les proportions si nécessaire

col1, col2 = st.columns(2)

with col1:
    # 🔽 Slider pour définir le seuil
    seuil = st.slider("", min_value=1, max_value=20, value=2)

if 'ENTREPRISES' in filtered_data_inseres.columns:
    structure_count = filtered_data_inseres['ENTREPRISES'].value_counts()

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
