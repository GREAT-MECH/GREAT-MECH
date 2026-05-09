import streamlit as st
import pandas as pd
import requests
import time
import random
import folium
from datetime import datetime

# --- 1. ENGINE PART CHECK ---
try:
    from streamlit_lottie import st_lottie
    from streamlit_folium import st_folium
    from streamlit_gsheets import GSheetsConnection
    PARTS_OK = True
except ImportError:
    PARTS_OK = False

# --- 2. SUPREME BRANDING ---
st.set_page_config(page_title="Great Mech Supreme", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-title { text-align: center; font-size: 50px; font-weight: 900; color: white; margin-bottom: 0; }
    
    @keyframes typing { from { width: 0 } to { width: 100% } }
    .moving-africa {
        color: #D4AF37; font-size: 22px; font-weight: bold; text-align: center;
        overflow: hidden; white-space: nowrap; border-right: 3px solid #D4AF37;
        margin: 0 auto; width: fit-content; animation: typing 4s steps(40, end) infinite;
    }

    /* Animated Ad Billboard */
    .ad-slot {
        background: linear-gradient(90deg, #111, #222); border: 1px solid #D4AF37;
        padding: 15px; border-radius: 10px; text-align: center; color: #D4AF37;
        font-weight: bold; margin-bottom: 20px;
    }

    .price-lock {
        background: #111; border: 2px solid #D4AF37; padding: 20px;
        border-radius: 12px; text-align: center; color: #D4AF37; font-size: 22px;
    }
</style>
""", unsafe_allow_html=True)

def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

# FREE MECHANIC ANIMATION
MECHANIC_ANIM = load_lottie("https://lottie.host/807e3240-5e5d-4f11-9a77-4f6c4966601b/Iu7E9x7A4C.json")

# --- 3. THE APP OPENER (ANIMATED MECHANIC) ---
if 'opener_played' not in st.session_state:
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    if PARTS_OK and MECHANIC_ANIM:
        st_lottie(MECHANIC_ANIM, height=400, key="intro")
    st.markdown("<div class='moving-africa'>Moving Africa to the next level...</div>", unsafe_allow_html=True)
    time.sleep(4)
    st.session_state.opener_played = True
    st.rerun()

# --- 4. DATA CONNECTION (ERROR PROTECTION) ---
if PARTS_OK:
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        master_db = conn.read(ttl=0)
    except:
        st.error("⚠️ DATABASE PERMISSION ERROR: Go to Google Sheets > Share > Set to 'Editor' for 'Anyone with link'.")
        st.stop()
else:
    st.warning("🔄 System is still installing requirements. Please wait 60 seconds and refresh.")
    st.stop()

# --- 5. IDENTITY PORTAL ---
if 'auth' not in st.session_state:
    st.session_state.update({'auth': False, 'role': None})

if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        phone = st.text_input("Verified Phone (+234...)")
        if st.button("ENTER EMPIRE"):
            if "+234000" in phone: st.session_state.role = "Founder"
            elif "8888" in phone: st.session_state.role = "Mechanic"
            else: st.session_state.role = "User"
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 6. ANIMATED VENDOR ADS (ALL PAGES) ---
spare_parts = ["🛠️ Perkins Filters", "🔋 Luminous Batteries", "⚙️ Cummins Injectors", "🚛 Mack Brake Pads"]
current_ad = spare_parts[int(time.time() / 5) % len(spare_parts)]
st.markdown(f"<div class='ad-slot'>VENDOR SPOTLIGHT: {current_ad} - 10% Off for Great Mech Partners!</div>", unsafe_allow_html=True)

# --- 7. FOUNDER COMMAND (REVENUE ANALYTICS) ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    cities = ["Lagos", "Abuja", "Nairobi", "Accra", "Johannesburg"]
    rev_data = pd.DataFrame({'City': cities, 'Revenue': [random.randint(400, 1500)*1000 for _ in range(5)]})
    
    st.subheader("Highest Paying Revenue by City")
    st.bar_chart(rev_data.set_index('City'))
    
    m1, m2 = st.columns(2)
    m1.metric("Leading City", rev_data.iloc[rev_data['Revenue'].idxmax()]['City'])
    m2.metric("Founder 15% Net Income", f"₦{rev_data['Revenue'].sum() * 0.15:,.2f}")

# --- 8. USER PORTAL (FIXED BUDGET) ---
elif st.session_state.role == "User":
    st.title("🚀 DEPLOY SPECIALIST")
    with st.form("service_request"):
        st.selectbox("Service Category", ["🚛 Truck", "🏎️ Car", "⚙️ Generator", "📹 CCTV", "☀️ Solar"])
        st.markdown("<div class='price-lock'><b>FIXED SERVICE FEE: ₦15,000</b></div><br>", unsafe_allow_html=True)
        loc = st.text_input("Your Exact Location")
        if st.form_submit_button("DEPLOY NOW"):
            st.success("Deployment Active! Your specialist is en route.")

# --- 9. MECHANIC HUB (MAP NAVIGATION) ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 JOB RADAR & NAVIGATION")
    st.subheader("User Location Map")
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=13)
    folium.Marker([6.5244, 3.3792], popup="Client Location", icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width=900, height=400)
    
    st.subheader("FINTECH PAYOUT")
    st.info("Verified Mechanics: Africa-wide bank settlement active (85% Split).")

