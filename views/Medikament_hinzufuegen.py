import streamlit as st
import pandas as pd

st.title('Medikament hinzufügen')

if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")

with st.form("add_medication_form"):
    name = st.text_input("Medikamentenname")
    col_dosis, col_einheit = st.columns([3, 2])
    with col_dosis:
        dosis = st.number_input("Dosis", min_value=0.0, step=1.0)
    with col_einheit:
        einheit = st.radio("Einheit", ["mg", "Tabletten"], label_visibility="collapsed")
    zeit = st.radio("Einnahmezeit", ["Morgen", "Mittag", "Abend"])
    weiteres = st.selectbox("Weiteres", ["Vor dem Essen", "Mit dem Essen", "Nach dem Essen", "--"])
    
    submitted = st.form_submit_button("Hinzufügen")
    
    if submitted:
        if name.strip() and dosis > 0:
            dosis_str = f"{dosis} {einheit}"
            st.session_state.medikamente.append({
                "Name": name.strip(),
                "Dosis": dosis_str,
                "Zeit": zeit,
                "Weiteres": weiteres
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
