# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import locale
# import gspread
# from google.oauth2.service_account import Credentials
# import os
# import sys


# def error_callback():
#     _, exc, tb = sys.exc_info()
#     st.error(f"Une erreur s'est produite: {exc}")
#     st.code(str(exc))


# SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# SERVICE_ACCOUNT_FILE = "eighth-jigsaw-446022-r0-638d8f86d788.json"
# SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1oNQc5xQO4bRj72v50po6Qg95jZzXp3VhBxyi7edx_ZY"


# # Modified to use a lower TTL and add a last_refreshed attribute
# @st.cache_data(ttl=30)  
# def charger_donnees():
#     try:
#         credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
#         client = gspread.authorize(credentials)
#         sheet = client.open_by_url(SPREADSHEET_URL).worksheet("GLOBAL")

#         data = sheet.get_all_records(head=3)

#         if not data:
#             st.warning("Aucune donnée trouvée dans la feuille Google Sheets.")
#             return pd.DataFrame()

#         return pd.DataFrame(data)

#     except Exception as e:
#         st.error(f"❌ Erreur lors du chargement des données : {e}")
#         return pd.DataFrame()


# def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
#     if df.empty:
#         return df
        
#     try:
#         # Suppression des caractères spéciaux dans les noms de colonnes
#         df.columns = df.columns.str.replace(r'[^a-zA-Z]', '', regex=True)

#         # Colonnes à convertir en chaîne
#         columns_str = {'CIN', 'NDETELEPHONE', 'EMAIL'} & set(df.columns)
#         for col in columns_str:
#             df[col] = df[col].astype(str)

#         # Colonnes à convertir en dates
#         columns_date = {'DATEDENAISSANCE', 'DATEDEPRISEDESERVICE'} & set(df.columns)
#         for col in columns_date:
#             df[col] = pd.to_datetime(df[col], errors='coerce')
#             df[col] = df[col].fillna(pd.NaT)  # Optionnel : Remplacer NaT par une autre valeur

#         # Colonnes sensibles (ne pas remplacer les valeurs manquantes)
#         sensitive_columns = {
#             'INTITULEPOSTE', 'LIEUDENAISSANCE', 'SITUATIONSOCIOPROFESSIONNELlinscription',
#             'STRUCTUREDIRECTIONPOLE', 'ENTREPRISES', 'TYPEDECONTRAT', 'STATUTACTUELenposteounon'
#         } & set(df.columns)
#         # Pas de remplissage des NaN pour ces colonnes

#         # Colonnes avec valeurs par défaut
#         columns_fixed = {
#             'ADRESSE': 'Non spécifié', 'CONTACTDURGENCE': 'Non fourni', 
#             'STATUTMATRIMONIALE': 'Non spécifié', 'PROFILAGE': 'Non défini', 
#             'COMMENTAIRE': 'Aucun commentaire', 'CONTACTENTREPRISE': 'Non précisé'
#         }
#         for col, value in columns_fixed.items():
#             if col in df.columns:
#                 df[col] = df[col].fillna(value)

#         # Colonnes numériques : conversion et remplissage avec 0
#         columns_numeric = {'REMUNERATION', 'DUREEMOIS'} & set(df.columns)
#         for col in columns_numeric:
#             df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

#         return df
#     except Exception as e:
#         st.error(f"❌ Erreur lors du prétraitement des données : {e}")
#         return df  # Retour du DataFrame original en cas d'erreur

# # Fonction pour ajouter un nouvel étudiant
# def add_student(new_data):
#     try:
#         # Charger les identifiants et se connecter à Google Sheets
#         credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
#         client = gspread.authorize(credentials)
#         sheet = client.open_by_url(SPREADSHEET_URL).worksheet("GLOBAL")
        
#         # Ajouter une nouvelle ligne
#         sheet.append_row(list(new_data.values()))
        
#         st.success("Étudiant ajouté avec succès!")
#         # Actualiser les données explicitement
#         st.cache_data.clear()
#         return True
#     except Exception as e:
#         st.error(f"Erreur lors de l'ajout de l'étudiant: {e}")
#         return False

# # Fonction pour le formulaire d'ajout d'étudiant
# def add_data():
#     with st.form("new_student_form"):
#         st.write("Entrez les informations de l'étudiant")
        
#         # Informations personnelles
#         col1, col2 = st.columns(2)
#         with col1:
#             nom = st.text_input("Nom")
#             prenom = st.text_input("Prénom")
#             sexe = st.selectbox("Sexe", options=["F", "M"])
#             date_naissance = st.date_input("Date de naissance")
#             telephone = st.text_input("Numéro de téléphone")
        
#         with col2:
#             email = st.text_input("Email")
#             cin = st.text_input("CIN")
#             domaine_formation = st.text_input("Domaine de formation")
#             adresse = st.text_input("Adresse")
        
#         # Informations professionnelles
#         st.write("Informations professionnelles")
#         col3, col4 = st.columns(2)
#         with col3:
#             entreprise = st.text_input("Entreprise")
#             poste = st.text_input("Intitulé du poste")
#             type_contrat = st.selectbox("Type de contrat", options=["CDI", "CDD", "Stage", "Freelance", "Autre"])
#             date_service = st.date_input("Date de prise de service")
        
