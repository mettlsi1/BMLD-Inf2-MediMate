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