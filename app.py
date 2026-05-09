import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME CONFIGURATION ---
st.set_page_config(page_title="Great Mech Global", layout="wide", page_icon="🦾")

# Clean CSS Styling - Fixed the Syntax Error
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .stButton>button { background: linear-gradient(45deg, #D4AF37, #AF8700); color: black !important; font-weight: bold; border-radius: 8px; border: none; height: 3em; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', Courier, monospace; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SHARED MEMORY (Google Sheets) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    db_data = conn.read()
except Exception:
    db_data = pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

# --- 3. FOUNDER CORE LOGIC ---
def process_split(amount):
    founder_cut = amount * 0.15
    mechanic_cut = amount * 0.85
    return founder_cut, mechanic_cut

# --- 4. NAVIGATION ---
st.sidebar.title("🦾 GREAT MECH OS")
app_mode = st.sidebar.selectbox("Command Center", ["Marketplace", "Mechanic Hub", "SOS Security", "Founder Ledger"])

# --- MODULE A: MARKETPLACE ---
if app_mode == "Marketplace":
    st.title("📍 Engineering Service Request")
    col_input, col_map = st.columns([1, 1.5])

    with col_input:
        service = st.selectbox("Select Category", ["Diesel Engine", "Solar Power", "Heavy Trucks", "CCTV"])
        budget = st.number_input("Proposed Fee (NGN)", min_value=5000)
        
        if st.button("🚀 DEPLOY REQUEST"):
            st.success("Broadcasted! View in Founder Ledger.")
            st.balloons()

    with col_map:
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB dark_matter")
            folium.Marker([lat, lon], icon=folium.Icon(color='gold')).add_to(m)
            st_folium(m, width=700, height=450)

# --- MODULE B: MECHANIC HUB ---
elif app_mode == "Mechanic Hub":
    st.title("🔧 Field Operations")
    if db_data.empty:
        st.info("No jobs found in database yet.")
    else:
        st.dataframe(db_data)

# --- MODULE C: SOS SECURITY ---
elif app_mode == "SOS Security":
    st.title("🚨 Emergency Shield")
    if st.button("TRIGGER SOS", type="primary"):
        st.error("EMERGENCY SIGNAL SENT.")

# --- MODULE D: FOUNDER LEDGER ---
elif app_mode == "Founder Ledger":
    st.title("📊 Global Revenue")
    st.dataframe(db_data)


