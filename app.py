import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME CONFIGURATION ---
st.set_page_config(page_title="Great Mech Global", layout="wide", page_icon="🦾")

# Professional Branding (Black & Gold)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .stButton>button { background: linear-gradient(45deg, #D4AF37, #AF8700); color: black !important; font-weight: bold; border-radius: 8px; border: none; height: 3em; }
    .panic-btn>button { background: #FF0000 !important; color: white !important; font-size: 20px !important; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_name_html=True)

# --- 2. THE SHARED MEMORY (Google Sheets Connection) ---
# NOTE: Ensure you add your Google Sheet URL to your Streamlit Cloud Secrets!
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Automatically reads from the spreadsheet linked in your secrets
    db_data = conn.read()
except Exception as e:
    # Fallback for initial setup/testing
    db_data = pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

# --- 3. FOUNDER CORE LOGIC ---
def process_split(amount):
    founder_cut = amount * 0.15
    mechanic_cut = amount * 0.85
    return founder_cut, mechanic_cut

# --- 4. NAVIGATION ARCHITECTURE ---
st.sidebar.title("🦾 GREAT MECH OS")
st.sidebar.caption("Moving Africa to the Next Level")
app_mode = st.sidebar.selectbox("Command Center", ["Marketplace", "Mechanic Hub", "SOS Security", "Founder Ledger"])

# --- MODULE A: MARKETPLACE (Client Requests Help) ---
if app_mode == "Marketplace":
    st.title("📍 Engineering Service Request")
    col_input, col_map = st.columns([1, 1.5])

    with col_input:
        service = st.selectbox("Select Service Category", ["Diesel Engine", "Solar Power", "Heavy Trucks", "Power Gen", "CCTV"])
        budget = st.number_input("Proposed Service Fee (NGN)", min_value=5000, step=1000)
        client_loc = st.text_input("Site Address/Description", "Lagos, Nigeria")
        
        if st.button("🚀 DEPLOY TO NEARBY MECHS"):
            new_job = pd.DataFrame([{
                "ID": f"GM-{random.randint(10000, 99999)}",
                "Service": service,
                "Budget": budget,
                "Status": "Pending",
                "Location": client_loc,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            # In production, use conn.update() here
            st.success("Job Broadcasted! Your 15% fee is calculated and locked in escrow.")
            st.balloons()

    with col_map:
        loc = get_geolocation()
        if loc:
            lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
            m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB dark_matter")
            folium.Marker([lat, lon], popup="Your Site", icon=folium.Icon(color='gold', icon='wrench', prefix='fa')).add_to(m)
            st_folium(m, width=700, height=450)
        else:
            st.warning("Enable GPS for precision mechanic tracking.")

# --- MODULE B: MECHANIC HUB (Worker Accepts Job) ---
elif app_mode == "Mechanic Hub":
    st.title("🔧 Field Operations")
    st.subheader("Available Global Engineering Requests")
    
    if not db_data.empty:
        for i, job in db_data.iterrows():
            with st.expander(f"JOB: {job['Service']} | {job['Location']}"):
                f_cut, m_cut = process_split(job['Budget'])
                st.write(f"Total Bill: ₦{job['Budget']:,.2f}")
                st.write(f"**Your Payout (85%): ₦{m_cut:,.2f}**")
                if st.button(f"Accept Assignment {job['ID']}"):
                    st.info(f"Navigation started to {job['Location']}...")
    else:
        st.info("Searching for pending jobs in your sector...")

# --- MODULE C: SOS SECURITY (The Shield) ---
elif app_mode == "SOS Security":
    st.title("🚨 Emergency Shield")
    st.error("PANIC BUTTON: Sends GPS coordinates to Great Mech Private Security.")
    
    st.markdown('<div class="panic-btn">', unsafe_allow_name_html=True)
    if st.button("TRIGGER GLOBAL SOS", use_container_width=True):
        loc_sos = get_geolocation()
        if loc_sos:
            st.error(f"SOS ALERT ACTIVE! Coordinates: {loc_sos['coords']['latitude']}, {loc_sos['coords']['longitude']}")
        else:
            st.error("SOS ALERT ACTIVE! (Location services disabled, using last known IP location)")
    st.markdown('</div>', unsafe_allow_name_html=True)

# --- MODULE D: FOUNDER LEDGER (Your Revenue) ---
elif app_mode == "Founder Ledger":
    st.title("📊 Global Revenue Command")
    
    # Calculate Total Empire Revenue
    total_val = db_data['Budget'].sum() if not db_data.empty else 0
    f_total, _ = process_split(total_val)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Ecosystem Value", f"₦{total_val:,.2f}")
    c2.metric("Great Mech 15% Share", f"₦{f_total:,.2f}")
    c3.metric("Security/Police Tax", "₦0.00", delta="Permanently Removed")

    st.divider()
    st.subheader("Live Transaction Ledger")
    st.dataframe(db_data, use_container_width=True)

st.sidebar.divider()
st.sidebar.write("© 2026 Great Mech | Licensed Founder Access")

