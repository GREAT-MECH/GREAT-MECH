import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- 1. PRESTIGE INTERFACE CONFIG & ANIMATIONS ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# Custom CSS: Black & Gold Aesthetic + Moving Africa Animation
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 12px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%;
    }
    .stTextInput>div>div>input { background-color: #1A1C24; color: gold; border: 1px solid #D4AF37; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1A1C24; color: gold; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; }
    
    .moving-africa {
        font-size: 1.4em; color: #D4AF37; text-align: center;
        animation: pulse 4s infinite ease-in-out;
    }
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SOVEREIGN ENGINE CORE DATA ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "founder@greatmech.com": {"name": "Anthony", "pin": "7777", "role": "Founder"},
        "mech@greatmech.com": {"name": "Sovereign Mech", "pin": "1234", "role": "Mechanic"}
    }
if 'jobs' not in st.session_state: st.session_state.jobs = {}
if 'ledger' not in st.session_state: st.session_state.ledger = []
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"

AFRICA_54 = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic",
    "Chad", "Comoros", "DR Congo", "Republic of the Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya",
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan",
    "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]

FAULT_SUGGESTIONS = [
    "Engine won't start", "Overheating issues", "Strange mechanical noise", 
    "Hydraulic failure", "Electrical fault / Wiring", "Fuel system leak", "Performance drop"
]

# --- 3. THE SOVEREIGN GATEWAY ---
if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🚀</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔒 Secure Login", "🛠️ Partner Registration"])
    with t1:
        email = st.text_input("Email", key="l_email")
        pin = st.text_input("4-Digit PIN", type="password", key="l_pin")
        if st.button("EXECUTE LOGIN"):
            if email in st.session_state.db and st.session_state.db[email]['pin'] == pin:
                st.session_state.user_data = st.session_state.db[email]
                st.session_state.auth_status = "verified"; st.rerun()
            else: st.error("Access Denied.")
    with t2:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_role = st.selectbox("Role", ["User", "Mechanic"])
        r_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        if st.button("GENERATE OTP"):
            st.session_state.temp_otp = str(random.randint(1000, 9999))
            st.warning(f"Sovereign OTP: {st.session_state.temp_otp}")
        if 'temp_otp' in st.session_state:
            otp_in = st.text_input("Enter Code")
            if st.button("ACTIVATE"):
                if otp_in == st.session_state.temp_otp:
                    st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "role": r_role}
                    st.success("Account Active. Please login."); del st.session_state.temp_otp

# --- 4. THE LIVE PORTAL (USER / MECHANIC / FOUNDER) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    role = user['role']
    
    with st.sidebar:
        st.markdown("## Great Mech 🌍")
        st.write(f"Welcome, {user['name']}")
        st.write("Founder Share: **15%**")
        st.write("Police Tax: **0%**")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY: Security Firm Alerted.")
        if st.button("Logout"): st.session_state.auth_status = "gateway"; st.rerun()

    # --- USER APP: AI DIAGNOSTIC & PAYSTACK ---
    if role == "User":
        st.markdown("### 🛠️ AI Diagnostic Portal")
        country = st.selectbox("Select Country", AFRICA_54)
        cat = st.selectbox("Category", ["Truck", "Car", "Diesel Generator", "CCTV", "Solar"])
        fault_desc = st.text_area("Describe the fault in detail...")
        fault_choice = st.selectbox("Or choose a common fault suggestion:", FAULT_SUGGESTIONS)
        
        if st.button("🤖 RUN AI DIAGNOSTIC"):
            job_id = f"GM-{random.randint(1000, 9999)}"
            st.session_state.jobs[job_id] = {"user": user['name'], "cat": cat, "fault": fault_desc or fault_choice, "status": "Waiting for Quote"}
            st.success(f"Diagnostic Report Sent to nearby Mechanics. Job ID: {job_id}")

        # Live Job Feed
        for j_id, data in list(st.session_state.jobs.items()):
            if data['status'] == "Quoted":
                st.divider()
                st.info(f"Mechanic Quote for {data['cat']} (#{j_id})")
                st.write(f"Transport: ₦{data['trans']:,.2f} | Service: ₦{data['serv']:,.2f}")
                
                # Payment Logic: 15% Founder Share + 0% Police Tax
                base_fees = data['trans'] + data['serv']
                founder_rev = base_fees * 0.15
                total_paystack = base_fees + founder_rev
                
                st.markdown(f"**Total Payable via Paystack: ₦{total_paystack:,.2f}**")
                if st.button(f"Pay Now for #{j_id}"):
                    data['status'] = "Paid"
                    st.session_state.ledger.append({"Date": datetime.now(), "Founder_15": founder_rev, "Mechanic_Pay": base_fees})
                    st.balloons()
            
            if data['status'] == "Paid":
                st.success(f"Payment Successful for #{j_id}! Mechanic is en route.")
                # GPS Tracking Map Activates here
                m_lat, m_lon = 6.5244 + random.uniform(-0.005, 0.005), 3.3792 + random.uniform(-0.005, 0.005)
                st.map(pd.DataFrame({'lat': [6.5244, m_lat], 'lon': [3.3792, m_lon]}))
                if st.button(f"Confirm Completion for #{j_id}"):
                    st.write("Thanks for using Great Mech 🌍"); del st.session_state.jobs[j_id]

    # --- MECHANIC APP: QUOTING SYSTEM ---
    elif role == "Mechanic":
        st.markdown("### 🔧 Incoming Service Requests")
        for j_id, data in st.session_state.jobs.items():
            if data['status'] == "Waiting for Quote":
                st.info(f"NEW REQUEST: {data['cat']} | Fault: {data['fault']}")
                t_fee = st.number_input("Input Transport Fee (₦)", key=f"t_{j_id}")
                s_fee = st.number_input("Input Service Fee (₦)", key=f"s_{j_id}")
                if st.button("Send Quote to User", key=f"btn_{j_id}"):
                    data.update({"trans": t_fee, "serv": s_fee, "status": "Quoted"}); st.rerun()

    # --- FOUNDER APP: SOVEREIGN REVENUE LEDGER ---
    if role == "Founder":
        st.divider()
        st.markdown("### 💰 Sovereign Revenue Ledger (15% Share)")
        if st.session_state.ledger:
            df = pd.DataFrame(st.session_state.ledger)
            st.table(df)
            st.metric("Total Platform Revenue", f"₦{df['Founder_15'].sum():,.2f}")
        else: st.info("Waiting for first transaction...")

    st.markdown("<p style='text-align:center; color:gray; margin-top:50px;'>Thanks for using Great Mech 🌍<br>Moving Africa to the next level.</p>", unsafe_allow_html=True)
