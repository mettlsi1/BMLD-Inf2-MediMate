import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.title('Medikamente')

col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Neues Medikament hinzufügen"):
            st.session_state.page = "add_medikament"
    with col2:
        if st.button("Medikamenten-Auflistung"):
            st.session_state.page = "list_medikamente"
