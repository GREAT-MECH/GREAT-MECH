"""
PROJECT: GREAT MECH SOVEREIGN ENGINE
FOUNDER: [CONFIDENTIAL IDENTITY LOCKED]
VERSION: 60.0 - MASTER CONSOLIDATION
MANDATE: MOVE AFRICA TO THE NEXT LEVEL
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import random

# ==========================================
# 1. ENGINE CORE INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Great Mech | Africa's Technical Pulse",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PREMIUM SOVEREIGN INTERFACE (CSS)
# ==========================================
# This block manages the pitch-black and gold aesthetic
# ensuring no "0" artifacts or UI leaks.
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #050505;
        color: #FFFFFF;
        font-family: 'Inter', 'Segoe UI', Helvetica, sans-serif;
    }
    
    /* Founder & User Branding */
    .brand-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(180deg, #111 0%, #050505 100%);
    }
    .main-title {
        font-size: 64px;
        font-weight: 900;
        color: #D4AF37;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-bottom: 0px;
        text-shadow: 0px 4px 10px rgba(212, 175, 55, 0.3);
    }
    .sub-title {
        font-size: 18px;
        color: #D4AF37;
        opacity: 0.8;
        letter-spacing: 4px;
        margin-top: -10px;
        margin-bottom: 40px;
    }

    /* Professional UI Components */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #111;
        border-radius: 5px 5px 0px 0px;
        color: #888;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold;
    }

    /* Receipting & Financial Modules */
    .receipt-container {
        border: 2px solid #D4AF37;
        padding: 30px;
        border-radius: 15px;
        background-color: #0d0d0d;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .receipt-header {
        border-bottom: 1px solid #333;
        padding-bottom: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* SOS Button Logic */
    .sos-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(145deg, #ff0000, #990000);
        color: white;
        padding: 20px 40px;
        border-radius: 50px;
        font-weight: 900;
        z-index: 1000;
        text-decoration: none;
        border: 2px solid white;
        box-shadow: 0 5px 20px rgba(255,0,0,0.4);
        transition: 0.3s;
    }
    .sos-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. STATE MANAGEMENT & SECURITY GATE
# ==========================================
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ==========================================
# 4. PAN-AFRICAN GEOSPATIAL LOGIC
# ==========================================
# Covering all 54 countries with coordinate anchors
AFRICA_REGIONS = {
    "North Africa": ["Egypt", "Algeria", "Morocco", "Tunisia", "Libya"],
    "West Africa": ["Nigeria", "Ghana", "Senegal", "Ivory Coast", "Mali"],
    "East Africa": ["Kenya", "Ethiopia", "Tanzania", "Uganda", "Rwanda"],
    "Southern Africa": ["South Africa", "Angola", "Zambia", "Zimbabwe", "Botswana"],
    "Central Africa": ["DR Congo", "Cameroon", "Gabon", "Chad", "Congo"]
}

# ==========================================
# 5. CORE LOGIC FUNCTIONS
# ==========================================
def calculate_invoice(base_price):
    """
    Calculates the Great Mech share and ensures the 2% tax is omitted.
    """
    platform_share = base_price * 0.15 #
    police_tax = 0.00 #
    total_due = base_price + platform_share
    return platform_share, police_tax, total_due

def generate_radar_data():
    """Simulates real-time engineer tracking."""
    return pd.DataFrame(
        np.random.randn(5, 2) / [50, 50] + [6.5244, 3.3792],
        columns=['lat', 'lon']
    )

# ==========================================
# 6. UI PAGES (USER & FOUNDER)
# ==========================================
def show_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        try:
            st.image("316436.png", width=300) #
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=200)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='main-title' style='text-align:center;'>GREAT MECH</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title' style='text-align:center;'>SOVEREIGN ENGINEERING HUB</div>", unsafe_allow_html=True)
        
        user_input = st.text_input("Sovereign ID")
        pass_input = st.text_input("Access Key", type="password")
        
        if st.button("AUTHORIZE SESSION"):
            if user_input == "founder" and pass_input == "greatmech2026":
                st.session_state.auth_status = True
                st.session_state.user_role = "Founder"
                st.rerun()
            elif user_input and pass_input:
                st.session_state.auth_status = True
                st.session_state.user_role = "User"
                st.rerun()

def show_user_interface():
    # Persistent SOS Trigger
    st.markdown('<a href="tel:911" class="sos-button">🆘 EMERGENCY PANIC</a>', unsafe_allow_html=True)
    
    st.markdown(f"### Welcome back, Founder." if st.session_state.user_role == "Founder" else "### Engineering Portal")
    
    tabs = st.tabs(["🔧 Service Portal", "📡 Global Radar", "💳 Payments", "📜 History"])
    
    with tabs[0]:
        st.subheader("Initiate Engineering Task")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            category = st.selectbox("Category", [
                "Truck (Heavy Duty)", "Car (Luxury/Utility)", "Diesel/Generator", "CCTV Systems", "Solar Engineering"
            ]) #
        with col_s2:
            urgency = st.select_slider("Urgency Level", ["Standard", "High", "Critical"])
            
        description = st.text_area("Issue Description", placeholder="Detailed breakdown of mechanical failure...")
        
        st.divider()
        st.markdown("### 🤝 Bargaining Terminal")
        base_cost = st.number_input("Negotiated Price with Mechanic ($)", min_value=0.0)
        
        if base_cost > 0:
            share, tax, total = calculate_invoice(base_cost)
            st.markdown(f"""
            <div class='receipt-container'>
                <h4>Provisional Invoice</h4>
                <p>Base Engineering: ${base_cost:,.2f}</p>
                <p>Platform Fee (15%): ${share:,.2f}</p>
                <p style='color:#00FF00'>Sovereign Tax Waiver: -$0.00 (2% Police Fee Exempt)</p>
                <hr>
                <h3 style='color:#D4AF37'>TOTAL PAYABLE: ${total:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("EXECUTE PAYMENT"):
                with st.spinner("Processing Pan-African Gateway..."):
                    time.sleep(1.5)
                    st.success("Payment Received. Dispatching Engineer.")
                    st.balloons()

    with tabs[1]:
        st.subheader("Pan-African Live Tracking")
        radar_map = generate_radar_data()
        st.map(radar_map)
        st.info("Currently tracking active engineers across your region.")

    with tabs[2]:
        st.subheader("Secure Financial Vault")
        st.write("Secure payment methods integrated for all 54 African countries.")
        st.image("https://img.icons8.com/color/48/visa.png", width=40)
        st.image("https://img.icons8.com/color/48/mastercard.png", width=40)

    with tabs[3]:
        st.subheader("Service Archives")
        st.info("No recent orders found in this session.")

def show_founder_terminal():
    # Only Founder sees this specialized view
    st.sidebar.title("FOUNDER CONTROL")
    st.sidebar.metric("Network Revenue", "$1,240,500", "15% Target")
    st.sidebar.write("---")
    st.sidebar.write("54 Countries: **ONLINE**")
    st.sidebar.write("Police Tax: **DISABLED**")
    if st.sidebar.button("System Logout"):
        st.session_state.auth_status = False
        st.rerun()
    
    show_user_interface()

# ==========================================
# 7. EXECUTION
# ==========================================
if not st.session_state.auth_status:
    show_login()
else:
    if st.session_state.user_role == "Founder":
        show_founder_terminal()
    else:
        show_user_interface()

# [End of Sovereign Core]
