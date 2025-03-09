import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Configuration Google Sheets
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "eighth-jigsaw-446022-r0-638d8f86d788.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1oNQc5xQO4bRj72v50po6Qg95jZzXp3VhBxyi7edx_ZY"

@st.cache_data(ttl=300)
def charger_donnees():
    try:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(SPREADSHEET_URL).worksheet("Feuil1")

        # Récupérer les données en précisant la ligne des en-têtes (3ᵉ ligne)
        data = sheet.get_all_records(head=3)

        if not data:
            st.warning("Aucune donnée trouvée dans la feuille Google Sheets.")
            return pd.DataFrame()

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Tester l'affichage des données
df = charger_donnees()
st.write("📊 **Aperçu des données chargées :**", df)