#         with col4:
#             remuneration = st.number_input("Rémunération (FCFA)", min_value=0)
#             duree_mois = st.number_input("Durée (mois)", min_value=0)
#             statut = st.selectbox("Statut", options=["INSERE", "NON INSERE"])
#             statut_poste = st.selectbox("En poste actuellement ?", options=["OUI", "NON"])
#             structure = st.text_input("Structure/Direction/Pôle")
        
#         submitted = st.form_submit_button("Ajouter l'étudiant")
        
#         if submitted:
#             # Créer un dictionnaire avec les données
#             new_student = {
#                 "NOM": nom,
#                 "PRENOM": prenom,
#                 "SEXE": sexe,
#                 "DATEDENAISSANCE": date_naissance.strftime("%Y-%m-%d"),
#                 "NDETELEPHONE": telephone,
#                 "EMAIL": email,
#                 "CIN": cin,
#                 "DOMAINEFORMATION": domaine_formation,
#                 "ADRESSE": adresse,
#                 "ENTREPRISES": entreprise,
#                 "INTITULEPOSTE": poste,
#                 "TYPEDECONTRAT": type_contrat,
#                 "DATEDEPRISEDESERVICE": date_service.strftime("%Y-%m-%d"),
#                 "REMUNERATION": remuneration,
#                 "DUREEMOIS": duree_mois,
#                 "STATUT": statut,
#                 "STATUTACTUELenposteounon": statut_poste,
#                 "STRUCTUREDIRECTIONPOLE": structure
#             }
            
#             # Ajouter l'étudiant
#             success = add_student(new_student)
#             if success:
#                 # Vider les champs après l'ajout
#                 st.experimental_rerun()

# # Fonction pour les KPIs


# def kpi(filtered_data):
#     # Vérifier si le DataFrame est vide
#     if filtered_data.empty:
#         st.warning("Aucune donnée disponible pour afficher les KPI.")
#         return
        
#     # CSS pour forcer les colonnes à avoir une largeur identique
#     st.markdown(
#         """
#         <style>
#         /* Styles pour les colonnes */
#         .stColumns > div {
#             width: 100% !important;
#             padding: 10px !important;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Calcul des KPI 
#     inserted_students_data = filtered_data[filtered_data['STATUT'] == 'INSERE'] if 'STATUT' in filtered_data.columns else pd.DataFrame()

#     # Calculer la rémunération moyenne uniquement pour les étudiants insérés
#     avg_salary = inserted_students_data['REMUNERATION'].mean() if not inserted_students_data.empty else 0

#     total_students = len(filtered_data)
#     active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0

#     # nombre d'étudiants insérés 
#     inserted_students = len(filtered_data[filtered_data['STATUT'] == 'INSERE']) if 'STATUT' in filtered_data.columns else 0
#     insertion_rate = (inserted_students / total_students * 100) if total_students > 0 else 0

#     # Calcul du taux de féminisation
#     female_students = len(filtered_data[filtered_data['SEXE'] == 'F']) if 'SEXE' in filtered_data.columns else 0
#     feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0

#     # Configuration de la localisation pour les nombres
#     try:
#         locale.setlocale(locale.LC_ALL, 'French_France.1252')
#     except locale.Error:
#         try:
#             locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
#         except locale.Error:
#             print("La locale spécifiée n'est pas supportée sur ce système.")

#     # Template HTML/CSS pour les KPI
#     kpi_template = """
#     <div style="
#         background-color: {bg_color};
#         padding: 10px;
#         border-radius: 10px;
#         text-align: center;
#         color: white;
#         font-size: 20px;
#         font-weight: bold;
#         margin-bottom: 20px;
#         width: 100%;
#         height: 200px;
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#     ">
#         <div style="font-size: 20px; font-weight: normal;">{title}</div>
#         <div style="font-size: 36px; margin-top: 10px;">{value}</div>
#     </div>
#     """
#     # Première ligne avec 3 colonnes
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         # Formater avg_salary avec 2 décimales avant de le convertir en chaîne
#         avg_salary_formatted = locale.format_string("%.2f", avg_salary, grouping=True)
#         st.markdown(kpi_template.format(
#             bg_color="#FF5722", title="Rémunération moyenne", value=f"{avg_salary_formatted} FCFA"),
#             unsafe_allow_html=True)
        
#     with col2:
#         st.markdown(kpi_template.format(
#             bg_color="#2196F3", title="Nombre total d'apprenants", value=total_students),
#             unsafe_allow_html=True)

#     with col3:
#         st.markdown(kpi_template.format(
#             bg_color="#FFC107", title="Apprenants en poste", value=inserted_students),
#             unsafe_allow_html=True)

#     # Deuxième ligne avec 3 colonnes
#     col4, col5, col6 = st.columns(3, gap="large")
#     with col4:
#         # Définir la couleur en fonction du taux d'insertion
#         if insertion_rate < 50:
#             bg_color = "#FF5722"  
#         else:
#             bg_color = "#4CAF50"  

#         st.markdown(kpi_template.format(
#             bg_color=bg_color, title="Taux d'insertion", value=f"{insertion_rate:.2f} %"),
#             unsafe_allow_html=True)

#     with col5:
#         st.markdown(kpi_template.format(
#             bg_color="#9C27B0", title="Taux de féminisation", value=f"{feminization_rate:.2f} %"),
#             unsafe_allow_html=True)

#     with col6:
#         st.markdown(kpi_template.format(
#             bg_color="#E0E0E0", title="(Vide)", value="--"),
#             unsafe_allow_html=True)
        
