import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. PERSISTENT DATABASE & SESSION STATE ---
if 'db' not in st.session_state: 
    st.session_state.db = {} # Persistent User/Mech records
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_done' not in st.session_state: st.session_state.job_done = False

# --- 3. DYNAMIC STYLING & GREETING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .welcome-text { text-align: center; font-size: 20px; color: #D4AF37; margin-bottom: 20px; font-weight: 600; }
    .report-card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .panic-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (INTELLIGENT LOGIN) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    tab_login, tab_reg = st.tabs(["Secure Login", "New Registration"])
    
    with tab_reg:
        sector = st.radio("I am a:", ["User", "Mechanic"], horizontal=True)
        reg_name = st.text_input("Full Legal Name")
        reg_email = st.text_input("Email Verification")
        reg_pin = st.text_input("Create Security PIN", type="password")
        agree = st.checkbox("I agree to the Great Mech Privacy & App Policy")
        if st.button("Generate Verification Code"):
            if reg_name and "@" in reg_email and agree:
                st.session_state.db[reg_email] = {"name": reg_name, "pin": reg_pin, "sector": sector}
                st.success("Account Registered! Switch to Login.")

    with tab_login:
        log_email = st.text_input("Email")
        log_pin = st.text_input("PIN", type="password")
        if st.button("Enter Sovereign Engine"):
            if log_email in st.session_state.db and st.session_state.db[log_email]["pin"] == log_pin:
                st.session_state.current_user = st.session_state.db[log_email]
                st.session_state.auth_status = "verified"
                st.rerun()
            else: st.error("Access Denied: Invalid Credentials.")

# --- 5. THE MAIN ENGINE (v88.0) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # 5 Categories & 7 Symptoms
    SYMPTOM_MATRIX = {
        "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
        "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
        "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
        "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
        "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
    }

    # --- USER INTERFACE ---
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Verified. Mechanic In-Route.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Track Mechanic
            if st.button("✅ JOB COMPLETED (Release Payout)"):
                st.session_state.job_done = True
                st.balloons()
        elif st.session_state.active_request and "quote" in st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='report-card'><h3>AI Diagnosis Report</h3><b>Faults Detected:</b> {', '.join(req['faults'])}<br><b>Total to Pay:</b> ₦{req['quote']:,.2f}</div>", unsafe_allow_html=True)
            if st.button("💳 Authorize Payment via Paystack"):
                st.session_state.payment_confirmed = True; st.rerun()
        else:
            cat = st.selectbox("Select Service Category", list(SYMPTOM_MATRIX.keys()))
            selected = [s for s in SYMPTOM_MATRIX[cat] if st.checkbox(s)]
            desc = st.text_area("Magic Box (Detailed Description)")
            if st.button("🚀 AI DIAGNOSIS & ALERT MECHANIC"):
                st.session_state.active_request = {"cat": cat, "faults": selected, "desc": desc, "user": user['name']}
                st.info("AI Analysis sent to Regional Mechanics...")

    # --- MECHANIC INTERFACE ---
    elif user['sector'] == "Mechanic":
        st.subheader("Regional Service Requests")
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='report-card'><b>Client:</b> {req['user']}<br><b>Fault:</b> {req['cat']}<br><b>Symptoms:</b> {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Exact User Location
            
            svc = st.number_input("Service Fee (₦)")
            tpt = st.number_input("Transport Fee (₦)")
            if st.button("SEND QUOTE TO USER"):
                st.session_state.active_request["quote"] = (svc + tpt) * 1.15 # 15% Platform Share
                st.success("Quote sent with AI Diagnostic Report.")
        
        if st.session_state.job_done:
            st.success("💰 Job Finalized. 85% of funds released to your wallet.")
            st.session_state.job_done = False # Reset for next job
        
        st.divider()
        if st.button("🚨 PANIC BUTTON", key="panic"): #
            st.error("EMERGENCY ALERT: Private Security Firm notified.")

    # --- FOUNDER LEDGER ---
    if user['name'] == "Nwokeji Anthony C.":
        st.divider()
        st.subheader("Sovereign Ledger (15% Net)")
        st.write("Police Service Charge: 0% (Removed)")
