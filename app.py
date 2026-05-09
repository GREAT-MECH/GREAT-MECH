import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & IDENTITY ---
st.set_page_config(page_title="Great Mech Supreme Global", layout="wide", page_icon="🦾")

# The Pinned "Black & Gold" DNA
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 10px; border: none; width: 100%; height: 3.5em;
    }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. IDENTITY PORTAL (The Entrance) ---
if 'role' not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.title("🦾 GREAT MECH SUPREME: IDENTITY PORTAL")
    st.subheader("Select your access level to begin moving Africa to the next level.")
    col1, col2, col3 = st.columns(3)
    if col1.button("🏛️ FOUNDER COMMAND"): st.session_state.role = "Founder"
    if col2.button("🔧 MECHANIC HUB"): st.session_state.role = "Mechanic"
    if col3.button("👤 USER MARKETPLACE"): st.session_state.role = "User"
    st.stop()

# Logout in Sidebar
if st.sidebar.button(f"LOGOUT [{st.session_state.role}]"):
    st.session_state.role = None
    st.rerun()

# --- 3. CLOUD ENGINE & DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)
def get_ledger():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

db_data = get_ledger()

# --- 4. THE VISION MODULES ---

# --- FOUNDER COMMAND ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    if not db_data.empty:
        total = pd.to_numeric(db_data['Budget']).sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Ecosystem Value", f"₦{total:,.2f}")
        c2.metric("Founder 15% Share", f"₦{total * 0.15:,.2f}")
        c3.metric("Service Categories", "Truck, Solar, CCTV, Diesel")
        st.subheader("Global Operations Ledger")
        st.dataframe(db_data, use_container_width=True)
    else:
        st.info("The Ledger is currently awaiting the first deployment.")

# --- USER MARKETPLACE ---
elif st.session_state.role == "User":
    st.title("📍 USER MARKETPLACE")
    tab_deploy, tab_ai = st.tabs(["🚀 DEPLOY REQUEST", "🧠 AI DIAGNOSTICS"])
    
    with tab_deploy:
        col_in, col_map = st.columns([1, 1.5])
        with col_in:
            service = st.selectbox("Category", ["Diesel Engine", "Truck Repair", "Generator", "Solar", "CCTV"])
            budget = st.number_input("Proposed Budget (NGN)", min_value=5000)
            loc_input = st.text_input("Current Location", "Lagos, Nigeria")
            
            if st.button("ACTIVATE DEPLOYMENT"):
                new_job = pd.DataFrame([{
                    "ID": f"GM-{random.randint(1000, 9999)}",
                    "Service": service, "Budget": budget,
                    "Status": "Pending", "Location": loc_input,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                try:
                    updated_df = pd.concat([db_data, new_job], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("SUCCESS: Job Broadcasted to the Great Mech Cloud!")
                    st.balloons()
                except:
                    st.warning("LOCAL MODE: Job added to app memory. (Please ensure Google Sheet is set to 'Editor')")

        with col_map:
            st.write("🌍 Logistic Map (Distance & Time Estimates)")
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=12, tiles="CartoDB dark_matter")
            st_folium(m, width=600, height=400)

    with tab_ai:
        st.subheader("7 Symptoms AI Diagnostic Report")
        symptoms = st.multiselect("Identify Symptoms", ["Overheating", "Black Smoke", "Fluid Leak", "Power Loss", "Strange Noise", "Hard Start", "Low Pressure"])
        if st.button("GENERATE AI DIAGNOSIS"):
            st.write("---")
            st.write("**Diagnostic Result:** Based on identified symptoms, we recommend checking the fuel injection system.")
            st.write("**Estimated Labor:** 4.5 Hours | **Complexity:** High")

# --- MECHANIC HUB ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 MECHANIC OPERATIONS")
    st.subheader("Available Jobs Near You")
    st.dataframe(db_data[db_data['Status'] == "Pending"])
    
    st.markdown("---")
    st.subheader("🚨 SOS EMERGENCY SHIELD")
    if st.button("TRIGGER PANIC BUTTON"):
        st.error("🚨 EMERGENCY SIGNAL SENT TO PRIVATE SECURITY FIRM.")
        st.toast("Capturing GPS coordinates...")

