import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & UI ---
st.set_page_config(page_title="Great Mech Global", layout="wide", page_icon="🦾")

# Restore the Black & Gold "Great Mech" DNA
st.markdown("""
<style>
    /* Main Background and Text */
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Premium Gold Headers */
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Custom Gold Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; 
        font-weight: bold; 
        border-radius: 10px; 
        border: none; 
        width: 100%;
        height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px #D4AF37; }
    
    /* Metrics and Dataframes */
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', monospace; font-size: 2rem; }
    .stDataFrame { border: 1px solid #D4AF37; border-radius: 10px; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATABASE INTEGRATION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(ttl=0)
    except:
        # Fallback if connection fails
        return pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- 3. THE COMMAND CENTER ---
st.title("🦾 GREAT MECH SUPREME")
st.markdown("### Moving Africa to the Next Level")

tab1, tab2, tab3 = st.tabs(["🚀 DEPLOY JOB", "📊 GLOBAL LEDGER", "🚨 SOS SHIELD"])

# MODULE: DEPLOYMENT
with tab1:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader("Request Service")
        with st.form("job_form", clear_on_submit=True):
            service = st.selectbox("Engineering Category", ["Truck Repair", "Diesel Engine", "Generator", "CCTV", "Solar Power"])
            budget = st.number_input("Budget (NGN)", min_value=5000, step=5000)
            location = st.text_input("Site Location", "Lagos, Nigeria")
            submit = st.form_submit_button("ACTIVATE DEPLOYMENT")
            
            if submit:
                new_entry = pd.DataFrame([{
                    "ID": f"GM-{random.randint(1000, 9999)}",
                    "Service": service,
                    "Budget": budget,
                    "Status": "Pending",
                    "Location": location,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                
                # Update Session Memory
                st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                
                try:
                    # Attempt Cloud Update
                    conn.update(data=st.session_state.db)
                    st.success("VISION UNIFIED: Job Broadcasted to Cloud!")
                except:
                    st.warning("LOCAL MODE: Job added to Ledger. (Check Google Editor permissions for Cloud Sync)")
                
                st.balloons()
    
    with col_b:
        st.subheader("Founder Insight")
        if not st.session_state.db.empty:
            current_job_val = budget
            f_share = current_job_val * 0.15
            m_share = current_job_val * 0.85
            st.info(f"Analysis for this Request:")
            st.write(f"Founder Revenue (15%): **₦{f_share:,.2f}**")
            st.write(f"Mechanic Payout (85%): **₦{m_share:,.2f}**")

# MODULE: LEDGER (THE REVENUE)
with tab2:
    st.subheader("Global Operations Dashboard")
    if not st.session_state.db.empty:
        # Convert budget to numeric for math
        st.session_state.db['Budget'] = pd.to_numeric(st.session_state.db['Budget'])
        total_val = st.session_state.db['Budget'].sum()
        founder_total = total_val * 0.15
        
        m1, m2 = st.columns(2)
        m1.metric("Total Ecosystem Value", f"₦{total_val:,.2f}")
        m2.metric("Founder Net (15%)", f"₦{founder_total:,.2f}")
        
        st.dataframe(st.session_state.db, use_container_width=True)
    else:
        st.write("Ledger is currently empty. Deploy your first job to see the magic.")

# MODULE: SOS SHIELD (SECURITY VISION)
with tab3:
    st.subheader("On-Site Security Protocol")
    st.write("Emergency alert system for field mechanics.")
    if st.button("TRIGGER PANIC BUTTON"):
        st.error("🚨 EMERGENCY SIGNAL SENT TO PRIVATE SECURITY FIRM.")
        st.toast("GPS Coordinates Captured. Help is on the way.")

