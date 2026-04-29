import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

st.title('📅 Medikamentenkalender')
st.markdown("Übersicht deiner Medikamente für die nächsten 7 Tage")

# Custom CSS für graublau Kästchen
st.markdown("""
<style>
    .day-container {
        background-color: #B0C4D4;
        border: 2px solid #6B8E99;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .day-container h4 {
        margin-top: 0;
        color: #2C3E50;
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
        
        # Starte den graublau gefärbten Container
        st.markdown(f"""
        <div class="day-container">
        <h4>{day_label} – {current_date.strftime('%d.%m.%Y')}</h4>
        """, unsafe_allow_html=True)
        
        # Zeige die Medikamente für diese Tageszeiten in 3 Spalten
        times_of_day = ["Morgen", "Mittag", "Abend"]
        cols = st.columns(3)
        
        for idx, zeit in enumerate(times_of_day):
            with cols[idx]:
                meds = schedule[current_date][zeit]
                
                st.markdown(f"**{zeit}**")
                
                if meds:
                    for med_idx, med in enumerate(meds):
                        # Erstelle einen eindeutigen Schlüssel für jedes Medikament
                        med_key = f"{current_date}_{zeit}_{med['Name']}_{med_idx}"
                        
                        # Prüfe ob das Medikament bereits eingenommen wurde
                        is_taken = med_key in st.session_state.taken_medications
                        
                        # Erstelle einen Button mit farblicher Kennzeichnung
                        if is_taken:
                            # Grüner Hintergrund für eingenommene Medikamente
                            button_label = f"✅ {med['Name']}"
                            button_key = f"btn_{med_key}"
                            if st.button(button_label, key=button_key, use_container_width=True):
                                # Toggle: Entferne das Medikament aus der Liste
                                st.session_state.taken_medications.remove(med_key)
                                st.rerun()
                        else:
                            # Normaler Button für noch nicht eingenommene Medikamente
                            button_label = f"🔷 {med['Name']}"
                            button_key = f"btn_{med_key}"
                            if st.button(button_label, key=button_key, use_container_width=True):
                                # Füge das Medikament zur Liste hinzu
                                st.session_state.taken_medications.append(med_key)
                                st.rerun()
                        
                        # Zeige Dosis und Weiteres als Text
                        st.caption(f"{med['Dosis']}" + (f" • {med['Weiteres']}" if med['Weiteres'] != '--' else ""))
                else:
                    st.markdown("*–*")
        
        # Beende den Container
        st.markdown("</div>", unsafe_allow_html=True)
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
