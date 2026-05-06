import streamlit as st
import pandas as pd
from functions.Blutdruckeingabe_functions import (
    initialize_blutdruck_state,
    validate_blutdruck_input,
    save_blutdruck,
    check_kritical_values  # NEU
)

st.title('Blutdruckeingabe')

# Zeige das Bild der korrekten Messhaltung
st.image("images/Blutdruckanweisungen.jpg", use_container_width=True, caption="Korrekte Messposition für Blutdruckmessung")

# Initialisiere die Blutdruckliste in der Session
initialize_blutdruck_state(st.session_state.data_manager)

st.markdown("Bitte geben Sie Ihre Blutdruckwerte ein.")

with st.form("add_blood_pressure_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        systolisch = st.number_input(
            "Systolischer Blutdruck (mmHg)",
            min_value=0,
            max_value=250,
            value=120,
            step=1
        )
    
    with col2:
        diastolisch = st.number_input(
            "Diastolischer Blutdruck (mmHg)",
            min_value=0,
            max_value=250,
            value=80,
            step=1
        )
    
    with col3:
        pws = st.number_input(
            "PWS (Puls)",
            min_value=40,
            max_value=200,
            value=70,
            step=1
        )
    
    submitted = st.form_submit_button("Speichern")
if submitted:
    if validate_blutdruck_input(systolisch, diastolisch, pws):
        save_blutdruck(systolisch, diastolisch, pws)
        st.success(f"Blutdruckwerte gespeichert: {systolisch}/{diastolisch} mmHg, Puls: {pws}")
        
        # Prüfe auf kritische Werte
        if check_kritical_values(systolisch, diastolisch, pws):
            st.warning("⚠️ Diese Werte befinden sich in einem kritischen Bereich. Bitte wiederholen Sie die Messung. Falls der Wert weiterhin in diesem Bereich liegt, wenden Sie sich umgehend an einen Notarzt. (Tel: 114)")
    else:
        st.error("Bitte gültige Werte eingeben.")

if st.session_state.blutdruck:
    st.markdown("### Gespeicherte Blutdruckwerte")
    bp_df = pd.DataFrame(st.session_state.blutdruck)
    bp_df.index = bp_df.index + 1
    st.dataframe(bp_df)
else:
    st.info("Noch keine Blutdruckwerte gespeichert.")

if st.button("Zur Blutdruckgrafik"):
    st.switch_page("views/Blutdruckgrafik.py")

if st.button("Zurück zur Startseite"):
    st.switch_page("views/home.py")