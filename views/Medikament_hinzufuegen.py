from functions.Medikamenten_functions import (
    initialize_medikamente_state,
    get_intervall_value,
    validate_medikament_input,
    save_medikament,
    get_einnahmezeit  # Neu hinzufügen
)

import datetime

import streamlit as st
from functions.Medikamenten_functions import (
    initialize_medikamente_state,
    get_intervall_value,
    validate_medikament_input,
    save_medikament,
    get_einnahmezeit
)

st.title('Medikament hinzufügen')

# Initialisiere die Medikamentenliste in der Session
initialize_medikamente_state(st.session_state.data_manager)

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")

with st.form("add_medication_form"):
    name = st.text_input("Medikamentenname")
    col_tabletten, col_mg = st.columns(2)
    with col_tabletten:
        tabletten = st.number_input("Anzahl Tabletten", min_value=0, step=1, value=0)
    with col_mg:
        mg = st.number_input("mg", min_value=0, step=1, value=0)
    if tabletten > 0 and mg > 0:
        dosis = f"{tabletten} Tabletten ({mg} mg)"
    elif tabletten > 0:
        dosis = f"{tabletten} Tabletten"
    elif mg > 0:
        dosis = f"{mg} mg"
    else:
        dosis = ""    
    
    zeit = get_einnahmezeit()  # Ersetzt die gesamte Uhrzeit-Logik

    weiteres = st.selectbox("Weiteres", ["--", "Vor dem Essen", "Mit dem Essen", "Nach dem Essen"])

    st.markdown("**Einnahmeintervall**")
    intervall_type = st.radio(
        "Wie oft soll das Medikament eingenommen werden?",
        ["Täglich", "Wöchentlich", "Alle ..."],
        label_visibility="collapsed",
        horizontal=False
    )

    x_value = 2
    intervall_einheit = "Tage"

    col1, col2 = st.columns([1, 1])
    with col1:
        x_value = st.number_input("", min_value=2, value=2, step=1, key="x_input")
    with col2:
        intervall_einheit = st.selectbox("", ["Tage", "Wochen"], key="einheit_select")

    submitted = st.form_submit_button("Hinzufügen")
    if submitted:
        if validate_medikament_input(name, dosis):
            intervall_value = get_intervall_value(intervall_type, x_value, intervall_einheit)
            save_medikament(name, dosis, zeit, weiteres, intervall_value)
            st.success(f"Medikament '{name}' hinzugefügt!")
        else:
            st.error("Bitte einen Namen und eine gültige Dosis eingeben.")

if st.button("Zurück zur Medikamentenliste"):
    st.switch_page("views/Medikamente.py")