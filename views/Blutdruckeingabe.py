import streamlit as st
import pandas as pd
from functions.Blutdruckeingabe_functions import (
    initialize_blutdruck_state,
    validate_blutdruck_input,
    save_blutdruck,
    check_kritical_values,
    classify_blood_pressure  # NEU
)

st.title('Blutdruckeingabe')

# Zeige das Bild der korrekten Messhaltung
st.image("images/Blutdruckanweisungen.jpg", use_container_width=True, caption="Korrekte Messposition für Blutdruckmessung")
st.caption("Quelle: [USZ - Blutdruck](https://www.usz.ch/blutdruck/)")

# Initialisiere die Blutdruckliste in der Session
initialize_blutdruck_state(st.session_state.data_manager)

st.markdown("Bitte geben Sie Ihre Blutdruckwerte ein.")

with st.form("add_blood_pressure_form"):
    inputs_config = {
        "Systolischer Blutdruck (mmHg)": {"min": 0, "max": 250, "value": 120},
        "Diastolischer Blutdruck (mmHg)": {"min": 0, "max": 250, "value": 80},
        "PWS (Puls)": {"min": 40, "max": 200, "value": 70}
    }
    
    cols = st.columns(3)
    values = {}
    
    for i, (label, config) in enumerate(inputs_config.items()):
        with cols[i]:
            values[label] = st.number_input(label, **config, step=1)
    
    systolisch = values["Systolischer Blutdruck (mmHg)"]
    diastolisch = values["Diastolischer Blutdruck (mmHg)"]
    pws = values["PWS (Puls)"]
    
    submitted = st.form_submit_button("Speichern")
if submitted:
    if validate_blutdruck_input(systolisch, diastolisch, pws):
        save_blutdruck(systolisch, diastolisch, pws)
        
        # Klassifiziere den Blutdruck
        category = classify_blood_pressure(systolisch, diastolisch)
        st.success(f"Blutdruckwerte gespeichert: {systolisch}/{diastolisch} mmHg, Puls: {pws}")
        st.info(f"**Kategorie:** {category}")
        
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

col1, col2 = st.columns(2)
with col1:
    if st.button("Zur Blutdruckgrafik"):
        st.switch_page("views/Blutdruckgrafik.py")
with col2:
    if st.button("Zurück zur Startseite"):
        st.switch_page("views/home.py")