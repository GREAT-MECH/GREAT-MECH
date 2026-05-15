import streamlit as st
import time

# ============================================================================
# GREAT MECH v70 - THE SOVEREIGN RESTORATION
# ============================================================================

st.set_page_config(page_title="Great Mech v70", page_icon="🌍", layout="wide")

# Black & Gold Prestige UI
st.markdown("""
    <style>
    .main { background-color: #050505; color: #d4af37; }
    .stApp { background-color: #050505; }
    h1, h2, h3 { color: #d4af37; font-family: 'Playfair Display', serif; text-align: center; }
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #aa8c2c); 
        color: black; font-weight: bold; border: none; border-radius: 5px;
    }
    .panic-btn>button { background: red !important; color: white !important; }
    .diag-box { border: 1px solid #d4af37; padding: 20px; border-radius: 10px; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ============================================================================
# CORE LOGIC: REVENUE & DIAGNOSTICS
# ============================================================================
FOUNDER_ACCOUNT = "Restricted: Founder's Vault"
FOUNDER_SHARE = 0.15
POLICE_FEE = 0.00 # Strictly 0%

FAULT_DATABASE = {
    "Truck Services": ["Transmission slipping", "Air brake failure", "Turbocharger lag", "Axle misalignment", "Engine overheating", "Fuel injector clog", "Hydraulic leak"],
    "Car Services": ["Check engine light", "Brake pad wear", "Suspension noise", "Battery drain", "Alternator failure", "AC cooling issue", "Transmission jerk"],
    "Diesel Engine/Generator": ["White smoke", "Hard starting", "Low oil pressure", "Governor hunting", "Coolant leak", "Fuel contamination", "Vibration issues"],
    "CCTV Systems": ["Video signal loss", "Night vision failure", "DVR storage error", "PTZ motor jam", "Power supply surge", "Network timeout", "Blurry lens"],
    "Solar Solutions": ["Inverter fault", "Battery bank drain", "Charge controller error", "Panel shading loss", "Ground fault", "Loose DC wiring", "Efficiency drop"]
}

# ============================================================================
### LOGIN SYSTEM
# ============================================================================
if not st.session_state.logged_in:
    st.title("GREAT MECH v70 LOGIN")
    with st.container():
        user = st.text_input("Founder/Mechanic ID")
        pin = st.text_input("Secure PIN", type="password")
        if st.button("Access Engine"):
            if pin: # Add specific logic here later
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# ============================================================================
### MAIN INTERFACE
# ============================================================================
st.title("GREAT MECH SUPREME ENGINE v70 🌍")
st.sidebar.markdown("### FOUNDER CONTROL")
menu = st.sidebar.radio("Navigation", ["AI Diagnostic Hub", "Emergency Panic Center", "Founder Revenue"])

if menu == "AI Diagnostic Hub":
    st.write("### ⚙️ 5 Core Engineering Verticals")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1: st.button("🚚 Truck")
    with col2: st.button("🚗 Car")
    with col3: st.button("⚙️ Diesel")
    with col4: st.button("📹 CCTV")
    with col5: st.button("☀️ Solar")

    st.markdown("---")
    category = st.selectbox("Select System for AI Diagnosis", list(FAULT_DATABASE.keys()))
    
    st.write("#### 🧠 AI Diagnostic Button")
    if st.button("Run Engineering Scan"):
        with st.spinner("Analyzing African Engineering Magic..."):
            time.sleep(2)
            st.success(f"Scan Complete for {category}")
            st.write("**Top 7 Potential Faults Detected:**")
            for fault in FAULT_DATABASE[category]:
                st.markdown(f"- {fault}")

elif menu == "Emergency Panic Center":
    st.write("### 🚨 Mechanic On-Site Protection")
    st.info("Emergency alerts go directly to Private Security. Police payment is 0%.")
    if st.button("🚨 TRIGGER PANIC BUTTON", help="Emergency Dispatch Only"):
        st.error("!!! ALERT SENT !!! Private Security is tracking your GPS. Stay safe.")

elif menu == "Founder Revenue":
    st.write("### 💰 Founder's Vault")
    amount = st.number_input("Total Service Invoice", min_value=0.0)
    f_cut = amount * FOUNDER_SHARE
    m_cut = amount - f_cut
    
    st.metric("Founder Earnings (15%)", f"{f_cut:.2f}")
    st.metric("Police/Security Fee", "0.00")
    st.write(f"**Action:** Payout of {f_cut:.2f} routed to {FOUNDER_ACCOUNT}")
    st.caption("Moving Africa to the next level, one invoice at a time.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    
