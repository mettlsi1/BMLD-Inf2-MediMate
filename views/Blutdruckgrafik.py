import altair as alt
import pandas as pd
import streamlit as st
from functions.Blutdruckeingabe_functions import initialize_blutdruck_state

st.title("Blutdruckgrafik")
initialize_blutdruck_state(st.session_state.data_manager)

if "blutdruck" not in st.session_state or not st.session_state.blutdruck:
    st.info("Keine Blutdruckdaten vorhanden.")
else:
    bp_df = pd.DataFrame(st.session_state.blutdruck)
    if not bp_df.empty:
        bp_df["Datum"] = pd.to_datetime(bp_df["Datum"])
        bp_df = bp_df.sort_values("Datum").tail(10)

        chart = alt.Chart(bp_df).transform_fold(
            ["Systolisch", "Diastolisch", "PWS"],
            as_=["Messwert", "Wert"]
        ).mark_line(point=True).encode(
            x=alt.X(
                "Datum:T",
                axis=alt.Axis(title="Datum und Uhrzeit", format="%d.%m %H:%M", labelAngle=-45)
            ),
            y=alt.Y(
                "Wert:Q",
                title="Messwert",
                scale=alt.Scale(domain=[20, 200])
            ),
            color="Messwert:N"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Noch keine Blutdruckwerte gespeichert.")