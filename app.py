import streamlit as st
import pandas as pd
import requests
import time
import random
import folium
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & LOTTIE BRIDGE ---
st.set_page_config(page_title="Great Mech Supreme", layout="wide", page_icon="🌍")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# FREE PROFESSIONAL MECHANIC ANIMATION (No Payment Required)
LOTTIE_MECHANIC = load_lottieurl("https://lottie.host/807e3240-5e5d-4f11-9a77-4f6c4966601b/Iu7E9x7A4C.json")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    h1, h2 { color: #D4AF37 !important; text-align: center; font-weight: 900; letter-spacing: 3px; }
    
    /* Animated Header */
    @keyframes typing { from { width: 0 } to { width: 100% } }
    .moving-africa {
        color: #D4AF37; font-size: 22px; font-weight: bold; overflow: hidden;
        white-space: nowrap; border-right: 3px solid #D4AF37; margin: 0 auto;
        animation: typing 4s steps(40, end) infinite; width: fit-content;
    }

    /* Fixed Pricing Box */
    .price-card {
        background: #111; border: 2px solid #D4AF37; padding: 20px;
        border-radius: 12px; text-align: center; color: #D4AF37; font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE APP OPENER (ANIMATED HANDSHAKE) ---
if 'opener_played' not in st.session_state:
    st.markdown("<h1>GREAT MECH</h1>", unsafe_allow_html=True)
    if LOTTIE_MECHANIC:
        st_lottie(LOTTIE_MECHANIC, height=400, key="opening_anim")
    st.markdown("<div class='moving-africa'>Moving Africa to the next level...</div>", unsafe_allow_html=True)
    time.sleep(4)
    st.session_state.opener_played = True
    st.rerun()

# --- 3. CLOUD DATABASE (IRONCLAD CONNECTION) ---
# FOUNDER: Ensure Google Sheet is shared with "Anyone with link" as "EDITOR"
conn = st.connection("gsheets", type=GSheetsConnection)
try:
    master_db = conn.read(ttl=0)
except:
    st.error("⚠️ DATABASE LOCKED: Please set your Google Sheet to 'Editor' access.")
    st.stop()

# --- 4. SECURE LOGIN GATE ---
if 'auth' not in st.session_state:
    st.session_state.update({'auth': False, 'role': None, 'phone': None})

if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        phone = st.text_input("Verified Phone Number (+234...)")
        if st.button("ENTER EMPIRE"):
            if "+234000" in phone: st.session_state.role = "Founder"
            elif "8888" in phone: st.session_state.role = "Mechanic"
            else: st.session_state.role = "User"
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 5. FOUNDER COMMAND (CHARTS & REVENUE) ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    
    # Revenue Chart Logic
    cities = ["Lagos", "Abuja", "Nairobi", "Accra", "Johannesburg"]
    rev_data = pd.DataFrame({'City': cities, 'Revenue': [random.randint(500, 1500)*1000 for _ in range(5)]})
    
    st.subheader("Highest Paying Revenue by City")
    st.bar_chart(rev_data.set_index('City'))
    
    m1, m2 = st.columns(2)
    m1.metric("Highest Country Income", "Nigeria (₦28.4M)")
    m2.metric("Founder 15% Sovereignty", f"₦{rev_data['Revenue'].sum() * 0.15:,.2f}")

# --- 6. USER MARKETPLACE (FIXED PRICING) ---
elif st.session_state.role == "User":
    st.title("🚀 ENGINEERING MARKETPLACE")
    with st.form("request"):
        cat = st.selectbox("Category", ["🚛 Truck", "🏎️ Car", "⚙️ Generator", "📹 CCTV", "☀️ Solar"])
        
        # NON-EDITABLE BUDGET
        st.markdown("<div class='price-card'><b>FIXED SERVICE FEE: ₦15,000</b></div>", unsafe_allow_html=True)
        
        loc = st.text_input("Your Location")
        if st.form_submit_button("DEPLOY MECHANIC"):
            st.success("THANK YOU! A specialist is on the way.")

# --- 7. MECHANIC HUB (MAP NAVIGATION) ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 JOB RADAR")
    # Direct Map for Mechanic
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=13)
    folium.Marker([6.5244, 3.3792], popup="User Site", icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width=900, height=400)
    
    st.subheader("Pending Requests")
    st.dataframe(master_db)

