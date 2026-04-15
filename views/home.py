import streamlit as st

st.title('Willkommen bei MediMate')
st.subheader("Dein Medikamenten-Monitoring-Tool")

st.markdown("Die Anwendung ermöglicht es Ihnen, Ihre Medikamenteneinnahme zu verfolgen. Bitte melden Sie sich an oder registrieren Sie sich, um fortzufahren.")

st.info("""Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

# Neuen Button hier hinzufügen
if st.button("Meine Medikamente"):
    st.switch_page("views/Medikamente.py")

st.write("Diese App wurde von den folgenden Personen im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt:")
st.write("- Jessica Schmid (schmij30@students.zhaw.ch)")
st.write("- Valeria Schönyan (schoeva1@students.zhaw.ch)")
st.write("- Simon Mettler (mettlsi1@students.zhaw.ch)")