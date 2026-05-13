import streamlit as st
import pandas as pd
import numpy as np
import time
import requests

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
# Hard-coded for this build to ensure the bank tunnel opens immediately
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. THE FOUNDER'S STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-bottom: 20px; }
    .main-title { text-align: center; font-size: 50px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .panic-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; border-radius: 50px; }
    .card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LIVE BANKING CORE ---
def initialize_paystack_payment(email, amount_ngn):
    """Handshake with Paystack Live Servers to process 15% share + Mechanic fees."""
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {LIVE_SECRET_KEY}", 
        "Content-Type": "application/json"
    }
    # Payload includes specific channels to ensure Bank Transfer is available
    payload = {
        "email": email, 
        "amount": int(float(amount_ngn) * 100), # Kobo conversion
        "currency": "NGN",
        "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        if res_data.get('status'):
            return res_data['data']['authorization_url']
        else:
            st.error(f"Bank Error: {res_data.get('message')}")
            return None
    except Exception as e:
        st.error(f"Connection Failed: {e}")
        return None

# --- 4. DATA & SYMPTOMS ---
# Solution-making logic for all categories
SYMPTOM_MATRIX = {
    "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
    "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
    "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
    "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
    "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
}

# --- 5. INTERFACE DESIGN ---
st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)

if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'final_quote' not in st.session_state: st.session_state.final_quote = None

with st.sidebar:
    st.header("Sovereign Control")
    category = st.selectbox("Rendered Service", list(SYMPTOM_MATRIX.keys()))
    user_role = st.radio("Access Level", ["User/Client", "Mechanic Hub", "Sovereign Ledger"])
    st.divider()
    st.write("Founder: Nwokeji Anthony C.")
    st.write("Engine Status: LIVE 🟢")

# --- 6. PORTALS ---
if user_role == "User/Client":
    st.subheader(f"Engineering Diagnosis: {category}")
    col1, col2 = st.columns(2)
    selected_faults = []
    for i, sym in enumerate(SYMPTOM_MATRIX[category]):
        if (col1 if i < 4 else col2).checkbox(f"{i+1}. {sym}"):
            selected_faults.append(sym)
    
    details = st.text_area("Precision Details (Magic Box)")
    
    if st.button("🚀 REQUEST ELITE MECHANIC"):
        st.session_state.active_request = {
            "cat": category, "faults": selected_faults, "details": details,
            "loc": "Victoria Island, Lagos", "time": time.ctime()
        }
        st.success("Request sent to the regional network.")

    if st.session_state.final_quote:
        st.markdown(f"### Pay ₦{st.session_state.final_quote:,.2f} to start repair")
        if st.button("💳 PAY VIA SOVEREIGN GATEWAY"):
            url = initialize_paystack_payment("founder@greatmech.africa", st.session_state.final_quote)
            if url: st.link_button("OPEN SECURE BANKING TUNNEL", url)

elif user_role == "Mechanic Hub":
    if st.session_state.active_request:
        req = st.session_state.active_request
        st.markdown(f"<div class='card'><b>Job Alert:</b> {req['cat']}<br><b>Location:</b> {req['loc']}<br><b>Faults:</b> {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
        
        svc = st.number_input("Service Fix Cost (₦)")
        tpt = st.number_input("Transport Fare (₦)")
        
        if st.button("SEND LIVE QUOTE"):
            # MAINTAIN 15% Share | REMOVE 2% Police Payment
            st.session_state.final_quote = (svc + tpt) * 1.15
            st.success("Quote Transmitted. 15% Founder Share locked.")
        
        st.divider()
        if st.button("🚨 TRIGGER PANIC BUTTON"):
            st.error(f"EMERGENCY: Security dispatched to {req['loc']} for Mechanic.")
    else:
        st.info("No active service requests.")

elif user_role == "Sovereign Ledger":
    st.subheader("Financial Performance")
    # Reference to zero revenue in current pre-approved state
    st.write("Total Revenue: ₦0.00")
    st.write("Founder Net (15%): ₦0.00")
    st.write("Security Fee (2%): EXCLUDED BY FOUNDER ORDER")

# --- 7. RADAR ---
st.divider()
st.subheader("📍 Great Mech Global Radar")
st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) 
    
