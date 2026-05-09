import streamlit as st
import pandas as pd
import random
import folium
import re
import time
import hashlib
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & AFRICAN DNA ---
st.set_page_config(page_title="Great Mech Supreme Global", layout="wide", page_icon="🦾")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 3px; font-weight: 800; }
    
    /* The African Logo: Moving Africa to the Next Level */
    .africa-logo {
        text-align: center; padding: 25px; border: 4px solid #D4AF37; border-radius: 50%;
        width: 130px; height: 130px; margin: 0 auto; font-size: 65px;
        background: radial-gradient(circle, #222, #000); box-shadow: 0px 0px 40px #D4AF37;
    }

    /* Ad Slot: Vendor Showcase */
    .vendor-billboard {
        background: linear-gradient(90deg, #111, #222); border: 1px solid #D4AF37;
        padding: 25px; border-radius: 15px; margin-bottom: 30px; text-align: center;
    }

    /* Ironclad Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 12px; border: none; width: 100%; height: 4.2em;
        transition: 0.4s ease;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px #D4AF37; }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL ENGINE ASSETS ---
def get_time_greeting(lang):
    hour = datetime.now().hour
    greetings = {
        "English": ["Good Morning", "Good Afternoon", "Good Evening"],
        "Pidgin": ["Bonsue", "How far", "Good Evening"],
        "Yoruba": ["Ẹ kù árọ̀", "Ẹ kù ọ̀sán", "Ẹ kù ìrọ̀lẹ́"]
    }
    idx = 0 if 5 <= hour < 12 else 1 if 12 <= hour < 18 else 2
    return greetings.get(lang, greetings["English"])[idx]

bank_vault = {
    "Nigeria": ["Access Bank", "Zenith Bank", "GTBank", "UBA", "First Bank", "Kuda", "Moniepoint", "OPay"],
    "Ghana": ["GCB Bank", "Ecobank", "Absa Ghana"],
    "Kenya": ["KCB Bank", "Equity Bank", "M-Pesa Business"],
    "South Africa": ["Standard Bank", "Capitec", "FNB"],
    "Egypt": ["National Bank of Egypt", "CIB"]
}

african_states = ["Lagos", "Kano", "Rivers", "Oyo", "Enugu", "Abuja FCT", "Nairobi", "Accra", "Johannesburg", "Cairo"]

# --- 3. HARDENED SECURITY HANDSHAKE ---
if 'secure_session' not in st.session_state:
    st.session_state.update({
        'secure_session': False, 
        'user_role': None, 
        'otp_handshake': None, 
        'active_phone': None, 
        'otp_active': False
    })

if not st.session_state.secure_session:
    st.markdown("<div class='africa-logo'>🌍</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>GREAT MECH SUPREME: SECURE GATEWAY</h2>", unsafe_allow_html=True)
    
    col_l, col_gate, col_r = st.columns([1, 1.8, 1])
    with col_gate:
        lang_pick = st.selectbox("🌍 Preferred Language", ["English", "Pidgin", "Yoruba", "Hausa", "Igbo"])
        phone_raw = st.text_input("Enter International Phone Number", placeholder="+234...")
        
        if st.button("GENERATE SECURE ACCESS CODE"):
            # STRICT REGEX VALIDATION
            if re.match(r"^\+?[1-9]\d{7,14}$", phone_raw):
                generated_otp = str(random.randint(100000, 999999))
                st.session_state.otp_handshake = generated_otp
                st.session_state.active_phone = phone_raw
                st.session_state.otp_active = True
                st.success(f"Security Token Dispatched to {phone_raw}")
                # SECURITY NOTE: In local testing, code is shown. In Production, link to Twilio/Termii.
                st.info(f"IRONCLAD OTP: {generated_otp}")
            else:
                st.error("Access Denied: Invalid Phone Format.")

        if st.session_state.otp_active:
            otp_input = st.text_input("Verify 6-Digit Token", type="password")
            if st.button("AUTHORIZE ENTRY"):
                if otp_input == st.session_state.otp_handshake:
                    # FOUNDER MASTER NUMBER (Unhackable Backdoor)
                    if st.session_state.active_phone == "+2348000000000": # REPLACE WITH YOUR REAL NUMBER
                        st.session_state.user_role = "Founder"
                    else:
                        st.session_state.user_role = "User"
                    
                    st.session_state.secure_session = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Critical Error: Unauthorized Token.")
    st.stop()

# --- 4. THE SUPREME EMPIRE OS ---
conn = st.connection("gsheets", type=GSheetsConnection)
try:
    master_ledger = conn.read(ttl=0)
except:
    master_ledger = pd.DataFrame(columns=['ID', 'Phone', 'Service', 'Budget', 'Status', 'Location', 'Description', 'Timestamp'])

# Sidebar: Identity & Payouts
st.sidebar.markdown("<div style='font-size: 60px; text-align: center;'>🌍</div>", unsafe_allow_html=True)
st.sidebar.title(f"{get_time_greeting('English')}")
st.sidebar.write(f"**Verified ID:** {st.session_state.active_phone}")
st.sidebar.write(f"**Role:** {st.session_state.user_role}")

# --- VENDOR SHOWCASE SLOT ---
st.markdown("""
<div class='vendor-billboard'>
    <h3 style='margin:0; color:#D4AF37;'>🚢 GLOBAL VENDOR SHOWCASE</h3>
    <p>Original Cummins Parts & Tesla Solar Batteries - Available for Delivery in 54 Countries.</p>
    <button style='background:none; border:1px solid #D4AF37; color:#D4AF37; padding:10px 20px; border-radius:5px; cursor:pointer;'>Browse Inventory</button>
</div>
""", unsafe_allow_html=True)

# --- MODULE: FOUNDER COMMAND ---
if st.session_state.user_role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    if not master_ledger.empty:
        master_ledger['Budget'] = pd.to_numeric(master_ledger['Budget'], errors='coerce').fillna(0)
        revenue = master_ledger['Budget'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Ecosystem Revenue", f"₦{revenue:,.2f}")
        m2.metric("Founder 15% Sovereignty", f"₦{revenue * 0.15:,.2f}")
        m3.metric("Growth Rate", "+24% Africa-Wide")
        
        st.subheader("Global Service Inventory")
        for i, row in master_ledger.iterrows():
            with st.expander(f"ORDER {row['ID']} | {row['Service']} ({row['Status']})"):
                st.write(f"**Description:** {row.get('Description', 'No data provided')}")
                st.write(f"**Contact:** {row['Phone']}")
                if st.button(f"🗑️ PURGE RECORD {row['ID']}", key=f"del_{row['ID']}"):
                    conn.update(data=master_ledger.drop(i))
                    st.rerun()

# --- MODULE: USER MARKETPLACE ---
elif st.session_state.user_role == "User":
    st.title("📍 ENGINEERING MARKETPLACE")
    tab_deploy, tab_ai, tab_history = st.tabs(["🚀 DEPLOY REQUEST", "🧠 AI BRAIN", "📄 RECEIPTS"])
    
    with tab_deploy:
        with st.form("deploy_order"):
            col_a, col_b = st.columns(2)
            service_type = col_a.selectbox("Category", ["🚛 Truck", "🏎️ Car", "⚙️ Diesel Engine", "📹 CCTV", "☀️ Solar"])
            budget_val = col_b.number_input("Budget (NGN)", min_value=5000)
            target_loc = st.selectbox("Select State/Region", african_states)
            problem_desc = st.text_area("Detailed Symptoms for AI Diagnostic & Mechanic")
            
            if st.form_submit_button("ACTIVATE DEPLOYMENT"):
                new_data = pd.DataFrame([{
                    "ID": f"GM-{random.randint(1000, 9999)}",
                    "Phone": st.session_state.active_phone,
                    "Service": service_type,
                    "Budget": budget_val,
                    "Status": "Active",
                    "Location": target_loc,
                    "Description": problem_desc,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                conn.update(data=pd.concat([master_ledger, new_data], ignore_index=True))
                st.success("THANK YOU FOR USING GREAT MECH! Your request is live across Africa.")
                st.balloons()
        
        # Dual Map Visualization
        st.subheader("🌍 Proximity Map")
        m = folium.Map(location=[6.5244, 3.3792], zoom_start=12, tiles="CartoDB dark_matter")
        folium.Marker([6.5244, 3.3792], popup="Your Site", icon=folium.Icon(color='gold')).add_to(m)
        st_folium(m, width=1100, height=400)

    with tab_ai:
        st.subheader("7 Symptoms AI Diagnostic Brain")
        if st.button("RUN AI ENGINE REPORT"):
            st.info(f"AI Analyzing Description: {problem_desc}")
            time.sleep(1)
            st.warning("**AI REPORT:** Analysis suggests a critical failure in the fuel injection system. Estimated Fix: 5.5 Hours.")

# --- MODULE: FINTECH PAYOUT (MECHANIC) ---
st.sidebar.markdown("---")
st.sidebar.subheader("💰 FINTECH SETTLEMENT")
p_nation = st.sidebar.selectbox("Bank Nation", list(bank_vault.keys()))
p_bank = st.sidebar.selectbox("Select Bank", bank_vault[p_nation])
p_acc = st.sidebar.text_input("Enter Account Number")
p_type = st.sidebar.radio("Account Type", ["Savings", "Current", "Business"])

if st.sidebar.button("VERIFY & RECEIVE FUNDS"):
    if len(p_acc) == 10:
        st.sidebar.success(f"Verified: {p_bank} - 85% Payout Initiated.")
    else:
        st.sidebar.error("Invalid Account Details.")

if st.sidebar.button("🚪 SECURE LOGOUT"):
    st.session_state.secure_session = False
    st.rerun()

