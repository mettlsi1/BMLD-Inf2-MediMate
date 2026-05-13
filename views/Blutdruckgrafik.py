import streamlit as st
import pandas as pd
from functions.Blutdruckeingabe_functions import initialize_blutdruck_state

st.title("Blutdruckgrafik")

# Initialisiere die Blutdruckdaten (falls noch nicht geschehen)
initialize_blutdruck_state(st.session_state.data_manager)

if "blutdruck" not in st.session_state or not st.session_state.blutdruck:
    st.info("Keine Blutdruckdaten vorhanden.")
else:
    bp_df = pd.DataFrame(st.session_state.blutdruck)
    if not bp_df.empty:
        bp_df["Datum"] = pd.to_datetime(bp_df["Datum"])
        bp_df = bp_df.sort_values("Datum")

        st.line_chart(
            bp_df.set_index("Datum")[["Systolisch", "Diastolisch", "PWS"]]
        )
    else:
        st.info("Noch keine Blutdruckwerte gespeichert.")