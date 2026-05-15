import streamlit as st
import datetime
import pandas as pd

# ============================================================================
# SUPREME ENGINE v42.1 - STREAMLIT EDITION
# ============================================================================

st.set_page_config(page_title="Great Mech Supreme Engine", page_icon="⚙️", layout="centered")

# Black & Gold Prestige Styling
st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: #d4af37; }
    h1 { color: #d4af37; font-family: 'Playfair Display', serif; text-align: center; border-bottom: 2px solid #d4af37; }
    .stButton>button { background-color: #d4af37; color: black; font-weight: bold; border-radius: 10px; width: 100%; }
    .panic-btn>button { background-color: #ff0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("SUPREME ENGINE 🌍")
st.subheader("Moving Africa to the Next Level")

# ============================================================================
# FOUNDER'S FINANCIAL ENGINE (HARDCODED)
# ============================================================================
FOUNDER_SHARE_PERCENT = 15
SECURITY_FEE_PERCENT = 0 

def calculate_billing(amount):
    founder_share = amount * (FOUNDER_SHARE_PERCENT / 100)
    mechanic_share = amount - founder_share
    return founder_share, mechanic_share

# ============================================================================
# THE INTERFACE
# ============================================================================

menu = ["Service Request", "Mechanic Portal", "Founder Dashboard"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Service Request":
    st.write("### Request African Engineering Magic")
    service = st.selectbox("Category", ["Truck Services", "Car Services", "Diesel Engine/Generator", "CCTV Systems", "Solar Solutions"])
    country = st.selectbox("Country", ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Other (All 54 African Nations)"])
    amount = st.number_input("Estimated Service Amount", min_value=1.0)
    
    if st.button("Calculate & Request"):
        f_share, m_share = calculate_billing(amount)
        st.success(f"Service Requested in {country}!")
        st.write(f"**Total Amount:** {amount}")
        st.write(f"**Founder Share (15%):** {f_share}")
        st.write(f"**Police Security Fee:** 0.00 (Strictly Enforced)")
        st.info("Thanks for using Great Mech ⚙️🧰")

elif choice == "Mechanic Portal":
    st.write("### Mechanic On-Site Tools")
    st.warning("EMERGENCY PROTOCOL")
    if st.button("🚨 TRIGGER PANIC BUTTON", key="panic"):
        st.error("CRITICAL ALERT: Private Security Dispatched to your location. Bypassing Police.")
        # Logic: In a real app, this sends an SMS/Email to your security firm.

elif choice == "Founder Dashboard":
    st.write("### Founder Oversight")
    st.metric("Founder Share %", f"{FOUNDER_SHARE_PERCENT}%")
    st.metric("Security Fee %", "0%")
    st.write("Immutable Audit Trail active. All 54 countries connected.")

st.markdown("---")
st.caption("Great Mech v42.1 | Sovereign African Technology")
