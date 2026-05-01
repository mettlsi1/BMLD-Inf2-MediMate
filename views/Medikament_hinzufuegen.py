import streamlit as st
import pandas as pd

def initialize_medikamente_state(data_manager):
    if "medikamente" not in st.session_state:
        med_df = data_manager.load_user_data(
            "medikamente.csv",
            initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres", "Intervall"])
        )
        st.session_state.medikamente = med_df.to_dict("records")

def get_intervall_value(intervall_type, x_value=None, intervall_einheit=None):
    if intervall_type == "Täglich":
        return "täglich"
    if intervall_type == "Wöchentlich":
        return "wöchentlich"
    if intervall_type == "Alle":
        if intervall_einheit == "Tage":
            return f"alle_{x_value}_tage"
        return f"alle_{x_value}_wochen"
    return None

def validate_medikament_input(name, dosis):
    return bool(name and name.strip()) and dosis > 0

def save_medikament(name, dosis, einheit, zeit, weiteres, intervall_value):
    dosis_str = f"{dosis} {einheit}"
    st.session_state.medikamente.append({
        "Name": name.strip(),
        "Dosis": dosis_str,
        "Zeit": zeit,
        "Weiteres": weiteres,
        "Intervall": intervall_value
    })

    data_manager = st.session_state.data_manager
    med_df = pd.DataFrame(st.session_state.medikamente)
    data_manager.save_user_data(med_df, "medikamente.csv")
    