import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konstanten
TIMES_OF_DAY = ["Morgen", "Mittag", "Abend"]

def initialize_session_state(data_manager):
    """Initialisiert alle Session State Variablen."""
    default_values = {
        "taken_medications": [],
        "show_success": False
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
    """Zeigt Erfolgsmeldung an."""
    if st.session_state.show_success:
        st.success("🎉 Super gemacht!")
        st.session_state.show_success = False

def are_all_medications_taken_for_day(medications, current_date, taken_list):
    """Prüft, ob alle Medikamente eines bestimmten Tages eingenommen wurden."""
    if not medications:
        return False
    
    return all(
        f"{current_date}_{med.get('Zeit', 'Morgen')}_{med['Name']}_{idx}" in taken_list
        for idx, med in enumerate(medications)
    )

def medication_due_on_date(med, date, start_date):
    intervall = str(med.get("Intervall") or "")
    delta_days = (date - start_date).days

    if intervall == "täglich":
        return True
    if intervall == "wöchentlich":
        return delta_days % 7 == 0
    if intervall.startswith("alle_"):
        parts = intervall.split("_")
        if len(parts) == 3:
            interval_value = int(parts[1])
            unit = parts[2]
            if unit == "tage":
                return delta_days % interval_value == 0
            if unit == "wochen":
                return delta_days % (interval_value * 7) == 0
    return False

def organize_medications_by_day(medications):
    from collections import defaultdict

    today = datetime.now().date()
    schedule = {
        today + timedelta(days=i): defaultdict(list)
        for i in range(7)
    }

    for med in medications:
        zeit = med.get("Zeit", "Morgen")
        for date in schedule:
            if medication_due_on_date(med, date, today):
                schedule[date][zeit].append(med)

    return schedule
