import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib as plt
import locale
import plotly.graph_objects as go
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
st.subheader("📊 Suivi Insertion de la promotion 5")


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



# Barre de recherche d'étudiant
st.sidebar.header("Rechercher un étudiant")
search_input = st.sidebar.text_input("Entrez le nom, prénom ou nom complet :")
search_domain = st.sidebar.text_input("Rechercher un domaine de formation")


df['NOM_COMPLET'] = (df['PRENOM'] + ' ' + df['NOM']).str.lower()


filtered_student = df[
    (df['NOM'].str.contains(search_input, case=False, na=False)) |
    (df['PRENOM'].str.contains(search_input, case=False, na=False)) |
    (df['NOM_COMPLET'].str.contains(search_input.lower(), na=False))
]

if search_input and not filtered_student.empty:
    st.subheader("Informations")
    student_data = filtered_student.iloc[0] 

    st.markdown(
        f"""
        <div style="background-color: #cfe5f1; padding: 15px; border-radius: 8px; border: 1px solid #ddd;">
            <h4 style="color: #001728;">{student_data['NOM']} {student_data['PRENOM']}</h4>
            <ul style="color: #001728;">
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
selected_domain = st.sidebar.selectbox(
    "Filtrer par domaine de formation", 
    options=["Tous"] + df['DOMAINEFORMATION'].dropna().unique().tolist()
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

if selected_domain != "Tous":
    filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'] == selected_domain]


if search_domain:
    filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'].str.contains(search_domain, case=False, na=False)]


def kpi():

    # Calcul KPI 
    avg_salary = filtered_data['REMUNERATION'].mean() if 'REMUNERATION' in filtered_data.columns else 0
    total_students = len(filtered_data)
    active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0
    insertion_rate = (active_students / total_students * 100) if total_students > 0 else 0
    # Calcul féminisation
    female_students = len(filtered_data[filtered_data['SEXE'] == 'F']) if 'SEXE' in filtered_data.columns else 0
    feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5, gap='small')

    with col1:
        st.info('Rémunération', icon="💰")
        st.metric(label="Moyenne", value=f"{avg_salary:.2f}")

    with col2:
        st.info('Apprenants', icon="🧑‍🎓")
        st.metric(label="Total", value=f"{total_students:,.0f}")

    with col3:
        st.info('En poste', icon="💼")
        st.metric(label="Total", value=f"{active_students:,.0f}")

    with col4:
        st.info('Taux d insertion', icon="📊")
        st.metric(label="Taux %", value=f"{insertion_rate:.2f} %")

    with col5:
        st.info('Taux de féminisation', icon="👩")
        st.metric(label="Taux %", value=f"{feminization_rate:.2f} %")


#kpi()

#st.subheader("Gestion des apprenants", divider='rainbow')
if "show_form" not in st.session_state:
    st.session_state.show_form = False
    
if st.button("Ajouter un nouvel apprenant"):
    st.session_state.show_form = not st.session_state.show_form  # Basculer l'état

if st.session_state.show_form:
    st.write("## Formulaire d'ajout")
    from add_data import *
    add_data() 
kpi()


st.divider()

colo1, colo2 = st.columns(2, gap="large")
with colo1:
    contract_count = filtered_data['TYPEDECONTRAT'].value_counts()

    # Création du diagramme circulaire complet
    fig = go.Figure(data=[go.Pie(
        labels=contract_count.index,
        values=contract_count.values,
        hole=0,  # Aucun trou pour un cercle complet
        marker=dict(
            colors=px.colors.qualitative.Set2, 
            line=dict(color='white', width=2)
        ),
        textinfo='percent',  # Afficher les pourcentages et étiquettes
        insidetextorientation='radial',
        hoverinfo='label+percent+value'
    )])

    # Mise en page pour séparer la légende
    fig.update_layout(
        title=dict(
            text="📈 Répartition des types de contrats",
            font=dict(size=18, color="#2c3e50", family="Arial"),
            x=0.5,
            xanchor="center"
        ),
        showlegend=True,  # Légende activée
        legend=dict(
            orientation="h",  # Légende horizontale
            yanchor="bottom",
            y=-0.3,  # Positionnée sous le diagramme
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(t=50, b=100),  # Ajout de marges pour séparer
    )

    # Affichage dans Streamlit
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
    st.plotly_chart(fig, use_container_width=True)

st.divider()

colon1, colon2 = st.columns(2, gap='large')
with colon1:
    #Rémuneration
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
            font=dict(size=16, color="#cfe5f1", family="Arial"), 
            x=0.5,  
            xanchor="right" 
        ),
        xaxis=dict(
            title="Rémunération (FCFA)",  
            titlefont=dict(size=16, color="#333"),  
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
    )

    # Affichage du graphique
    st.plotly_chart(fig, use_container_width=True)

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
            title="Évolution des apprenants en poste au fil du temps",
            labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
            markers=True
        )
        
        fig.update_traces(text=evolution_data['Nombre'], textposition='top center')

        fig.update_layout(
            xaxis=dict(tickangle=45),
            xaxis_title="Mois et Année",
            yaxis_title="Nombre d'apprenants",
            yaxis=dict(tickformat='d'), 
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")



# Comptage des bénéficiaires par structure
structure_count = filtered_data['STRUCTUREDIRECTIONPOLE'].value_counts()
title=dict(
        text="📈 Répartition des types de contrats",
        font=dict(size=24, color="#cfe5f1", family="Arial"),
        x=0.5,
        xanchor="right" 
    ),
fig = px.bar(
    x=structure_count.index, 
    y=structure_count.values, 
    title=" Répartition des bénéficiaires par structure", 
    labels={'x': 'Structure', 'y': 'Nombre'},
    text=structure_count, 
    
)


fig.update_traces(
    marker_color=px.colors.qualitative.Vivid,  
    texttemplate='%{text}',  
    textposition='outside',  
)

# Personnalisation du layout
fig.update_layout(
    title=dict(
        text="📈 Répartition des bénéficiaires par structure",
        font=dict(size=24, color="#cfe5f1", family="Arial"),
        x=0.5,  
        xanchor="right" 
    ),
    xaxis=dict(
        title="Structure",
        tickangle=45,  
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title="Nombre de bénéficiaires",
        gridcolor="lightgrey",
        range=[0, structure_count.values.max() * 1.2],  
    ),
    plot_bgcolor="white", 
    bargap=0.2,  
)


st.plotly_chart(fig, use_container_width=True)




# Répartition des postes 
st.subheader("Répartition des postes occupés ")
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
st.plotly_chart(fig, use_container_width=True)

company_count = filtered_data['ENTREPRISES'].value_counts()


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
        font=dict(size=24, color="#cfe5f1", family="Arial"),
        x=0.5,  
        xanchor="center"
    ),
    xaxis=dict(
        title="Entreprise",
        titlefont=dict(size=16, color="#333"),
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
    bargap=0.15 
)


st.plotly_chart(fig, use_container_width=True)



# fig = px.box(
#     filtered_data,
#     x='TYPEDECONTRAT',
#     y='REMUNERATION',
#     title="Distribution des rémunérations par type de contrat",
#     labels={'TYPEDECONTRAT': 'Type de contrat', 'REMUNERATION': 'Rémunération (FCFA)'},
#     color='TYPEDECONTRAT'
# )
# st.plotly_chart(fig, use_container_width=True)

heatmap_data = filtered_data.pivot_table(
    index='STRUCTUREDIRECTIONPOLE',
    columns='INTITULEPOSTE',
    values='NOM',  
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


# # Aperçu des données
st.subheader("Aperçu des données 📋")
st.dataframe(df.head(), use_container_width=True)
