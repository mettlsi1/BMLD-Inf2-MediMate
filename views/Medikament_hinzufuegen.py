import streamlit as st
import pandas as pd

st.title('Medikament hinzufügen')
# Initialisiere die Medikamentenliste in der Session, falls sie noch nicht existiert
if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")
# Erstelle ein Formular für die Medikamenteneingabe
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
    
    # Intervall-Auswahl
    st.markdown("**Einnahmeintervall**")
    intervall_type = st.radio(
        "Wie oft soll das Medikament eingenommen werden?",
        ["Täglich", "Alle X Tage", "Wöchentlich", "X Wöchentlich"],
        label_visibility="collapsed",
        horizontal=False
    )
    
    # Abhängig von der Auswahl weitere Eingabefelder
    intervall_value = None
    if intervall_type == "Täglich":
        intervall_value = "täglich"
    elif intervall_type == "Alle X Tage":
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.markdown("**Alle**")
        with col2:
            tage = st.number_input("Tage", min_value=2, value=2, step=1, key="tage_input")
        with col3:
            st.markdown("**Tage**")
        intervall_value = f"alle_{tage}_tage"
    elif intervall_type == "Wöchentlich":
        intervall_value = "wöchentlich"
    elif intervall_type == "X Wöchentlich":
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.markdown("Alle")
        with col2:
            wochen = st.number_input("Wochen", min_value=2, value=2, step=1, key="wochen_input")
        with col3:
            st.markdown("**Wöchentlich**")
        intervall_value = f"alle_{wochen}_wochen"
    
    submitted = st.form_submit_button("Hinzufügen")
    # Überprüfe die Eingaben und füge das Medikament zur Liste hinzu
    if submitted:
        if name.strip() and dosis > 0:
            dosis_str = f"{dosis} {einheit}"
            st.session_state.medikamente.append({
                "Name": name.strip(),
                "Dosis": dosis_str,
                "Zeit": zeit,
                "Weiteres": weiteres,
                "Intervall": intervall_value
            })
            # Speichere die aktualisierte Liste auf der Switch Drive
            data_manager = st.session_state.data_manager
            med_df = pd.DataFrame(st.session_state.medikamente)
            data_manager.save_user_data(med_df, 'medikamente.csv')
            st.success(f"Medikament '{name}' hinzugefügt!")
        else:
            st.error("Bitte einen Namen und eine gültige Dosis eingeben.")

if st.button("Zurück zur Medikamentenliste"):
    st.switch_page("views/Medikamente.py")
    