# # Main application 
# st.subheader("📊 SUIVI INSERTION DE LA PROMOTION 6")
# px.defaults.template = "plotly_dark"

# # refresh button
# if st.button("🔄 Rafraîchir"):
#     st.cache_data.clear()

# # Load data
# df = charger_donnees()
# df = preprocess_data(df)
# df = df.convert_dtypes()
# # print(df.dtypes)
# # print(df.head())  
# # print(df.info())

# import datetime
# #st.caption(f"Dernière actualisation: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
# with open("styles.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# print(df.columns)

# st.markdown(
#     """
#     <style>
#         .css-18e3th9 {background-color: #1a1a1a;}
#         .css-10trblm {color: #ffffff;}
#         .css-12ttj6m {color: #ffffff;}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # Barre de recherche d'étudiant
# st.sidebar.header("Rechercher un étudiant")
# search_input = st.sidebar.text_input("Entrez le numéro de téléphone ou l'e-mail :")

# # Vérifier si une recherche est effectuée
# if search_input:
#     filtered_students = df[
#         (df['NDETELEPHONE'].astype(str).str.contains(search_input, case=False, na=False)) |
#         (df['EMAIL'].str.contains(search_input, case=False, na=False))
#     ]

#     # Affichage des résultats
#     if not filtered_students.empty:
#         st.subheader("Informations Apprenant")

#         # Parcourir les étudiants trouvés et afficher leurs informations
#         for _, student_data in filtered_students.iterrows():
#             student_data = student_data.fillna("Non spécifié")

#             st.markdown(
#                 f"""
#                 <div style="background-color: #cfe5f1; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px;">
#                     <h4 style="color: #001728;"><center>{student_data['NOM']} {student_data['PRENOM']}</center></h4>
#                     <ul style="color: #001728;">
#                         <li><strong>Numéro de Téléphone :</strong> {student_data['NDETELEPHONE']}</li>
#                         <li><strong>E-mail :</strong> {student_data['EMAIL']}</li>
#                         <li><strong>Poste occupé :</strong> {student_data['INTITULEPOSTE']}</li>
#                         <li><strong>Entreprise :</strong> {student_data['ENTREPRISES']}</li>
#                         <li><strong>Type de contrat :</strong> {student_data['TYPEDECONTRAT']}</li>
#                         <li><strong>Rémunération :</strong> {student_data['REMUNERATION']} FCFA</li>
#                         <li><strong>Durée du contrat :</strong> {student_data['DUREEMOIS']} Mois</li>
#                         <li><strong>Statut actuel :</strong> {'En poste' if student_data['STATUTACTUELenposteounon'] == 'OUI' else 'Non en poste'}</li>
#                     </ul>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#     else:
#         st.error("Aucun étudiant trouvé.")

# # filtres 
# st.sidebar.header("Filtres interactifs")


# selected_domains = st.sidebar.multiselect(
#     "Filtrer par domaine de formation", 
#     options=df['DOMAINEFORMATION'].dropna().unique().tolist(),
#     default=[]
# )

# selected_companies = st.sidebar.multiselect(
#     "Filtrer par entreprise", 
#     options=df['ENTREPRISES'].dropna().unique().tolist(),
#     default=[]
# )


# selected_statuses = st.sidebar.multiselect(
#     "Filtrer par statut", 
#     options=["En poste", "Non en poste"],
#     default=[]
# )


# selected_contracts = st.sidebar.multiselect(
#     "Filtrer par type de contrat", 
#     options=df['TYPEDECONTRAT'].dropna().unique().tolist(),
#     default=[]
# )

# filtered_data = df.copy()

# if selected_domains:
#     filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'].isin(selected_domains)]

# if selected_companies:
#     filtered_data = filtered_data[filtered_data['ENTREPRISES'].isin(selected_companies)]

# if selected_statuses:
#     status_values = ["OUI" if status == "En poste" else "NON" for status in selected_statuses]
#     filtered_data = filtered_data[filtered_data['STATUTACTUELenposteounon'].isin(status_values)]


# if selected_contracts:
#     filtered_data = filtered_data[filtered_data['TYPEDECONTRAT'].isin(selected_contracts)]

# # st.write("Résultats filtrés :")
# # st.dataframe(filtered_data)

# st.sidebar.image("data/logo.jpg", caption="Logo de l'organisation")
# #st.subheader("Gestion des apprenants", divider='rainbow')
# if "show_form" not in st.session_state:
#     st.session_state.show_form = False
    
# if st.button("➕"):
#     st.session_state.show_form = not st.session_state.show_form  # Basculer l'état

# if st.session_state.show_form:
#     st.write("## Formulaire d'ajout")
#     add_data() 

# kpi(filtered_data)


# st.divider()

# # st.markdown(
# #     """
# #     <hr style="height: 4px; background: linear-gradient(90deg, #FF7F0E, #1F77B4); border: none; border-radius: 2px; margin: 20px 0;">
# #     """,
# #     unsafe_allow_html=True,
# # )

# st.subheader("Aperçus des données filtrées")
# st.dataframe(filtered_data.head())
# st.divider()
# colo1, colo2 = st.columns(2, gap="large")
# with colo1:

#     filtered_data['TYPEDECONTRAT'] = filtered_data['TYPEDECONTRAT'].fillna('Sans emploi')

#     filtered_data.loc[filtered_data['TYPEDECONTRAT'] == '', 'TYPEDECONTRAT'] = 'Sans emploi'

