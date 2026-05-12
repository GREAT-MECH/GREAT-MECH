import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. SOVEREIGN CONFIG & SCREEN-FIT STYLING ---
st.set_page_config(
    page_title="Great Mech | Africa's Pulse", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Industrial Theme */
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Animation: Moving Africa to the Next Level */
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-top: -10px; margin-bottom: 20px; }
    
    /* Full-Screen Console Header */
    .main-title { 
        text-align: center; 
        font-size: clamp(30px, 5vw, 55px); 
        font-weight: 900; 
        color: #D4AF37; 
        margin-top: -50px;
        padding-bottom: 10px;
    }
    
    /* Sidebar Aesthetics */
    section[data-testid="stSidebar"] { 
        background-color: #0c0c0c !important; 
        border-right: 1px solid #D4AF37; 
        width: 300px !important;
    }
    
    /* Tightening Containers for Screen Fit */
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; }
    .diag-output { 
        border-left: 5px solid #D4AF37; 
        padding: 15px; 
        background: #111; 
        border-radius: 0 10px 10px 0; 
        font-size: 15px; 
    }
    
    /* Professional Action Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background-color: #D4AF37; 
        color: black; 
        font-weight: bold; 
        border: none; 
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FFF; color: #000; box-shadow: 0 0 15px #D4AF37; }
</style>
""", unsafe_allow_html=True)

# --- 2. DYNAMIC FAULT MATRIX (Service-Specific) ---
SYMPTOM_MAP = {
    "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
    "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
    "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
    "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
    "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
}

# --- 3. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    
    service_cat = st.selectbox("CHOOSE SERVICE", list(SYMPTOM_MAP.keys())) #
    mode = st.radio("COMMAND MODE", ["Diagnosis Portal", "Mechanic Hub", "Sovereign Ledger"])
    
    st.divider()
    country = st.selectbox("Territory (54 Countries)", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt", "Ethiopia", "Morocco"])
    st.caption(f"System Optimized for {country}")
    
    if st.button("Secure Logout"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown('<a href="tel:911" style="color:red; text-decoration:none; font-weight:bold; display:block; text-align:center; border:1px solid red; padding:5px; border-radius:5px;">🆘 EMERGENCY PANIC</a>', unsafe_allow_html=True) #

# --- 4. MAIN CONSOLE: FULL SCREEN FIT ---
if mode == "Diagnosis Portal":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE ⚙️🧰</div>", unsafe_allow_html=True)
    
    # 7 Dynamic Symptoms
    st.subheader(f"7 Symptom Profile: {service_cat}")
    symptoms = SYMPTOM_MAP[service_cat]
    col1, col2 = st.columns(2)
    selected_symptoms = []
    
    for i, sym in enumerate(symptoms):
        target = col1 if i < 4 else col2
        if target.checkbox(f"{i+1}. {sym}"):
            selected_symptoms.append(sym)
    
    # Description Box & AI Logic
    desc_text = st.text_area("Engineering Details / Extra Symptoms", height=100, placeholder="Describe the fault in detail...")

    if st.button("🚀 EXECUTE AI DIAGNOSIS"): #
        with st.spinner("Processing Engineering Magic..."):
            time.sleep(1.5)
            analysis_context = ", ".join(selected_symptoms) if selected_symptoms else "Unlisted/Manual Description"
            st.markdown(f"""
            <div class='diag-output'>
                <b>AI DIAGNOSIS RESULTS:</b><br>
                <b>Primary Symptoms:</b> {analysis_context}<br>
                <b>Expert Analysis:</b> {desc_text if desc_text else "Analyzing physical symptoms..."}<br><br>
                <b>Conclusion:</b> Logic indicates a critical malfunction in {service_cat} systems. 
                Initiating mechanic-user synchronization.
            </div>
            """, unsafe_allow_html=True)

    # Pricing & Banking (Invisible 2% Fee Logic)
    if 'base_price' in st.session_state:
        final_total = st.session_state.base_price * 1.15 #
        st.divider()
        c1, c2, c3 = st.columns([2,1,1])
        c1.markdown(f"### Total Service Amount: **${final_total:,.2f}**")
        if c2.button("💳 PAY VIA BANK"):
            st.success("Sovereign Gateway Secured.")

# --- 5. MECHANIC HUB ---
elif mode == "Mechanic Hub":
    st.subheader("Bargaining Terminal")
    st.info("Negotiate amount with user. 15% Founder share is calculated upon submission.") #
    proposed = st.number_input("Negotiated Base Price ($)", min_value=0.0, step=10.0)
    if st.button("Lock & Transmit Quote"):
        st.session_state.base_price = proposed
        st.success("Quote sent to User Portal.")

# --- 6. SOVEREIGN LEDGER ---
elif mode == "Sovereign Ledger":
    st.subheader("Regional Transaction Records")
    # Simulation of local currency display
    st.write(f"Showing verified transactions for {country}:")
    st.table(pd.DataFrame({
        "Order ID": ["GM-104", "GM-209", "GM-315"],
        "Service": ["Truck", "Solar", "Diesel/Gen"],
        "Local Total": ["₦1,850,000", "₦720,000", "₦440,000"],
        "Status": ["Verified", "Verified", "Verified"]
    }))

# --- 7. RADAR (Bottom Docked) ---
st.divider()
st.markdown("### 📍 Sovereign Proximity Radar")
map_data = pd.DataFrame(np.random.randn(2, 2) / [120, 120] + [6.5244, 3.3792], columns=['lat', 'lon'])
st.map(map_data, use_container_width=True)
        
