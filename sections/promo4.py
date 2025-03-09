# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.io as pio
# import matplotlib as plt
# import locale
# import plotly.graph_objects as go
# import gspread
# from google.oauth2.service_account import Credentials


# df = pd.read_excel('SUIVI GLOBAL P6.xlsx', engine='openpyxl', skiprows=2)


# def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
#     # Suppression des caractères spéciaux dans les noms de colonnes
#     df.columns = df.columns.str.replace('[^a-zA-Z]', '', regex=True)

#     # Conversion des colonnes en chaînes pour éviter les erreurs de conversion
#     for col in ['CIN', 'NDETELEPHONE', 'EMAIL']:
#         if col in df.columns:
#             df[col] = df[col].astype(str)

#     # Conversion des colonnes en dates
#     if 'DATEDENAISSANCE' in df.columns:
#         df['DATEDENAISSANCE'] = pd.to_datetime(df['DATEDENAISSANCE'], errors='coerce')
#     if 'DATEDEPRISEDESERVICE' in df.columns:
#         df['DATEDEPRISEDESERVICE'] = pd.to_datetime(df['DATEDEPRISEDESERVICE'], errors='coerce')

#     # Colonnes sensibles : ne pas remplir les valeurs manquantes
#     sensitive_columns = [
#         'INTITULEPOSTE', 
#         'LIEUDENAISSANCE', 
#         'SITUATIONSOCIOPROFESSIONNELlinscription',
#         'STRUCTUREDIRECTIONPOLE', 
#         'ENTREPRISES', 
#         'TYPEDECONTRAT', 
#         'STATUTACTUELenposteounon'
#     ]
#     for col in sensitive_columns:
#         if col in df.columns:
#             # Ne pas remplir les valeurs manquantes dans ces colonnes
#             df[col] = df[col]

#     # Remplissage des valeurs manquantes avec des valeurs fixes pour d'autres colonnes
#     columns_fixed = {
#         'ADRESSE': 'Non spécifié',
#         'CONTACTDURGENCE': 'Non fourni',
#         'STATUTMATRIMONIALE': 'Non spécifié',
#         'PROFILAGE': 'Non défini',
#         'COMMENTAIRE': 'Aucun commentaire',
#         'CONTACTENTREPRISE': 'Non précisé'
#     }
#     for col, value in columns_fixed.items():
#         if col in df.columns:
#             df[col] = df[col].fillna(value)

#     # Colonnes numériques : remplissage avec 0
#     if 'REMUNERATION' in df.columns:
#         df['REMUNERATION'] = pd.to_numeric(df['REMUNERATION'], errors='coerce').fillna(0)
    
#     if 'DUREEMOIS' in df.columns:
#         df['DUREEMOIS'] = pd.to_numeric(df['DUREEMOIS'], errors='coerce').fillna(0)

#     return df

# # Appliquer la fonction preprocess_data
# df = preprocess_data(df)

# # Afficher les colonnes disponibles pour vérifier leur type
# print(df.dtypes)

# # Réparer automatiquement les colonnes non compatibles avec Streamlit
# df = df.convert_dtypes()





# st.subheader("📊 SUIVI INSERTION DE LA PROMOTION 6")


# px.defaults.template = "plotly_dark"  


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

# # st.write("Résultats filtrés :")
# # st.dataframe(filtered_data)

# st.sidebar.image("data/logo.jpg", caption="Logo de l'organisation")



# def kpi():
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

#     # avg_salary = filtered_data['REMUNERATION'].mean() if 'REMUNERATION' in filtered_data.columns else 0
#     total_students = len(filtered_data)
#     active_students = len(filtered_data[filtered_data['STATUTACTUELenposteounon'] == 'OUI']) if 'STATUTACTUELenposteounon' in filtered_data.columns else 0
#     # insertion_rate = (active_students / total_students * 100) if total_students > 0 else 0

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
#         print("La locale spécifiée n'est pas supportée sur ce système.")

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
#             bg_color = "#FF5722"  # Rouge pour un taux inférieur à 50 %
#         else:
#             bg_color = "#4CAF50"  # Vert pour un taux supérieur ou égal à 50 %

#         # Afficher le KPI avec la couleur conditionnelle
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

# #kpi()

