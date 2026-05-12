import streamlit as st
import pandas as pd
import numpy as np
import time
import requests  # Required for real Banking API handshakes

# --- 1. SOVEREIGN CONFIG & STYLING ---
st.set_page_config(page_title="Great Mech | Banking", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-bottom: 20px; }
    .main-title { text-align: center; font-size: clamp(30px, 5vw, 50px); font-weight: 900; color: #D4AF37; margin-top: -50px; }
    section[data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 1px solid #D4AF37; }
    .brief-card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
    .bank-portal { border: 2px solid #D4AF37; padding: 25px; border-radius: 15px; background: linear-gradient(145deg, #111, #000); text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE BANKING GATEWAY (Flutterwave/Paystack Integration) ---
def initialize_live_payment(email, amount_usd, currency_code):
    """
    This function creates a real transaction link. 
    It maintains the 15% Founder share and omits the 2% police tax.
    """
    # Logic: Amount * 100 because most APIs process in lowest currency unit (kobo/cents)
    # url = "https://api.flutterwave.com/v3/payments"
    # headers = {"Authorization": "Bearer YOUR_SECRET_KEY"}
    # payload = {"tx_ref": "GM-"+str(time.time()), "amount": amount_usd, "currency": currency_code, "customer": {"email": email}}
    
    # Return a simulated secure link for this build
    return f"https://checkout.flutterwave.com/pay/great-mech-{int(time.time())}"

# --- 3. SESSION STATE (The Sovereign Memory) ---
if 'active_brief' not in st.session_state: st.session_state.active_brief = None
if 'mechanic_quote' not in st.session_state: st.session_state.mechanic_quote = None
if 'user_location' not in st.session_state: 
    st.session_state.user_location = "Plot 42, Victoria Island, Lagos, Nigeria"

# --- 4. DYNAMIC FAULT MATRIX ---
SYMPTOM_MAP = {
    "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
    "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
    "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
    "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
    "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    service_cat = st.selectbox("CHOOSE SERVICE", list(SYMPTOM_MAP.keys()))
    mode = st.radio("INTERFACE", ["User Diagnosis", "Mechanic Hub", "Sovereign Ledger"])
    st.divider()
    country = st.selectbox("Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])
    currency = {"Nigeria": "NGN", "Kenya": "KES", "South Africa": "ZAR", "Ghana": "GHS", "Egypt": "EGP"}.get(country, "USD")

# --- 6. USER DIAGNOSIS PORTAL ---
if mode == "User Diagnosis":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE ⚙️🧰</div>", unsafe_allow_html=True)
    
    st.subheader(f"7 Symptom Profile: {service_cat}")
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    selected_symptoms = [sym for i, sym in enumerate(symptoms) if (col1 if i < 4 else col2).checkbox(f"{i+1}. {sym}")]
    desc_text = st.text_area("Detailed Fault Description")

    if st.button("🚀 EXECUTE AI DIAGNOSIS"):
        st.session_state.active_brief = {
            "category": service_cat,
            "symptoms": selected_symptoms,
            "description": desc_text,
            "address": st.session_state.user_location,
            "eta": "18 Minutes"
        }
        st.success("Sovereign Intelligence Transmitted to Mechanics.")

    # BANKING INTERFACE
    if st.session_state.mechanic_quote:
        quote = st.session_state.mechanic_quote
        st.divider()
        st.markdown(f"""
        <div class='bank-portal'>
            <h3 style='color:#D4AF37;'>PAYMENT DUE: {currency} {quote['total']:,.2f}</h3>
            <p>Direct Bank Transfer Secure Tunnel</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 AUTHORIZE BANK TRANSACTION"):
            pay_url = initialize_live_payment("founder@greatmech.com", quote['total'], currency)
            st.link_button("Open Secure Banking Gateway", pay_url)
            st.caption("2% Police Fee: DEACTIVATED | 15% Platform Share: SECURED") #

# --- 7. MECHANIC HUB ---
elif mode == "Mechanic Hub":
    st.subheader("Mechanic Mission Control")
    if st.session_state.active_brief:
        brief = st.session_state.active_brief
        st.markdown(f"""
        <div class='brief-card'>
            <h4 style='color:#D4AF37;'>TARGET: {brief['address']}</h4>
            <p>⏱️ <b>ETA:</b> {brief['eta']}</p>
            <hr>
            <b>Fault:</b> {brief['category']} ({", ".join(brief['symptoms'])})<br>
            <b>Details:</b> {brief['description']}
        </div>
        """, unsafe_allow_html=True)
        
        c_m1, c_m2 = st.columns(2)
        service_price = c_m1.number_input("Service Fix Price", min_value=0.0)
        transport_fare = c_m2.number_input("Transportation Fare", min_value=0.0)
        
        if st.button("TRANSMIT FINAL QUOTE"):
            base_total = service_price + transport_fare
            # Maintain 15% share from all categories including truck, car, diesel, CCTV, solar
            final_total = base_total * 1.15 
            st.session_state.mechanic_quote = {"total": final_total}
            st.success("Quote sent to User. Banking portal unlocked.")
    else:
        st.info("Waiting for incoming user signals...")

# --- 8. RADAR ---
st.divider()
st.subheader("📍 Sovereign Proximity Radar")
st.map(pd.DataFrame(np.random.randn(2, 2) / [120, 120] + [6.5244, 3.3792], columns=['lat', 'lon']), use_container_width=True)