#     contract_count = filtered_data['TYPEDECONTRAT'].value_counts()

#     fig = go.Figure(data=[go.Pie(
#         labels=contract_count.index,
#         values=contract_count.values,
#         hole=0,  
#         marker=dict(
#             colors=px.colors.qualitative.Set2, 
#             line=dict(color='white', width=2)
#         ),
#         textinfo='percent',  
#         insidetextorientation='radial',
#         hoverinfo='label+percent+value'
#     )])


#     fig.update_layout(
#         title=dict(
#             text="📈 Répartition des types de contrats",
#             font=dict(size=18, color="#2c3e50", family="Arial"),
#             x=0.5,
#             xanchor="center"
#         ),
#         showlegend=True,  
#         legend=dict(
#             orientation="h",  
#             yanchor="bottom",
#             y=-0.3,  
#             xanchor="center",
#             x=0.5,
#             font=dict(size=14)
#         ),
#         margin=dict(t=50, b=100),  
#     )

#     st.plotly_chart(fig, use_container_width=True)

# # Add a second chart in the second column
# # with colo2:
# #     if 'SEXE' in filtered_data.columns:
# #         gender_data = filtered_data['SEXE'].value_counts().reset_index()
# #         gender_data.columns = ['Sexe', 'Nombre']
        
# #         # Map 'F' and 'M' to more descriptive labels
# #         gender_map = {'F': 'Femmes', 'M': 'Hommes'}
# #         gender_data['Sexe'] = gender_data['Sexe'].map(gender_map)
        
# #         fig_gender = px.bar(
# #             gender_data, 
# #             x='Sexe', 
# #             y='Nombre',
# #             color='Sexe',
# #             color_discrete_map={'Femmes': '#E91E63', 'Hommes': '#2196F3'},
# #             title="Répartition par genre"
# #         )
        
# #         fig_gender.update_layout(
# #             title=dict(
# #                 text="👥 Répartition par genre",
# #                 font=dict(size=18, color="#2c3e50", family="Arial"),
# #                 x=0.5,
# #                 xanchor="center"
# #             ),
# #             xaxis_title="",
# #             yaxis_title="Nombre d'apprenants",
# #             showlegend=True
# #         )
        
# #         st.plotly_chart(fig_gender, use_container_width=True)

# with colo2:
#     #Durée Moyenne
#     contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
#     fig = px.bar(
#         contract_duration,
#         x=contract_duration.index,
#         y=contract_duration.values,
#         title="Durée moyenne des contrats par type",
#         labels={'x': 'Type de contrat', 'y': 'Durée moyenne (mois)'}
#     )
#     st.plotly_chart(fig, use_container_width=True)

# st.divider()

# colon1, colon2 = st.columns(2, gap='large')

# filtered_data_inseres = filtered_data[filtered_data['REMUNERATION'].notna() & (filtered_data['REMUNERATION'] > 0)]

# with colon1:
#     # Création de l'histogramme des rémunérations des apprenants insérés
#     # Réduire le nombre de bins pour des barres plus larges
#     fig = px.histogram(
#         filtered_data_inseres,
#         x='REMUNERATION',
#         nbins=8,  
#         title="Distribution des rémunérations",
#         labels={'REMUNERATION': 'Rémunération (FCFA)'},
#         color_discrete_sequence=['#FF7F0E'],
#         text_auto=True
#     )
    
#     fig.update_traces(
#         marker_line_color='white',
#         marker_line_width=1.5,
#         opacity=0.9,
#         marker=dict(line=dict(width=2))  # Augmenter la largeur de la bordure des barres
#     )
    
#     # Personnalisation du layout
#     fig.update_layout(
#         title=dict(
#             text="📈 Distribution des rémunérations",
#             font=dict(size=14, color="#333", family="Arial"),
#             x=0.5,
#             xanchor="center"  # Centrer le titre
#         ),
#         xaxis=dict(
#             title="Rémunération (FCFA)",
#             titlefont=dict(size=16, color="#333"),
#             tickfont=dict(size=14),
#             gridcolor="lightgrey"
#         ),
#         yaxis=dict(
#             title="Nombre d'apprenants",
#             titlefont=dict(size=16, color="#333"),
#             tickfont=dict(size=14),
#             gridcolor="lightgrey"
#         ),
#         plot_bgcolor="white",
#         bargap=0.1,  # Ajuster cette valeur pour contrôler l'espacement entre les barres
#     )
    
#     # Affichage du graphique
#     st.plotly_chart(fig, use_container_width=True)

# with colon2:
#     if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
#         # Filtrer les données avant la conversion pour éliminer les lignes problématiques
#         filtered_data = filtered_data[~filtered_data['DATEDEPRISEDESERVICE'].isna()]
        
#         # Vérifier le format de date réel
#         sample_date = filtered_data['DATEDEPRISEDESERVICE'].iloc[0] if len(filtered_data) > 0 else None
        
#         # Convertir la colonne de date avec le format DD/MM/YY
#         try:
#             filtered_data['DATEDEPRISEDESERVICE'] = pd.to_datetime(
#                 filtered_data['DATEDEPRISEDESERVICE'], 
#                 format='%d/%m/%y',  # Format "02/09/24"
#                 errors='coerce'
#             )
#         except Exception as e:
#             st.warning(f"Erreur lors de la conversion des dates: {e}")
#             # Essayer un format alternatif
#             try:
#                 filtered_data['DATEDEPRISEDESERVICE'] = pd.to_datetime(
#                     filtered_data['DATEDEPRISEDESERVICE'], 
#                     errors='coerce'
#                 )
#             except:
#                 st.error("Impossible de convertir les dates.")
        