# #st.subheader("Gestion des apprenants", divider='rainbow')
# if "show_form" not in st.session_state:
#     st.session_state.show_form = False
    
# if st.button("Ajouter un nouvel apprenant"):
#     st.session_state.show_form = not st.session_state.show_form  # Basculer l'état

# if st.session_state.show_form:
#     st.write("## Formulaire d'ajout")
#     from add_data import *
#     add_data() 
# kpi()


# st.divider()
# st.subheader("Aperçus des données filtrées")
# st.dataframe(filtered_data.head())
# st.divider()
# colo1, colo2 = st.columns(2, gap="large")
# with colo1:
#     contract_count = filtered_data['TYPEDECONTRAT'].value_counts()

#     # Création du diagramme circulaire complet
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

#     # Mise en page pour séparer la légende
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
# with colon1:
#     #Rémuneration
#     fig = px.histogram(
#         filtered_data,
#         x='REMUNERATION',
#         nbins=20,  
#         title="Distribution des rémunérations ",
#         labels={'REMUNERATION': 'Rémunération (FCFA)'},
#         color_discrete_sequence=['#FF7F0E'],  
#         text_auto=True
#     )

#     fig.update_traces(
#         marker_line_color='white',  
#         marker_line_width=1.5,  
#         opacity=0.9  
#     )

#     # Personnalisation du layout
#     fig.update_layout(
#         title=dict(
#             text="📈 Distribution des rémunérations ",
#             font=dict(size=16, color="#cfe5f1", family="Arial"), 
#             x=0.5,  
#             xanchor="right" 
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
#         bargap=0.1, 
#     )


#     # Affichage du graphique
#     st.plotly_chart(fig, use_container_width=True)

# with colon2:
#     #st.subheader("📈 Évolution temporelle des apprenants en poste")
#     if 'DATEDEPRISEDESERVICE' in filtered_data.columns:
#         time_data = filtered_data[filtered_data['DATEDEPRISEDESERVICE'].notna()]
#         time_data = time_data[time_data['STATUTACTUELenposteounon'] == 'OUI']
        
#         time_data['MONTH_YEAR'] = time_data['DATEDEPRISEDESERVICE'].dt.to_period('M')
#         evolution_data = time_data.groupby('MONTH_YEAR').size().reset_index(name='Nombre')
#         evolution_data['MONTH_YEAR'] = pd.to_datetime(evolution_data['MONTH_YEAR'].astype(str))
        
#         try:
#             locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8') 
#         except locale.Error:
#             try:
#                 locale.setlocale(locale.LC_TIME, 'fra')  
#             except locale.Error:
#                 st.warning("Impossible de configurer la locale en français. Les mois resteront en anglais.")
        

#         evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR'].dt.strftime('%B %Y')
#         evolution_data['MONTH_YEAR_FR'] = evolution_data['MONTH_YEAR_FR'].str.capitalize()  # Capitaliser la première lettre
        

#         evolution_data = evolution_data.sort_values('MONTH_YEAR')

#         fig = px.line(
#             evolution_data, 
#             x='MONTH_YEAR_FR', 
#             y='Nombre', 
#             title="Évolution des apprenants en poste au fil du temps",
#             labels={'MONTH_YEAR_FR': 'Mois et Année', 'Nombre': 'Nombre d\'apprenants'},
#             markers=True
#         )
        
#         fig.update_traces(text=evolution_data['Nombre'], textposition='top center')

#         fig.update_layout(
#             xaxis=dict(tickangle=45),
#             xaxis_title="Mois et Année",
#             yaxis_title="Nombre d'apprenants",
#             yaxis=dict(tickformat='d'), 
#         )
        
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.warning("La colonne `DATEDEPRISEDESERVICE` n'est pas disponible ou contient uniquement des valeurs manquantes.")



# # Comptage des bénéficiaires par structure
# structure_count = filtered_data['STRUCTUREDIRECTIONPOLE'].value_counts()
# title=dict(
#         text="📈 Répartition des types de contrats",
#         font=dict(size=24, color="#cfe5f1", family="Arial"),
#         x=0.5,
#         xanchor="right" 
#     ),
# fig = px.bar(
#     x=structure_count.index, 
#     y=structure_count.values, 
#     title=" Répartition des bénéficiaires par structure", 
#     labels={'x': 'Structure', 'y': 'Nombre'},
#     text=structure_count, 
    
