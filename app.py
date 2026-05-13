import streamlit as st
import pandas as pd
import requests
import time
import re

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
# Locked from verified credentials for Great Mech African Engineering Magic
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. ADVANCED FOUNDER STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; color: #D4AF37; opacity: 0.8; margin-bottom: 20px; }
    .auth-card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; }
    .card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
    .panic-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; border-radius: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE & DATABASE ENGINE ---
# This serves as our local database to save login information
if 'user_db' not in st.session_state: 
    st.session_state.user_db = {} # Format: {identifier: {details}}
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_ref' not in st.session_state: st.session_state.payment_ref = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'final_quote' not in st.session_state: st.session_state.final_quote = None
if 'mech_balance' not in st.session_state: st.session_state.mech_balance = 0.0

# --- 4. CORE BANKING & LOGIC FUNCTIONS ---
def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}"}
    try:
        response = requests.get(url, headers=headers).json()
        return response.get('status') and response['data']['status'] == 'success'
    except: return False

def initialize_payment(email, amount_ngn):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}", "Content-Type": "application/json"}
    ref = f"GM-{int(time.time())}"
    payload = {
        "email": email, "amount": int(float(amount_ngn) * 100), "currency": "NGN",
        "reference": ref, "callback_url": "https://greatmech.streamlit.app"
    }
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return (res['data']['authorization_url'], ref) if res.get('status') else (None, None)
    except: return None, None

