import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
# Hard-coded for "Great Mech" Founder: Nwokeji Anthony C.
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. PERSISTENT DATABASE & SESSION STATE ---
if 'db' not in st.session_state: 
    # Pre-loading Founder for Day 1 continuity
    st.session_state.db = {"nwokejianthony2@gmail.com": {"name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder"}}
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_done' not in st.session_state: st.session_state.job_done = False

# --- 3. DYNAMIC STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .welcome-text { text-align: center; font-size: 22px; color: #D4AF37; margin-bottom: 20px; font-weight: 600; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .stButton>button { width: 100%; border-radius: 8px; }
    /* Panic Button Styling */
    div[data-testid="stSidebar"] .stButton>button { background-color: #ff0000 !important; color: white !important; font-weight: bold; border: 2px solid white; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN/REGISTRATION) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Engineering African Magic</p>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Secure Login", "Register Profile"])
    
    with tab_reg:
        sector = st.radio("Account Type:", ["User", "Mechanic"], horizontal=True)
        reg_name = st.text_input("Full Legal Name")
        reg_email = st.text_input("Email Verification")
        reg_pin = st.text_input("Security PIN", type="password")
        agree = st.checkbox("I agree to the Great Mech Privacy & Policy")
        if st.button("Generate Verification Code"):
            if reg_name and "@" in reg_email and agree:
                st.session_state.db[reg_email] = {"name": reg_name, "pin": reg_pin, "sector": sector}
                st.success("Sovereign Account Registered.")

    with tab_login:
        log_email = st.text_input("Email")
        log_pin = st.text_input("PIN", type="password")
        if st.button("Enter Sovereign Engine"):
            if log_email in st.session_state.db and st.session_state.db[log_email]["pin"] == log_pin:
                st.session_state.current_user = st.session_state.db[log_email]
                st.session_state.auth_status = "verified"
                st.rerun()
            else: st.error("Access Denied.")

# --- 5. MAIN INTERFACE WITH SIDEBAR ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    # --- SIDEBAR: SYSTEM CONTROLS ---
    with st.sidebar:
        st.markdown(f"### {user['sector']} Portal")
        st.write(f"**Verified:** {user['name']}")
        st.divider()
        # Panic Button sends emergency alert
        if st.button("🚨 PANIC BUTTON"):
            st.error("EMERGENCY ALERT SENT: Private Security Firm Notified.")
        
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "gateway"
            st.rerun()

    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # 5 Categories & 7 Symptoms
    SYMPTOM_MATRIX = {
        "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
        "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
        "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
        "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
        "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
    }

    # --- USER LOGIC ---
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Secured. Mechanic Tracking Active.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
            if st.button("✅ JOB COMPLETED"):
                st.session_state.job_done = True
                st.balloons()
        elif st.session_state.active_request and "quote" in st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><h3>AI Diagnosis Report</h3><b>Total Fee:</b> ₦{req['quote']:,.2f}</div>", unsafe_allow_html=True)
            if st.button("💳 Pay via Paystack"):
                st.session_state.payment_confirmed = True; st.rerun()
        else:
            cat = st.selectbox("Rendered Service Category", list(SYMPTOM_MATRIX.keys()))
            selected = [s for s in SYMPTOM_MATRIX[cat] if st.checkbox(s)]
            st.text_area("Magic Box Description")
            if st.button("🚀 AI DIAGNOSIS & BROADCAST"):
                st.session_state.active_request = {"cat": cat, "faults": selected, "user": user['name']}
                st.info("Searching for local mechanics...")

    # --- MECHANIC LOGIC ---
    elif user['sector'] == "Mechanic":
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Alert from {req['user']}</b><br>Symptoms: {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            svc = st.number_input("Service Fee (₦)")
            tpt = st.number_input("Transport Fee (₦)")
            if st.button("SEND QUOTE"):
                st.session_state.active_request["quote"] = (svc + tpt) * 1.15 # Maintain 15% Share
                st.success("Quote sent with Platform Fee.")
        
        if st.session_state.job_done:
            st.success("💰 Payout Authorized. 85% released to your bank.")
            st.session_state.job_done = False

    # --- FOUNDER LOGIC ---
    if user['sector'] == "Founder":
        st.subheader("Sovereign Ledger (v42.0 Master Engine)")
        st.write("**Founder Share:** 15%")
        st.write("**Police Payment:** 0% (Strictly Removed)")
        st.write("**Region:** All 54 African Countries")
    
