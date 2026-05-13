import streamlit as st
import pandas as pd
import requests
import time

# --- 1. SOVEREIGN IDENTITY & LIVE KEYS ---
# Hard-coded from verified file 320313.png for Live Production
LIVE_SECRET_KEY = "sk_live_5d70f03c20eea14b71be5b" 

st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# --- 2. THE FOUNDER'S STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; color: #D4AF37; } 100% { opacity: 0.5; } }
    .moving-africa { text-align: center; font-size: 14px; font-weight: bold; letter-spacing: 3px; animation: pulse 3s infinite; margin-bottom: 20px; }
    .main-title { text-align: center; font-size: 50px; font-weight: 900; color: #D4AF37; margin-bottom: 0px; }
    .panic-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; border-radius: 50px; }
    .card { border: 1px solid #D4AF37; padding: 20px; background: #111; border-radius: 10px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LIVE BANKING & PAYOUT CORE ---
def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        res = response.json()
        return res.get('status') and res['data']['status'] == 'success'
    except: return False

def initialize_paystack_payment(email, amount_ngn):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}", "Content-Type": "application/json"}
    ref = f"GM-{int(time.time())}"
    payload = {
        "email": email, "amount": int(float(amount_ngn) * 100), "currency": "NGN",
        "reference": ref, "callback_url": "https://greatmech.streamlit.app",
        "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        return (res_data['data']['authorization_url'], ref) if res_data.get('status') else (None, None)
    except: return None, None

def get_banks(country_code="NG"):
    url = f"https://api.paystack.co/bank?country={country_code}"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        return {bank['name']: bank['code'] for bank in response.json()['data']}
    except: return {"Manual Entry": "000"}

def create_recipient(name, account, b_code):
    url = "https://api.paystack.co/transferrecipient"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}", "Content-Type": "application/json"}
    payload = {"type": "nuban", "name": name, "account_number": account, "bank_code": b_code, "currency": "NGN"}
    res = requests.post(url, json=payload, headers=headers).json()
    return res['data']['recipient_code'] if res.get('status') else None

def send_payout(amount, r_code):
    url = "https://api.paystack.co/transfer"
    headers = {"Authorization": f"Bearer {LIVE_SECRET_KEY}", "Content-Type": "application/json"}
    payload = {"source": "balance", "amount": int(float(amount) * 100), "recipient": r_code, "reason": "GM Job Payout"}
    return requests.post(url, json=payload, headers=headers).json().get('status')

# --- 4. STATE MANAGEMENT ---
if 'payment_ref' not in st.session_state: st.session_state.payment_ref = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'final_quote' not in st.session_state: st.session_state.final_quote = None
if 'mech_balance' not in st.session_state: st.session_state.mech_balance = 0.0

# --- 5. INTERFACE ---
st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Sovereign Control")
    category = st.selectbox("CATEGORY", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
    role = st.radio("ACCESS", ["User Portal", "Mechanic Hub", "Sovereign Ledger"])
    st.divider()
    st.write("Founder: Nwokeji Anthony C.") #
    st.write("Engine: LIVE 🟢")

# --- 6. LOGIC PORTALS ---
if role == "User Portal":
    if st.session_state.payment_confirmed:
        st.success("✅ TRANSACTION VERIFIED. Dispatching Elite Mechanic.")
        if st.button("MARK JOB AS COMPLETE"):
            earned = st.session_state.final_quote / 1.15
            st.session_state.mech_balance += earned
            st.session_state.payment_confirmed = False
            st.rerun()
    elif st.session_state.final_quote:
        st.markdown(f"### Total Service Fee: ₦{st.session_state.final_quote:,.2f}")
        if st.button("💳 PAY VIA SOVEREIGN GATEWAY"):
            url, ref = initialize_paystack_payment("client@greatmech.africa", st.session_state.final_quote)
            if url:
                st.session_state.payment_ref = ref
                st.link_button("OPEN SECURE BANKING TUNNEL", url)
        if st.session_state.payment_ref:
            if st.button("🔄 VERIFY PAYMENT"):
                if verify_payment(st.session_state.payment_ref):
                    st.session_state.payment_confirmed = True
                    st.rerun()
    else:
        st.subheader(f"Engineering Diagnosis: {category}")
        st.button("🚀 REQUEST ELITE DISPATCH")

elif role == "Mechanic Hub":
    st.subheader("Your Sovereign Wallet")
    st.metric("Earned (85%)", f"₦{st.session_state.mech_balance:,.2f}")
    
    with st.expander("🏦 Link African Bank Account"):
        country = st.selectbox("Country", ["Nigeria", "Ghana", "Kenya"])
        bank_dict = get_banks("NG" if country == "Nigeria" else "GH")
        sel_bank = st.selectbox("Select Bank", list(bank_dict.keys()))
        acc_num = st.text_input("Account Number")
        if st.button("Link Account"):
            r_id = create_recipient("Mechanic", acc_num, bank_dict[sel_bank])
            if r_id: st.session_state.r_id = r_id; st.success("Account Linked.")

    if st.session_state.mech_balance > 0:
        if st.button("💸 WITHDRAW EARNINGS"):
            if send_payout(st.session_state.mech_balance, st.session_state.get('r_id')):
                st.success("Payout Initiated!"); st.session_state.mech_balance = 0.0

    st.divider()
    if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY ALERT: Private Security Dispatched.") #

elif role == "Sovereign Ledger":
    st.subheader("Founder Financials")
    rev = st.session_state.final_quote if st.session_state.payment_confirmed else 0.0
    st.write(f"Total Revenue: ₦{rev:,.2f}")
    st.write(f"Founder Net (15%): ₦{rev - (rev/1.15) if rev > 0 else 0:,.2f}") #
    st.write("Police Tax (2%): 0% (Banned)") #

st.divider()
st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon'])) #
        
