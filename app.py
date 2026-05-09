import streamlit as st
import pandas as pd
import random
import folium
import re
import time
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & CSS ANIMATIONS ---
st.set_page_config(page_title="Great Mech Supreme", layout="wide", page_icon="🌍")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Animated Header: Letter by Letter */
    @keyframes typing { from { width: 0 } to { width: 100% } }
    .moving-africa {
        color: #D4AF37; font-size: 24px; font-weight: bold; overflow: hidden;
        white-space: nowrap; border-right: 3px solid #D4AF37;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        text-align: center; margin-bottom: 20px;
    }

    /* Animated Logo */
    @keyframes pulse { 0% { transform: scale(1); box-shadow: 0 0 20px #D4AF37; } 50% { transform: scale(1.1); box-shadow: 0 0 50px #D4AF37; } 100% { transform: scale(1); box-shadow: 0 0 20px #D4AF37; } }
    .africa-logo-anim {
        text-align: center; padding: 20px; border: 4px solid #D4AF37; border-radius: 50%;
        width: 120px; height: 120px; margin: 0 auto; font-size: 60px;
        background: black; animation: pulse 3s infinite ease-in-out;
    }

    /* Animated Ad Flip */
    @keyframes flip { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
    .ad-flip { animation: flip 1.5s ease-in-out; border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; background: #111; text-align: center; }

    .stButton>button { background: linear-gradient(45deg, #D4AF37, #AF8700); color: black !important; font-weight: bold; border-radius: 10px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE APP OPENER (MECHANIC ANIMATION) ---
if 'opener_played' not in st.session_state:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.write("🔧 **A Mechanic is approaching with his toolbox...**")
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    st.session_state.opener_played = True
    st.rerun()

# --- 3. HEADER ARCHITECTURE ---
st.markdown("<h1 style='text-align: center; color: white;'>GREAT MECH</h1>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level...</div>", unsafe_allow_html=True)

# --- 4. GLOBAL BANK & CITY DATA ---
bank_vault = {"Nigeria": ["Access", "GTB", "Zenith", "OPay", "Kuda"], "Kenya": ["Equity", "KCB", "M-Pesa"]}
cities = ["Lagos", "Abuja", "Port Harcourt", "Nairobi", "Accra", "Johannesburg"]

# --- 5. SECURE IDENTITY PORTAL (MODIFIED FOR ROLES) ---
if 'auth' not in st.session_state:
    st.session_state.update({'auth': False, 'role': None, 'phone': None})

if not st.session_state.auth:
    st.markdown("<div class='africa-logo-anim'>🌍</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        phone = st.text_input("Verified Phone Number")
        if st.button("AUTHORIZE"):
            if "+234000" in phone: st.session_state.role = "Founder" # Master Founder Key
            elif "8888" in phone: st.session_state.role = "Mechanic"
            else: st.session_state.role = "User"
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 6. ADVERTISING ENGINE (ANIMATED FLIPS) ---
parts = ["🛠️ Perkins Fuel Filter", "🔋 Luminous Solar Battery", "🚛 Heavy Duty Brake Pads", "📹 4K Night Vision CCTV"]
current_part = parts[int(time.time() % len(parts))]
st.markdown(f"<div class='ad-flip'><b>VENDOR SHOWCASE:</b> New stock of {current_part} arrived!</div>", unsafe_allow_html=True)

# --- 7. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)
master_db = conn.read(ttl=0)

# --- 8. ROLE-BASED DASHBOARDS ---

# FOUNDER: High-Level Insights
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND")
    # Highest Revenue Charts
    chart_data = pd.DataFrame({'City': cities, 'Revenue': [random.randint(50, 500)*1000 for _ in range(6)]})
    st.subheader("Highest Paying Revenue (By City)")
    st.bar_chart(chart_data.set_index('City'))
    
    m1, m2 = st.columns(2)
    m1.metric("Highest Country Income", "Nigeria (₦12.5M)")
    m2.metric("Founder 15% Share", f"₦{chart_data['Revenue'].sum() * 0.15:,.2f}")

# USER: Marketplace (FIXED BUDGET)
elif st.session_state.role == "User":
    st.title("📍 SERVICE MARKETPLACE")
    with st.form("request"):
        # Real Emojis for easy identification
        cat = st.selectbox("Category", ["🚛 Truck/Heavy Duty", "🏎️ Car/Sedan", "⚙️ Diesel Generator", "📹 CCTV Security", "☀️ Solar Power"])
        st.write("**Standard Service Fee: ₦10,000 (Non-Editable)**") # Fixed budget as requested
        loc = st.text_input("Your Exact Location")
        if st.form_submit_button("DEPLOY MECHANIC"):
            st.success("THANK YOU FOR USING GREAT MECH!")

# MECHANIC: Field Ops (MAP DIRECT)
elif st.session_state.role == "Mechanic":
    st.title("🔧 JOB RADAR")
    st.subheader("User Location & Navigation")
    # Map to direct mechanic to user
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=13)
    folium.Marker([6.5244, 3.3792], popup="User Site", icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width=700, height=300)
    
    st.subheader("Available Job Queue")
    st.dataframe(master_db[master_db['Status'] == "Pending"])