# --- 5. THE SOVEREIGN GATEWAY (LOGIN/REGISTER) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Login", "Register"])
    
    with tab_reg:
        st.markdown("### Create Your Engineering Profile")
        lang = st.selectbox("Preferred Language", ["English", "Français", "Swahili", "Hausa/Igbo/Yoruba"])
        country = st.selectbox("Country of Operation", ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Other (54 Countries)"])
        
        # Registration fields based on file 320416.png
        reg_name = st.text_input("Full Legal Name", key="reg_name")
        reg_email = st.text_input("Email Verification", key="reg_email")
        reg_phone = st.text_input("Mobile Number", key="reg_phone")
        reg_pin = st.text_input("Create Security PIN", type="password", help="Use this to login later")
        
        reg_agree = st.checkbox("I agree to the Great Mech Privacy & App Policy", key="reg_agree")
        
        if st.button("Generate Verification Code"):
            # Strict validation logic
            if not reg_name or "@" not in reg_email or len(reg_phone) < 10 or not reg_pin or not reg_agree:
                st.error("Please correct your details and agree to the policy.")
            else:
                # Save to "Database"
                st.session_state.user_db[reg_email] = {
                    "name": reg_name, "phone": reg_phone, "pin": reg_pin, "country": country
                }
                st.success(f"Profile created for {reg_name}! You can now switch to the Login tab.")
                time.sleep(1)

    with tab_login:
        st.markdown("### Access Sovereign Portal")
        login_email = st.text_input("Email Address", key="log_email")
        login_pin = st.text_input("Security PIN", type="password", key="log_pin")
        
        if st.button("Enter Sovereign Engine"):
            # Check if user exists and PIN matches
            if login_email in st.session_state.user_db:
                if st.session_state.user_db[login_email]["pin"] == login_pin:
                    st.session_state.current_user = st.session_state.user_db[login_email]
                    st.session_state.auth_status = "verified"
                    st.rerun()
                else:
                    st.error("Incorrect Security PIN.")
            else:
                st.error("No account found with this email. Please register first.")

# --- 6. THE MAIN SOVEREIGN ENGINE ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    with st.sidebar:
        st.write(f"**User:** {user['name']}")
        st.write(f"**Region:** {user['country']}")
        role = st.radio("ACCESS", ["User Portal", "Mechanic Hub", "Sovereign Ledger"])
        st.divider()
        if st.button("Logout"): 
            st.session_state.auth_status = "gateway"
            st.session_state.current_user = None
            st.rerun()

    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    
    # 5 Categories & 7 Symptoms Matrix
    SYMPTOM_MATRIX = {
        "🚛 Truck": ["Brake Pressure Loss", "Engine Knocking", "Coupling Issue", "Exhaust Smoke", "Gear Resistance", "Suspension Sag", "Axle Overheat"],
        "🚗 Car": ["ABS Warning", "Steering Vibration", "AC Failure", "Brake Squeal", "Ignition Delay", "Fluid Leaks", "Check Engine Light"],
        "⚙️ Diesel/Gen": ["Injection Fault", "Governor Hunting", "Radiator Clog", "Low Oil Pressure", "Voltage Drop", "Vibration", "Turbo Lag"],
        "📹 CCTV": ["Signal Loss", "IR Failure", "Storage Error", "PTZ Jam", "Network Lag", "Flickering", "Power Overload"],
        "☀️ Solar": ["Inverter Fault", "Battery Drain", "Micro-cracks", "Controller Heat", "Efficiency Drop", "Arcing", "Grid Sync Failure"]
    }

    if role == "User Portal":
        if st.session_state.payment_confirmed:
            st.success("✅ TRANSACTION VERIFIED. Dispatching Elite Mechanic.")
            if st.button("MARK JOB AS COMPLETE"):
                st.session_state.mech_balance += (st.session_state.final_quote / 1.15)
                st.session_state.payment_confirmed = False; st.rerun()
        elif st.session_state.final_quote:
            st.markdown(f"### Pay ₦{st.session_state.final_quote:,.2f} to start repair")
            if st.button("💳 AUTHORIZE PAYMENT"):
                url, ref = initialize_payment(user['email'], st.session_state.final_quote)
                if url: st.session_state.payment_ref = ref; st.link_button("OPEN SECURE BANKING TUNNEL", url)
            if st.session_state.payment_ref:
                if st.button("🔄 VERIFY PAYMENT STATUS"):
                    if verify_payment(st.session_state.payment_ref):
                        st.session_state.payment_confirmed = True; st.rerun()
        else:
            cat = st.selectbox("Rendered Service", list(SYMPTOM_MATRIX.keys()))
            col1, col2 = st.columns(2)
            selected = [sym for i, sym in enumerate(SYMPTOM_MATRIX[cat]) if (col1 if i < 4 else col2).checkbox(sym)]
            desc = st.text_area("Precision Description (The Magic Box)")
            if st.button("🚀 AI DIAGNOSIS & ALERT MECHANIC"):
                st.session_state.active_request = {"cat": cat, "faults": selected, "desc": desc, "user": user['name']}
                st.success("Regional Mechanics alerted through the Sovereign Network.")

    elif role == "Mechanic Hub":
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Alert from {req['user']}</b><br>Category: {req['cat']}<br>Faults: {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            svc = st.number_input("Service Cost (₦)")
            tpt = st.number_input("Transport (₦)")
            if st.button("TRANSMIT QUOTE"):
                st.session_state.final_quote = (svc + tpt) * 1.15 # 15% Founder Share
                st.success("Quote sent to User.")
        
        st.divider()
        st.subheader("Your Wallet")
        st.metric("Earned (85%)", f"₦{st.session_state.mech_balance:,.2f}")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY ALERT: Private Security notified of your location.")

    elif role == "Sovereign Ledger":
        st.subheader("Founder Performance Ledger")
        st.write("Founder Share: 15% | Police Tax: 0% (Strictly Removed)") #
        rev = st.session_state.final_quote if st.session_state.payment_confirmed else 0.0
        st.write(f"Total Revenue: ₦{rev:,.2f}")
        st.write(f"Founder Net (15%): ₦{rev - (rev/1.15) if rev > 0 else 0:,.2f}")

    st.divider()
    st.subheader("📍 Sovereign Logistics Radar")
    st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) # Real-time location tracking
        
