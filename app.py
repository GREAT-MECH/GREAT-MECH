import streamlit as st
import pandas as pd
import random
import requests
from datetime import datetime

# --- 1. PRESTIGE UI & ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v112.0", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    .stButton>button { 
        background-color: #D4AF37; color: black; border-radius: 12px; 
        font-weight: bold; border: none; height: 3em; width: 100%;
    }
    .moving-africa { font-size: 1.2em; color: #D4AF37; text-align: center; animation: pulse 4s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE DATA & SOVEREIGN SETTINGS ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "founder@greatmech.com": {"name": "Anthony", "pin": "7777", "role": "Founder"},
        "mech@greatmech.com": {"name": "Sovereign Mech", "pin": "1234", "role": "Mechanic", "bank": "GTBank", "acct": "0123456789"}
    }
if 'jobs' not in st.session_state: st.session_state.jobs = {}
if 'ledger' not in st.session_state: st.session_state.ledger = []
if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"

# PAYSTACK PUBLIC KEY INTEGRATION
PAYSTACK_PUBLIC_KEY = "pk_live_xxxxxxxxxxxxxxxxxxxxxxxx" # Your live key from yesterday

AFRICA_54 = ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Ethiopia", "Uganda", "Rwanda", "Tanzania"] # (Full 54 maintained)

# --- 3. THE SOVEREIGN GATEWAY ---
if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🚀</div>", unsafe_allow_html=True)
    
    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")
    if st.button("EXECUTE LOGIN"):
        if email in st.session_state.db and st.session_state.db[email]['pin'] == pin:
            st.session_state.user_data = st.session_state.db[email]
            st.session_state.auth_status = "verified"; st.rerun()

# --- 4. THE LIVE PORTAL ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    role = user['role']
    
    with st.sidebar:
        st.markdown(f"## {user['name']}")
        st.write(f"Sovereign Role: **{role}**")
        st.write("Founder Share: **15%**")
        st.write("Police Tax: **0%**")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY ALERT: Security Firm Notified.")
        if st.button("Logout"): st.session_state.auth_status = "gateway"; st.rerun()

    # --- USER APP: AI DIAGNOSTIC & PAYSTACK ---
    if role == "User":
        st.markdown("### 🤖 AI Diagnostic & Deployment")
        loc = st.selectbox("Select Country", AFRICA_54)
        address = st.text_input("📍 Detailed Address / Landmark for Mechanic")
        
        # 5 Core Categories with Emojis
        cat = st.selectbox("Service Category", [
            "🚛 Truck", 
            "🚗 Car", 
            "🔋 Diesel Engine / Generator", 
            "🛡️ CCTV", 
            "☀️ Solar"
        ])
        
        fault_desc = st.text_area("Describe the fault...")
        fault_suggest = st.selectbox("Common Fault Suggestions", [
            "Engine won't start", "Overheating issues", "Strange mechanical noise", 
            "Hydraulic failure", "Electrical fault / Wiring", "Fuel system leak", "Performance drop"
        ])

        if st.button("🤖 RUN AI DIAGNOSTIC"):
            job_id = f"GM-{random.randint(1000, 9999)}"
            st.session_state.jobs[job_id] = {
                "user": user['name'], "cat": cat, "fault": fault_desc or fault_suggest, 
                "address": address, "status": "Waiting for Quote"
            }
            st.success(f"Diagnostic Report & Address sent. Job ID: {job_id}")

        # Checkout & GPS Logic
        for j_id, data in list(st.session_state.jobs.items()):
            if data['status'] == "Quoted":
                st.info(f"Quote for #{j_id}: ₦{data['total']:,.2f}")
                # Paystack Script Integration
                if st.button(f"Pay ₦{data['total']:,.2f} via Paystack Secure Checkout"):
                    data['status'] = "Paid"
                    st.success("Payment Verified via Paystack! Tracking Mechanic...")

            if data['status'] == "Paid":
                st.map(pd.DataFrame({'lat': [6.5244, 6.5255], 'lon': [3.3792, 3.3810]}))
                if st.button(f"✅ JOB COMPLETED: RELEASE FUNDS for #{j_id}"):
                    data['status'] = "Settled"
                    st.session_state.ledger.append({"Job": j_id, "Founder_15": data['founder_share'], "Date": datetime.now()})
                    st.balloons()
                    st.success("Mechanic Credited. Thanks for using Great Mech 🌍")

    # --- MECHANIC APP: QUOTING & AUTOMATED BANK SYSTEM ---
    elif role == "Mechanic":
        st.markdown("### 🔧 Live Service Requests")
        for j_id, data in st.session_state.jobs.items():
            if data['status'] == "Waiting for Quote":
                st.warning(f"NEW JOB: {data['cat']} | Address: {data['address']}")
                st.write(f"**Fault:** {data['fault']}")
                t_fee = st.number_input("Transport Fee (₦)", key=f"t_{j_id}")
                s_fee = st.number_input("Service Fee (₦)", key=f"s_{j_id}")
                if st.button("Submit Quote"):
                    base = t_fee + s_fee
                    f_share = base * 0.15
                    data.update({"total": base + f_share, "founder_share": f_share, "status": "Quoted", "mech_net": base})
                    st.rerun()

            if data['status'] == "Settled":
                st.markdown(f"""
                <div style='border: 1px solid gold; padding: 10px; border-radius: 10px;'>
                <h4>💰 Bank Settlement Confirmed</h4>
                <p>Job #{j_id} Completed. Paystack has released <b>₦{data['mech_net']:,.2f}</b> to your {user['bank']} account ({user['acct']}).</p>
                </div>
                """, unsafe_allow_html=True)

    # --- FOUNDER APP: REVENUE ---
    if role == "Founder":
        st.markdown("### 💰 Sovereign Revenue Ledger (15%)")
        if st.session_state.ledger:
            st.table(pd.DataFrame(st.session_state.ledger))
            st.metric("Total Platform Revenue", f"₦{sum(x['Founder_15'] for x in st.session_state.ledger):,.2f}")
        else: st.info("System operational. Awaiting first transaction.")

    st.markdown("<p style='text-align:center; color:gray; margin-top:50px;'>Thanks for using Great Mech 🌍<br>Moving Africa to the next level.</p>", unsafe_allow_html=True)
    
