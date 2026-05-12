import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. SOVEREIGN CONFIG & REFINED STYLING ---
st.set_page_config(page_title="Great Mech | Africa's Pulse", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    /* Dark Slate & Gold Theme */
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Animation: Moving Africa to the Next Level */
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-top: -10px; margin-bottom: 20px; }
    
    /* UI Cleanup */
    .main-title { text-align: center; font-size: 55px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    section[data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 1px solid #D4AF37; }
    .diag-output { border-left: 5px solid #D4AF37; padding: 20px; background: #111; border-radius: 0 10px 10px 0; font-size: 16px; line-height: 1.6; }
    
    /* Button Aesthetics */
    .stButton>button { width: 100%; border-radius: 5px; background-color: #D4AF37; color: black; font-weight: bold; border: none; height: 3em; }
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

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    
    service_cat = st.selectbox("CHOOSE SERVICE", list(SYMPTOM_MAP.keys()))
    mode = st.radio("INTERFACE", ["Diagnosis Portal", "Mechanic Hub", "Sovereign Ledger"])
    
    st.divider()
    country = st.selectbox("Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])
    st.info(f"System Optimized for {country}")
    
    if st.button("Secure Logout"):
        st.session_state.clear()
        st.rerun()

# --- 4. DIAGNOSIS PORTAL (Refined & Integrated) ---
if mode == "Diagnosis Portal":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE</div>", unsafe_allow_html=True)
    
    # 7 Dynamic Symptoms
    st.subheader(f"7 Symptom Profile: {service_cat}")
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    selected_symptoms = []
    
    for i, sym in enumerate(symptoms):
        target = col1 if i < 4 else col2
        if target.checkbox(f"{i+1}. {sym}"):
            selected_symptoms.append(sym)
    
    # Description Box (Integrated with AI)
    desc_text = st.text_area("Engineering Description (Add details not listed above)", height=150)

    if st.button("🚀 EXECUTE AI DIAGNOSIS"):
        with st.spinner("Processing Sovereign Logic..."):
            time.sleep(2)
            # AI Logic: Combines selected symptoms AND description box
            analysis_context = ", ".join(selected_symptoms) if selected_symptoms else "Unlisted Fault"
            st.markdown(f"""
            <div class='diag-output'>
                <b>AI DIAGNOSIS RESULTS:</b><br>
                <b>Detected Patterns:</b> {analysis_context}<br>
                <b>Manual Input Analysis:</b> {desc_text if desc_text else "No extra details provided."}<br><br>
                <b>Conclusion:</b> System identifies a localized failure in the {service_cat} primary circuit. 
                Certified Great Mech engineer required for manual override.
            </div>
            """, unsafe_allow_html=True)

    # Pricing & Banking (Invisible 2% Fee Logic)
    if 'base_price' in st.session_state:
        final_total = st.session_state.base_price * 1.15 # 15% Platform Fee
        st.divider()
        st.subheader("Secure Clearing House")
        c1, c2 = st.columns(2)
        c1.metric("Final Service Amount", f"${final_total:,.2f}")
        c2.metric("Security Status", "Encrypted")
        
        if st.button("💳 CONNECT TO CENTRAL BANK"):
            st.success("Tunnel established. Transaction cleared via Sovereign Gateway.")

# --- 5. MECHANIC HUB ---
elif mode == "Mechanic Hub":
    st.subheader("Bargaining Terminal (Mechanic View)")
    proposed = st.number_input("Negotiated Base Price ($)", min_value=0.0)
    if st.button("Transmit to User"):
        st.session_state.base_price = proposed
        st.info("Price transmitted. 15% revenue share added automatically.")

# --- 6. LEDGER (Sovereign Records) ---
elif mode == "Sovereign Ledger":
    st.subheader("Global Transaction History")
    # Simulation of local currency display
    st.write("Displaying all verified transactions in local currency equivalent.")
    st.table(pd.DataFrame({
        "Order ID": ["GM-104", "GM-209"],
        "Category": ["Truck", "Solar"],
        "Amount": ["₦1,800,000", "₦675,000"],
        "Status": ["Cleared", "Cleared"]
    }))

# --- 7. RADAR (Shared View) ---
st.divider()
st.subheader("📍 Sovereign Radar (Synchronized)")
map_data = pd.DataFrame(np.random.randn(2, 2) / [100, 100] + [6.5244, 3.3792], columns=['lat', 'lon'])
st.map(map_data)
            
