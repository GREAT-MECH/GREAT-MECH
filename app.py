import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. SOVEREIGN CONFIG & STYLING ---
st.set_page_config(page_title="Great Mech | Autonomous", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #111 !important; border-right: 1.5px solid #D4AF37; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; }
    .diag-box { border: 1px solid #00FF00; padding: 15px; border-radius: 10px; background: #001a00; color: #00FF00; }
    .bank-portal { border: 2px solid #D4AF37; padding: 25px; border-radius: 15px; background: linear-gradient(145deg, #111, #000); text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. CORE LOGIC: PRICING & CURRENCY ---
# Mapping 54 countries to local currencies (Sample)
CURRENCY_MAP = {
    "Nigeria": {"symbol": "₦", "rate": 1500}, 
    "Kenya": {"symbol": "KSh", "rate": 130},
    "South Africa": {"symbol": "R", "rate": 19},
    "Ghana": {"symbol": "GH₵", "rate": 14},
    "Egypt": {"symbol": "E£", "rate": 48}
}

def get_local_price(usd_amount, country):
    data = CURRENCY_MAP.get(country, {"symbol": "$", "rate": 1})
    return f"{data['symbol']}{usd_amount * data['rate']:,.2f}"

# --- 3. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    try:
        st.image("316436.png", width=150)
    except:
        st.image("https://img.icons8.com/isometric/512/africa.png", width=100)
    
    st.markdown("### SOVEREIGN NAV")
    app_mode = st.radio("INTERFACE", ["User Portal", "Mechanic Portal", "Sovereign Ledger"])
    
    country_context = st.selectbox("Current Territory", list(CURRENCY_MAP.keys()))
    
    st.divider()
    if st.button("End Session"):
        st.session_state.clear()
        st.rerun()
    st.markdown('<a href="tel:911" style="color:red; text-decoration:none; font-weight:bold;">🆘 EMERGENCY SOS</a>', unsafe_allow_html=True)

# --- 4. USER PORTAL ---
if app_mode == "User Portal":
    st.markdown("<div class='main-title'>GREAT MECH AI DIAGNOSIS</div>", unsafe_allow_html=True)
    
    # 7 Fault Symptoms (Mechanical Core)
    st.subheader("Select Manifested Symptoms")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.checkbox("1. Unusual Engine Noise (Knocking/Hissing)")
        s2 = st.checkbox("2. Fluid Leakage (Oil/Coolant/Diesel)")
        s3 = st.checkbox("3. Loss of Power / Stalling")
        s4 = st.checkbox("4. Excessive Exhaust Smoke")
    with col2:
        s5 = st.checkbox("5. Electrical/Sensor Failure")
        s6 = st.checkbox("6. Transmission/Gear Slippage")
        s7 = st.checkbox("7. Overheating Indicators")

    desc_box = st.text_area("Detailed Symptom Description", placeholder="Describe exactly what happened before the failure...")

    if st.button("✨ RUN AI DIAGNOSIS"):
        with st.spinner("Analyzing mechanical fault patterns..."):
            time.sleep(2)
            st.markdown("""
            <div class='diag-box'>
                <b>AI DIAGNOSIS COMPLETE:</b><br>
                Probability: 88% Fuel Injector Malfunction / 12% Sensor Calibration.<br>
                Recommendation: Immediate onsite inspection required.
            </div>
            """, unsafe_allow_html=True)
            st.session_state.diag_complete = True

    # Negotiated Amount (Presented to User, NOT Editable)
    # In a real app, this value comes from the Mechanic Portal via the cloud
    if 'mech_quote' in st.session_state:
        base = st.session_state.mech_quote
        founder_cut = base * 0.15 #
        total_usd = base + founder_cut
        
        st.divider()
        st.subheader("🔒 Secure Service Agreement")
        st.info(f"The Mechanic has proposed a fix cost. Platform fee (15%) has been applied.")
        
        col_p1, col_p2 = st.columns(2)
        col_p1.metric("Total Payable (Local)", get_local_price(total_usd, country_context))
        col_p2.metric("Platform Status", "Verified (No 2% Tax)") #

        if st.button("💳 CONNECT TO BANKING SYSTEM"):
            st.markdown(f"""
            <div class='bank-portal'>
                <h3>Sovereign Banking Tunnel</h3>
                <p>Establishing secure connection to {country_context} Central Clearing...</p>
                <button style='padding:10px; background:#D4AF37; border:none; border-radius:5px;'>Confirm Transaction</button>
            </div>
            """, unsafe_allow_html=True)

# --- 5. MECHANIC PORTAL (FOR NEGOTIATION) ---
elif app_mode == "Mechanic Portal":
    st.subheader("Mechanic Negotiation Terminal")
    st.write("Discuss the fix with the user, then enter the base amount below.")
    
    proposed_base = st.number_input("Base Negotiated Price ($USD)", min_value=0.0)
    if st.button("Transmit Quote to User"):
        st.session_state.mech_quote = proposed_base
        st.success("Quote sent. User is now reviewing the final price (including platform share).")

# --- 6. RADAR (AUTOMATIC LOCATION) ---
if app_mode in ["User Portal", "Mechanic Portal"]:
    st.divider()
    st.subheader("📍 Real-Time Proximity Radar")
    st.write("Location Services: **ON (Automatic)**")
    
    # Simulating shared map for both parties
    map_data = pd.DataFrame(
        np.random.randn(2, 2) / [100, 100] + [6.5244, 3.3792],
        columns=['lat', 'lon']
    )
    st.map(map_data)
    st.caption("ETA to reaching target: 14 Minutes.")

# --- 7. LEDGER (LOCAL CURRENCY) ---
elif app_mode == "Sovereign Ledger":
    st.subheader("Official Engineering Ledger")
    # Historical Data Mockup
    history = [
        {"id": "GM-9912", "cat": "Solar", "usd": 450},
        {"id": "GM-8821", "cat": "Truck", "usd": 1200}
    ]
    
    for item in history:
        st.markdown(f"""
        <div style='border:1px solid #333; padding:10px; border-radius:5px; margin-bottom:10px;'>
            <b>Order {item['id']}</b> | {item['cat']}<br>
            Total Paid: <span style='color:#D4AF37;'>{get_local_price(item['usd'], country_context)}</span>
        </div>
        """, unsafe_allow_html=True)
    
