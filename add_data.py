import streamlit as st
import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.replace('[^a-zA-Z]', '', regex=True)
    df['DATEDENAISSANCE'] = pd.to_datetime(df['DATEDENAISSANCE'], errors='coerce')
    df['DATEDEPRISEDESERVICE'] = pd.to_datetime(df['DATEDEPRISEDESERVICE'], errors='coerce')

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


def add_data():
    # Charger le fichier Excel
    df = pd.read_excel('SUIVI_GLOBAL_P5.xlsx', engine='openpyxl', skiprows=1)
    df = preprocess_data(df)

    # Formulaire
    with st.form("add_apprenant", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        nom = col1.selectbox("Nom", df["NOM"].unique())
        prenom = col2.selectbox("Prénom", df["PRENOM"].unique())
        ncin = col3.selectbox("NCIN", df["NCIN"].unique())
        sexe = col4.selectbox("Sexe", df["SEXE"].unique())

        col5, col6, col7, col8 = st.columns(4)
        age = col5.selectbox("Âge", df["AGE"].unique())
        datenaiss = col6.date_input(label="Date de naissance")
        lieu = col7.selectbox("Lieu de naissance", df["LIEUDENAISSANCE"].unique())
        adresse = col8.selectbox("Adresse", df["ADRESSE"].unique())

        col9, col10, col11, col12 = st.columns(4)
        email = col9.selectbox("Email", df["EMAIL"].unique())
        telephone = col10.selectbox("Téléphone", df["NDETELEPHONE"].unique())
        contacturg = col11.selectbox("Contact d'urgence", df["CONTACTDURGENCE"].unique())
        domaine = col12.selectbox("Domaine de formation", df["DOMAINEFORMATION"].unique())

        col13, col14, col15, col16 = st.columns(4)
        trancheage = col13.selectbox("Tranche d'âge", df["TRANCHESDAGE"].unique())
        situation = col14.selectbox("Situation socioprofessionnelle", df["SITUATIONSOCIOPROFESSIONNELlinscription"].unique())
        niveau = col15.selectbox("Niveau d'étude", df["NIVEAUDETUDElinscription"].unique())
        emploi = col16.selectbox("Emploi", df["EMPLOI"].unique())

        col17, col18, col19, col20 = st.columns(4)
        statutmatrimoniale = col17.selectbox("Statut matrimonial", df["STATUTMATRIMONIALE"].unique())
        profilage = col18.selectbox("Profilage", df["PROFILAGE"].unique())
        intituleposte = col19.selectbox("Intitulé du poste", df["INTITULEPOSTE"].unique())
        structure = col20.selectbox("Structure/Direction/Pôle", df["STRUCTUREDIRECTIONPOLE"].unique())

        col21, col22, col23, col24 = st.columns(4)
        entreprises = col21.selectbox("Entreprises", df["ENTREPRISES"].unique())
        statut = col22.selectbox("Statut", df["STATUT"].unique())
        typedcontrat = col23.selectbox("Type de contrat", df["TYPEDECONTRAT"].unique())
        datedprise = col24.selectbox("Date de prise de service", df["DATEDEPRISEDESERVICE"].unique())

        col25, col26, col27, col28 = st.columns(4)
        remuneration = col25.selectbox("Rémunération", df["REMUNERATION"].unique())
        dureemois = col26.selectbox("Durée (mois)", df["DUREEMOIS"].unique())
        contactentreprise = col27.selectbox("Contact entreprise", df["CONTACTENTREPRISE"].unique())
        statutactuel = col28.selectbox("Statut actuel (en poste ou non)", df["STATUTACTUELenposteounon"].unique())

        col29, col30, col31, col32 = st.columns(4)
        commentaire = col29.selectbox("Commentaire", df["COMMENTAIRE"].unique())
        pourmailing = col30.selectbox("Pour mailing", df["POURMAILING"].unique())

        btn = st.form_submit_button("Save Data To Excel", type="primary")

        if btn:
            if nom == "" or prenom == "" or ncin == "":
                st.warning("All fields are required")
                return False
            else:
                df = pd.concat([df, pd.DataFrame.from_records([{ 
                    'NOM': nom,
                    'PRENOM': prenom,
                    'NCIN': ncin,
                    'SEXE': sexe,
                    'AGE': age,
                    'DATEDENAISSANCE': datenaiss,
                    'LIEUDENAISSANCE': lieu,
                    'ADRESSE': adresse,
                    'EMAIL': email,
                    'NDETELEPHONE': telephone,
                    'CONTACTDURGENCE': contacturg,
                    'DOMAINEFORMATION': domaine,
                    'TRANCHESDAGE': trancheage,
                    'SITUATIONSOCIOPROFESSIONNELlinscription': situation,
                    'NIVEAUDETUDElinscription': niveau,
                    'EMPLOI': emploi,
                    'STATUTMATRIMONIALE': statutmatrimoniale,
                    'PROFILAGE': profilage,
                    'INTITULEPOSTE': intituleposte,
                    'STRUCTUREDIRECTIONPOLE': structure,
                    'ENTREPRISES': entreprises,
                    'STATUT': statut,
                    'TYPEDECONTRAT': typedcontrat,
                    'DATEDEPRISEDESERVICE': datedprise,
                    'REMUNERATION': remuneration,
                    'DUREEMOIS': dureemois,
                    'CONTACTENTREPRISE': contactentreprise,
                    'STATUTACTUELenposteounon': statutactuel,
                    'COMMENTAIRE': commentaire,
                    'POURMAILING': pourmailing
                }])])

                try:
                    # Nouveau fichier pour les données mises à jour
                    updated_file = "SUIVI_GLOBAL_P5_updated.xlsx"
                    df.to_excel(updated_file, index=False)
                    st.success(f"{nom} has been added successfully to {updated_file}!")
                except Exception as e:
                    st.warning(f"Unable to write, please close your dataset! ({e})")
                    return False

add_data()
