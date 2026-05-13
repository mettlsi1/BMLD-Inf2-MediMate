import streamlit as st

st.title("Willkommen bei MediMate")
st.subheader("Dein Medikamenten-Monitoring-Tool")

st.info("Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.")

st.markdown("### Was MediMate für dich erledigt")
st.write(
    "- 📝 Medikamente verwalten\n"
    "- 📅 Einnahmeplan im Kalender sehen\n"
    "- 🩺 Blutdruckwerte erfassen"
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.header("💊 Medikamente")
    st.write("Übersicht über deine Medikamente und Einnahmezeiten.")
    if st.button("Zu meinen Medikamenten"):
        st.switch_page("views/Medikamente.py")

with col2:
    st.header("📅 Kalender")
    st.write("Dein Einnahmezeitplan auf einen Blick.")
    if st.button("Zum Kalender"):
        st.switch_page("views/Kalender.py")

with col3:
    st.header("🩸 Blutdruck")
    st.write("Blutdruckwerte erfassen und dokumentieren.")
    if st.button("Blutdruck erfassen"):
        st.switch_page("views/Blutdruckeingabe.py")

st.divider()

st.write("Diese App wurde im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt:")
st.write("- Jessica Schmid\n- Valeria Schönyan\n- Simon Mettler")