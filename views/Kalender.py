import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
import time

st.title('📅 Medikamentenkalender')
st.markdown("Übersicht deiner Medikamente für die nächsten 7 Tage")

# Custom CSS für graublau Kästchen
st.markdown("""
<style>
    .stContainer {
        background-color: #E8EFF5;
        border: 3px solid #6B8E99;
        border-radius: 10px;
        padding: 15px;
        margin: 12px 0;
    }
    
    .stContainer h4 {
        margin-top: 0;
        margin-bottom: 15px;
        color: #2C3E50;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Lade Medikamente aus der Session State
if "medikamente" not in st.session_state:
    data_manager = st.session_state.data_manager
    med_df = data_manager.load_user_data(
        'medikamente.csv',
        initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres"])
    )
    st.session_state.medikamente = med_df.to_dict('records')

# Initialisiere die taken_medications Liste, um eingenommene Medikamente zu speichern
if "taken_medications" not in st.session_state:
    st.session_state.taken_medications = []

# Initialisiere das Flag für die Erfolgsmeldung
if "show_success" not in st.session_state:
    st.session_state.show_success = False

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# Zeige die Erfolgsmeldung an, wenn das Flag gesetzt ist
if st.session_state.show_success:
    st.success("🎉 Super gemacht!")
    st.session_state.show_success = False

# Zeige Balloons, wenn das Flag gesetzt ist
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# Funktion zur Überprüfung, ob alle Medikamente eines Tages eingenommen wurden
def are_all_medications_taken_for_day(medications, current_date, taken_list):
    """
    Prüft, ob alle Medikamente eines bestimmten Tages eingenommen wurden.
    """
    all_meds_for_day = []
    times_of_day = ["Morgen", "Mittag", "Abend"]
    
    for zeit in times_of_day:
        for med_idx, med in enumerate(medications):
            if med.get("Zeit") == zeit:
                med_key = f"{current_date}_{zeit}_{med['Name']}_{med_idx}"
                all_meds_for_day.append(med_key)
    
    # Prüfe ob alle Medikamente des Tages in der taken_list sind
    return len(all_meds_for_day) > 0 and all(med_key in taken_list for med_key in all_meds_for_day)

# Funktion zum Organisieren der Medikamente nach Tagen und Zeiten
def organize_medications_by_day(medications):
    """
    Organisiert Medikamente für die nächsten 7 Tage nach Tageszeit.
    Gibt ein Dictionary mit Daten als Schlüssel zurück.
    """
    today = datetime.now().date()
    schedule = {}
    
    # Initialisiere die nächsten 7 Tage
    for i in range(7):
        current_date = today + timedelta(days=i)
        schedule[current_date] = {
            "Morgen": [],
            "Mittag": [],
            "Abend": []
        }
    
    # Ordne Medikamente den Zeiten zu
    for med in medications:
        zeit = med.get("Zeit", "Morgen")
        for i in range(7):
            current_date = today + timedelta(days=i)
            schedule[current_date][zeit].append(med)
    
    return schedule

# Organisiere die Medikamente
if st.session_state.medikamente:
    schedule = organize_medications_by_day(st.session_state.medikamente)
    
    # Starte den Wrapper für die ganze Tabelle
    st.markdown("""
    <div class="calendar-wrapper">
    """, unsafe_allow_html=True)
    
    # Zeige die nächsten 7 Tage in einer Tabellenstruktur
    for i in range(7):
        current_date = datetime.now().date() + timedelta(days=i)
    
    # Formatiere das Datum schön
        if i == 0:
            day_label = "🟢 Heute"
        elif i == 1:
            day_label = "🟡 Morgen"
        else:
            day_label = calendar.day_name[current_date.weekday()]
    
    # Starte den graublau gefärbten Container
    with st.container():
        st.markdown(f"<h4>{day_label} – {current_date.strftime('%d.%m.%Y')}</h4>", unsafe_allow_html=True)
        
        # Zeige die Medikamente für diese Tageszeiten in 3 Spalten
        times_of_day = ["Morgen", "Mittag", "Abend"]
        cols = st.columns(3)
        
        for idx, zeit in enumerate(times_of_day):
            with cols[idx]:
                meds = schedule[current_date][zeit]
                
                st.markdown(f"**{zeit}**")
                
                if meds:
                    for med_idx, med in enumerate(meds):
                        # ... (restlicher Code für die Medikamente bleibt unverändert)
                else:
                    st.markdown("*–*")
    
    st.markdown("")  # Abstand zwischen den Containern

else:
    st.info("📋 Noch keine Medikamente hinzugefügt. Bitte füge zunächst ein Medikament hinzu.")

# Buttons für Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Medikament hinzufügen"):
        st.switch_page("views/Medikament_hinzufuegen.py")

with col2:
    if st.button("📊 Zur Medikamentenliste"):
        st.switch_page("views/Medikamente.py")
