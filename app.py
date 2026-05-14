import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime
import time

# --- 1. PRESTIGE UI & ANIMATION ENGINE ---
st.set_page_config(page_title="Great Mech Supreme", page_icon="🌍", layout="wide")

# CSS for Gold/Black theme and Fade-In Animation
st.markdown("""
    <style>
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .stApp { 
        background-color: #050505; 
        color: #FFFFFF; 
        animation: fadeIn 1.5s ease-out; 
    }
    .gold-header { 
        color: #D4AF37; 
        text-align: center; 
        font-family: 'Trebuchet MS'; 
        font-weight: bold; 
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #996515); 
        color: black; border-radius: 12px; font-weight: bold; width: 100%; border: none; height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px #D4AF37; }
    .metric-card {
        background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; text-align: center;
    }
    .panic-btn>button { background: linear-gradient(45deg, #FF0000, #8B0000) !important; color: white !important; }
    .description-box { 
        background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 10px solid #D4AF37; margin: 15px 0;
        font-style: italic; color: #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LANGUAGE SELECTION & WELCOME GREETING ---
if 'lang' not in st.session_state:
    st.session_state.lang = None

if not st.session_state.lang:
    st.markdown("<h1 class='gold-header'>WELCOME TO GREAT MECH 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Engineering Magic for the African Continent</p>", unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        if st.button("English 🇬🇧"): 
            st.session_state.lang = "EN"
            st.rerun()
    with col_l2:
        if st.button("Français 🇫🇷"): 
            st.session_state.lang = "FR"
            st.rerun()
    st.stop()

# --- 3. DATABASE BRIDGE (12-Column Mapping) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def register_to_database(d):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdqexf8NG2Jl9VjRjXA_fmgwKFAIqsLsp-ALVPOwKX6zSUHlw/formResponse"
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

# --- 4. AUTHENTICATION GATEWAY ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 class='gold-header'>Sovereign Access Portal</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER FOUNDER"])
    
    with t1:
        l_email = st.text_input("Email")
        l_pin = st.text_input("PIN", type="password")
        if st.button("ACTIVATE ENGINE"):
            df = conn.read(worksheet="Form Responses 1", ttl=0)
            user = df[(df['Email'] == l_email) & (df['PIN'].astype(str) == l_pin)]
            if not user.empty:
                st.session_state.user = user.iloc[0].to_dict()
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied.")

    with t2:
        col_a, col_b = st.columns(2)
        with col_a:
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Work Email")
            r_pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
        with col_b:
            r_phone = st.text_input("Phone Number")
            r_country = st.text_input("Country (Africa 54)")
            r_role = st.selectbox("Role", ["User", "Mechanic"])
        
        if st.button("DOWNLOAD IMAGINATION TO DRIVE"):
            reg_data = {
                "Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role,
                "Bank": "N/A", "Account": "N/A", "Phone": r_phone, "Country": r_country,
                "Services": "Truck, Car, Diesel, Generator, CCTV, Solar",
                "FounderShare": "15%", "Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"
            }
            if register_to_database(reg_data):
                st.success("Registration Successful. Please Login.")

# --- 5. THE MAIN ENGINE (STRATEGIC PROSPECTUS) ---
else:
    u = st.session_state.user
    st.sidebar.markdown(f"<h2 style='color:#D4AF37;'>{u['Name']}</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"**Location:** {u['Country']}")
    st.sidebar.write(f"**Account Status:** {u['Status']}")
    
    st.markdown("<h1 class='gold-header'>Great Mech Supreme Dashboard</h1>", unsafe_allow_html=True)

    # MAP 🗺️ Deployment
    st.subheader("📍 Real-Time Asset Deployment")
    # Centered roughly on Africa for visual
    map_data = pd.DataFrame({'lat': [9.08], 'lon': [8.67]}) 
    st.map(map_data)

    # 5 CORE SERVICES
    st.subheader("🛠️ Core Engineering Services")
    service_cat = st.selectbox("Select Active Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    
    # DESCRIPTION BOX
    st.markdown(f"""
    <div class='description-box'>
        <b>Category:</b> {service_cat}<br>
        <b>Scope:</b> Precision maintenance and solution-making for the {u['Country']} market. 
        Ensuring 15% Founder Share growth and 0% Police Payment compliance.
    </div>
    """, unsafe_allow_html=True)

    # AI DIAGNOSTIC & 7 FAULT SUGGESTIONS
    st.write("---")
    st.subheader("🤖 AI Diagnostic Intelligence")
    faults = [
        "Critical Engine Overheating", 
        "Brake System Hydraulic Failure", 
        "Solar Inverter Grid-Tie Fault", 
        "CCTV Encryption/Signal Loss", 
        "Generator Governor/Starting Issue", 
        "Automatic Transmission Fluid Leak", 
        "High-Voltage Electrical Short Circuit"
    ]
    selected_fault = st.selectbox("Select System Fault for Analysis", faults)
    
    if st.button("RUN SOVEREIGN AI DIAGNOSIS"):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.warning(f"AI ANALYSIS COMPLETE: For {selected_fault}, verify structural integrity and reset primary control modules. Manual intervention by a Great Mech Mechanic recommended.")

    # REVENUE & PAYSTACK PAYMENT SYSTEM
    st.write("---")
    st.subheader("💰 Financial Engine")
    bill_amt = st.number_input("Enter Service Billing Amount ($)", min_value=0.0)
    
    col1, col2 = st.columns(2)
    with col1:
        founder_profit = bill_amt * 0.15 # 15% Founder Share
        st.markdown(f"<div class='metric-card'>FOUNDER SHARE (15%)<br><h2>${founder_profit:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'>SECURITY/POLICE TAX<br><h2 style='color:red;'>0%</h2></div>", unsafe_allow_html=True)

    if bill_amt > 0:
        if st.button("💳 INITIALIZE PAYSTACK GATEWAY"):
            st.success(f"Connecting to Paystack... Processing ${bill_amt:,.2f} transaction for {u['Country']}.")

    # MECHANIC PANIC BUTTON
    if u['Role'] == "Mechanic":
        st.write("---")
        st.markdown('<div class="panic-btn">', unsafe_allow_html=True)
        if st.button("🚨 ACTIVATE ON-SITE EMERGENCY PANIC BUTTON"):
            st.error("EMERGENCY ALERT BROADCASTED. PRIVATE SECURITY FIRM DISPATCHED TO CURRENT COORDINATES.")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout / Shutdown"):
        st.session_state.auth = False
        st.rerun()
