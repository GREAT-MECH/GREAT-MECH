import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# --- 1. CORE IDENTITY & CONFIG ---
st.set_page_config(page_title="Great Mech v71", page_icon="🛠️", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = {"founder@greatmech.com": {"name": "Anthony", "pin": "7777", "sector": "Founder"}}

if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

# --- 2. SOVEREIGN GATEWAY (DEBUG ACTIVATED) ---
if st.session_state.auth_status == "gateway":
    st.title("🌍 Great Mech Sovereign Engine")
    st.info("Sovereign Debug Mode: Bypassing restricted SMS gateway for local testing.")
    
    tab_reg, tab_login = st.tabs(["🛠️ Registration", "🔒 Login"])
    
    with tab_reg:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_phone = st.text_input("Phone (e.g. +234...)")
        if st.button("Generate Sovereign OTP"):
            st.session_state.temp_otp = str(random.randint(1000, 9999))
            # In Debug, we show the code directly since the SMS is blocked in 321487.png
            st.warning(f"Your Security Code is: {st.session_state.temp_otp}")
            
        if 'temp_otp' in st.session_state:
            otp_in = st.text_input("Enter Code")
            if st.button("Activate Account"):
                if otp_in == st.session_state.temp_otp:
                    st.session_state.db[r_email] = {"name": r_name, "sector": "User"}
                    st.success("Account Active! Please switch to Login tab.")
                else: st.error("Invalid Code.")

# --- 3. THE NEXT LEVEL: GPS TRACKING MAP ---
elif st.session_status == "verified" or st.session_state.auth_status == "verified":
    st.title("📍 Real-Time Engineering Magic")
    
    # 15% Maintenance Logic
    st.sidebar.markdown("### Sovereign Ledger")
    st.sidebar.write("Founder Commission: 15%")
    st.sidebar.write("Police/Security Tax: 0%")
    
    # Panic Button for Mechanics
    if st.sidebar.button("🚨 PANIC BUTTON"):
        st.sidebar.error("EMERGENCY ALERT SENT TO PRIVATE SECURITY.")

    # GPS SIMULATION (Lagos Coordinates)
    # We create a map showing the Mechanic moving toward the User
    st.subheader("Mechanic Tracking")
    
    # Initial location (Lagos Mainland)
    base_lat, base_lon = 6.5244, 3.3792 
    
    # Create tracking data
    map_data = pd.DataFrame({
        'lat': [base_lat, base_lat + 0.005],
        'lon': [base_lon, base_lon + 0.005],
        'name': ['Your Location', 'Mechanic (En Route)']
    })

    st.map(map_data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Arrival", "14 Mins")
    with col2:
        st.metric("Platform Fee (15%)", "₦2,400")

    if st.button("Confirm Mechanic Arrival"):
        st.balloons()
        st.success("Service started. Moving Africa to the next level.")
        
