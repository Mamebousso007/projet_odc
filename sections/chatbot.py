import random
import time
import streamlit as st
from openai import OpenAI
import os

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Assistant Dashboard P5 & P6",
    page_icon="📊",
    layout="centered"
)

# Chargement de la clé API
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.warning("⚠️ Veuillez configurer votre clé API OpenAI dans les variables d'environnement.")

# Base de connaissances locale pour les dashboards Promotion 5 et 6
knowledge_base = {
    "indicateurs clés": "Les principaux indicateurs suivis incluent le taux d'insertion professionnelle, la progression des apprenants et le taux de réussite.",
    "statistiques emploi": "Actuellement, 80% des apprenants de la Promotion 5 sont employés, tandis que 75% de la Promotion 6 sont en stage ou en emploi.",
    "taux d'abandon": "Le taux d'abandon pour la Promotion 5 est de 10%, et pour la Promotion 6, il est de 8%. Nous surveillons activement ces chiffres.",
    "évolution compétences": "Une évaluation des compétences est réalisée chaque trimestre pour mesurer la progression des apprenants et identifier les besoins d'accompagnement.",
    "projets en cours": "Les projets en cours pour la Promotion 5 incluent un partenariat avec des entreprises locales, tandis que la Promotion 6 travaille sur des simulations de recrutement.",
    "besoins entreprises": "Les entreprises recherchent principalement des compétences en gestion de projet, en communication et en analyse de données. Nous adaptons les formations en conséquence."
}

# Fonction pour appeler l'API OpenAI
def get_openai_response(prompt, history):
    try:
        client = OpenAI(api_key=API_KEY)
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception:
        return None  # Retourne None en cas d'échec

# Fonction de fallback
def fallback_response(prompt):
    for keyword, info in knowledge_base.items():
        if keyword in prompt.lower():
            return info
    return "Je suis désolé, je n'ai pas d'information spécifique sur ce sujet. Pouvez-vous reformuler votre question ?"

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour! Comment puis-je vous aider concernant les dashboards Promotion 5 et 6 ?"}]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie utilisateur
if prompt := st.chat_input("Posez votre question sur les dashboards P5 et P6..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        full_response = get_openai_response(prompt, st.session_state.messages[:-1])
        if not full_response:  
            full_response = fallback_response(prompt)
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Bouton pour réinitialiser
if st.button("Nouvelle conversation"):
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour! Comment puis-je vous aider concernant les dashboards Promotion 5 et 6 ?"}]
    st.experimental_rerun()
