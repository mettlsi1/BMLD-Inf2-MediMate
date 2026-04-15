import streamlit as st

st.title('Medikament hinzufügen')

if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")

name = st.text_input("Medikamentenname", key="new_med_name")
dosis = st.number_input("Dosis (z. B. in mg)", min_value=0.0, step=0.1, key="new_med_dosis")
zeit = st.time_input("Einnahmezeit", key="new_med_zeit")

if st.button("Hinzufügen", key="save_med_button"):
    if name.strip() and dosis > 0:
        st.session_state.medikamente.append({
            "Name": name.strip(),
            "Dosis": dosis,
            "Zeit": zeit.strftime("%H:%M")
        })
        st.success(f"Medikament '{name}' hinzugefügt!")
    else:
        st.error("Bitte einen Namen und eine gültige Dosis eingeben.")

if st.button("Zurück zur Medikamentenliste"):
    st.switch_page("views/Medikamente.py")
