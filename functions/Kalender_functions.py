import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konstanten
TIMES_OF_DAY = ["Morgen", "Mittag", "Abend"]

def initialize_session_state(data_manager):
    """Initialisiert alle Session State Variablen."""
    if "medikamente" not in st.session_state:
        med_df = data_manager.load_user_data(
            'medikamente.csv',
            initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres"])
        )
        st.session_state.medikamente = med_df.to_dict('records')

    if "taken_medications" not in st.session_state:
        st.session_state.taken_medications = []

    if "show_success" not in st.session_state:
        st.session_state.show_success = False

    if "show_balloons" not in st.session_state:
        st.session_state.show_balloons = False

def show_success_message():
    """Zeigt Erfolgs- und Ballon-Meldungen."""
    if st.session_state.show_success:
        st.success("🎉 Super gemacht!")
        st.session_state.show_success = False

    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False

def are_all_medications_taken_for_day(medications, {current_date}, taken_list):
    """Prüft, ob alle Medikamente eines bestimmten Tages eingenommen wurden."""
    all_meds_for_day = []
    
    for zeit in TIMES_OF_DAY:
        for med_idx, med in enumerate(medications):
            if med.get("Zeit") == zeit:
                med_key = f"{current_date}_{zeit}_{med['Name']}_{med_idx}"
                all_meds_for_day.append(med_key)
    
    return len(all_meds_for_day) > 0 and all(med_key in taken_list for med_key in all_meds_for_day)

def organize_medications_by_day(medications):
    """Organisiert Medikamente für die nächsten 7 Tage nach Tageszeit."""
    today = datetime.now().date()
    schedule = {}
    
    for i in range(7):
        current_date = today + timedelta(days=i)
        schedule[current_date] = {}
    
    for med in medications:
        zeit = med.get("Zeit", "Morgen")
        for i in range(7):
            current_date = today + timedelta(days=i)
            # Wenn dieser Zeit-Schlüssel noch nicht existiert, erstelle ihn
            if zeit not in schedule[current_date]:
                schedule[current_date][zeit] = []
            schedule[current_date][zeit].append(med)
    
    return schedule