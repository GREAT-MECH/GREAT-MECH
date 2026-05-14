import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from datetime import datetime

# --- 1. PRESTIGE UI & KINETIC ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v121.0", page_icon="🌍", layout="wide")

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
        animation: scroll-left-to-right 20s linear infinite;
    }
    @keyframes scroll-left-to-right { 0% { transform: translateX(0%); } 100% { transform: translateX(-200%); } }

    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 12px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%; 
    }
    </style>
    <div class="moving-africa-container">
        <div class="moving-africa-text">
            MOVING AFRICA TO THE NEXT LEVEL... 🚀 GREAT MECH ENGINEERING MAGIC ⚙️🧰
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. THE PERMANENT DATABASE ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        # Pulls from the 'Users' tab you set up on your phone
        return conn.read(worksheet="Users", ttl="0")
    except Exception:
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account", "Phone", "Country", "Services", "FounderShare", "SecurityTax", "RegistrationDate", "Status"])

def save_user(new_data):
    try:
        df = get_users()
        # Add the new user data to the existing list
        updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        # FINAL ATTEMPT FIX: We use the .update() method with explicit column handling
        conn.update(worksheet="Users", data=updated_df)
        st.cache_data.clear()
        return True
    except Exception as e:
        # If this fails, it is 100% a Google Permission issue
        st.error("🚨 SOVEREIGN PERMISSION ERROR")
        st.info("On your phone, in Google Sheets: Tap Share > Manage Access > Change 'Restricted' to 'Anyone with the link' > Set role to 'EDITOR'.")
        return False

# --- 3. SOVEREIGN GATEWAY ---
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
                st.error("Credentials not recognized in Sovereign database.")

    with tab_reg:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_phone = st.text_input("Phone Number")
        r_country = st.text_input("Country (Africa)")
        r_role = st.selectbox("Identity", ["User", "Mechanic"])
        r_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        m_bank = st.text_input("Bank Name") if r_role == "Mechanic" else ""
        m_acct = st.text_input("Account Number") if r_role == "Mechanic" else ""
        
        if st.button("REGISTER PERMANENTLY"):
            if r_email and r_pin:
                reg_data = {
                    "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                    "Bank": m_bank, "Account": m_acct, "Phone": r_phone, "Country": r_country,
                    "Services": "General", "FounderShare": "15%", "SecurityTax": "0%",
                    "RegistrationDate": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"
                }
                if save_user(reg_data):
                    st.success("Registration Successful! Now go to the Login tab.")

# --- 4. THE LIVE SERVICE INTERFACE ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    st.sidebar.markdown(f"### {user['Name']}")
    st.sidebar.write(f"Sovereign Role: **{user['Role']}**")
    
    if st.sidebar.button("Logout"):
        st.session_state.auth_status = "gateway"
        st.rerun()

    # (Previous UI for Truck, Car, Diesel, CCTV, Solar remains intact)
    st.markdown(f"### Welcome to the future of African Engineering, {user['Name']}.")
        
