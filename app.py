import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. PRESTIGE UI & KINETIC ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v124.0", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    .moving-africa-container { width: 100%; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #D4AF37; padding: 10px 0; }
    .moving-africa-text { display: inline-block; padding-left: 100%; font-size: 1.5em; color: #D4AF37; font-weight: bold; animation: scroll-left-to-right 20s linear infinite; }
    @keyframes scroll-left-to-right { 0% { transform: translateX(0%); } 100% { transform: translateX(-200%); } }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%; }
    </style>
    <div class="moving-africa-container"><div class="moving-africa-text">
    MOVING AFRICA TO THE NEXT LEVEL... 🚀 GREAT MECH ENGINEERING MAGIC... 🌍 54 COUNTRIES... 15% FOUNDER SHARE...
    </div></div>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        # worksheet="Users" MUST match your tab name exactly
        return conn.read(worksheet="Users", ttl=0)
    except Exception:
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account", "Phone", "Country"])

def save_user(new_data):
    try:
        df = get_users()
        updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        # Final Force-Push to Google Sheets
        conn.update(worksheet="Users", data=updated_df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Sovereign DB Error: Ensure Sheet tab is 'Users' and Shared as 'Editor'.")
        return False

# --- 3. SOVEREIGN GATEWAY ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech Portal 🌍</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER"])
    
    with t1:
        # Unique IDs added to prevent the error in 321988.png
        e_log = st.text_input("Email Address", key="login_email_box")
        p_log = st.text_input("4-Digit PIN", type="password", key="login_pin_box")
        if st.button("ACTIVATE SESSION"):
            db = get_users()
            user_match = db[(db['Email'] == e_log) & (db['PIN'].astype(str) == p_log)]
            if not user_match.empty:
                st.session_state.user_data = user_match.iloc[0].to_dict()
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Invalid credentials. Please Register first if you haven't.")

    with t2:
        st.markdown("### Join the Partner Network")
        r_name = st.text_input("Full Name", key="reg_name")
        r_email = st.text_input("Email Address", key="reg_email")
        r_phone = st.text_input("Phone Number", key="reg_phone")
        r_country = st.text_input("Country (in Africa)", key="reg_country")
        r_role = st.selectbox("I am a:", ["User", "Mechanic"], key="reg_role")
        r_pin = st.text_input("Create 4-Digit PIN", type="password", max_chars=4, key="reg_pin")
        
        m_bank = ""
        m_acct = ""
        if r_role == "Mechanic":
            m_bank = st.text_input("Bank Name", key="reg_bank")
            m_acct = st.text_input("Account Number", key="reg_acct")
        
        if st.button("CREATE PERMANENT ACCOUNT"):
            if r_email and r_pin:
                data = {
                    "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                    "Bank": m_bank, "Account": m_acct, "Phone": r_phone, "Country": r_country
                }
                if save_user(data):
                    st.success("Sovereign Account Created! Switch to the LOGIN tab now.")

# --- 4. VERIFIED INTERFACE ---
elif st.session_state.auth_status == "verified":
    u = st.session_state.user_data
    st.sidebar.success(f"Verified: {u['Name']}")
    if st.sidebar.button("Logout"):
        st.session_state.auth_status = "gateway"
        st.rerun()
    
    st.markdown(f"## Welcome, Partner {u['Name']} 🌍")
    st.info(f"Identity: {u['Role']} | Founder Share: 15% | Police Tax: 0%")
    
    # Mechanic specific view
    if u['Role'] == "Mechanic":
        st.markdown("### 🔧 Your Service Station")
        st.write(f"Bank for Settlement: {u['Bank']}")
        st.write(f"Account: {u['Account']}")
    
    # User specific view
    else:
        st.markdown("### 🤖 Engineering AI Diagnostic")
        st.selectbox("Select Equipment", ["🚛 Heavy Truck", "🚗 Personal Vehicle", "🔋 Diesel Gen", "🛡️ CCTV/Security", "☀️ Solar System"])
        st.text_area("Describe the Fault")
        if st.button("REQUEST SOVEREIGN MECHANIC"):
            st.success("Searching for nearby Great Mech partners...")

    st.markdown("---")
    st.markdown("<p style='text-align:center;'>Great Mech Engineering: Africa's Next Level.</p>", unsafe_allow_html=True)
            
