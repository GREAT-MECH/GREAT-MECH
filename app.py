import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME CONFIG & THEME ---
st.set_page_config(page_title="Great Mech Supreme OS", layout="wide", page_icon="🦾")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; }
    .stButton>button { background: linear-gradient(45deg, #D4AF37, #AF8700); color: black !important; font-weight: bold; border-radius: 10px; border: none; width: 100%; height: 3em; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF; border-radius: 4px 4px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE IDENTITY ENGINE (LOGIN) ---
if 'auth_role' not in st.session_state:
    st.session_state.auth_role = None

if st.session_state.auth_role is None:
    st.title("🦾 GREAT MECH IDENTITY PORTAL")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("FOUNDER LOGIN"): st.session_state.auth_role = "Founder"
    if col2.button("MECHANIC LOGIN"): st.session_state.auth_role = "Mechanic"
    if col3.button("USER LOGIN"): st.session_state.auth_role = "User"
    if col4.button("PARTNER LOGIN"): st.session_state.auth_role = "Partner"
    st.stop()

# Logout Option
if st.sidebar.button("LOGOUT " + st.session_state.auth_role):
    st.session_state.auth_role = None
    st.rerun()

# --- 3. DATA & VISION LOGIC ---
conn = st.connection("gsheets", type=GSheetsConnection)
try:
    db_data = conn.read(ttl=0)
except:
    db_data = pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

# --- 4. DASHBOARD BY ROLE ---

# --- FOUNDER VIEW ---
if st.session_state.auth_role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    total_rev = db_data['Budget'].astype(float).sum() if not db_data.empty else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Ecosystem Value", f"₦{total_rev:,.2f}")
    c2.metric("Founder 15% Net", f"₦{total_rev*0.15:,.2f}")
    c3.metric("Active Mechanics", "54 Countries")
    
    st.subheader("Global Operations Ledger")
    st.dataframe(db_data, use_container_width=True)

# --- USER VIEW (THE MARKETPLACE) ---
elif st.session_state.auth_role == "User":
    st.title("📍 REQUEST ENGINEERING MAGIC")
    tab_req, tab_diag = st.tabs(["🚀 DEPLOY REQUEST", "🧠 AI DIAGNOSTICS"])
    
    with tab_req:
        col_in, col_map = st.columns([1, 1.5])
        with col_in:
            service = st.selectbox("Category", ["Diesel Engine", "Truck Repair", "Solar", "CCTV"])
            budget = st.number_input("Budget (NGN)", min_value=5000)
            loc_input = st.text_input("Enter Address", "Lagos, Nigeria")
            
            if st.button("DEPLOY TO CLOUD"):
                new_job = pd.DataFrame([{
                    "ID": f"GM-{random.randint(1000, 9999)}",
                    "Service": service, "Budget": budget,
                    "Status": "Pending", "Location": loc_input,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                updated_df = pd.concat([db_data, new_job], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Broadcasted! Waiting for Mechanic.")
                st.balloons()
        
        with col_map:
            st.write("🌍 Logistic View (Distance & Time)")
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=12, tiles="CartoDB dark_matter")
            st_folium(m, width=600, height=400)

    with tab_diag:
        st.subheader("7 Symptoms AI Diagnostic")
        symptoms = st.multiselect("Select Symptoms", ["Engine Overheating", "Black Smoke", "Fluid Leak", "Power Loss", "Strange Noise", "Won't Start", "Battery Failure"])
        if st.button("GENERATE AI REPORT"):
            st.info("AI Analysis: Based on symptoms, checking fuel injection and cooling systems. Estimated fix: 3 hours.")

# --- MECHANIC VIEW ---
elif st.session_state.auth_role == "Mechanic":
    st.title("🔧 FIELD OPERATIONS HUB")
    st.subheader("Available Jobs Near You")
    st.dataframe(db_data[db_data['Status'] == "Pending"])
    
    st.subheader("🚨 SOS EMERGENCY SHIELD")
    if st.button("TRIGGER PANIC BUTTON"):
        st.error("EMERGENCY SIGNAL SENT TO PRIVATE SECURITY.")

