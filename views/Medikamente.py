import streamlit as st
import pandas as pd

st.title('Deine Medikamente')

# Lade Medikamente aus der Switch Drive, falls nicht im Session-State
if "medikamente" not in st.session_state:
    data_manager = st.session_state.data_manager
    med_df = data_manager.load_user_data(
        'medikamente.csv',
        initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres"])
    )
    st.session_state.medikamente = med_df.to_dict('records')


if st.session_state.medikamente:
    df = pd.DataFrame(st.session_state.medikamente)
    df.index = df.index + 1
    st.dataframe(df)
else:
    st.info("Noch keine Medikamente hinzugefügt.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Medikament hinzufügen"):
        st.switch_page("views/Medikament_hinzufuegen.py")