#         # Filtrer les dates invalides
#         filtered_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'].notna()]
        
#         # Vérifier les dates futures
#         today = pd.Timestamp.now()
#         filtered_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'] <= today]
        
#         # Filtrer les données pour ne garder que les apprenants insérés
#         time_data = filtered_data[filtered_data['STATUT'] == 'INSERE']
        
#         if len(time_data) > 0:
#             # Créer une période mensuelle
#             time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
            
#             # Compter le nombre d'apprenants par mois
#             evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
            
#             # Convertir en datetime pour l'affichage
#             evolution_data['MONTH_YEAR'] = pd.to_datetime(evolution_data['MONTH_YEAR'].astype(str))
            
#             # Créer un libellé en français
#             try:
#                 locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
#             except:
#                 try:
#                     locale.setlocale(locale.LC_TIME, 'fra')
#                 except:
#                     pass
                    
#             evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y')
#             evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR_FR'].str.capitalize()
            
#             # Trier par ordre chronologique
#             evolution_data = evolution_data.sort_values('MONTH_YEAR')
            
#             # Créer le graphique
#             fig = px.line(
#                 evolution_data,
#                 x='MONTH_YEAR_FR',
#                 y='Nombre',
#                 title="Évolution des apprenants insérés au fil du temps",
#                 labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
#                 markers=True,
#                 color_discrete_sequence=['#1E90FF']
#             )
            
#             # Ajouter les valeurs sur chaque point avec texte noir
#             fig.update_traces(
#                 text=evolution_data['Nombre'], 
#                 textposition='top center',
#                 textfont=dict(color='black', size=14, family="Arial Bold"),  # Texte noir et plus gras
#                 mode='lines+markers+text',
#                 line=dict(width=3),
#                 marker=dict(size=10)
#             )
            
#             # Personnaliser la mise en page
#             fig.update_layout(
#                 title=dict(
#                     text="📈 Évolution des apprenants insérés",
#                     font=dict(size=14, color="#333", family="Arial"),
#                     x=0.5,
#                     xanchor="center"
#                 ),
#                 xaxis=dict(
#                     title="Mois et Année",
#                     titlefont=dict(size=16, color="#333"),
#                     tickangle=45,
#                     tickfont=dict(size=12),
#                     # Forcer l'ordre des catégories
#                     categoryorder='array',
#                     categoryarray=evolution_data['MONTH_YEAR_FR'].tolist()
#                 ),
#                 yaxis=dict(
#                     title="Nombre d'apprenants",
#                     titlefont=dict(size=16, color="#333"),
#                     tickfont=dict(size=14),
#                     tickformat='d',
#                     gridcolor="lightgrey"
#                 ),
#                 plot_bgcolor="white",
#                 height=500
#             )
            
#             # Afficher le graphique
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("Aucune donnée valide trouvée après filtrage des dates.")
#     else:
#         st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible.")
# # Filtrer uniquement les apprenants insérés
# # Filtrer uniquement les apprenants insérés
# filtered_data_inseres = filtered_data[filtered_data['STATUT'] == 'INSERE']

# # Comptage des bénéficiaires insérés par structure
# structure_count = filtered_data_inseres['ENTREPRISES'].value_counts()

# # Créer le graphique à barres
# fig = px.bar(
#     x=structure_count.index, 
#     y=structure_count.values, 
#     title="Répartition des bénéficiaires insérés par structure", 
#     labels={'x': 'Structure', 'y': 'Nombre de bénéficiaires insérés'},
#     text=structure_count,  
# )

# # Personnalisation des traces
# fig.update_traces(
#     marker_color=px.colors.qualitative.Vivid,  # Palette de couleurs vibrantes
#     textposition='outside',  # Position du texte à l'extérieur des barres
#     textfont=dict(color='black', size=14, family="Arial Bold"),  # Texte en noir et en gras
#     hovertemplate="<b>Structure:</b> %{x}<br><b>Nombre de bénéficiaires:</b> %{y}<extra></extra>"
# )

# # Personnalisation du layout
# fig.update_layout(
#     title=dict(
#         text="📈 Répartition des bénéficiaires insérés par structure",
#         font=dict(size=24, color="#333", family="Arial"),
#         x=0.5,  
#         xanchor="center" 
#     ),
#     xaxis=dict(
#         title="Structure",
#         tickangle=45,  # Angle des étiquettes pour éviter le chevauchement
#         tickfont=dict(size=12)
#     ),
#     yaxis=dict(
#         title="Nombre de bénéficiaires insérés",
#         gridcolor="lightgrey",
#         range=[0, structure_count.values.max() * 1.2],  # Ajouter un peu d'espace au-dessus de la barre la plus haute
#     ),
#     plot_bgcolor="white", 
#     bargap=0.2,  # Espacement entre les barres
# )

# # Afficher le graphique dans Streamlit
# st.plotly_chart(fig, use_container_width=True)





# filtered_data_inseres = filtered_data[filtered_data['STATUT'] == 'INSERE']

# # Répartition des postes
# filtered_data_inseres = filtered_data_inseres[filtered_data_inseres['INTITULEPOSTE'].notna()]


