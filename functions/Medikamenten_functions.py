import streamlit as st
import pandas as pd
import datetime

def initialize_medikamente_state(data_manager):
    if "medikamente" not in st.session_state:
        med_df = data_manager.load_user_data(
            'medikamente.csv',
            initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres", "Intervall"])
        )
        st.session_state.medikamente = med_df.to_dict('records')

def get_einnahmezeit():
    st.markdown("**Einnahmezeit**")
    
    # Einzelnes Zeit-Eingabefeld statt zwei separaten Feldern
    zeit_input = st.time_input(
        "Wähle die Einnahmezeit",
        value=datetime.time(8, 0),  # Standardwert 08:00
        key="uhrzeit_input"
    )
    
    # Konvertiere datetime.time zu String Format "HH:MM"
    return zeit_input.strftime("%H:%M")

def get_intervall_value(intervall_type, x_value=None, intervall_einheit=None):
    fixed_intervals = {
        "Täglich": "täglich",
        "Wöchentlich": "wöchentlich"
    }
    
    if intervall_type in fixed_intervals:
        return fixed_intervals[intervall_type]
    
    if intervall_type == "Alle" and intervall_einheit:
        suffix = "tage" if intervall_einheit == "Tage" else "wochen"
        return f"alle_{x_value}_{suffix}"
    
    return None

def validate_medikament_input(name, dosis):
    return name.strip() != "" and dosis != ""

def save_medikament(name, dosis, zeit, weiteres, intervall_value):
    st.session_state.medikamente.append({
        "Name": name.strip(), "Dosis": dosis, "Zeit": zeit, 
        "Weiteres": weiteres, "Intervall": intervall_value
    })

    data_manager = st.session_state.data_manager
    med_df = pd.DataFrame(st.session_state.medikamente)
    data_manager.save_user_data(med_df, 'medikamente.csv')
    return dosis
