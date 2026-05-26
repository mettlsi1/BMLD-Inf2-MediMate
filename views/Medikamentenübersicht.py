import streamlit as st
import pandas as pd
from functions.Medikamenten_functions import initialize_medikamente_state

st.title('Deine Medikamente')

# Initialisiere die Medikamentenliste in der Session
data_manager = st.session_state.data_manager
initialize_medikamente_state(data_manager)

if st.session_state.medikamente:
    st.subheader(f"Du nimmst {len(st.session_state.medikamente)} Medikament{'e' if len(st.session_state.medikamente) != 1 else ''}")
    
    for index, med in enumerate(st.session_state.medikamente):
        # Karten-basiertes Layout mit border
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 3, 0.5])
            
            # Medikamentenname und Dosis
            with col1:
                st.markdown(f"### 💊 {med['Name']}")
                st.caption(f"**Dosis:** {med['Dosis']}")
            
            # Zeit und Intervall
            with col2:
                st.markdown(f"**⏰ Zeiten:** {med['Zeit']}")
                if med.get('Intervall'):
                    st.caption(f"**Rhythmus:** {med['Intervall']}")
            
            # Löschen Button
            with col3:
                if st.button("🗑️", key=f"delete_{index}", help="Medikament löschen"):
                    st.session_state.medikamente.pop(index)
                    med_df = pd.DataFrame(st.session_state.medikamente)
                    data_manager.save_user_data(med_df, 'medikamente.csv')
                    st.rerun()
else:
    st.info("📝 Noch keine Medikamente hinzugefügt. Füge jetzt dein erstes Medikament hinzu!")

# Buttons nebeneinander
st.divider()
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("➕ Medikament hinzufügen", use_container_width=True):
        st.switch_page("views/Medikament_hinzufuegen.py")

with col2:
    if st.button("📅 Zum Kalender", use_container_width=True):
        st.switch_page("views/Kalender.py")

with col3:
    if st.button("🏠 Zur Startseite", use_container_width=True):
        st.switch_page("views/home.py")