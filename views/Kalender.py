import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

st.title('📅 Medikamentenkalender')
st.markdown("Übersicht deiner Medikamente für die nächsten 7 Tage")

# Lade Medikamente aus der Session State
if "medikamente" not in st.session_state:
    data_manager = st.session_state.data_manager
    med_df = data_manager.load_user_data(
        'medikamente.csv',
        initial_value=pd.DataFrame(columns=["Name", "Dosis", "Zeit", "Weiteres"])
    )
    st.session_state.medikamente = med_df.to_dict('records')

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
    
    # Ordne Medikamente den Zeiten zu (derzeit nehmen wir an, alle sind täglich)
    for med in medications:
        zeit = med.get("Zeit", "Morgen")
        for i in range(7):
            current_date = today + timedelta(days=i)
            schedule[current_date][zeit].append(med)
    
    return schedule

# Organisiere die Medikamente
if st.session_state.medikamente:
    schedule = organize_medications_by_day(st.session_state.medikamente)
    
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
        
        # Container für jeden Tag mit Kästchen-Design
        with st.container(border=True):
            # Kopfzeile mit Datum
            st.markdown(f"**{day_label} – {current_date.strftime('%d.%m.%Y')}**")
            
            # Zeige die Medikamente für diese Tageszeiten in 3 Spalten
            times_of_day = ["Morgen", "Mittag", "Abend"]
            cols = st.columns(3)
            
            for idx, zeit in enumerate(times_of_day):
                with cols[idx]:
                    meds = schedule[current_date][zeit]
                    
                    st.markdown(f"**{zeit}**")
                    
                    if meds:
                        for med in meds:
                            st.markdown(
                                f"🔷 **{med['Name']}**\n:"
                                f" {med['Dosis']}\n"
                                f" {med['Weiteres'] if med['Weiteres'] != '--' else ''}"
                            )
                    else:
                        st.markdown("*–*")

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
