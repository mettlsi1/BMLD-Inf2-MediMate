import pandas as pd 
import streamlit as st

st.set_page_config(page_title="MediMate", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Medikamente.py", title="Medikamente", icon="☢️")

pg = st.navigation([pg_home, pg_second])
pg.run()
