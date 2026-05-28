import streamlit as st
from datetime import datetime, timedelta
from functions.Kalender_functions import (
    initialize_session_state,
    show_success_message,
    are_all_medications_taken_for_day,
    organize_medications_by_day
)

# Initialisiere Session State
initialize_session_state(st.session_state.data_manager)
show_success_message()

# Buttons für Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Medikament hinzufügen"):
        st.switch_page("views/Medikament_hinzufuegen.py")

with col2:
    if st.button("📊 Zur Medikamentenliste"):
        st.switch_page("views/Medikamentenübersicht.py")

st.title('Medikamentenkalender')
st.markdown("Übersicht deiner Medikamente für die nächsten 7 Tage")

# Organisiation der Medikamente
if st.session_state.medikamente:
    schedule = organize_medications_by_day(st.session_state.medikamente)

    # nächsten 7 Tage in einer Tabellenstruktur anzeigen
    for i in range(7):
        current_date = datetime.now().date() + timedelta(days=i)

        # Trennlinie vor jedem Tag (außer dem ersten)
        if i > 0:
            st.markdown("---")
        
        # Datumsformatierung
        if i == 0:
            day_label = "🟢 Heute"
        elif i == 1:
            day_label = "🟡 Morgen"
        else:
            deutsche_wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            day_label = deutsche_wochentage[current_date.weekday()]
        
        # graublauen Container starten
        with st.container():
            st.markdown(f"<h4>{day_label} – {current_date.strftime('%d.%m.%Y')}</h4>", unsafe_allow_html=True)

            # Medikamente in Spalten anzeigen
            times = sorted(schedule[current_date].keys())
            cols = st.columns(len(times)) if times else [st.container()]

            for idx, zeit in enumerate(times):
                with cols[idx]:
                    meds = schedule[current_date][zeit]
        
                    st.markdown(f"**{zeit}**")
        
                    
                    if meds:
                        for med_idx, med in enumerate(meds):
                            med_key = f"{current_date}_{zeit}_{med['Name']}_{med_idx}"
                            is_taken = med_key in st.session_state.taken_medications
                            
                            if i == 0:
                                if is_taken:
                                    button_label = f"✅ {med['Name']}"
                                    if st.button(button_label, key=f"btn_{med_key}", use_container_width=True):
                                        st.session_state.taken_medications.remove(med_key)
                                        st.rerun()
                                else:
                                    button_label = f"🔷 {med['Name']}"
                                    if st.button(button_label, key=f"btn_{med_key}", use_container_width=True):
                                        st.session_state.taken_medications.append(med_key)
                                        st.session_state.show_success = True
                                        
                                        st.rerun()
                                
                                st.caption(f"{med['Dosis']}" + (f" • {med['Weiteres']}" if med['Weiteres'] != '--' else ""))
                            else:
                                if is_taken:
                                    st.markdown(f"✅ **{med['Name']}**")
                                else:
                                    st.markdown(f"🔷 **{med['Name']}**")
                                
                                st.caption(f"{med['Dosis']}" + (f" • {med['Weiteres']}" if med['Weiteres'] != '--' else ""))
                    else:
                        st.markdown("*–*")

else:
    st.info("📋 Noch keine Medikamente hinzugefügt. Bitte füge zunächst ein Medikament hinzu.")

