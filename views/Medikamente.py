import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.title('Medikamente')

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Neues Medikament hinzufügen"):
        st.session_state.page = "add_medikament"
with col2:
    if st.button("Medikamenten-Auflistung"):
        st.session_state.page = "list_medikamente"

# Neue Logik für das Eingabefeld
if st.session_state.get("page") == "add_medikament":
    st.subheader("Neues Medikament hinzufügen")
    
    # Eingabefelder
    name = st.text_input("Medikamentenname", key="med_name")
    dosis = st.number_input("Dosis (z. B. in mg)", min_value=0.0, step=0.1, key="med_dosis")
    zeit = st.time_input("Einnahmezeit", key="med_zeit")
    
    # Button zum Hinzufügen
    if st.button("Hinzufügen", key="add_button"):
        if name and dosis > 0:  # Einfache Validierung
            # Hier kannst du die Daten speichern, z. B. in st.session_state oder einer Datenbank
            # Beispiel: Speichere in einer Liste im Session-State
            if "medikamente" not in st.session_state:
                st.session_state.medikamente = []
            st.session_state.medikamente.append({
                "name": name,
                "dosis": dosis,
                "zeit": str(zeit)  # Zeit als String speichern
            })
            st.success(f"Medikament '{name}' hinzugefügt!")
            # Optional: Formular zurücksetzen
            st.session_state.page = None
        else:
            st.error("Bitte alle Felder ausfüllen.")