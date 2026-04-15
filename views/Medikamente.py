import streamlit as st
import pandas as pd

st.title('Medikamente')

if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Medikament hinzufügen"):
        st.switch_page("views/Medikament_hinzufuegen.py")

st.subheader("Deine Medikamente")

if st.session_state.medikamente:
    df = pd.DataFrame(st.session_state.medikamente)
    df.index = df.index + 1
    st.dataframe(df)
else:
    st.info("Noch keine Medikamente hinzugefügt.")