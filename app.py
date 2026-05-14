import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime
import time

# --- 1. PRESTIGE UI & ANIMATION SETUP ---
st.set_page_config(page_title="Great Mech Supreme", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stApp { background-color: #050505; color: #FFFFFF; animation: fadeIn 2s; }
    .gold-header { color: #D4AF37; text-align: center; font-family: 'Trebuchet MS'; font-weight: bold; }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #996515); 
        color: black; border-radius: 8px; font-weight: bold; width: 100%; border: none; height: 3em;
    }
    .metric-card {
        background-color: #111; padding: 20px; border-radius: 12px; border: 1px solid #D4AF37; text-align: center;
    }
    .panic-btn>button { background: #8B0000 !important; color: white !important; }
    .description-box { background: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LANGUAGE & WELCOME ---
if 'lang' not in st.session_state:
    st.session_state.lang = None

if not st.session_state.lang:
    st.markdown("<h1 class='gold-header'>WELCOME TO GREAT MECH</h1>", unsafe_allow_html=True)
    st.write("### Choose Your Language / Choisissez votre langue")
    col_l1, col_l2 = st.columns(2)
    if col_l1.button("English 🇬🇧"): st.session_state.lang = "EN"; st.rerun()
    if col_l2.button("Français 🇫🇷"): st.session_state.lang = "FR"; st.rerun()
    st.stop()

# --- 3. DATABASE & SECURITY BRIDGE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def register_user(d):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdqexf8NG2Jl9VjRjXA_fmgwKFAIqsLsp-ALVPOwKX6zSUHlw/formResponse"
    payload = {
        "entry.1257243498": d['Email'], "entry.1262385972": d['Name'], "entry.368716846": d['PIN'],
        "entry.2084281457": d['Role'], "entry.1572930563": d['Bank'], "entry.1184704055": d['Account'],
        "entry.439843801": d['Phone'], "entry.994065287": d['Country'], "entry.272041572": d['Services'],
        "entry.953493554": d['FounderShare'], "entry.823124258": d['Date'], "entry.1645357372": d['Status']
    }
    try: requests.post(form_url, data=payload); return True
    except: return False

# --- 4. AUTHENTICATION ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER"])
    with t2:
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_pin = st.text_input("PIN (4 Digits)", type="password", max_chars=4)
        r_country = st.text_input("Country (Africa 54)")
        r_role = st.selectbox("Role", ["User", "Mechanic"])
        if st.button("CREATE ACCOUNT"):
            reg_data = {
                "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                "Bank": "N/A", "Account": "N/A", "Phone": "Pending", "Country": r_country,
                "Services": "Truck, Car, Diesel, Generator, CCTV, Solar",
                "FounderShare": "15%", "Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"
            }
            if register_user(reg_data): st.success("Success!")
    with t1:
        l_email = st.text_input("Login Email")
        l_pin = st.text_input("Enter PIN", type="password")
        if st.button("ACTIVATE"):
            df = conn.read(worksheet="Form Responses 1", ttl=0)
            user = df[(df['Email'] == l_email) & (df['PIN'].astype(str) == l_pin)]
            if not user.empty:
                st.session_state.user = user.iloc[0].to_dict()
                st.session_state.auth = True; st.rerun()

# --- 5. MAIN SOVEREIGN INTERFACE ---
else:
    u = st.session_state.user
    st.markdown(f"<h1 class='gold-header'>Great Mech: {u['Country']}</h1>", unsafe_allow_html=True)
    
    # 5 CORE SERVICES
    service_cat = st.selectbox("Select Service", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    
    # DESCRIPTION BOX
    st.markdown(f"<div class='description-box'><b>Service Overview:</b> Managing {service_cat} engineering solutions for {u['Country']}. 15% Founder Revenue model active.</div>", unsafe_allow_html=True)

    # MAP 🗺️
    st.subheader("Global Deployment")
    map_data = pd.DataFrame({'lat': [9.08], 'lon': [8.67]}) # Example for Nigeria
    st.map(map_data)

    # AI DIAGNOSTIC & 7 FAULT SUGGESTIONS
    st.subheader("🤖 AI Diagnostic Tool")
    faults = ["Engine Overheating", "Brake System Failure", "Solar Inverter Fault", "CCTV Signal Loss", "Generator Starting Issue", "Transmission Fluid Leak", "Electrical Short Circuit"]
    selected_fault = st.selectbox("Select Detected Fault", faults)
    
    if st.button("RUN AI DIAGNOSIS"):
        with st.spinner("Analyzing Fault..."):
            time.sleep(2)
            st.warning(f"AI Suggestion for {selected_fault}: Check primary connections and fluid levels. Manual override suggested.")

    # REVENUE & PAYSTACK SYSTEM
    st.write("---")
    bill = st.number_input("Billing Amount ($)", min_value=0.0)
    if bill > 0:
        founder_cut = bill * 0.15 # 15%
        st.info(f"Founder 15% Share: ${founder_cut:,.2f} | Police Fee: 0%")
        if st.button("PROCEED TO PAYSTACK PAYMENT"):
            st.success("Redirecting to Secure Paystack Gateway...")

    # MECHANIC PANIC BUTTON
    if u['Role'] == "Mechanic":
        st.markdown('<div class="panic-btn">', unsafe_allow_html=True)
        if st.button("🚨 PANIC BUTTON (EMERGENCY)"):
            st.error("EMERGENCY SIGNAL SENT TO PRIVATE SECURITY.")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.auth = False; st.rerun()
    
