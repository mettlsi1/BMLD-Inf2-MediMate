import streamlit as st

st.title('Medikament hinzufügen')

if "medikamente" not in st.session_state:
    st.session_state.medikamente = []

st.markdown("Bitte fülle die folgenden Felder aus, um ein neues Medikament zu speichern.")

with st.form("add_medication_form"):
    name = st.text_input("Medikamentenname")
    dosis = st.number_input("Dosis (z. B. in mg)", min_value=0.0, step=0.1)
    zeit = st.selectbox("Einnahmezeit", ["Morgen", "Mittag", "Abend"])
    weiteres = st.selectbox("Weiteres", ["Vor dem Essen", "Mit dem Essen", "Nach dem Essen", "--"])
    
    submitted = st.form_submit_button("Hinzufügen")
    
    if submitted:
        if name.strip() and dosis > 0:
            st.session_state.medikamente.append({
                "Name": name.strip(),
                "Dosis": dosis,
                "Zeit": zeit,
                "Weiteres": weiteres
            })
            st.success(f"Medikament '{name}' hinzugefügt!")
        else:
            st.error("Bitte einen Namen und eine gültige Dosis eingeben.")

if st.button("Zurück zur Medikamentenliste"):
    st.switch_page("views/Medikamente.py")