# post_count = filtered_data_inseres['INTITULEPOSTE'].value_counts().head(10)

# # Créer le graphique
# fig = px.bar(
#     post_count, 
#     x=post_count.index, 
#     y=post_count.values, 
#     title="Top 10 des postes occupés par les apprenants insérés", 
#     labels={'x': 'Postes', 'y': 'Nombre'},
#     color=post_count.values, 
#     color_continuous_scale='Viridis',
#     text=post_count.values  
# )

# # Personnalisation du layout pour les postes
# fig.update_layout(
#     title=dict(
#         text="📈 Top 10 des postes occupés par les apprenants insérés",
#         font=dict(size=24, color="#333", family="Arial"),
#         x=0.5,  
#         xanchor="center"
#     ),
#     xaxis=dict(
#         title="Postes",
#         tickangle=-45,
#         tickfont=dict(size=12)
#     ),
#     yaxis=dict(
#         title="Nombre d'apprenants insérés",
#         gridcolor="lightgrey"
#     ),
#     plot_bgcolor="white"
# )

# # Personnalisation des barres et des textes
# fig.update_traces(
#     textposition="outside",  
#     textfont=dict(color="black", size=14),  
#     hovertemplate="<b>Poste occupé:</b> %{x}<br><b>Nombre:</b> %{y}<extra></extra>"
# )

# # Afficher le graphique
# st.plotly_chart(fig, use_container_width=True)

# # Répartition des entreprises pour les apprenants insérés

# # st.subheader("Nombre d'apprenants insérés par entreprise")
# company_count = filtered_data_inseres['ENTREPRISES'].value_counts()

# fig = px.bar(
#     x=company_count.index,
#     y=company_count.values,
#     title="Nombre d'apprenants insérés par entreprise",
#     labels={'x': 'Entreprise', 'y': 'Nombre d\'apprenants insérés'},
#     text=company_count.values,  
#     color_discrete_sequence=px.colors.sequential.Viridis 
# )

# fig.update_traces(
#     marker_line_color='white',  
#     marker_line_width=1.5,  
#     opacity=0.9,  
#     textposition="outside"  
# )

# fig.update_layout(
#     title=dict(
#         text="📈 Nombre d'apprenants insérés par entreprise",
#         font=dict(size=24, color="#333", family="Arial"),
#         x=0.5,  
#         xanchor="center"
#     ),
#     xaxis=dict(
#         title="Entreprise",
#         titlefont=dict(size=16, color="#333"),
#         tickfont=dict(size=14),
#         tickangle=-45,  
#         gridcolor="lightgrey"
#     ),
#     yaxis=dict(
#         title="Nombre d'apprenants insérés",
#         titlefont=dict(size=16, color="#333"),
#         tickfont=dict(size=14),
#         gridcolor="lightgrey"
#     ),
#     plot_bgcolor="white",  
#     bargap=0.15 
# )

# st.plotly_chart(fig, use_container_width=True)

# # Afficher le nombre total d'apprenants insérés
# #st.write(f"Nombre total d'apprenants insérés : {len(filtered_data_inseres)}") 


# # # ======= MAIN APPLICATION =======
# # def main():
# #     try:
# #         st.title("📊 SUIVI INSERTION DE LA PROMOTION 6")
        
# #         # Configuration du thème Plotly
# #         px.defaults.template = "plotly_dark"
        
# #         # Chargement des styles CSS si nécessaire
# #         try:
# #             with open("styles.css") as f:
# #                 st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# #         except FileNotFoundError:
# #             pass
        
# #         # Style global de l'application
# #         st.markdown(
# #             """
# #             <style>
# #                 .css-18e3th9 {background-color: #1a1a1a;}
# #                 .css-10trblm {color: #ffffff;}
# #                 .css-12ttj6m {color: #ffffff;}
# #             </style>
# #             """,
# #             unsafe_allow_html=True,
# #         )
        
# #         # Chargement des données depuis Google Sheets
# #         df = charger_donnees()
        
# #         # Vérifier si les données ont été chargées avec succès
# #         if df.empty:
# #             st.warning("Aucune donnée n'a pu être chargée. Veuillez vérifier votre connexion Google Sheets.")
# #             # Afficher un bouton pour réessayer
# #             if st.button("Réessayer de charger les données"):
# #                 st.cache_data.clear()
# #                 st.experimental_rerun()
# #             return
        
# #         # Prétraitement des données
# #         df = preprocess_data(df)
        
# #         # Barre de recherche d'étudiant
# #         st.sidebar.header("Rechercher un étudiant")
# #         search_input = st.sidebar.text_input("Entrez le numéro de téléphone ou l'e-mail :")
        
# #         # Vérifier si une recherche est effectuée
# #         if search_input:
# #             filtered_students = df[
# #                 (df['NDETELEPHONE'].astype(str).str.contains(search_input, case=False, na=False)) |
# #                 (df['EMAIL'].str.contains(search_input, case=False, na=False))
# #             ]
        
# #             # Affichage des résultats
# #             if not filtered_students.empty:
# #                 st.subheader("Informations Apprenant")
        
# #                 # Parcourir les étudiants trouvés et afficher leurs informations
# #                 for _, student_data in filtered_students.iterrows():
# #                     student_data = student_data.fillna("Non spécifié")
        
