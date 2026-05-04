import streamlit as st

st.title('Willkommen bei MediMate')
st.subheader("Dein Medikamenten-Monitoring-Tool")

st.info("""Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

# Buttons für Medikamentenpage und Kalenderpage
col1, col2 = st.columns(2)

with col1:
    if st.button("💊 Meine Medikamente"):
        st.switch_page("views/Medikamente.py")

with col2:
    if st.button("📅 Mein Kalender"):
        st.switch_page("views/Kalender.py")

st.write("Diese App wurde von den folgenden Personen im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt:")
st.write("- Jessica Schmid (schmij30@students.zhaw.ch)")
st.write("- Valeria Schönyan (schoeva1@students.zhaw.ch)")
st.write("- Simon Mettler (mettlsi1@students.zhaw.ch)")