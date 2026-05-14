import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. UI & KINETIC ANIMATION ---
st.set_page_config(page_title="Great Mech | v123.0", page_icon="🌍", layout="wide")

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
    MOVING AFRICA TO THE NEXT LEVEL... 🚀 0% POLICE TAX... 15% FOUNDER SHARE... 🌍 54 COUNTRIES...
    </div></div>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        # worksheet="Users" must match the tab name you set on your phone
        return conn.read(worksheet="Users", ttl=0)
    except Exception:
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account", "Phone", "Country"])

def save_user(new_data):
    try:
        df = get_users()
        updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        # v123.0 FORCE-PUSH: Explicitly telling the connection to write
        conn.update(worksheet="Users", data=updated_df)
        
        # Clear all caches to ensure login works immediately
        st.cache_data.clear()
        st.cache_resource.clear()
        return True
    except Exception as e:
        st.error("🚨 CONNECTION BLOCK")
        st.info("Your Sheet is set to 'Editor' in **321977.png**, but Streamlit Secrets might still say 'read_only = true'. Please double-check your Secrets.")
        return False

# --- 3. GATEWAY ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech Sovereign Portal 🌍</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER"])
    
    with t1:
        e_log = st.text_input("Email")
        p_log = st.text_input("PIN", type="password")
        if st.button("ACTIVATE SESSION"):
            db = get_users()
            user_match = db[(db['Email'] == e_log) & (db['PIN'].astype(str) == p_log)]
            if not user_match.empty:
                st.session_state.user_data = user_match.iloc[0].to_dict()
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Access Denied. If you just registered, wait 60 seconds.")

    with t2:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_phone = st.text_input("Phone")
        r_country = st.text_input("Country")
        r_role = st.selectbox("Role", ["User", "Mechanic"])
        r_pin = st.text_input("PIN (4 Digits)", type="password", max_chars=4)
        m_bank = st.text_input("Bank") if r_role == "Mechanic" else ""
        m_acct = st.text_input("Account") if r_role == "Mechanic" else ""
        
        if st.button("CREATE SOVEREIGN ACCOUNT"):
            if r_email and r_pin:
                data = {
                    "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                    "Bank": m_bank, "Account": m_acct, "Phone": r_phone, "Country": r_country
                }
                if save_user(data):
                    st.success("Account Secured in Google Sheets! Switch to Login tab.")

# --- 4. VERIFIED INTERFACE ---
elif st.session_state.auth_status == "verified":
    u = st.session_state.user_data
    st.sidebar.success(f"Partner: {u['Name']}")
    if st.sidebar.button("Logout"):
        st.session_state.auth_status = "gateway"
        st.rerun()
    
    st.markdown(f"### Great Mech Engine: Online")
    st.write(f"Welcome {u['Name']}. Your {u['Role']} dashboard is ready for Africa.")
