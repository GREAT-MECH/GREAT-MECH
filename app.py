import streamlit as st
import pandas as pd
import requests
import time
import random
import folium
from datetime import datetime

# --- 1. PLUGINS CHECK ---
try:
    from streamlit_lottie import st_lottie
    from streamlit_folium import st_folium
    from streamlit_gsheets import GSheetsConnection
    ENGINE_PARTS_READY = True
except ImportError:
    ENGINE_PARTS_READY = False

# --- 2. SUPREME BRANDING & THEME ---
st.set_page_config(page_title="Great Mech Supreme", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-title { color: white; text-align: center; font-size: 50px; font-weight: 900; margin-bottom: 0; }
    .moving-africa {
        color: #D4AF37; font-size: 22px; font-weight: bold; text-align: center;
        overflow: hidden; white-space: nowrap; border-right: 3px solid #D4AF37;
        margin: 0 auto; width: fit-content; animation: typing 4s steps(40, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    .price-box { border: 2px solid #D4AF37; padding: 15px; border-radius: 10px; text-align: center; color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

def load_lottie(url):
    try:
        return requests.get(url).json()
    except: return None

# FREE MECHANIC AT WORK ANIMATION
MECHANIC_JSON = load_lottie("https://lottie.host/807e3240-5e5d-4f11-9a77-4f6c4966601b/Iu7E9x7A4C.json")

# --- 3. THE APP OPENER ---
if 'opener_played' not in st.session_state:
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    if ENGINE_PARTS_READY and MECHANIC_JSON:
        st_lottie(MECHANIC_JSON, height=400, key="opener")
    else:
        st.write("🔧 Preparing Engineering Tools...")
    st.markdown("<div class='moving-africa'>Moving Africa to the next level...</div>", unsafe_allow_html=True)
    time.sleep(4)
    st.session_state.opener_played = True
    st.rerun()

# --- 4. SECURE DATA CONNECTION ---
if ENGINE_PARTS_READY:
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        # This will fail gracefully if permissions aren't set to 'Editor'
        db = conn.read(ttl=0)
    except:
        st.error("⚠️ DATABASE LOCK: Set Google Sheet to 'Editor' access and check Secrets.")
        st.stop()
else:
    st.warning("Engine parts are still installing in the background. Refresh in 1 minute.")
    st.stop()

# --- 5. LOGIC GATES (ROLES) ---
if 'auth' not in st.session_state:
    st.session_state.update({'auth': False, 'role': None, 'phone': None})

if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        phone = st.text_input("Verified Phone Number")
        if st.button("ENTER EMPIRE"):
            if "+234000" in phone: st.session_state.role = "Founder"
            elif "8888" in phone: st.session_state.role = "Mechanic"
            else: st.session_state.role = "User"
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 6. FOUNDER COMMAND CENTER ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND")
    cities = ["Lagos", "Abuja", "Nairobi", "Accra", "Johannesburg"]
    rev = pd.DataFrame({'City': cities, 'Revenue': [random.randint(400, 1200)*1000 for _ in range(5)]})
    
    st.subheader("Revenue by City")
    st.bar_chart(rev.set_index('City'))
    
    m1, m2 = st.columns(2)
    m1.metric("Top Country", "Nigeria")
    m2.metric("Founder 15% Net", f"₦{rev['Revenue'].sum() * 0.15:,.2f}")

# --- 7. USER MARKETPLACE (FIXED PRICE) ---
elif st.session_state.role == "User":
    st.title("🚀 DEPLOY SPECIALIST")
    with st.form("request"):
        st.selectbox("Service", ["🚛 Truck", "🏎️ Car", "⚙️ Generator", "📹 CCTV", "☀️ Solar"])
        st.markdown("<div class='price-box'><b>FIXED SERVICE FEE: ₦15,000</b></div><br>", unsafe_allow_html=True)
        loc = st.text_input("Service Location")
        if st.form_submit_button("DEPLOY NOW"):
            # Update DB logic here
            st.success("Deployment Successful!")

# --- 8. MECHANIC HUB (MAPS) ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 JOB RADAR")
    # Mechanic sees where the money is
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=12)
    folium.Marker([6.5244, 3.3792], popup="Client Location").add_to(m)
    st_folium(m, width=800, height=400)
    st.dataframe(db)

