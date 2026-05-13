import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & CONFIG ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. PERSISTENT DATABASE ---
if 'db' not in st.session_state: 
    st.session_state.db = {
        "nwokejianthony2@gmail.com": {
            "name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"
        }
    }

# System State Management
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'recovery_mode' not in st.session_state: st.session_state.recovery_mode = False
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_status' not in st.session_state: st.session_state.job_status = "idle"

# --- 3. UNIVERSAL STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .main-title { text-align: center; font-size: 40px; font-weight: 900; color: #D4AF37; margin-bottom: 20px; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stSidebar"] .stButton>button { background-color: #ff0000 !important; color: white !important; font-weight: bold; }
    .forget-btn-container { text-align: left; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN / REG / RECOVERY) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    
    # RECOVERY INTERFACE (Triggered by Forget PIN)
    if st.session_state.recovery_mode:
        st.markdown("### 🔐 Security Recovery")
        f_email = st.text_input("Enter Registered Email", key="recovery_email_input")
        
        if st.button("Send Recovery SMS OTP"):
            if f_email in st.session_state.db:
                st.session_state.rec_otp = str(random.randint(1000, 9999))
                # Logic sends OTP to st.session_state.db[f_email]['phone']
                st.info("Recovery code sent to your registered phone number.")
            else: st.error("Email not found.")
        
        if 'rec_otp' in st.session_state:
            otp_val = st.text_input("Enter OTP from SMS", key="recovery_otp_input")
            new_pin = st.text_input("New PIN", type="password", key="recovery_pin_input")
            if st.button("Reset PIN & Login"):
                if otp_val == st.session_state.rec_otp:
                    st.session_state.db[f_email]['pin'] = new_pin
                    st.session_state.current_user = st.session_state.db[f_email]
                    st.session_state.auth_status = "verified"
                    st.session_state.recovery_mode = False
                    st.rerun()
                else: st.error("Invalid Code.")
        
        if st.button("Back to Login"):
            st.session_state.recovery_mode = False
            st.rerun()

    else:
        tab_login, tab_reg = st.tabs(["Secure Login", "Register Profile"])
        
        with tab_login:
            l_email = st.text_input("Email", key="login_email")
            l_pin = st.text_input("PIN", type="password", key="login_pin")
            
            if st.button("Enter Sovereign Engine"):
                if l_email in st.session_state.db and st.session_state.db[l_email]["pin"] == l_pin:
                    st.session_state.current_user = st.session_state.db[l_email]
                    st.session_state.auth_status = "verified"
                    st.rerun()
                else: st.error("Access Denied.")
            
            # Forget PIN placed exactly under the login button
            if st.button("Forget PIN?"):
                st.session_state.recovery_mode = True
                st.rerun()

        with tab_reg:
            sec = st.radio("Sector:", ["User", "Mechanic"], horizontal=True)
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Email", key="reg_email")
            r_phone = st.text_input("Phone Number")
            r_pin = st.text_input("Create PIN", type="password")
            if st.button("Verify Registration"):
                st.session_state.temp_otp = str(random.randint(1000, 9999))
                # SMS sent invisibly
                st.success(f"OTP sent to {r_phone}.")
            
            if 'temp_otp' in st.session_state:
                otp_in = st.text_input("Enter SMS OTP")
                if st.button("Confirm Account"):
                    if otp_in == st.session_state.temp_otp:
                        st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "sector": sec, "phone": r_phone}
                        st.success("Account Active.")
                        del st.session_state.temp_otp

# --- 5. THE APP SWITCHER (POST-LOGIN INTERFACES) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    with st.sidebar:
        st.markdown(f"### {user['sector']} Portal")
        st.write(f"**Verified:** {user['name']}")
        if st.button("🚨 PANIC BUTTON"):
            st.error("EMERGENCY ALERT: Private Security Dispatched.")
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "gateway"
            st.rerun()

    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # USER INTERFACE (AI Diagnosis & 15% Share Logic)
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Secured. Mechanic Tracking Active.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
            if st.button("✅ JOB COMPLETED"):
                st.session_state.job_status = "completed"
                st.balloons()
        else:
            cat = st.selectbox("Category", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
            st.multiselect("Symptoms", ["Engine Noise", "Fluid Leak", "Power Loss", "Smoke", "Brakes", "Overheat", "Vibration"])
            if st.button("🚀 AI DIAGNOSIS"):
                st.session_state.active_request = {"cat": cat, "user": user['name']}
                st.info("Broadcasted to regional mechanics.")

    # MECHANIC INTERFACE (Negotiation & Payout)
    elif user['sector'] == "Mechanic":
        if st.session_state.active_request:
            st.markdown(f"<div class='card'><b>Job Request: {st.session_state.active_request['cat']}</b></div>", unsafe_allow_html=True)
            svc = st.number_input("Service Fee (₦)")
            tpt = st.number_input("Transport Fee (₦)")
            if st.button("SEND QUOTE"):
                st.session_state.active_request["quote"] = (svc + tpt) * 1.15
                st.success("Quote sent (Includes 15% Founder Share).")
        
        if st.session_state.job_status == "completed":
            st.subheader("Final Payout")
            acc = st.text_input("Account Number for Credit")
            if st.button("VERIFY & PAY"):
                st.success(f"Verified. 85% released to {acc}.")
                st.session_state.job_status = "idle"

    # FOUNDER INTERFACE
    elif user['sector'] == "Founder":
        st.subheader("Sovereign Master Ledger")
        st.write("Commission: 15% | Security Tax: 0%")
        
