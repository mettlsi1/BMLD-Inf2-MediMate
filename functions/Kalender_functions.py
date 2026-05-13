import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konstanten
TIMES_OF_DAY = ["Morgen", "Mittag", "Abend"]

def initialize_session_state(data_manager):
    """Initialisiert alle Session State Variablen."""
    default_values = {
        "taken_medications": [],
        "show_success": False,
        "show_balloons": False
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "medikamente" not in st.session_state or st.session_state.medikamente is None:
        med_df = data_manager.load_user_data(
            'medikamente.csv',
            initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres", "Intervall"])
        )
        st.session_state.medikamente = med_df.to_dict('records')

def show_success_message():
    """Zeigt Erfolgs- und Ballon-Meldungen."""
    if st.session_state.show_success:
        st.success("🎉 Super gemacht!")
        st.session_state.show_success = False

    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False

def are_all_medications_taken_for_day(medications, current_date, taken_list):
    """Prüft, ob alle Medikamente eines bestimmten Tages eingenommen wurden."""
    if not medications:
        return False
    
    return all(
        f"{current_date}_{med.get('Zeit', 'Morgen')}_{med['Name']}_{idx}" in taken_list
        for idx, med in enumerate(medications)
    )

def organize_medications_by_day(medications):
    """Organisiert Medikamente für die nächsten 7 Tage nach Tageszeit."""
    from collections import defaultdict
    
    today = datetime.now().date()
    schedule = {
        today + timedelta(days=i): defaultdict(list)
        for i in range(7)
    }
    
    for med in medications:
        zeit = med.get("Zeit", "Morgen")
        for dates in schedule.values():
            dates[zeit].append(med)
    
    return schedule