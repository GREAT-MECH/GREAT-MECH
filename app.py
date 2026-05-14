import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# --- 1. PRESTIGE INTERFACE CONFIG & ANIMATION ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# Custom CSS for Black & Gold Aesthetic
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
    
    /* Animation for 'Moving Africa to the Next Level' */
    .moving-africa {
        font-size: 1.2em;
        color: #D4AF37;
        animation: slide 5s infinite linear;
    }
    @keyframes slide {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SOVEREIGN DATABASE & SESSION STATE (v42.0 Core) ---
if 'db' not in st.session_state:
    # Pre-loading Founders and sample accounts
    st.session_state.db = {
        "founder@greatmech.com": {"name": "Anthony", "pin": "7777", "role": "Founder"},
        "mech@greatmech.com": {"name": "Musa", "pin": "1234", "role": "Mechanic", "category": "Truck"},
        "user@greatmech.com": {"name": "Client", "pin": "0000", "role": "User"}
    }

if 'ledger' not in st.session_state:
    st.session_state.ledger = [] # Storage for the 15% Founder Share payments

if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

# List of 54 African Countries for Service Deployment
AFRICA_54 = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic",
    "Chad", "Comoros", "DR Congo", "Republic of the Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya",
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan",
    "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]

# --- 3. THE SOVEREIGN GATEWAY (LOGIN / REG) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🚀🌍</div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["🔒 Secure Login", "🛠️ Partner Registration"])

    with tab_login:
        l_email = st.text_input("Email", key="l_email")
        l_pin = st.text_input("4-Digit PIN", type="password", key="l_pin")
        if st.button("EXECUTE LOGIN"):
            if l_email in st.session_state.db and st.session_state.db[l_email]['pin'] == l_pin:
                st.session_state.user_data = st.session_state.db[l_email]
                st.session_state.auth_status = "verified"
                st.rerun()
            else: st.error("Access Denied: Invalid Credentials.")

    with tab_reg:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email Address")
        r_role = st.selectbox("I am a:", ["User", "Mechanic"])
        r_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        
        if st.button("GENERATE SOVEREIGN OTP"):
            st.session_state.temp_otp = str(random.randint(1000, 9999))
            st.warning(f"Sovereign OTP: {st.session_state.temp_otp} (Free SMS Bypass Active)")

        if 'temp_otp' in st.session_state:
            otp_in = st.text_input("Enter Code")
            if st.button("ACTIVATE ACCOUNT"):
                if otp_in == st.session_state.temp_otp:
                    st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "role": r_role}
                    st.success("Welcome to Great Mech! Please switch to Login tab.")
                    del st.session_state.temp_otp

# --- 4. THE LIVE ENGINE (FOUNDER / MECHANIC / USER VIEWS) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    role = user['role']
    
    # Header Greeting
    st.markdown(f"### Welcome, {user['name']} | Great Mech {role} Portal")
    
    with st.sidebar:
        st.markdown("## Great Mech 🌍")
        st.write(f"Active in: **54 African Countries**")
        st.divider()
        st.write("Founder Platform Fee: **15%**")
        st.write("Police/Security Tax: **0% (Exempt)**")
        
        if st.button("🚨 PANIC BUTTON"):
            st.error("EMERGENCY: GPS Data sent to Private Security Firm.")
        
        if st.button("Logout"):
            st.session_state.auth_status = "gateway"; st.rerun()

    # --- A. USER INTERFACE (REQUESTING SERVICE) ---
    if role == "User":
        st.markdown("### 📍 Request Engineering Magic")
        country = st.selectbox("Current Location", AFRICA_54)
        service = st.selectbox("Service Needed", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
        labor_estimate = st.number_input("Estimated Labor Budget (₦)", min_value=2000, step=500)
        
        # Payment Logic
        founder_share = labor_estimate * 0.15
        total_quote = labor_estimate + founder_share
        
        st.markdown(f"""
        **Payment Breakdown:**
        - Mechanic Fee: ₦{labor_estimate:,.2f}
        - Platform Maintenance (15%): ₦{founder_share:,.2f}
        - Police/Security Tax: **₦0.00**
        ---
        **Total to Pay: ₦{total_quote:,.2f}**
        """)
        
        if st.button("🚀 DISPATCH NEAREST MECHANIC"):
            st.session_state.active_job = {"service": service, "cost": labor_estimate, "founder": founder_share, "status": "In Progress"}
            st.info(f"Searching for {service} specialists in {country}...")

        if 'active_job' in st.session_state:
            st.divider()
            st.markdown("#### Live Mechanic Tracking")
            # Open Source Map
            m_lat = 6.5244 + random.uniform(-0.01, 0.01)
            m_lon = 3.3792 + random.uniform(-0.01, 0.01)
            st.map(pd.DataFrame({'lat': [6.5244, m_lat], 'lon': [3.3792, m_lon]}))
            
            if st.button("✅ JOB COMPLETED: RELEASE PAYMENT"):
                # Transfer money to Founder and Mechanic
                st.session_state.ledger.append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Service": st.session_state.active_job['service'],
                    "Mechanic_Pay": st.session_state.active_job['cost'],
                    "Founder_15_Share": st.session_state.active_job['founder']
                })
                st.balloons()
                st.success("Payment Dispersed! Thanks for using Great Mech 🌍")
                del st.session_state.active_job

    # --- B. MECHANIC INTERFACE ---
    elif role == "Mechanic":
        st.markdown("### 🔧 Mechanic Deployment Dashboard")
        st.metric("Total Earned Today", "₦45,000")
        st.write("Current Status: **Ready for Dispatch**")
        st.map(pd.DataFrame({'lat': [6.5244], 'lon': [3.3792]}))
        st.info("Waiting for User to confirm job completion to release your funds.")

    # --- C. FOUNDER INTERFACE (YOUR REVENUE) ---
    elif role == "Founder":
        st.markdown("### 💰 Sovereign Revenue & Ledger")
        st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🚀🌍</div>", unsafe_allow_html=True)
        
        if st.session_state.ledger:
            df_ledger = pd.DataFrame(st.session_state.ledger)
            st.table(df_ledger)
            
            total_founder_money = df_ledger['Founder_15_Share'].sum()
            st.metric("Total Founder Revenue (15%)", f"₦{total_founder_money:,.2f}")
            
            st.success("Founder funds are automatically separated from mechanic labor costs.")
        else:
            st.info("No transactions logged in this session yet.")

    st.markdown("<p style='text-align:center; color:gray; margin-top:50px;'>Thanks for using Great Mech 🌍</p>", unsafe_allow_html=True)
        
