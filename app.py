import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib as plt
import locale

# Chargement des données
df = pd.read_excel('SUIVI_GLOBAL_P5.xlsx', engine='openpyxl', skiprows=1)

# Prétraitement des données
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Suppression des caractères spéciaux dans les colonnes
    df.columns = df.columns.str.replace('[^a-zA-Z]', '', regex=True)

    # Conversion des colonnes en dates
    df['DATEDENAISSANCE'] = pd.to_datetime(df['DATEDENAISSANCE'], errors='coerce')
    df['DATEDEPRISEDESERVICE'] = pd.to_datetime(df['DATEDEPRISEDESERVICE'], errors='coerce')

    # Remplissage des valeurs manquantes
    columns_mode = [
        'LIEUDENAISSANCE', 
        'SITUATIONSOCIOPROFESSIONNELlinscription', 
        'INTITULEPOSTE', 
        'STRUCTUREDIRECTIONPOLE', 
        'ENTREPRISES', 
        'TYPEDECONTRAT', 
        'STATUTACTUELenposteounon'
    ]
    for col in columns_mode:
        if col in df.columns and not df[col].dropna().empty:
            mode_value = df[col].mode().iloc[0]
            df[col] = df[col].fillna(mode_value)

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

# Titre principal
st.set_page_config(page_title="Dashboard Entreprise", layout="wide")
st.title("📊 Suivi des étudiants ODC")


# Utiliser le thème dans vos visualisations
px.defaults.template = "plotly_dark"  # ou un autre thème natif comme "plotly" ou "seaborn"


with open("styles.css") as f:
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

# KPI 
st.header("📌 Indicateurs clés")
col1, col2, col3 = st.columns(3)

