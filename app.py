import pandas as pd 
import streamlit as st

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_MediMate"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---


st.set_page_config(page_title="MediMate", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Medikamentenübersicht.py", title="Medikamentenübersicht", icon="💊")
pg_add = st.Page("views/Medikament_hinzufuegen.py", title="Medikament hinzufügen", icon="➕")
pg_calendar = st.Page("views/Kalender.py", title="Kalender", icon="📅")
pg_Blutdruckeingabe = st.Page("views/Blutdruckeingabe.py", title="Blutdruckeingabe", icon="🩸")
pg_bloodchart = st.Page("views/Blutdruckgrafik.py", title="Blutdruckgrafik", icon="📈")

pg = st.navigation([
    pg_home,
    pg_second,
    pg_add,
    pg_calendar,
    pg_Blutdruckeingabe,
    pg_bloodchart
])
pg.run()
