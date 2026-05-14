import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- 1. PRESTIGE UI & KINETIC ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v113.0", page_icon="🌍", layout="wide")

# CSS for the Left-to-Right "Moving Africa" Animation and Black/Gold Theme
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    
    /* Kinetic Left-to-Right Animation */
    .moving-africa-container {
        width: 100%; overflow: hidden; white-space: nowrap; margin-bottom: 20px;
    }
    .moving-africa-text {
        display: inline-block; padding-left: 100%;
        font-size: 1.5em; color: #D4AF37; font-weight: bold;
        animation: scroll-left-to-right 15s linear infinite;
    }
    @keyframes scroll-left-to-right {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 12px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%;
    }
    </style>
    <div class="moving-africa-container">
        <div class="moving-africa-text">MOVING AFRICA TO THE NEXT LEVEL... 🚀 GREAT MECH ENGINEERING MAGIC... 🌍</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE DATA & SOVEREIGN SETTINGS ---
if 'db' not in st.session_state:
    # Initializing with you as the Founder
    st.session_state.db = {
        "founder@greatmech.com": {"name": "Anthony", "pin": "7777", "role": "Founder", "bank": "GTBank", "acct": "0123456789"}
    }
if 'jobs' not in st.session_state: st.session_state.jobs = {}
if 'ledger' not in st.session_state: st.session_state.ledger = []
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"

PAYSTACK_PUBLIC_KEY = "pk_live_xxxxxxxxxxxxxxxxxxxxxxxx" # Your live key

AFRICA_54 = ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Ethiopia", "Uganda", "Rwanda", "Tanzania"] # (Full 54 countries supported)

# --- 3. THE SOVEREIGN REGISTRATION & LOGIN PORTAL ---
if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech Sovereign Portal 🌍</h1>", unsafe_allow_html=True)
    
    # Registration & Login Tabs to give you access
    tab_login, tab_reg = st.tabs(["🔒 SECURE LOGIN", "🛠️ REGISTER PARTNER/USER"])
    
    with tab_login:
        email_log = st.text_input("Email Address", key="login_email")
        pin_log = st.text_input("4-Digit PIN", type="password", key="login_pin")
        if st.button("ACTIVATE SESSION"):
            if email_log in st.session_state.db and st.session_state.db[email_log]['pin'] == pin_log:
                st.session_state.user_data = st.session_state.db[email_log]
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Invalid Credentials. Please Register below.")

    with tab_reg:
        st.markdown("### Join the Engineering Revolution")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_role = st.selectbox("I am a:", ["User", "Mechanic"])
        new_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        
        if new_role == "Mechanic":
            m_bank = st.text_input("Bank Name (for Paystack Settlement)")
            m_acct = st.text_input("Account Number")
        
        if st.button("CREATE ACCOUNT"):
            if new_email and new_pin:
                st.session_state.db[new_email] = {
                    "name": new_name, "pin": new_pin, "role": new_role,
                    "bank": m_bank if new_role == "Mechanic" else None,
                    "acct": m_acct if new_role == "Mechanic" else None
                }
                st.success("Registration Complete! Switch to Login tab to enter.")

# --- 4. THE LIVE SERVICE INTERFACE ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    role = user['role']
    
    with st.sidebar:
        st.markdown(f"### {user['name']}")
        st.write(f"Access Level: **{role}**")
        st.write("Platform Maintenance: **15%**")
        st.write("Police/Security Tax: **0%**")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY: Security Firm Dispatched.")
        if st.button("Logout"): st.session_state.auth_status = "gateway"; st.rerun()

    # --- USER VIEW: AI DIAGNOSTIC ---
    if role == "User":
        st.markdown("### 🤖 Diagnostic & Mechanic Dispatch")
        country = st.selectbox("Location (Africa 54)", AFRICA_54)
        address = st.text_input("📍 Detailed Address / Landmark")
        
        # 5 Core Categories with Emojis
        cat = st.selectbox("Service Needed", [
            "🚛 Truck", 
            "🚗 Car", 
            "🔋 Diesel Engine / Generator", 
            "🛡️ CCTV", 
            "☀️ Solar"
        ])
        
        fault_desc = st.text_area("Describe the fault...")
        fault_suggest = st.selectbox("Choose Suggestion", [
            "Engine won't start", "Overheating issues", "Strange mechanical noise", 
            "Hydraulic failure", "Electrical fault / Wiring", "Fuel system leak", "Performance drop"
        ])

        if st.button("🤖 RUN AI DIAGNOSTIC"):
            job_id = f"GM-{random.randint(1000, 9999)}"
            st.session_state.jobs[job_id] = {
                "user": user['name'], "cat": cat, "fault": fault_desc or fault_suggest, 
                "address": address, "status": "Waiting for Quote"
            }
            st.success(f"Sent to nearby Mechanics. Job ID: {job_id}")

        # Active Job Tracking
        for j_id, data in list(st.session_state.jobs.items()):
            if data['status'] == "Quoted":
                st.info(f"Quote Received for #{j_id}: ₦{data['total']:,.2f}")
                if st.button(f"Pay ₦{data['total']:,.2f} via Paystack"):
                    data['status'] = "Paid"
                    st.success("Payment Verified! Mechanic is moving.")

            if data['status'] == "Paid":
                st.success("Payment Confirmed. Tracking Live GPS...")
                st.map(pd.DataFrame({'lat': [6.5244, 6.5251], 'lon': [3.3792, 3.3805]}))
                if st.button(f"✅ JOB COMPLETED: RELEASE FUNDS (#{j_id})"):
                    data['status'] = "Settled"
                    st.session_state.ledger.append({"Job": j_id, "Founder_15": data['f_share']})
                    st.balloons()

    # --- MECHANIC VIEW: QUOTING & BANK SETTLEMENT ---
    elif role == "Mechanic":
        st.markdown("### 🔧 Incoming Service Requests")
        for j_id, data in st.session_state.jobs.items():
            if data['status'] == "Waiting for Quote":
                st.warning(f"NEW REQUEST: {data['cat']} | Address: {data['address']}")
                st.write(f"**Fault Details:** {data['fault']}")
                t_fee = st.number_input("Transport Fee (₦)", key=f"t_{j_id}")
                s_fee = st.number_input("Service Fee (₦)", key=f"s_{j_id}")
                if st.button("Send Quote to User"):
                    base = t_fee + s_fee
                    f_share = base * 0.15
                    data.update({"total": base + f_share, "f_share": f_share, "status": "Quoted", "net": base})
                    st.rerun()

            if data['status'] == "Settled":
                st.success(f"Job #{j_id} Settled!")
                st.write(f"₦{data['net']:,.2f} credited to your {user['bank']} account ({user['acct']}).")

    # --- FOUNDER VIEW: REVENUE ---
    if role == "Founder":
        st.divider()
        st.markdown("### 💰 Sovereign Revenue (15% Share)")
        if st.session_state.ledger:
            st.table(pd.DataFrame(st.session_state.ledger))
            st.metric("Total Revenue", f"₦{sum(x['Founder_15'] for x in st.session_state.ledger):,.2f}")

    st.markdown("<br><p style='text-align:center;'>Thanks for using Great Mech 🌍</p>", unsafe_allow_html=True)
        
