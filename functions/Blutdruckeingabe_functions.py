import streamlit as st
import pandas as pd
from datetime import datetime

def initialize_blutdruck_state(data_manager):
    if "blutdruck" not in st.session_state:
        bp_df = data_manager.load_user_data(
            'blutdruck.csv',
            initial_value=pd.DataFrame(columns=["Datum", "Systolisch", "Diastolisch", "PWS"])
        )
        st.session_state.blutdruck = bp_df.to_dict('records')

def validate_blutdruck_input(systolisch, diastolisch, pws):
    return systolisch > 0 and diastolisch > 0 and pws > 0

def check_kritical_values(systolisch, diastolisch, pws):
    """
    Prüft, ob die Blutdruckwerte kritisch sind.
    Kritisch bei: zu hohem Druck (>=180/>=110) oder zu niedrigem Druck (<70/<40)
    Rückgabe: True wenn kritisch, False wenn normal
    """
    # Zu hoher Druck
    high_critical = systolisch >= 180 or diastolisch >= 110
    # Zu niedriger Druck
    low_critical = systolisch < 70 or diastolisch < 40
    
    return high_critical or low_critical

def classify_blood_pressure(systolisch, diastolisch):
    """
    Klassifiziert den Blutdruck basierend auf WHO-Richtlinien.
    Rückgabe: String mit der Kategorie
    """
    if 70 <= systolisch <= 120 and 40 <= diastolisch <= 80:
        return "Optimaler Blutdruck"
    elif 120 <= systolisch <= 129 and 80 <= diastolisch <= 84:
        return "Normaler Blutdruck"
    elif 130 <= systolisch <= 138 and 85 <= diastolisch <= 89:
        return "Hochnormaler Blutdruck"
    elif 140 <= systolisch <= 159 and 90 <= diastolisch <= 99:
        return "Leichter Bluthochdruck"
    elif 160 <= systolisch <= 179 and 100 <= diastolisch <= 109:
        return "Mäßiger Bluthochdruck"
    elif systolisch >= 180 or diastolisch >= 110:
        return "Schwerer Bluthochdruck"
    else:
        return "Unklassifiziert"

def save_blutdruck(systolisch, diastolisch, pws):
    st.session_state.blutdruck.append({
        "Datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Systolisch": systolisch,
        "Diastolisch": diastolisch,
        "PWS": pws
    })

    data_manager = st.session_state.data_manager
    bp_df = pd.DataFrame(st.session_state.blutdruck)
    data_manager.save_user_data(bp_df, 'blutdruck.csv')
    return True