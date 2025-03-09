import streamlit as st


# --- PAGE SETUP ---
Information = st.Page(
    "sections/info.py",
    title="A propos",
    icon=":material/account_circle:",
    default=True,
)
promotion5 = st.Page(
    "sections/promo5.py",
    title="Promotion 5",
    icon=":material/bar_chart:",
)
promotion6 = st.Page(
    "sections/promo6.py",
    title="Promotion 6",
    icon=":material/bar_chart:",
)
promotion2 = st.Page(
    "sections/promo2.py",
    title="Promotion 2",
    icon=":material/smart_toy:",
)
chatbot = st.Page("sections/chatbot.py", title="Chatbot", icon=":material/chat:")

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [Information],
        "Projects": [promotion5,promotion6, promotion2],
        "Chatbot": [chatbot]
    }
)




# --- RUN NAVIGATION ---
pg.run()