avg_salary = df['REMUNERATION'].mean() if 'REMUNERATION' in df.columns else 0
total_students = len(df)
active_students = len(df[df['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in df.columns else 0

col1.metric("💰 Rémunération moyenne", f"{avg_salary:.2f} FCFA")
col2.metric("👥 Nombre total d'aprenants", total_students)
col3.metric("✅ Apprenants en poste", active_students)



# Barre de recherche d'étudiant
st.sidebar.header("Rechercher un étudiant")
search_input = st.sidebar.text_input("Entrez le nom, prénom ou numéro CNI :")

# Filtrage d'un étudiant spécifique
filtered_student = df[
    (df['NOM'].str.contains(search_input, case=False, na=False)) |
    (df['PRENOM'].str.contains(search_input, case=False, na=False)) |
    (df['NCIN'].astype(str).str.contains(search_input, case=False, na=False))
]

if search_input and not filtered_student.empty:
    # Affichage des informations de l'étudiant
    st.subheader("Informations de l'étudiant sélectionné")
    student_data = filtered_student.iloc[0]  # On sélectionne la première ligne correspondant à l'étudiant

    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #ddd;">
            <h4 style="color: #007BFF;">{student_data['NOM']} {student_data['PRENOM']}</h4>
            <ul>
                <li><strong>Numéro CNI :</strong> {student_data['NCIN']}</li>
                <li><strong>Poste occupé :</strong> {student_data.get('INTITULEPOSTE', 'Non spécifié')}</li>
                <li><strong>Entreprise :</strong> {student_data.get('ENTREPRISES', 'Non spécifiée')}</li>
                <li><strong>Type de contrat :</strong> {student_data.get('TYPEDECONTRAT', 'Non spécifié')}</li>
                <li><strong>Rémunération :</strong> {student_data.get('REMUNERATION', 'Non spécifiée')} FCFA</li>
                <li><strong>Durée du contrat :</strong> {student_data.get('DUREEMOIS', 'Non spécifiée')} mois</li>
                <li><strong>Statut actuel :</strong> {'En poste' if student_data['STATUTACTUELenposteounon'] == 'OUI' else 'Non en poste'}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    if search_input:
        st.error("Aucun étudiant trouvé.")



# Aperçu des données
st.subheader("Aperçu des données 📋")
st.dataframe(df.head(), use_container_width=True)

# Ajout de filtres interactifs
st.sidebar.header("Filtres interactifs")
selected_company = st.sidebar.selectbox(
    "Filtrer par entreprise", 
    options=["Toutes"] + df['ENTREPRISES'].dropna().unique().tolist()
)

selected_status = st.sidebar.selectbox(
    "Filtrer par statut", 
    options=["Tous", "En poste", "Non en poste"]
)

selected_contract = st.sidebar.selectbox(
    "Filtrer par type de contrat", 
    options=["Tous"] + df['TYPEDECONTRAT'].dropna().unique().tolist()
)

# Application des filtres
filtered_data = df.copy()

if selected_company != "Toutes":
    filtered_data = filtered_data[filtered_data['ENTREPRISES'] == selected_company]

if selected_status != "Tous":
    status_value = "OUI" if selected_status == "En poste" else "NON"
    filtered_data = filtered_data[filtered_data['STATUTACTUELenposteounon'] == status_value]

if selected_contract != "Tous":
    filtered_data = filtered_data[filtered_data['TYPEDECONTRAT'] == selected_contract]

# Affichage des données filtrées
st.subheader("Données filtrées 📋")
st.dataframe(filtered_data, use_container_width=True)

# Visualisations mises à jour
st.markdown("### Visualisations mises à jour")
col1, col2 = st.columns(2)

with col1:
    contract_count = filtered_data['TYPEDECONTRAT'].value_counts()
    fig = px.pie(
        names=contract_count.index, 
        values=contract_count.values, 
        title="Répartition des types de contrats (Filtrée)"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    structure_count = filtered_data['STRUCTUREDIRECTIONPOLE'].value_counts()
    fig = px.bar(
        x=structure_count.index, 
        y=structure_count.values, 
        title="Répartition des bénéficiaires par structure (Filtrée)", 
        labels={'x': 'Structure', 'y': 'Nombre'},
        text=structure_count
    )
    st.plotly_chart(fig, use_container_width=True)

# Comparaison des rémunérations filtrées
st.subheader("Comparaison des rémunérations (Filtrée)")
fig = px.histogram(
    filtered_data, 
    x='REMUNERATION', 
    nbins=20, 
    title="Distribution des rémunérations (Filtrée)", 
    labels={'REMUNERATION': 'Rémunération (FCFA)'},
    color_discrete_sequence=['#636EFA'],
    text_auto=True
    
)
st.plotly_chart(fig, use_container_width=True)

# Répartition des postes filtrée
st.subheader("Répartition des postes occupés (Filtrée)")
post_count = filtered_data['INTITULEPOSTE'].value_counts().head(10)  # Top 10 des postes
fig = px.bar(
    post_count, 
    x=post_count.index, 
    y=post_count.values, 
    title="Top 10 des postes occupés (Filtrée)", 
    labels={'x': 'Postes', 'y': 'Nombre'},
    color=post_count.values, 
    color_continuous_scale='Viridis',
    text=post_count
)
st.plotly_chart(fig, use_container_width=True)

company_count = filtered_data['ENTREPRISES'].value_counts()
fig = px.bar(
    company_count,
    x=company_count.index,
    y=company_count.values,
    title="Nombre d'étudiants par entreprise",
    labels={'x': 'Entreprise', 'y': 'Nombre d\'étudiants'}
)
st.plotly_chart(fig, use_container_width=True)

contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
fig = px.bar(
    contract_duration,
    x=contract_duration.index,
    y=contract_duration.values,
    title="Durée moyenne des contrats par type",
    labels={'x': 'Type de contrat', 'y': 'Durée moyenne (mois)'}
)
st.plotly_chart(fig, use_container_width=True)

fig = px.box(
    filtered_data,
    x='TYPEDECONTRAT',
    y='REMUNERATION',
    title="Distribution des rémunérations par type de contrat",
    labels={'TYPEDECONTRAT': 'Type de contrat', 'REMUNERATION': 'Rémunération (FCFA)'},
    color='TYPEDECONTRAT'
)
st.plotly_chart(fig, use_container_width=True)

heatmap_data = filtered_data.pivot_table(
    index='STRUCTUREDIRECTIONPOLE',
    columns='INTITULEPOSTE',
    values='NOM',  # Remplacez par une autre colonne si nécessaire
    aggfunc='count',
    fill_value=0
)

# # Evolution des rémunérations au fil du temps
# if 'DATEDEPRISEDESERVICE' in filtered_data.columns and not filtered_data['DATEDEPRISEDESERVICE'].isna().all():
#     # Convertir la date en année pour simplifier l'analyse
#     filtered_data['AnneePriseService'] = filtered_data['DATEDEPRISEDESERVICE'].dt.year

#     # Calculer la rémunération moyenne par année
#     remuneration_by_year = filtered_data.groupby('AnneePriseService')['REMUNERATION'].mean().reset_index()

#     # Tracer une courbe
#     fig = px.line(
#         remuneration_by_year,
#         x='AnneePriseService',
#         y='REMUNERATION',
#         title="Évolution des rémunérations moyennes par année",
#         labels={'AnneePriseService': 'Année', 'REMUNERATION': 'Rémunération moyenne (FCFA)'},
#         markers=True
#     )
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.warning("Les données de prise de service ne sont pas disponibles ou contiennent des valeurs manquantes.")




# Courbe temporelle - évolution des apprenants en poste
st.subheader("📈 Évolution temporelle des apprenants en poste")
if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
    # Filtrer uniquement les apprenants en poste avec des dates valides
    time_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'].notna()]
    time_data = time_data[time_data['STATUTACTUELenposteounon'] == 'OUI']
    
    # Grouper par mois et année
    time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
    evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
    evolution_data['MONTH_YEAR'] = pd.to_datetime(evolution_data['MONTH_YEAR'].astype(str))
    
    # Configurer la locale en français pour les mois
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Configuration pour Unix/Linux/MacOS
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'fra')  # Configuration pour Windows
        except locale.Error:
            st.warning("Impossible de configurer la locale en français. Les mois resteront en anglais.")
    
    # Ajouter la colonne avec les mois en français
    evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y')
    evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR_FR'].str.capitalize()  # Capitaliser la première lettre
    
    # Trier les données
    evolution_data = evolution_data.sort_values('MONTH_YEAR')

    # Créer la courbe
    fig = px.line(
        evolution_data, 
        x='MONTH_YEAR_FR', 
        y='Nombre', 
        title="Évolution des apprenants en poste au fil du temps",
        labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
        markers=True
    )
    fig.update_layout(
        xaxis=dict(tickangle=45),
        xaxis_title="Mois et Année",
        yaxis_title="Nombre d'apprenants"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")