# )


# fig.update_traces(
#     marker_color=px.colors.qualitative.Vivid,  
#     texttemplate='%{text}',  
#     textposition='outside',  
# )

# # Personnalisation du layout
# fig.update_layout(
#     title=dict(
#         text="📈 Répartition des bénéficiaires par structure",
#         font=dict(size=24, color="#cfe5f1", family="Arial"),
#         x=0.5,  
#         xanchor="right" 
#     ),
#     xaxis=dict(
#         title="Structure",
#         tickangle=45,  
#         tickfont=dict(size=12)
#     ),
#     yaxis=dict(
#         title="Nombre de bénéficiaires",
#         gridcolor="lightgrey",
#         range=[0, structure_count.values.max() * 1.2],  
#     ),
#     plot_bgcolor="white", 
#     bargap=0.2,  
# )


# st.plotly_chart(fig, use_container_width=True)




# # Répartition des postes 
# st.subheader("Répartition des postes occupés ")
# post_count = filtered_data['INTITULEPOSTE'].value_counts().head(10)  
# fig = px.bar(
#     post_count, 
#     x=post_count.index, 
#     y=post_count.values, 
#     title="Top 10 des postes occupés ", 
#     labels={'x': 'Postes', 'y': 'Nombre'},
#     color=post_count.values, 
#     color_continuous_scale='Viridis',
#     text=post_count
# )
# st.plotly_chart(fig, use_container_width=True)

# company_count = filtered_data['ENTREPRISES'].value_counts()


# fig = px.bar(
#     x=company_count.index,
#     y=company_count.values,
#     title="Nombre d'étudiants par entreprise",
#     labels={'x': 'Entreprise', 'y': 'Nombre d\'étudiants'},
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
#         text="📈Nombre d'étudiants par entreprise",
#         font=dict(size=24, color="#cfe5f1", family="Arial"),
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
#         title="Nombre d'étudiants",
#         titlefont=dict(size=16, color="#333"),
#         tickfont=dict(size=14),
#         gridcolor="lightgrey"
#     ),
#     plot_bgcolor="white",  
#     bargap=0.15 
# )


# st.plotly_chart(fig, use_container_width=True)

# # print(df.columns)

# # # fig = px.box(
# # #     filtered_data,
# # #     x='TYPEDECONTRAT',
# # #     y='REMUNERATION',
# # #     title="Distribution des rémunérations par type de contrat",
# # #     labels={'TYPEDECONTRAT': 'Type de contrat', 'REMUNERATION': 'Rémunération (FCFA)'},
# # #     color='TYPEDECONTRAT'
# # # )
# # # st.plotly_chart(fig, use_container_width=True)

# # heatmap_data = filtered_data.pivot_table(
# #     index='STRUCTUREDIRECTIONPOLE',
# #     columns='INTITULEPOSTE',
# #     values='NOM',  
# #     aggfunc='count',
# #     fill_value=0
# # )

# # # Evolution des rémunérations au fil du temps
# # if 'DATEDEPRISEDESERVICE' in filtered_data.columns and not filtered_data['DATEDEPRISEDESERVICE'].isna().all():
# #     # Convertir la date en année pour simplifier l'analyse
# #     filtered_data['AnneePriseService'] = filtered_data['DATEDEPRISEDESERVICE'].dt.year

# #     # Calculer la rémunération moyenne par année
# #     remuneration_by_year = filtered_data.groupby('AnneePriseService')['REMUNERATION'].mean().reset_index()

# #     # Tracer une courbe
# #     fig = px.line(
# #         remuneration_by_year,
# #         x='AnneePriseService',
# #         y='REMUNERATION',
# #         title="Évolution des rémunérations moyennes par année",
# #         labels={'AnneePriseService': 'Année', 'REMUNERATION': 'Rémunération moyenne (FCFA)'},
# #         markers=True
# #     )
# #     st.plotly_chart(fig, use_container_width=True)
# # else:
# #     st.warning("Les données de prise de service ne sont pas disponibles ou contiennent des valeurs manquantes.")


# # # # Aperçu des données
# # st.subheader("Aperçu des données 📋")
# # st.dataframe(df.head(), use_container_width=True)
# # 