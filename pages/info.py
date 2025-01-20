import streamlit as st
import pandas as pd
import locale


def promo6():
    
    global_data = pd.read_excel('SUIVI_GLOBAL_P6.xlsx', engine='openpyxl', skiprows=2)
    st.header("📌 INDICATEURS CLES DE LA PROMOTION 6")
    # CSS pour forcer les colonnes à avoir une largeur identique
    st.markdown(
        """
        <style>
        /* Styles pour les colonnes */
        .stColumns > div {
            width: 100% !important;
            padding: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


  
    # Calcul des KPI globaux
    total_students = len(global_data)
    female_students = len(global_data[global_data['SEXE'] == 'F']) if 'SEXE' in global_data.columns else 0
    male_students = len(global_data[global_data['SEXE'] == 'H']) if 'SEXE' in global_data.columns else 0
    feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0
    masculinization_rate = (male_students / total_students * 100) if total_students > 0 else 0

    # Configuration de la localisation pour les nombres
    try:
        locale.setlocale(locale.LC_ALL, 'French_France.1252')
    except locale.Error:
        print("La locale spécifiée n'est pas supportée sur ce système.")

    # Template HTML/CSS pour les KPI
    kpi_template = """
        <div style="
            background-color: {bg_color};
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            width: 100%;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
            <div style="font-size: 20px; font-weight: normal;">{title}</div>
            <div style="font-size: 36px; margin-top: 10px;">{value}</div>
        </div>
        """
   
    # Première ligne avec 3 colonnes
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(kpi_template.format(
        bg_color="#2196F3", icon="👨‍🎓", title="Nombre total d'apprenants", value=total_students),
        unsafe_allow_html=True)


    with col2:
        st.markdown(kpi_template.format(
            bg_color="#9C27B0",icon = "👨", title="Taux de féminisation", value=f"{feminization_rate:.2f} %"),
            unsafe_allow_html=True)

    with col3:
        st.markdown(kpi_template.format(
            bg_color="#4CAF50",icon = "👩‍🦰", title="Taux de masculinisation      ", value=f"{masculinization_rate:.2f} %"),
            unsafe_allow_html=True)

def promo5():
    st.header("📌 INDICATEURS CLES DE LA PROMOTION 5")
    global_data = pd.read_excel('SUIVI_GLOBAL_P5.xlsx', engine='openpyxl', skiprows=1)
    st.markdown(
        """
        <style>
        /* Styles pour les colonnes */
        .stColumns > div {
            width: 100% !important;
            padding: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # Calcul des KPI globaux
    total_students = len(global_data)
    female_students = len(global_data[global_data['SEXE'] == 'F']) if 'SEXE' in global_data.columns else 0
    male_students = len(global_data[global_data['SEXE'] == 'M']) if 'SEXE' in global_data.columns else 0
    feminization_rate = (female_students / total_students * 100) if total_students > 0 else 0
    masculinization_rate = (male_students / total_students * 100) if total_students > 0 else 0

    # Configuration de la localisation pour les nombres
    try:
        locale.setlocale(locale.LC_ALL, 'French_France.1252')
    except locale.Error:
        print("La locale spécifiée n'est pas supportée sur ce système.")

    # Template HTML/CSS pour les KPI
    kpi_template = """
    <div style="
        background-color: {bg_color};
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        color: #2196F3;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        width: 100%;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid #2196F3; 
    ">
        <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
        <div style="font-size: 30px; font-weight: normal;">{title}</div>
        <div style="font-size: 46px; margin-top: 10px;">{value}</div>
    </div>
    """

    # Première ligne avec 3 colonnes
    col1, col2, col3 = st.columns(3, gap="large")

    st.markdown(kpi_template.format(
    bg_color="transparent", icon="👨‍🎓", title="Nombre total d'apprenants", value=total_students),
    unsafe_allow_html=True)


    # with col2:
    #     st.markdown(kpi_template.format(
    #         bg_color="#9C27B0",icon = "👨", title="Taux de féminisation", value=f"{feminization_rate:.2f} %"),
    #         unsafe_allow_html=True)

    # with col3:
    #     st.markdown(kpi_template.format(
    #         bg_color="#4CAF50",icon = "👩‍🦰", title="Taux de masculinisation      ", value=f"{masculinization_rate:.2f} %"),
    #         unsafe_allow_html=True)
        
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    labels = ['Féminin', 'Masculin']
    sizes = [female_students, male_students]
    colors = ['#FF99CC', '#99CCFF']
    explode = (0.1, 0)  
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
    ax.axis('equal')  

    st.pyplot(fig)

    st.markdown("### Taux de féminisation")
    st.progress(int(feminization_rate))
    st.markdown("### Taux de masculinisation")
    st.progress(int(masculinization_rate))



def about_page():
    st.header("A propos")
    # st.image("data/logo.jpg")
    promo6()
    st.divider()  
    promo5()


about_page()