import streamlit as st
import pandas as pd

st.title('Deine Medikamente')

# Lade Medikamente aus der Switch Drive, falls nicht im Session-State
data_manager = st.session_state.data_manager

if st.session_state.medikamente:
    for index, med in enumerate(st.session_state.medikamente):
        col1, col2, col3 = st.columns([4, 4, 1])
        col1.write(f"**{med['Name']}**")
        col2.write(f"{med['Dosis']} — {med['Zeit']} — {med.get('Intervall', '')}")
        if col3.button("Löschen", key=f"delete_{index}"):
            st.session_state.medikamente.pop(index)
            med_df = pd.DataFrame(st.session_state.medikamente)
            data_manager.save_user_data(med_df, 'medikamente.csv')
            st.experimental_rerun()
else:
    st.info("Noch keine Medikamente hinzugefügt.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Medikament hinzufügen"):
        st.switch_page("views/Medikament_hinzufuegen.py")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📅 Zum Kalender"):
        st.switch_page("views/Kalender.py")
