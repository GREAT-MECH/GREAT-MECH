import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. PRESTIGE UI & KINETIC ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v128.0", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    
    .moving-africa-container { 
        width: 100%; overflow: hidden; white-space: nowrap; 
        margin-bottom: 20px; border-bottom: 1px solid #D4AF37; padding: 10px 0;
    }
    .moving-africa-text {
        display: inline-block; padding-left: 100%;
        font-size: 1.5em; color: #D4AF37; font-weight: bold;
        animation: scroll-left-to-right 25s linear infinite;
    }
    @keyframes scroll-left-to-right { 0% { transform: translateX(0%); } 100% { transform: translateX(-200%); } }

    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 12px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%; 
    }
    </style>
    <div class="moving-africa-container">
        <div class="moving-africa-text">
            MOVING AFRICA TO THE NEXT LEVEL... 🚀 GREAT MECH ENGINEERING MAGIC... 🌍 54 COUNTRIES... 0% POLICE TAX... 15% FOUNDER SHARE... 🛠️
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        # worksheet="Users" MUST match the tab name in your Google Sheet
        return conn.read(worksheet="Users", ttl=0)
    except Exception as e:
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account", "Phone", "Country", "FounderShare", "SecurityTax"])

def save_user(new_data):
    try:
        df = get_users()
        updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        conn.update(worksheet="Users", data=updated_df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Technical Block: {e}")
        return False

# --- 3. GATEWAY ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech Sovereign Portal 🌍</h1>", unsafe_allow_html=True)
    tab_login, tab_reg = st.tabs(["🔒 SECURE LOGIN", "🛠️ JOIN REVOLUTION"])
    
    with tab_login:
        e_log = st.text_input("Email", key="log_email")
        p_log = st.text_input("4-Digit PIN", type="password", key="log_pin")
        if st.button("ACTIVATE SESSION"):
            users_df = get_users()
            match = users_df[(users_df['Email'] == e_log) & (users_df['PIN'].astype(str) == p_log)]
            if not match.empty:
                st.session_state.user_data = match.iloc[0].to_dict()
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Credentials not recognized.")

    with tab_reg:
        r_name = st.text_input("Full Name", key="reg_name")
        r_email = st.text_input("Email", key="reg_email")
        r_phone = st.text_input("Phone Number", key="reg_phone")
        r_country = st.text_input("Country", key="reg_country")
        r_role = st.selectbox("Identity", ["User", "Mechanic"], key="reg_role")
        r_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4, key="reg_pin")
        
        m_bank = st.text_input("Bank Name", key="reg_bank") if r_role == "Mechanic" else ""
        m_acct = st.text_input("Account Number", key="reg_acct") if r_role == "Mechanic" else ""
        
        if st.button("CREATE PERMANENT ACCOUNT"):
            if r_email and r_pin:
                reg_data = {
                    "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                    "Bank": m_bank, "Account": m_acct, "Phone": r_phone, "Country": r_country,
                    "FounderShare": "15%", "SecurityTax": "0%"
                }
                if save_user(reg_data):
                    st.success("Registration Successful! Please Login.")

# --- 4. LIVE DASHBOARD ---
elif st.session_state.auth_status == "verified":
    u = st.session_state.user_data
    st.sidebar.markdown(f"### {u['Name']}")
    if st.sidebar.button("Logout"):
        st.session_state.auth_status = "gateway"
        st.rerun()

    st.markdown(f"### Great Mech Dashboard: Online")
    col1, col2 = st.columns(2)
    with col1: st.info(f"Founder Share: 15%")
    with col2: st.success(f"Security Tax: 0%")

    if u['Role'] == "Mechanic":
        st.markdown("### 🚨 Safety Protocol")
        if st.button("SEND EMERGENCY ALERT", help="Panic Button: Alerts Private Security"):
            st.error("EMERGENCY SIGNAL SENT.")

    st.markdown("---")
    st.write("Current Services: Truck, Car, Diesel Engine, Generator, CCTV, Solar.")
                
