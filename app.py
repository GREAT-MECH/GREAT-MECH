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
    .brief-card { border-left: 5px solid #D4AF37; padding: 15px; background: #1a1a1a; border-radius: 5px; margin-bottom: 20px; }
    .diag-output { border: 1px solid #00FF00; padding: 15px; background: #001a00; color: #00FF00; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 2. DYNAMIC FAULT MATRIX ---
SYMPTOM_MAP = {
    "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
    "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
    "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
    "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
    "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
}

# --- 3. SESSION STATE FOR DATA TRANSMISSION ---
if 'active_brief' not in st.session_state:
    st.session_state.active_brief = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    service_cat = st.selectbox("CHOOSE SERVICE", list(SYMPTOM_MAP.keys())) #
    mode = st.radio("COMMAND MODE", ["Diagnosis Portal", "Mechanic Hub", "Sovereign Ledger"])
    st.divider()
    country = st.selectbox("Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])

# --- 5. DIAGNOSIS PORTAL (User Action) ---
if mode == "Diagnosis Portal":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE ⚙️🧰</div>", unsafe_allow_html=True)
    st.subheader(f"7 Symptom Profile: {service_cat}")
    
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    selected_symptoms = []
    
    for i, sym in enumerate(symptoms):
        target = col1 if i < 4 else col2
        if target.checkbox(f"{i+1}. {sym}"):
            selected_symptoms.append(sym)
    
    desc_text = st.text_area("Engineering Details", height=100, placeholder="Describe the fault...")

    if st.button("🚀 EXECUTE AI DIAGNOSIS"): #
        with st.spinner("Analyzing..."):
            time.sleep(1)
            # Store data for the mechanic
            st.session_state.active_brief = {
                "category": service_cat,
                "symptoms": selected_symptoms,
                "description": desc_text
            }
            st.markdown(f"""<div class='diag-output'><b>AI DIAGNOSIS COMPLETE:</b> Data transmitted to regional mechanics.</div>""", unsafe_allow_html=True)

# --- 6. MECHANIC HUB (Data Receipt) ---
elif mode == "Mechanic Hub":
    st.subheader("Incoming Service Request")
    
    if st.session_state.active_brief:
        brief = st.session_state.active_brief
        st.markdown(f"""
        <div class='brief-card'>
            <h4 style='color:#D4AF37; margin-top:0;'>CLIENT FAULT REPORT: {brief['category']}</h4>
            <b>Selected Symptoms:</b> {", ".join(brief['symptoms']) if brief['symptoms'] else "None Selected"}<br>
            <b>User Description:</b> {brief['description'] if brief['description'] else "No additional details provided."}
        </div>
        """, unsafe_allow_html=True)
        
        proposed = st.number_input("Enter Negotiated Base Price ($)", min_value=0.0)
        if st.button("Lock & Send Quote to User"):
            st.session_state.base_price = proposed
            st.success("Quote sent. 15% share added automatically.") #
    else:
        st.warning("Waiting for user diagnosis...")

# --- 7. LEDGER & RADAR (Full Screen) ---
elif mode == "Sovereign Ledger":
    st.subheader("Regional Transaction Records")
    st.table(pd.DataFrame({"Order ID": ["GM-104"], "Service": [service_cat], "Local Total": ["Verified"], "Status": ["Cleared"]}))

st.divider()
st.markdown("### 📍 Sovereign Proximity Radar")
st.map(pd.DataFrame(np.random.randn(2, 2) / [120, 120] + [6.5244, 3.3792], columns=['lat', 'lon']), use_container_width=True)
    
