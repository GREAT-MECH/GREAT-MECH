import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. SOVEREIGN ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech | Operations", page_icon="🌍", layout="wide")

# --- 2. DATABASE SIMULATION (Operational Memory) ---
if 'job_registry' not in st.session_state:
    st.session_state.job_registry = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "User"

# --- 3. MASTER AESTHETIC ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #111 !important; border-right: 1px solid #D4AF37; }
    .main-title { text-align: center; font-size: 45px; font-weight: 900; color: #D4AF37; letter-spacing: 4px; }
    .receipt-card { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background: #000; margin-bottom: 10px; }
    .sos-trigger { display: block; text-align: center; background: #FF0000; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-decoration: none; border: 1px solid white; }
</style>
""", unsafe_allow_html=True)

# --- 4. FUNCTIONAL LOGIC ---
def process_payment(category, mechanic, price):
    """Executes the 15% split and saves the job to the registry."""
    founder_share = price * 0.15
    total_invoice = price + founder_share
    job_id = f"GM-{random_id()}"
    
    new_job = {
        "id": job_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category,
        "mechanic": mechanic,
        "base_price": price,
        "founder_share": founder_share,
        "total": total_invoice,
        "status": "Completed"
    }
    st.session_state.job_registry.append(new_job)
    return new_job

def random_id():
    return np.random.randint(10000, 99999)

# --- 5. INTERFACE MODULES ---
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
        user = st.text_input("Sovereign ID")
        key = st.text_input("Security Key", type="password")
        if st.button("AUTHORIZE"):
            if user == "founder" and key == "greatmech2026":
                st.session_state.authenticated = True
                st.session_state.user_role = "Founder"
                st.rerun()
            elif user and key:
                st.session_state.authenticated = True
                st.session_state.user_role = "User"
                st.rerun()

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:#D4AF37;'>COMMAND</h2>", unsafe_allow_html=True)
        menu = st.radio("GO TO:", ["🛠️ Request Mechanic", "📡 Radar", "🧾 Ledger", "📊 Founder Analytics"])
        st.divider()
        if st.button("End Session"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown('<a href="tel:911" class="sos-trigger">🆘 PANIC BUTTON</a>', unsafe_allow_html=True)
    return menu

# --- 6. MAIN RUNTIME ---
if not st.session_state.authenticated:
    login_screen()
else:
    choice = sidebar_nav()
    st.markdown(f"<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)

    if choice == "🛠️ Request Mechanic":
        st.subheader("Bargaining Terminal")
        with st.form("service_form"):
            cat = st.selectbox("Category", ["🚛 Truck", "🚗 Car", "⚙️ Diesel Engine", "📹 CCTV", "☀️ Solar"])
            mech = st.text_input("Mechanic Name/ID")
            price = st.number_input("Negotiated Amount ($)", min_value=0.0)
            submit = st.form_submit_button("LOCK PRICE & PAY")
            
            if submit and price > 0:
                receipt = process_payment(cat, mech, price)
                st.success(f"Success! Job {receipt['id']} is now live.")
                st.balloons()

    elif choice == "📡 Radar":
        st.subheader("Live Engineering Synchronization")
        st.map(pd.DataFrame(np.random.randn(5, 2) / [50, 50] + [6.5244, 3.3792], columns=['lat', 'lon']))

    elif choice == "🧾 Ledger":
        st.subheader("Transaction History")
        if not st.session_state.job_registry:
            st.write("No jobs processed yet.")
        for job in reversed(st.session_state.job_registry):
            with st.container():
                st.markdown(f"""
                <div class='receipt-card'>
                    <b>ID: {job['id']}</b> | {job['date']}<br>
                    Service: {job['category']} (Mech: {job['mechanic']})<br>
                    Founder Share: ${job['founder_share']:,.2f} | <b>Total: ${job['total']:,.2f}</b>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "📊 Founder Analytics":
        if st.session_state.user_role == "Founder":
            total_revenue = sum(j['founder_share'] for j in st.session_state.job_registry)
            st.metric("Total Platform Earnings (15%)", f"${total_revenue:,.2f}")
            st.write("Police Tax (2%): **WAIVED**")
            if st.session_state.job_registry:
                df = pd.DataFrame(st.session_state.job_registry)
                st.line_chart(df['founder_share'])
        else:
            st.error("Access Restricted to Founder.")

