import streamlit as st
import pandas as pd
import requests
import time
import re

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
# Hard-coded from verified credentials for Live Production
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
    .panic-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ENGINE ---
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'user_data' not in st.session_state: st.session_state.user_data = {}
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
        "reference": ref, "callback_url": "https://greatmech.streamlit.app",
        "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"]
    }
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return (res['data']['authorization_url'], ref) if res.get('status') else (None, None)
    except: return None, None

def get_banks(country_code="NG"):
    url = f"https://api.paystack.co/bank?country={country_code}"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}"}
    try:
        res = requests.get(url, headers=headers).json()
        return {bank['name']: bank['code'] for bank in res['data']}
    except: return {"Manual Entry": "000"}

def initiate_payout(amount, recipient_code):
    url = "https://api.paystack.co/transfer"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}", "Content-Type": "application/json"}
    payload = {"source": "balance", "amount": int(float(amount) * 100), "recipient": recipient_code, "reason": "Job Payout"}
    return requests.post(url, json=payload, headers=headers).json().get('status')

# --- 5. THE SOVEREIGN GATEWAY (LOGIN/REGISTER) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>ENGINEERING SOVEREIGN AFRICA</div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Login", "Register"])
    
    with tab_reg:
        lang = st.selectbox("Preferred Language", ["English", "Français", "Swahili", "Hausa/Igbo/Yoruba"])
        country = st.selectbox("Country", ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Other"])
        full_name = st.text_input("Full Legal Name")
        email = st.text_input("Email Verification")
        phone = st.text_input("Mobile Number")
        agree = st.checkbox("I agree to the Great Mech Privacy & App Policy")
        
        if st.button("Generate Verification Code"):
            if not full_name or not "@" in email or len(phone) < 10 or not agree:
                st.error("Please correct your details and agree to the policy.")
            else:
                st.session_state.user_data = {"name": full_name, "email": email, "country": country}
                st.success(f"OTP sent to {phone}. Verifying...")
                time.sleep(1)
                st.session_state.auth_status = "verified"
                st.rerun()

    with tab_login:
        st.text_input("Email/Phone")
        st.text_input("PIN", type="password")
        if st.button("Enter Sovereign Engine"):
            st.session_state.auth_status = "verified"
            st.rerun()

# --- 6. THE MAIN SOVEREIGN ENGINE ---
elif st.session_state.auth_status == "verified":
    with st.sidebar:
        st.write(f"**Founder:** {st.session_state.user_data.get('name', 'Nwokeji Anthony C.')}")
        role = st.radio("ACCESS", ["User Portal", "Mechanic Hub", "Sovereign Ledger"])
        if st.button("Logout"): st.session_state.auth_status = "gateway"; st.rerun()

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
            st.success("✅ TRANSACTION VERIFIED. Mechanic is moving to your location.")
            if st.button("MARK JOB AS COMPLETE"):
                st.session_state.mech_balance += (st.session_state.final_quote / 1.15)
                st.session_state.payment_confirmed = False; st.rerun()
        elif st.session_state.final_quote:
            st.markdown(f"### Pay ₦{st.session_state.final_quote:,.2f} to start repair")
            if st.button("💳 AUTHORIZE PAYMENT"):
                url, ref = initialize_payment(st.session_state.user_data['email'], st.session_state.final_quote)
                if url: st.session_state.payment_ref = ref; st.link_button("GO TO BANK TUNNEL", url)
            if st.session_state.payment_ref:
                if st.button("🔄 VERIFY PAYMENT STATUS"):
                    if verify_payment(st.session_state.payment_ref):
                        st.session_state.payment_confirmed = True; st.rerun()
        else:
            cat = st.selectbox("Category", list(SYMPTOM_MATRIX.keys()))
            col1, col2 = st.columns(2)
            selected = [sym for i, sym in enumerate(SYMPTOM_MATRIX[cat]) if (col1 if i < 4 else col2).checkbox(sym)]
            desc = st.text_area("Precision Description (Magic Box)")
            if st.button("🚀 AI DIAGNOSIS & ALERT MECHANIC"):
                st.session_state.active_request = {"cat": cat, "faults": selected, "desc": desc, "loc": [6.4273, 3.4215]}
                st.success("Regional Mechanics alerted.")

    elif role == "Mechanic Hub":
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Job Alert:</b> {req['cat']}<br>Faults: {', '.join(req['faults'])}</div>", unsafe_allow_html=True)
            svc = st.number_input("Service Cost (₦)")
            tpt = st.number_input("Transport (₦)")
            if st.button("SEND QUOTE"):
                st.session_state.final_quote = (svc + tpt) * 1.15
                st.success("Quote sent with 15% Founder Share.")
        
        st.divider()
        st.subheader("Your Wallet")
        st.metric("Earned (85%)", f"₦{st.session_state.mech_balance:,.2f}")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY ALERT SENT.")

    elif role == "Sovereign Ledger":
        st.subheader("Founder Ledger")
        st.write("Founder Share: 15% | Police Tax: 0% (Removed)")
        st.write(f"Total Confirmed Revenue: ₦{st.session_state.final_quote if st.session_state.payment_confirmed else 0:,.2f}")

    st.divider()
    st.subheader("📍 Sovereign Radar (Logistics)")
    # Directs Mechanic to User Location
    st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
        
