import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. SOVEREIGN CONFIG & STYLING ---
st.set_page_config(page_title="Great Mech | Africa's Pulse", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-bottom: 20px; }
    .main-title { text-align: center; font-size: clamp(30px, 5vw, 50px); font-weight: 900; color: #D4AF37; margin-top: -50px; }
    section[data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 1px solid #D4AF37; }
    .brief-card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
    .status-pill { padding: 5px 15px; border-radius: 20px; background: #D4AF37; color: #000; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (The Data Bridge) ---
if 'active_brief' not in st.session_state: st.session_state.active_brief = None
if 'mechanic_quote' not in st.session_state: st.session_state.mechanic_quote = None
if 'user_location' not in st.session_state: 
    # Simulated current user address
    st.session_state.user_location = "Plot 42, Victoria Island, Lagos, Nigeria"

# --- 3. DYNAMIC FAULT MATRIX ---
SYMPTOM_MAP = {
    "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
    "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
    "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
    "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
    "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    service_cat = st.selectbox("CHOOSE SERVICE", list(SYMPTOM_MAP.keys()))
    mode = st.radio("INTERFACE", ["User Diagnosis", "Mechanic Hub", "Sovereign Ledger"])
    st.divider()
    country = st.selectbox("Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])

# --- 5. USER DIAGNOSIS PORTAL ---
if mode == "User Diagnosis":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE ⚙️🧰</div>", unsafe_allow_html=True)
    
    # Step A: Symptom Selection
    st.subheader(f"7 Symptom Profile: {service_cat}")
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    selected_symptoms = [sym for i, sym in enumerate(symptoms) if (col1 if i < 4 else col2).checkbox(f"{i+1}. {sym}")]
    desc_text = st.text_area("Detailed Fault Description")

    if st.button("🚀 EXECUTE AI DIAGNOSIS"):
        with st.spinner("Transmitting to Network..."):
            time.sleep(1)
            st.session_state.active_brief = {
                "category": service_cat,
                "symptoms": selected_symptoms,
                "description": desc_text,
                "address": st.session_state.user_location,
                "eta": "18 Minutes"
            }
            st.success("Diagnosis Sent. Waiting for Mechanic's Quote...")

    # Step B: Payment Receipt (Appears once Mechanic quotes)
    if st.session_state.mechanic_quote:
        quote = st.session_state.mechanic_quote
        st.divider()
        st.markdown("### 💳 Secure Service Payment")
        st.info("Mechanic is ready. Total below includes Service, Transportation, and Platform Fee.")
        
        c1, c2 = st.columns(2)
        c1.metric("Final Amount Payable", f"${quote['total']:,.2f}")
        c2.write(f"**Includes Transport to:** {st.session_state.user_location}")
        
        if st.button("PROCEED TO BANK TRANSACTION"):
            st.balloons()
            st.success("Payment Cleared. Mechanic Dispatched.")

# --- 6. MECHANIC HUB (Quoting & Location) ---
elif mode == "Mechanic Hub":
    st.subheader("Mechanic Mission Control")
    
    if st.session_state.active_brief:
        brief = st.session_state.active_brief
        
        # Displaying exact location and time data
        st.markdown(f"""
        <div class='brief-card'>
            <span class='status-pill'>NEW REQUEST</span>
            <h4 style='color:#D4AF37;'>TARGET: {brief['address']}</h4>
            <p>⏱️ <b>Estimated Arrival:</b> {brief['eta']}</p>
            <hr>
            <b>Fault:</b> {brief['category']} ({", ".join(brief['symptoms'])})<br>
            <b>Details:</b> {brief['description']}
        </div>
        """, unsafe_allow_html=True)
        
        # Mechanic Inputs
        col_m1, col_m2 = st.columns(2)
        service_price = col_m1.number_input("Service Fix Price ($)", min_value=0.0)
        transport_fare = col_m2.number_input("Transportation Fare ($)", min_value=0.0)
        
        if st.button("TRANSMIT FINAL QUOTE"):
            base_total = service_price + transport_fare
            founder_share = base_total * 0.15 # 15% Platform revenue
            final_total = base_total + founder_share
            
            st.session_state.mechanic_quote = {
                "service": service_price,
                "transport": transport_fare,
                "total": final_total
            }
            st.success(f"Quote Sent: Total ${final_total:,.2f} (Includes your transport + platform fee)")
    else:
        st.info("Waiting for incoming user requests...")

# --- 7. RADAR & LEDGER ---
st.divider()
st.subheader("📍 Sovereign Radar")
st.map(pd.DataFrame(np.random.randn(2, 2) / [120, 120] + [6.5244, 3.3792], columns=['lat', 'lon']), use_container_width=True)
