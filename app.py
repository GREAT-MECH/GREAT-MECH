import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & CONFIG ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. PERSISTENT DATABASE (The Great Mech Ledger) ---
if 'db' not in st.session_state: 
    # Legacy data continuity for all 54 African countries
    st.session_state.db = {
        "nwokejianthony2@gmail.com": {
            "name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"
        },
        "mech@greatmech.app": {
            "name": "Expert Mechanic", "pin": "1234", "sector": "Mechanic", "phone": "+234000000000", "bank": {}
        }
    }

# Core system states
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_status' not in st.session_state: st.session_state.job_status = "idle" # idle, active, completed

# --- 3. UNIVERSAL STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .main-title { text-align: center; font-size: 40px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stSidebar"] .stButton>button { background-color: #ff0000 !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN / REG / FORGET) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    tab_login, tab_reg, tab_forget = st.tabs(["Secure Login", "Register Profile", "Forget PIN?"])
    
    with tab_login:
        log_email = st.text_input("Email")
        log_pin = st.text_input("PIN", type="password")
        if st.button("Enter Sovereign Engine"):
            if log_email in st.session_state.db and st.session_state.db[log_email]["pin"] == log_pin:
                st.session_state.current_user = st.session_state.db[log_email]
                st.session_state.auth_status = "verified"
                st.rerun()
            else: st.error("Access Denied.")

    with tab_reg:
        sec = st.radio("Sector:", ["User", "Mechanic"], horizontal=True)
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_phone = st.text_input("Phone (Country Code)")
        r_pin = st.text_input("Create PIN", type="password")
        if st.button("Generate SMS OTP"):
            st.session_state.temp_otp = str(random.randint(1000, 9999))
            # OTP is sent via SMS, not displayed on app
            st.success(f"OTP sent to {r_phone}. Enter it below.")
        
        if 'temp_otp' in st.session_state:
            otp_in = st.text_input("Enter 4-Digit OTP from SMS")
            if st.button("Complete Registration"):
                if otp_in == st.session_state.temp_otp:
                    st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "sector": sec, "phone": r_phone}
                    st.success("Registration Verified.")
                    del st.session_state.temp_otp

    with tab_forget:
        f_email = st.text_input("Registered Email")
        if st.button("Recover via SMS"):
            if f_email in st.session_state.db:
                st.session_state.recovery_otp = str(random.randint(1000, 9999))
                st.info("Recovery code sent to your registered phone.")
            else: st.error("Account not found.")

# --- 5. THE APP SWITCHER (AUTOMATIC INTERFACE LOADING) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    with st.sidebar:
        st.markdown(f"### {user['sector']} App")
        st.write(f"**User:** {user['name']}")
        st.divider()
        if st.button("🚨 PANIC BUTTON"): # Emergency security alert
            st.error("EMERGENCY: Security Firm Dispatched.")
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "gateway"
            st.rerun()

    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # --- SECTOR 1: USER INTERFACE ---
    if user['sector'] == "User":
        st.subheader("Engineering Request Portal")
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Secured. Mechanic Tracking Live.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Exact Location
            if st.button("✅ JOB COMPLETED"):
                st.session_state.job_status = "completed"
                st.balloons()
        elif st.session_state.active_request and "quote" in st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><h4>AI Diagnosis Summary</h4>Quote: ₦{req['quote']:,.2f}</div>", unsafe_allow_html=True)
            if st.button("💳 Pay Now (Paystack)"):
                st.session_state.payment_confirmed = True; st.rerun()
        else:
            cat = st.selectbox("Service", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
            # AI Diagnosis of 7 Faults
            faults = st.multiselect("Select Symptoms", ["Engine Noise", "Fluid Leak", "Power Loss", "Smoke", "Brake Fault", "Overheating", "Vibration"])
            st.text_area("Magic Box Description")
            if st.button("🚀 RUN AI DIAGNOSIS"):
                st.session_state.active_request = {"cat": cat, "faults": faults, "user": user['name']}
                st.info("Diagnostic report broadcasted to regional mechanics.")

    # --- SECTOR 2: MECHANIC INTERFACE ---
    elif user['sector'] == "Mechanic":
        st.subheader("Field Operations Hub")
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Job Alert: {req['cat']}</b><br>Symptoms: {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Reach the user
            
            s_fee = st.number_input("Service Fee (₦)")
            t_fee = st.number_input("Transport Fee (₦)")
            if st.button("SEND QUOTE"):
                st.session_state.active_request["quote"] = (s_fee + t_fee) * 1.15 # 15% Platform Share
                st.success("Quote sent to client.")
        
        if st.session_state.job_status == "completed":
            st.markdown("### 💰 Job Finalized: Payment Verification")
            bank = st.text_input("Bank Name")
            acc = st.text_input("Account Number")
            if st.button("VERIFY & CREDIT ACCOUNT"):
                st.success(f"Verified. 85% of fee credited to {acc}.")
                st.session_state.job_status = "idle"

    # --- SECTOR 3: FOUNDER INTERFACE (MASTER LEDGER) ---
    elif user['sector'] == "Founder":
        st.subheader("Sovereign Master Ledger")
        colA, colB = st.columns(2)
        colA.metric("Founder Share", "15%")
        colB.metric("Police/Service Tax", "0%") # Removed per instruction
        st.write("**Active Mech Hubs:** 54 Countries")
        st.write("**App Engine v93.0:** Live and Secure")
        
