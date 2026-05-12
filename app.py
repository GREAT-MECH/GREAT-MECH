import streamlit as st
import pandas as pd
import numpy as np
import time
import requests # Necessary for Banking API calls

# --- 1. SOVEREIGN CONFIG & STYLING ---
st.set_page_config(page_title="Great Mech | Banking Terminal", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-bottom: 20px; }
    .main-title { text-align: center; font-size: clamp(30px, 5vw, 50px); font-weight: 900; color: #D4AF37; margin-top: -50px; }
    section[data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 1px solid #D4AF37; }
    .bank-portal { border: 2px solid #D4AF37; padding: 25px; border-radius: 15px; background: #111; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE BANKING GATEWAY (Logic) ---
def initialize_payment(email, amount_usd, country):
    """
    Connects to the Banking API (e.g., Paystack/Flutterwave).
    This function will trigger the real transaction.
    """
    # 2% Police fee is silently ignored here
    # We only process (Base + Transport) + 15% Platform Fee
    amount_in_cents = int(amount_usd * 100) 
    
    # Placeholder for Real API Secret Key
    # headers = {"Authorization": "Bearer YOUR_SECRET_KEY"}
    # payload = {"email": email, "amount": amount_in_cents, "currency": "USD"}
    # response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
    
    return "https://secure.banking-gateway.com/pay/GM-LIVE-AUTH"

# --- 3. SESSION STATE ---
if 'active_brief' not in st.session_state: st.session_state.active_brief = None
if 'mechanic_quote' not in st.session_state: st.session_state.mechanic_quote = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    service_cat = st.selectbox("CHOOSE SERVICE", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
    mode = st.radio("INTERFACE", ["User Portal", "Mechanic Hub"])
    st.divider()
    country = st.selectbox("Territory", ["Nigeria", "Kenya", "South Africa", "Ghana", "Egypt"])

# --- 5. USER PORTAL & BANKING ---
if mode == "User Portal":
    st.markdown("<div class='main-title'>ENGINEERING CONSOLE ⚙️🧰</div>", unsafe_allow_html=True)
    
    if st.button("🚀 EXECUTE AI DIAGNOSIS"):
        # Auto-detect location and send to Mechanic
        st.session_state.active_brief = {
            "category": service_cat,
            "address": "123 Sovereign Way, Lagos", # Simulated GPS
            "eta": "15 mins"
        }
        st.success("Brief & Location sent to Mechanic.")

    if st.session_state.mechanic_quote:
        quote = st.session_state.mechanic_quote
        st.markdown(f"""
        <div class='bank-portal'>
            <h3 style='color:#D4AF37;'>Final Payment: ${quote['total']:,.2f}</h3>
            <p>Payment covers Service & Transportation</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 CONNECT TO LIVE BANKING"):
            # Execute the real banking handshake
            payment_url = initialize_payment("user@example.com", quote['total'], country)
            st.success(f"Secure Tunnel Established. Redirecting to Central Bank...")
            st.link_button("Complete Transaction on Banking Portal", payment_url)

# --- 6. MECHANIC HUB (Location Awareness) ---
elif mode == "Mechanic Hub":
    st.subheader("Mission Logistics")
    if st.session_state.active_brief:
        brief = st.session_state.active_brief
        st.info(f"📍 **TARGET ADDRESS:** {brief['address']}") #
        st.write(f"⏱️ **Estimated Travel Time:** {brief['eta']}") #
        
        service_p = st.number_input("Service Fix Cost ($)", min_value=0.0)
        transport_p = st.number_input("Transportation Fare ($)", min_value=0.0)
        
        if st.button("TRANSMIT QUOTE"):
            # Maintain 15% share, exclude 2% police tax
            base = service_p + transport_p
            total = base * 1.15 
            st.session_state.mechanic_quote = {"total": total}
            st.success("Price transmitted to User's Banking Terminal.")
    else:
        st.write("Waiting for incoming signal...")

# --- 7. RADAR ---
st.divider()
st.subheader("📍 Real-Time Synchronization Radar")
st.map(pd.DataFrame(np.random.randn(2, 2) / [120, 120] + [6.5244, 3.3792], columns=['lat', 'lon']))
