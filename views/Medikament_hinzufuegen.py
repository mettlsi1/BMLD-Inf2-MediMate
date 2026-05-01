import streamlit as st
from functions.Medikamenten_functions import (
    initialize_medikamente_state,
    get_intervall_value,
    validate_medikament_input,
    save_medikament
)

st.title('Medikament hinzufügen')

# Initialisiere die Medikamentenliste in der Session
initialize_medikamente_state(st.session_state.data_manager)

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")

with st.form("add_medication_form"):
    name = st.text_input("Medikamentenname")
    col_dosis, col_einheit = st.columns([3, 2])
    with col_dosis:
        dosis = st.number_input("Dosis", min_value=0, step=1)
    with col_einheit:
        einheit = st.radio(
            "Einheit",
            ["mg", "Tabletten"],
            label_visibility="collapsed",
            horizontal=True
        )

    zeit = st.radio("Einnahmezeit", ["Morgen", "Mittag", "Abend"], horizontal=True)
    weiteres = st.selectbox("Weiteres", ["--", "Vor dem Essen", "Mit dem Essen", "Nach dem Essen"])

    st.markdown("**Einnahmeintervall**")
    intervall_type = st.radio(
        "Wie oft soll das Medikament eingenommen werden?",
        ["Täglich", "Wöchentlich", "Alle"],
        label_visibility="collapsed",
        horizontal=False
    )

    x_value = 2
    intervall_einheit = "Tage"
    if intervall_type == "Alle":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("**Alle**")
        with col2:
            x_value = st.number_input("", min_value=2, value=2, step=1, key="x_input")
        with col3:
            intervall_einheit = st.selectbox("", ["Tage", "Wochen"], key="einheit_select")

    submitted = st.form_submit_button("Hinzufügen")
    if submitted:
        if validate_medikament_input(name, dosis):
            intervall_value = get_intervall_value(intervall_type, x_value, intervall_einheit)
            save_medikament(name, dosis, einheit, zeit, weiteres, intervall_value)
            st.success(f"Medikament '{name}' hinzugefügt!")
        else:
            st.error("Bitte einen Namen und eine gültige Dosis eingeben.")

if st.button("Zurück zur Medikamentenliste"):
    st.switch_page("views/Medikamente.py")