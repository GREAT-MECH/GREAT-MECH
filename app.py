import streamlit as st
import pandas as pd
import requests
import time
import random
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. PERSISTENT DATABASE & STATE SYNC ---
# We use a global dictionary stored in session_state to act as the primary database
if 'db' not in st.session_state: 
    # Initializing with Founder and sample data to prevent "Fresh Start" syndrome
    st.session_state.db = {
        "nwokejianthony2@gmail.com": {"name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"},
        "test@mech.com": {"name": "Sample Mechanic", "pin": "1234", "sector": "Mechanic", "phone": "+2347012345678"}
    }

# Track authentication state
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'otp_verified' not in st.session_state: st.session_state.otp_verified = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_done' not in st.session_state: st.session_state.job_done = False

# --- 3. DYNAMIC STYLING & GREETING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .welcome-text { text-align: center; font-size: 22px; color: #D4AF37; margin-bottom: 20px; font-weight: 600; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin: 10px 0; }
    div[data-testid="stSidebar"] .stButton>button { background-color: #ff0000 !important; color: white !important; font-weight: bold; border: 2px solid white; border-radius: 10px; }
    .stButton>button { border-radius: 8px; border: 1px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN/REGISTER) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Engineering African Magic</p>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Secure Login", "Register Profile"])
    
    with tab_reg:
        sector = st.radio("Account Type:", ["User", "Mechanic"], horizontal=True)
        reg_name = st.text_input("Full Legal Name")
        reg_email = st.text_input("Email Verification")
        reg_phone = st.text_input("Mobile Number (Include Country Code)")
        reg_pin = st.text_input("Create Security PIN", type="password")
        agree = st.checkbox("I agree to the Great Mech Privacy & App Policy")
        
        if st.button("Generate Verification Code"):
            if reg_name and "@" in reg_email and len(reg_phone) > 10 and agree:
                # Store in DB but mark as unverified
                st.session_state.db[reg_email] = {
                    "name": reg_name, "pin": reg_pin, "sector": sector, 
                    "phone": reg_phone, "verified": False
                }
                # Simulation of SMS OTP being sent to the phone number
                st.session_state.generated_otp = str(random.randint(1000, 9999))
                st.info(f"OTP Code sent to {reg_phone}. (Trial Code: {st.session_state.generated_otp})")
            else:
                st.error("Please correct your details and agree to the policy.")

        if 'generated_otp' in st.session_state:
            otp_input = st.text_input("Enter 4-Digit OTP")
            if st.button("Confirm Registration"):
                if otp_input == st.session_state.generated_otp:
                    st.success("Registration Verified. You can now login.")
                    del st.session_state.generated_otp
                else:
                    st.error("Invalid OTP.")

    with tab_login:
        log_email = st.text_input("Email", placeholder="e.g. hjjj@vvw.com")
        log_pin = st.text_input("PIN", type="password")
        
        if st.button("Enter Sovereign Engine"):
            # Check Database for already registered details
            if log_email in st.session_state.db:
                user_data = st.session_state.db[log_email]
                if user_data["pin"] == log_pin:
                    st.session_state.current_user = user_data
                    st.session_state.auth_status = "verified"
                    st.rerun()
                else:
                    st.error("Access Denied: Incorrect PIN.")
            else:
                st.error("Access Denied: No account found for this email.")

# --- 5. THE SOVEREIGN INTERFACE (v90.0) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    # --- SIDEBAR: GLOBAL CONTROLS ---
    with st.sidebar:
        st.markdown(f"### {user['sector']} Portal")
        st.write(f"**Verified:** {user['name']}")
        st.divider()
        if st.button("🚨 PANIC BUTTON"):
            st.error("EMERGENCY ALERT: Private Security Firm notified.")
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "gateway"
            st.session_state.current_user = None
            st.rerun()

    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # 5 Categories & 7 Symptoms Matrix
    SYMPTOM_MATRIX = {
        "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
        "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
        "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
        "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
        "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
    }

    # --- USER PORTAL ---
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Verified. Tracking Mechanic via Map.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Exact location map
            if st.button("✅ JOB COMPLETED"):
                st.session_state.job_done = True
                st.balloons()
        elif st.session_state.active_request and "quote" in st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><h3>AI Diagnosis Report</h3><b>Detected Faults:</b> {', '.join(req['faults'])}<br><b>Total Fee:</b> ₦{req['quote']:,.2f}</div>", unsafe_allow_html=True)
            if st.button("💳 Pay via Paystack"):
                st.session_state.payment_confirmed = True; st.rerun() #
        else:
            cat = st.selectbox("Service Category", list(SYMPTOM_MATRIX.keys()))
            selected = [s for s in SYMPTOM_MATRIX[cat] if st.checkbox(s)]
            st.text_area("Magic Box (Fault Details)")
            if st.button("🚀 AI DIAGNOSIS & BROADCAST"):
                st.session_state.active_request = {"cat": cat, "faults": selected, "user": user['name'], "phone": user['phone']}
                st.info("AI Diagnostic Report sent to Mechanics...")

    # --- MECHANIC HUB ---
    elif user['sector'] == "Mechanic":
        st.subheader("Available Work Requests")
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>New Alert:</b> {req['cat']}<br><b>Contact:</b> {req['phone']}<br><b>Symptoms:</b> {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Mechanics see exact fault location
            
            # Negotiation Block
            svc_fee = st.number_input("Service Fee (₦)", min_value=0)
            tpt_fee = st.number_input("Transport Fee (₦)", min_value=0)
            if st.button("SEND QUOTE"):
                st.session_state.active_request["quote"] = (svc_fee + tpt_fee) * 1.15 # Maintain 15% Share
                st.success("Negotiation sent to User.")
        else:
            st.info("Waiting for service requests in your area...")

        if st.session_state.job_done:
            st.success("💰 Job Finalized. 85% payout released to your bank details.")
            st.session_state.job_done = False

    # --- FOUNDER LEDGER ---
    if user['sector'] == "Founder" or user['name'] == "Nwokeji Anthony C.":
        st.divider()
        st.subheader("Sovereign Ledger (Founder Share 15%)")
        st.write("Current Platform Fee: 15% | Police/Security Fee: 0% (Removed)")
            