# #                     st.markdown(
# #                         f"""
# #                         <div style="background-color: #cfe5f1; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px;">
# #                             <h4 style="color: #001728;"><center>{student_data['NOM']} {student_data['PRENOM']}</center></h4>
# #                             <ul style="color: #001728;">
# #                                 <li><strong>Numéro de Téléphone :</strong> {student_data['NDETELEPHONE']}</li>
# #                                 <li><strong>E-mail :</strong> {student_data['EMAIL']}</li>
# #                                 <li><strong>Poste occupé :</strong> {student_data['INTITULEPOSTE']}</li>
# #                                 <li><strong>Entreprise :</strong> {student_data['ENTREPRISES']}</li>
# #                                 <li><strong>Type de contrat :</strong> {student_data['TYPEDECONTRAT']}</li>
# #                                 <li><strong>Rémunération :</strong> {student_data['REMUNERATION']} FCFA</li>
# #                                 <li><strong>Durée du contrat :</strong> {student_data['DUREEMOIS']} Mois</li>
# #                                 <li><strong>Statut actuel :</strong> {'En poste' if student_data['STATUTACTUELenposteounon'] == 'OUI' else 'Non en poste'}</li>
# #                             </ul>
# #                         </div>
# #                         """,
# #                         unsafe_allow_html=True
# #                     )
# #             else:
# #                 st.error("Aucun étudiant trouvé.")
        
# #         # Filtres interactifs
# #         st.sidebar.header("Filtres interactifs")
        
# #         selected_domains = st.sidebar.multiselect(
# #             "Filtrer par domaine de formation", 
# #             options=df['DOMAINEFORMATION'].dropna().unique().tolist(),
# #             default=[]
# #         )
        
# #         selected_companies = st.sidebar.multiselect(
# #             "Filtrer par entreprise", 
# #             options=df['ENTREPRISES'].dropna().unique().tolist(),
# #             default=[]
# #         )
        
# #         selected_statuses = st.sidebar.multiselect(
# #             "Filtrer par statut", 
# #             options=["En poste", "Non en poste"],
# #             default=[]
# #         )
        
# #         selected_contracts = st.sidebar.multiselect(
# #             "Filtrer par type de contrat", 
# #             options=df['TYPEDECONTRAT'].dropna().unique().tolist(),
# #             default=[]
# #         )
        
# #         # Ajouter un bouton pour rafraîchir les données
# #         if st.sidebar.button("Rafraîchir les données"):
# #             st.cache_data.clear()
# #             st.experimental_rerun()
        
# #         filtered_data = df.copy()
        
# #         if selected_domains:
# #             filtered_data = filtered_data[filtered_data['DOMAINEFORMATION'].isin(selected_domains)]
        
# #         if selected_companies:
# #             filtered_data = filtered_data[filtered_data['ENTREPRISES'].isin(selected_companies)]
        
# #         if selected_statuses:
# #             status_values = ["OUI" if status == "En poste" else "NON" for status in selected_statuses]
# #             filtered_data = filtered_data[filtered_data['STATUTACTUELenposteounon'].isin(status_values)]
        
# #         if selected_contracts:
# #             filtered_data = filtered_data[filtered_data['TYPEDECONTRAT'].isin(selected_contracts)]
        
# #         # Logo dans la barre latérale
# #         try:
# #             st.sidebar.image("data/logo.jpg", caption="Logo de l'organisation")
# #         except FileNotFoundError:
# #             pass
        
# #         # Formulaire d'ajout d'étudiant
# #         if "show_form" not in st.session_state:
# #             st.session_state.show_form = False
            
# #         if st.button("Ajouter un nouvel apprenant"):
# #             st.session_state.show_form = not st.session_state.show_form
        
# #         if st.session_state.show_form:
# #             st.write("## Formulaire d'ajout")
# #             add_data()
        
# #         # Affichage des KPI
# #         kpi(filtered_data)
        
# #         # Ne pas montrer le DataFrame brut en production
# #         # st.write(df.head())

# #         st.divider()
# #         st.subheader("Aperçus des données filtrées")
# #         st.dataframe(filtered_data.head())
# #         st.divider()
        
# #         # Visualisations - première ligne
# #         colo1, colo2 = st.columns(2, gap="large")
# #         with colo1:
# #             # Vérifier si des données sont disponibles
# #             if filtered_data.empty or 'TYPEDECONTRAT' not in filtered_data.columns:
# #                 st.warning("Aucune donnée disponible pour la répartition des types de contrats.")
# #             else:
# #                 contract_count = filtered_data['TYPEDECONTRAT'].value_counts()
# #                 if contract_count.empty:
# #                     st.warning("Aucun type de contrat disponible pour l'analyse.")
# #                 else:
# #                     # Création du diagramme circulaire
# #                     fig = go.Figure(data=[go.Pie(
# #                         labels=contract_count.index,
# #                         values=contract_count.values,
# #                         hole=0,  
# #                         marker=dict(
# #                             colors=px.colors.qualitative.Set2, 
# #                             line=dict(color='white', width=2)
# #                         ),
# #                         textinfo='percent',  
# #                         insidetextorientation='radial',
# #                         hoverinfo='label+percent+value'
# #                     )])
                
# #                     # Mise en page pour séparer la légende
# #                     fig.update_layout(
# #                         title=dict(
# #                             text="📈 Répartition des types de contrats",
# #                             font=dict(size=18, color="#2c3e50", family="Arial"),
# #                             x=0.5,
# #                             xanchor="center"
# #                         ),
# #                         showlegend=True,  
# #                         legend=dict(
# #                             orientation="h",  
# #                             yanchor="bottom",
# #                             y=-0.3,  
# #                             xanchor="center",
# #                             x=0.5,
# #                             font=dict(size=14)
# #                         ),
# #                         margin=dict(t=50, b=100),  
# #                     )
                
