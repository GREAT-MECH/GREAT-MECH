import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. SOVEREIGN CONFIG & STYLING ---
st.set_page_config(page_title="Great Mech | Dynamic Ops", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #111 !important; border-right: 2px solid #D4AF37; }
    .main-title { text-align: center; font-size: 50px; font-weight: 900; color: #D4AF37; letter-spacing: 5px; }
    .diag-card { border: 1.5px solid #00FF00; padding: 20px; border-radius: 12px; background: #001a00; color: #00FF00; margin-top: 20px; }
    .stCheckbox label { font-size: 18px !important; color: #EEE !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DYNAMIC SYMPTOM MATRIX ---
# These are the 7 symptoms that breathe and change based on the category
SYMPTOM_MAP = {
    "🚛 Truck Maintenance": [
        "Air Brake Pressure Loss", "Heavy Engine Knocking", "Fifth Wheel Coupling Issue",
        "Excessive Diesel Smoke (Black/White)", "Gear Shifting Resistance", 
        "Suspension Sagging", "Hub/Axle Overheating"
    ],
    "🚗 Car Repair": [
        "ABS Warning Light", "Steering Vibration", "AC Cooling Failure",
        "Brake Squealing", "Unusual Ignition Delay", 
        "Fluid Leaks Under Chassis", "Check Engine Light (OBD-II)"
    ],
    "⚙️ Diesel Engine/Generator": [
        "Fuel Injection Timing Fault", "Governor Instability (Hunting)", "Radiator Clogging",
        "Low Oil Pressure Alert", "Alternator Voltage Drop", 
        "Excessive Vibration", "Turbocharger Lag"
    ],
    "📹 CCTV Systems": [
        "Video Signal Interruption", "Night Vision IR Failure", "DVR/NVR Storage Error",
        "PTZ Rotation Jam", "Network Latency/Lag", 
        "Flickering Image Feed", "Power Supply Overload"
    ],
    "☀️ Solar Engineering": [
        "Inverter 'Ground Fault' Error", "Battery Charge Discrepancy", "Panel Surface Micro-cracks",
        "Charge Controller Overheating", "Efficiency Drop (>20%)", 
        "Loose DC Wiring/Arcing", "Grid-Tie Sync Failure"
    ]
}

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.write("Engineering Magic for 54 Countries")
    
    st.divider()
    # CORE SERVICE SELECTION (Triggers the Symptoms)
    service_cat = st.radio("SELECT CORE SERVICE", list(SYMPTOM_MAP.keys()))
    
    st.divider()
    country = st.selectbox("Operating Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])
    mode = st.radio("Portal View", ["User Diagnosis", "Mechanic Negotiation", "Sovereign Ledger"])
    
    st.markdown('<a href="tel:911" style="color:red; font-weight:bold;">🆘 EMERGENCY SOS</a>', unsafe_allow_html=True)

# --- 4. MAIN PORTAL: DYNAMIC DIAGNOSIS ---
if mode == "User Diagnosis":
    st.markdown(f"<div class='main-title'>{service_cat.split(' ')[1].upper()} DIAGNOSIS</div>", unsafe_allow_html=True)
    
    st.subheader(f"7 Fault Symptoms: {service_cat}")
    
    # Generate the 7 symptoms dynamically from the Matrix
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    
    selected_symptoms = []
    for i, symptom in enumerate(symptoms):
        target_col = col1 if i < 4 else col2
        if target_col.checkbox(f"{i+1}. {symptom}"):
            selected_symptoms.append(symptom)
            
    description = st.text_area("Additional Engineering Description", placeholder="Enter specific fix requirements...")

    if st.button("🧠 RUN AI DIAGNOSIS"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            with st.spinner("Analyzing Sovereign Data..."):
                time.sleep(1.5)
                st.markdown(f"""
                <div class='diag-card'>
                    <b>AI ANALYSIS COMPLETE FOR {service_cat.upper()}</b><br>
                    Detected Patterns: {", ".join(selected_symptoms)}<br><br>
                    <i>Result: High priority fault detected. Dispatching closest certified engineer.</i>
                </div>
                """, unsafe_allow_html=True)

# --- 5. SECURE PRICING & BANKING ---
    if 'quote' in st.session_state:
        base = st.session_state.quote
        total = base * 1.15 # Automatic 15% Share applied
        
        st.divider()
        st.subheader("💳 Secure Payment Portal")
        st.write("Pricing is fixed based on Mechanic-Founder Agreement.")
        
        c1, c2 = st.columns(2)
        # Displaying locked final price
        c1.metric("Final Service Fee", f"${total:,.2f}") 
        c2.metric("Founder Share", "15% Included")
        
        if st.button("CONNECT TO CENTRAL BANK"):
            st.success("Tunneling to Secure Banking Gateway... 2% Police Fee REMOVED.")

# --- 6. MECHANIC INTERFACE ---
elif mode == "Mechanic Negotiation":
    st.subheader("Mechanic Terminal")
    st.write("Negotiate with user and input base cost. 15% will be added automatically.")
    mech_price = st.number_input("Negotiated Base Price ($)", min_value=0.0)
    if st.button("Submit to User"):
        st.session_state.quote = mech_price
        st.info("Price transmitted to User Portal.")

# --- 7. RADAR ---
st.divider()
st.subheader("📍 Sovereign Radar")
map_data = pd.DataFrame(np.random.randn(2, 2) / [80, 80] + [6.5244, 3.3792], columns=['lat', 'lon'])
st.map(map_data)
st.caption("Automatic location sync: User ↔ Mechanic.")
        
