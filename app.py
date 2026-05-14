import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. PRESTIGE UI ---
st.set_page_config(page_title="Great Mech | v133.0", page_icon="🌍")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 12px; font-weight: bold; width: 100%; }
    .founder-info { color: #D4AF37; border: 1px solid #D4AF37; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SOVEREIGN DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        # worksheet="Form Responses 1" is the default name Google creates
        return conn.read(worksheet="Form Responses 1", ttl=0)
    except:
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account", "Phone", "Country", "Services", "FounderShare", "Registration Date", "Status"])

def register_user(d):
    # Form Response URL derived from your link
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdqexf8NG2Jl9VjRjXA_fmgwKFAIqsLsp-ALVPOwKX6zSUHlw/formResponse"
    
    # Mapping Entry IDs from your pre-filled link
    payload = {
        "entry.1257243498": d['Email'], "entry.1262385972": d['Name'], "entry.368716846": d['PIN'],
        "entry.2084281457": d['Role'], "entry.1572930563": d['Bank'], "entry.1184704055": d['Account'],
        "entry.439843801": d['Phone'], "entry.994065287": d['Country'], "entry.272041572": d['Services'],
        "entry.953493554": d['FounderShare'], "entry.823124258": d['Date'], "entry.1645357372": d['Status']
    }
    try:
        requests.post(form_url, data=payload)
        return True
    except:
        return False

# --- 3. INTERFACE ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>Great Mech Portal 🌍</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER"])
    
    with t2:
        r_email = st.text_input("Email")
        r_name = st.text_input("Full Name")
        r_pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        r_role = st.selectbox("Role", ["User", "Mechanic"])
        r_country = st.text_input("Country")
        r_phone = st.text_input("Phone Number")
        
        if st.button("CREATE SOVEREIGN ACCOUNT"):
            reg_data = {
                "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                "Bank": "N/A", "Account": "N/A", "Phone": r_phone, "Country": r_country,
                "Services": "Truck, Car, Engine, Generator, CCTV, Solar",
                "FounderShare": "15%", "Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"
            }
            if register_user(reg_data):
                st.success("Registration Sent! Switch to Login.")
            else:
                st.error("Connection Interrupted.")

    with t1:
        e_log = st.text_input("Email", key="l_email")
        p_log = st.text_input("PIN", type="password", key="l_pin")
        if st.button("ACTIVATE"):
            db = get_users()
            # Matching logic based on the 12-column sheet
            match = db[(db['Email'] == e_log) & (db['PIN'].astype(str) == p_log)]
            if not match.empty:
                st.session_state.user = match.iloc[0].to_dict()
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied.")

else:
    u = st.session_state.user
    st.write(f"### Welcome Partner, {u['Name']} 🌍")
    st.markdown(f"<div class='founder-info'>FOUNDER SHARE: 15% | POLICE/SECURITY TAX: 0%</div>", unsafe_allow_html=True)
    
    if u['Role'] == "Mechanic":
        if st.button("🚨 PANIC BUTTON (EMERGENCY)"):
            st.error("EMERGENCY SIGNAL SENT TO PRIVATE SECURITY.")
            
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
                