# #                     st.plotly_chart(fig, use_container_width=True) 
        
# #         with colo2:
# #             #Durée Moyenne
# #             if filtered_data.empty or 'TYPEDECONTRAT' not in filtered_data.columns or 'DUREEMOIS' not in filtered_data.columns:
# #                 st.warning("Aucune donnée disponible pour la durée moyenne des contrats.")
# #             else:
# #                 contract_duration = filtered_data.groupby('TYPEDECONTRAT')['DUREEMOIS'].mean().sort_values()
# #                 if contract_duration.empty:
# #                     st.warning("Données insuffisantes pour calculer la durée moyenne des contrats.")
# #                 else:
# #                     fig = px.bar(
# #                         contract_duration,
# #                         x=contract_duration.index,
# #                         y=contract_duration.values,
# #                         title="Durée moyenne des contrats par type",
# #                         labels={'x': 'Type de contrat', 'y': 'Durée moyenne (mois)'}
# #                     )
# #                     st.plotly_chart(fig, use_container_width=True)
        
# #         st.divider()
        
# #         # Visualisations - deuxième ligne
# #         colon1, colon2 = st.columns(2, gap='large')
# #         with colon1:
# #             #Rémuneration
# #             if filtered_data.empty or 'REMUNERATION' not in filtered_data.columns:
# #                 st.warning("Aucune donnée disponible pour l'analyse des rémunérations.")
# #             else:
# #                 fig = px.histogram(
# #                     filtered_data,
# #                     x='REMUNERATION',
# #                     nbins=20,  
# #                     title="Distribution des rémunérations",
# #                     labels={'REMUNERATION': 'Rémunération (FCFA)'},
# #                     color_discrete_sequence=['#FF7F0E'],  
# #                     text_auto=True
# #                 )
            
# #                 fig.update_traces(
# #                     marker_line_color='white',  
# #                     marker_line_width=1.5,  
# #                     opacity=0.9  
# #                 )
            
# #                 # Personnalisation du layout
# #                 fig.update_layout(
# #                     title=dict(
# #                         text="📈 Distribution des rémunérations",
# #                         font=dict(size=16, color="#cfe5f1", family="Arial"), 
# #                         x=0.5,  
# #                         xanchor="right" 
# #                     ),
# #                     xaxis=dict(
# #                         title="Rémunération (FCFA)",  
# #                         titlefont=dict(size=16, color="#333"),  
# #                         tickfont=dict(size=14),
# #                         gridcolor="lightgrey"  
# #                     ),
# #                     yaxis=dict(
# #                         title="Nombre d'apprenants",  
# #                         titlefont=dict(size=16, color="#333"),  
# #                         tickfont=dict(size=14),  
# #                         gridcolor="lightgrey"  
# #                     ),
# #                     plot_bgcolor="white", 
# #                     bargap=0.1, 
# #                 )
            
# #                 st.plotly_chart(fig, use_container_width=True)
        
# #         with colon2:
# #             if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
# #                 time_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'].notna()]
# #                 time_data = time_data[time_data['STATUTACTUELenposteounon'] == 'OUI']
                
# #                 if not time_data.empty:
# #                     time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
# #                     evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
# #                     evolution_data['MONTH_YEAR'] = pd.to_datetime(evolution_data['MONTH_YEAR'].astype(str))
                    
# #                     try:
# #                         locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8') 
# #                     except locale.Error:
# #                         try:
# #                             locale.setlocale(locale.LC_TIME, 'fra')  
# #                         except locale.Error:
# #                             st.warning("Impossible de configurer la locale en français. Les mois resteront en anglais.")
                    
# #                     evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y')
# #                     evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR_FR'].str.capitalize()
                    
# #                     evolution_data = evolution_data.sort_values('MONTH_YEAR')
        
# #                     fig = px.line(
# #                         evolution_data, 
# #                         x='MONTH_YEAR_FR', 
# #                         y='Nombre', 
# #                         title="Évolution des apprenants en poste au fil du temps",
# #                         labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
# #                         markers=True
# #                     )
                    
# #                     fig.update_traces(text=evolution_data['Nombre'], textposition='top center')
        
# #                     fig.update_layout(
# #                         xaxis=dict(tickangle=45),
# #                         xaxis_title="Mois et Année",
# #                         yaxis_title="Nombre d'apprenants",
# #                         yaxis=dict(tickformat='d'), 
# #                     )
                    
# #                     st.plotly_chart(fig, use_container_width=True)
# #                 else:
# #                     st.warning("Aucune donnée disponible pour l'évolution temporelle.")
# #             else:
# #                 st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")
        
# #         # Répartition des bénéficiaires par structure
# #         if filtered_data.empty or 'STRUCTUREDIRECTIONPOLE' not in filtered_data.columns:
# #             st.warning("Aucune donnée disponible pour la répartition par structure.")
# #         # else:
# #         #     structure_count = filtered_data['STRUCTUREDIRECTIONPOLE'].value_counts()
# #         #     if structure_count.empty

# #     except Exception as e:
# #         st.error(f"Une erreur s'est produite : {str(e)}")


# # if __name__ == "__main__":
# #     main()
