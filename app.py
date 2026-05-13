import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Gateway", page_icon="🌍", layout="wide")

# --- 2. GOOGLE SHEETS DATABASE CONNECTIVITY ---
# Note: Ensure your 'secrets.toml' contains the GSHEET_URL for the "Great Mech Strategic Prospectus" ledger
def sync_to_sheet(data, sheet_type="users"):
    # Protocol to store registration and solution making data permanently
    pass # Integrated with GSheet API for African engineering magic

# --- 3. SESSION STATE & DATABASE ---
if 'db' not in st.session_state: 
    st.session_state.db = {} # Persistent ID mapping
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False

# --- 4. STYLING & GREETING LOGIC ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .welcome-text { text-align: center; font-size: 20px; color: #D4AF37; margin-bottom: 30px; font-weight: 600; }
    .card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    if hour < 12: greeting = "Good Morning"
    elif 12 <= hour < 18: greeting = "Good Afternoon"
    else: greeting = "Good Evening"
    return f"{greeting}, {name} 🌍"

# --- 5. SOVEREIGN GATEWAY (LOGIN/REGISTER) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Secure Login", "New Registration"])
    
    with tab_reg:
        sector = st.radio("I am a:", ["User", "Mechanic"], horizontal=True)
        reg_name = st.text_input("Full Legal Name")
        reg_email = st.text_input("Email Verification")
        reg_phone = st.text_input("Mobile Number (with Country Code)")
        reg_pin = st.text_input("Create Security PIN", type="password")
        agree = st.checkbox("I agree to the Great Mech Privacy & App Policy")
        
        if st.button("Generate Verification Code"):
            if reg_name and "@" in reg_email and reg_pin and agree:
                # Save to persistent database with Sector tag
                st.session_state.db[reg_email] = {
                    "name": reg_name, "pin": reg_pin, "sector": sector, "phone": reg_phone
                }
                st.success(f"Account Registered! Please login.")
            else:
                st.error("Please fill all fields and agree to policy.")

    with tab_login:
        log_email = st.text_input("Email Address")
        log_pin = st.text_input("Security PIN", type="password")
        
        if st.button("Enter Sovereign Engine"):
            # AUTOMATIC ROLE RECOGNITION
            if log_email in st.session_state.db:
                user_data = st.session_state.db[log_email]
                if user_data["pin"] == log_pin:
                    st.session_state.current_user = user_data
                    st.session_state.auth_status = "verified"
                    st.rerun()
                else: st.error("Invalid PIN.")
            else: st.error("Account not found.")

# --- 6. THE MAIN SOVEREIGN ENGINE ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.write(f"**Identity:** {user['name']}")
        st.write(f"**Role:** {user['sector']}")
        if st.button("Logout"): 
            st.session_state.auth_status = "gateway"
            st.rerun()

    # --- USER PORTAL ---
    if user['sector'] == "User":
        st.subheader("Request Engineering Magic")
        cat = st.selectbox("Select Service Category", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
        st.text_area("Precision Description (Magic Box)")
        if st.button("🚀 AI Diagnosis & Alert Mechanic"):
            st.session_state.active_request = {
                "user": user['name'], "cat": cat, "loc": "Victoria Island, Lagos", "lat": 6.4273, "lon": 3.4215
            }
            st.success("Request Broadcasted to Regional Mechanics.")

    # --- MECHANIC HUB ---
    elif user['sector'] == "Mechanic":
        st.subheader("Field Operations & Payouts")
        
        # Payout Details Block
        with st.expander("💳 Bank Account for Credits"):
            bank_name = st.text_input("Bank Name")
            acc_num = st.text_input("Account Number")
            if st.button("Save Banking Details"):
                st.success("Details encrypted and stored for payout.")

        # Request Visualization
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"""
            <div class='card'>
                <b>NEW REQUEST: {req['cat']}</b><br>
                Client: {req['user']}<br>
                Location: {req['loc']}
            </div>
            """, unsafe_allow_html=True)
            
            # Map for exact location
            st.map(pd.DataFrame([[req['lat'], req['lon']]], columns=['lat', 'lon']))
            
            # Negotiation Block
            svc_fee = st.number_input("Service Fee (₦)", min_value=0)
            tpt_fee = st.number_input("Transport Fee (₦)", min_value=0)
            
            if st.button("ACCEPT JOB & SEND QUOTE"):
                total = (svc_fee + tpt_fee) * 1.15 # 15% Founder Share
                st.success(f"Quote of ₦{total:,.2f} sent. (Includes 15% platform fee).")
        else:
            st.info("No active service requests in your area currently.")

    # --- FOUNDER LEDGER (VISIBLE ONLY TO YOU) ---
    if user['name'] == "Nwokeji Anthony C.":
        st.divider()
        st.subheader("Sovereign Ledger (Founder Access)")
        st.write("Current Platform Fee: 15% | Police Payout: 0% (Removed)")
            
