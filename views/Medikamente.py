import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Medikamente')

# Optional: Session-State initialisieren
if "page" not in st.session_state:
    st.session_state.page = None
if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Neues Medikament hinzufügen"):
        st.session_state.page = "add_medikament"

# Formular zum Hinzufügen
if st.session_state.get("page") == "add_medikament":
    st.subheader("Neues Medikament hinzufügen")

    name = st.text_input("Medikamentenname", key="med_name")
    dosis = st.number_input("Dosis (z. B. in mg)", min_value=0.0, step=0.1, key="med_dosis")
    zeit = st.time_input("Einnahmezeit", key="med_zeit")

    if st.button("Hinzufügen", key="add_button"):
        if name and dosis > 0:
            st.session_state.medikamente.append({
                "name": name,
                "dosis": dosis,
                "zeit": str(zeit)
            })
            st.success(f"Medikament '{name}' hinzugefügt!")
            st.session_state.page = None
        else:
            st.error("Bitte alle Felder ausfüllen.")

# Automatische Auflistung
st.subheader("Aufgenommene Medikamente")

if st.session_state.medikamente:
    df = pd.DataFrame(st.session_state.medikamente)
    import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Medikamente')

# Optional: Session-State initialisieren
if "page" not in st.session_state:
    st.session_state.page = None
if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Neues Medikament hinzufügen"):
        st.session_state.page = "add_medikament"

# Formular zum Hinzufügen
if st.session_state.get("page") == "add_medikament":
    st.subheader("Neues Medikament hinzufügen")

    name = st.text_input("Medikamentenname", key="med_name")
    dosis = st.number_input("Dosis (z. B. in mg)", min_value=0.0, step=0.1, key="med_dosis")
    zeit = st.time_input("Einnahmezeit", key="med_zeit")

    if st.button("Hinzufügen", key="add_button"):
        if name and dosis > 0:
            st.session_state.medikamente.append({
                "name": name,
                "dosis": dosis,
                "zeit": str(zeit)
            })
            st.success(f"Medikament '{name}' hinzugefügt!")
            st.session_state.page = None
        else:
            st.error("Bitte alle Felder ausfüllen.")

# Automatische Auflistung
st.subheader("Deine Medikamente")

if st.session_state.medikamente:
    df = pd.DataFrame(st.session_state.medikamente)
    st.dataframe(df)
else:
    st.info("Noch keine Medikamente hinzugefügt.")
    st.dataframe(df)
else:
    st.info("Noch keine Medikamente hinzugefügt.")