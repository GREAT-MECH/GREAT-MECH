import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Great Mech Global", layout="wide", page_icon="🦾")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .stButton>button { background: linear-gradient(45deg, #D4AF37, #AF8700); color: black !important; font-weight: bold; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        return conn.read()
    except:
        return pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

db_data = get_data()

# --- APP NAVIGATION ---
st.sidebar.title("🦾 GREAT MECH OS")
app_mode = st.sidebar.selectbox("Command Center", ["Marketplace", "Mechanic Hub", "Founder Ledger"])

# --- MARKETPLACE (THE TEST) ---
if app_mode == "Marketplace":
    st.title("📍 Request Engineering Service")
    
    with st.form("job_form"):
        service = st.selectbox("Category", ["Diesel Engine", "Solar Power", "Heavy Trucks"])
        budget = st.number_input("Budget (NGN)", min_value=5000)
        submitted = st.form_submit_button("🚀 DEPLOY REQUEST")
        
        if submitted:
            new_job = pd.DataFrame([{
                "ID": f"GM-{random.randint(10000, 99999)}",
                "Service": service,
                "Budget": budget,
                "Status": "Pending",
                "Location": "Lagos, Nigeria",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # Combine and Update
            updated_df = pd.concat([db_data, new_job], ignore_index=True)
            conn.update(data=updated_df)
            st.success("SUCCESS: Job recorded in the Cloud Ledger!")
            st.balloons()

# --- FOUNDER LEDGER ---
elif app_mode == "Founder Ledger":
    st.title("📊 Global Revenue")
    total_val = db_data['Budget'].astype(float).sum() if not db_data.empty else 0
    st.metric("Total Ecosystem Value", f"₦{total_val:,.2f}")
    st.dataframe(db_data, use_container_width=True)

# --- MECHANIC HUB ---
elif app_mode == "Mechanic Hub":
    st.title("🔧 Jobs Near You")
    st.dataframe(db_data[db_data['Status'] == "Pending"])

