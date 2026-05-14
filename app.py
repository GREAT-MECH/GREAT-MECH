import streamlit as st
import pandas as pd
import random
import time

# --- 1. PRESTIGE INTERFACE CONFIG ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# Custom CSS for Black & Gold Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; }
    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 10px; 
        font-weight: bold; border: none; width: 100%;
    }
    .stTextInput>div>div>input { background-color: #1A1C24; color: gold; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        color: white; border-bottom: 2px solid transparent; 
    }
    .stTabs [data-baseweb="tab"]:hover { color: #D4AF37; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SOVEREIGN MEMORY & RECOVERY ---
if 'db' not in st.session_state:
    # Founder credentials preserved
    st.session_state.db = {
        "founder@greatmech.com": {"name": "Founder", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"}
    }

for key in ['auth_status', 'user_data', 'temp_otp']:
    if key not in st.session_state:
        st.session_state[key] = "gateway" if key == 'auth_status' else None

# --- 3. THE SOVEREIGN GATEWAY (LOGIN & REGISTRATION) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>🌍 GREAT MECH SOVEREIGN ENGINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Engineering Africa's Future | v101.0 Master Build</p>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["🔒 Secure Login", "🛠️ Account Registration"])

    with tab_login:
        st.markdown("### Access Portal")
        l_email = st.text_input("Registered Email", key="login_email")
        l_pin = st.text_input("4-Digit Security PIN", type="password", key="login_pin")
        if st.button("EXECUTE LOGIN"):
            if l_email in st.session_state.db and st.session_state.db[l_email]['pin'] == l_pin:
                st.session_state.user_data = st.session_state.db[l_email]
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials.")

    with tab_reg:
        st.markdown("### Join the Sovereign Network")
        r_name = st.text_input("Full Name / Business Name")
        r_email = st.text_input("Email Address")
        r_phone = st.text_input("Phone Number (include +234, etc.)")
        r_pin = st.text_input("Create 4-Digit Security PIN", type="password", max_chars=4)
        r_sector = st.selectbox("Category", ["User", "Mechanic (Truck/Car/Gen/Solar/CCTV)"])

        if st.button("GENERATE SECURITY OTP"):
            if r_phone and r_email:
                st.session_state.temp_otp = str(random.randint(1000, 9999))
                # Debugging bypass due to country restriction
                st.info(f"Sovereign OTP Generated: {st.session_state.temp_otp}")
            else:
                st.error("Please provide valid contact details.")

        if st.session_state.temp_otp:
            otp_check = st.text_input("Enter the 4-Digit Code", key="otp_verify")
            if st.button("ACTIVATE SOVEREIGN ACCOUNT"):
                if otp_check == st.session_state.temp_otp:
                    st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "sector": r_sector, "phone": r_phone}
                    st.success("Verification Successful. Proceed to Login.")
                    st.session_state.temp_otp = None
                else:
                    st.error("Invalid Code. Verification Failed.")

# --- 4. THE LIVE PORTAL (GPS & LEDGER) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    
    with st.sidebar:
        st.markdown(f"## Welcome, {user['name']}")
        st.write(f"**Sector:** {user['sector']}")
        st.divider()
        # Panic Button Directive
        if st.button("🚨 PANIC BUTTON (EMERGENCY)"):
            st.error("POLICE BYPASSED: Alert sent to Private Security Firm.")
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "gateway"; st.rerun()

    st.markdown("### 📍 Real-Time Mechanic Tracking Map")
    
    # 54 Africa Logic: 15% Platform Share, 0% Security Tax
    with st.expander("Sovereign Ledger Details"):
        st.write("Platform Maintenance Fee: **15%**")
        st.write("Regional Security/Police Charge: **0% (Removed)**")

    # GPS Simulation: Tracking Mechanic movement
    view_data = pd.DataFrame({
        'lat': [6.5244, 6.5300], 
        'lon': [3.3792, 3.3900],
        'color': ['#D4AF37', '#FF0000']
    })
    
    st.map(view_data)
    
    st.metric(label="Mechanic Estimated Arrival", value="11 Mins", delta="-2 Mins")
    
    if st.button("Confirm Service Completion"):
        st.balloons()
        st.success("Transaction Complete. 15% Founders Share Logged.")
        
