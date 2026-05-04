import streamlit as st

st.title('Willkommen bei MediMate')
st.subheader("Dein Medikamenten-Monitoring-Tool")

st.info("""Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

# Button für Medikamentenpage
if st.button("Meine Medikamente"):
    st.switch_page("views/Medikamente.py")

if st.button("Kalender"):
    st.switch_page("views/Kalender.py")

st.write("Diese App wurde von den folgenden Personen im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt:")
st.write("- Jessica Schmid (schmij30@students.zhaw.ch)")
st.write("- Valeria Schönyan (schoeva1@students.zhaw.ch)")
st.write("- Simon Mettler (mettlsi1@students.zhaw.ch)")