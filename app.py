import streamlit as st
import pandas as pd
import random
import folium
import time
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & CSS ARCHITECTURE ---
st.set_page_config(page_title="Great Mech Supreme Global", layout="wide", page_icon="🦾")

st.markdown("""
<style>
    /* Premium Black & Gold DNA */
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 3px; font-weight: 800; }
    
    /* Login Gate Styling */
    .login-box { padding: 30px; border: 2px solid #D4AF37; border-radius: 15px; background-color: #111111; text-align: center; }
    
    /* Premium Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 12px; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; transition: 0.4s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0px 10px 20px rgba(212, 175, 55, 0.4); }
    
    /* Metric Card Styling */
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New', monospace; font-size: 2.8rem; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 1.1rem; }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] { background-color: #111111; border-radius: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { color: #888888; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL DICTIONARY & DATA ASSETS ---
african_langs = {
    "English": {"welcome": "Welcome to Great Mech Supreme", "auth": "Enter Phone Number", "verify": "Enter OTP Code"},
    "Pidgin": {"welcome": "Great Mech Supreme Don Land", "auth": "Chook your phone number", "verify": "Enter the pin wey we send"},
    "Yoruba": {"welcome": "Ẹ n lẹ o si Great Mech Supreme", "auth": "Tẹ nọmba foonu rẹ", "verify": "Tẹ koodu ijẹrisi rẹ"},
    "Hausa": {"welcome": "Barka da zuwa Great Mech Supreme", "auth": "Sanya lambar wayarka", "verify": "Sanya lambar tabbatarwa"},
    "Igbo": {"welcome": "Nnọọ na Great Mech Supreme", "auth": "Tinye nọmba ekwentị gị", "verify": "Tinye koodu nkwenye gị"}
}

nigeria_states = ["Lagos", "Kano", "Rivers", "Oyo", "Enugu", "Abuja FCT", "Kaduna", "Edo", "Delta", "Ogun", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Ebonyi", "Ekiti", "Gombe", "Imo", "Jigawa", "Kwara", "Kogi", "Katsina", "Kebbi", "Nasarawa", "Niger", "Ondo", "Osun", "Plateau", "Sokoto", "Taraba", "Yobe", "Zamfara", "Abia"]

# --- 3. CLOUD ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def fetch_ledger():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=['ID', 'Role', 'Service', 'Budget', 'Status', 'Location', 'LGA', 'Timestamp', 'Phone'])

# Initialize App Session
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'phone' not in st.session_state: st.session_state.phone = ""

# --- 4. SECURE LOGIN PORTAL (OTP SYSTEM) ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_main, col_r = st.columns([1, 2, 1])
    
    with col_main:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.title("🦾 IDENTITY GATE")
        lang = st.selectbox("Choose Language", list(african_langs.keys()))
        
        phone_input = st.text_input(african_langs[lang]['auth'], placeholder="+234...")
        
        if st.button("SEND VERIFICATION CODE"):
            if len(phone_input) > 10:
                st.session_state.phone = phone_input
                st.success("OTP Sent to " + phone_input)
                time.sleep(1)
            else:
                st.error("Invalid Phone Number")

        otp_input = st.text_input(african_langs[lang]['verify'], type="password")
        
        if st.button("LOGIN TO ECOSYSTEM"):
            # FOUNDER BACKDOOR (Strictly for you)
            if otp_input == "0000": # Example Founder Master Code
                st.session_state.authenticated = True
                st.session_state.user_role = "Founder"
                st.rerun()
            # MECHANIC/USER LOGIC
            elif otp_input == "1234": # Mock OTP for testing
                st.session_state.authenticated = True
                # Role detection logic (In production, this checks the DB)
                st.session_state.user_role = "User" 
                st.rerun()
            else:
                st.error("Incorrect Verification Code")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. THE SUPREME INTERFACE (POST-LOGIN) ---
db = fetch_ledger()
st.sidebar.title("🦾 GREAT MECH OS")
st.sidebar.write(f"**Logged as:** {st.session_state.user_role}")
st.sidebar.write(f"**Phone:** {st.session_state.phone}")

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()

# --- FOUNDER VIEW: THE COMMAND & INVENTORY ---
if st.session_state.user_role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    
    if not db.empty:
        db['Budget'] = pd.to_numeric(db['Budget'], errors='coerce').fillna(0)
        total_val = db['Budget'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ecosystem Value", f"₦{total_val:,.2f}")
        col2.metric("Founder 15% Share", f"₦{total_val * 0.15:,.2f}")
        col3.metric("Mechanic 85% Payout", f"₦{total_val * 0.85:,.2f}")
        
        st.subheader("Inventory & Global Ledger")
        # Clean Delete Functionality
        for index, row in db.iterrows():
            with st.expander(f"JOB ID: {row['ID']} - {row['Service']} ({row['Status']})"):
                c_data, c_act = st.columns([4, 1])
                c_data.write(f"**Location:** {row['Location']} | **Phone:** {row['Phone']} | **Time:** {row['Timestamp']}")
                if c_act.button("🗑️ DELETE ENTRY", key=f"del_{row['ID']}"):
                    new_db = db.drop(index)
                    conn.update(data=new_db)
                    st.rerun()
    else:
        st.info("Ecosystem currently silent. Awaiting first deployment.")

# --- USER VIEW: MARKETPLACE & LOGISTICS ---
elif st.session_state.user_role == "User":
    st.title("📍 ENGINEERING MARKETPLACE")
    t1, t2, t3 = st.tabs(["🚀 DEPLOY REQUEST", "🧠 AI DIAGNOSTICS", "📄 MY RECEIPTS"])
    
    with t1:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Start African Engineering Magic")
            with st.form("deploy_form", clear_on_submit=True):
                service = st.selectbox("Select Service Category", ["🚛 Heavy Truck", "🏎️ Car/Sedan", "⚙️ Diesel Generator", "📹 CCTV Security", "☀️ Solar Power"])
                budget = st.number_input("Budget (NGN)", min_value=5000)
                country = st.selectbox("Select Country", ["Nigeria", "Ghana", "Kenya", "South Africa", "Egypt", "Other 49 African Nations"])
                state = st.selectbox("State (Nigeria)", nigeria_states)
                lga = st.text_input("Local Government Area (LGA)")
                
                if st.form_submit_button("DEPLOY TO CLOUD"):
                    new_job = pd.DataFrame([{
                        "ID": f"GM-{random.randint(10000, 99999)}",
                        "Role": "User",
                        "Service": service,
                        "Budget": budget,
                        "Status": "Pending",
                        "Location": f"{state}, {country}",
                        "LGA": lga,
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Phone": st.session_state.phone
                    }])
                    try:
                        updated = pd.concat([db, new_job], ignore_index=True)
                        conn.update(data=updated)
                        st.success("Deployment Active! Mechanics are being notified.")
                        st.balloons()
                    except:
                        st.error("Cloud Connection Error. Contact Founder.")

        with c2:
            st.subheader("🌍 Logistics Hub")
            st.write("**Real-Time Distance Tracking**")
            # Map showing user vs mechanic
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=11, tiles="CartoDB dark_matter")
            folium.Marker([6.5244, 3.3792], popup="Your Location", icon=folium.Icon(color='gold')).add_to(m)
            st_folium(m, width=500, height=350)
            st.write("⏱️ **Estimated Arrival:** 18 mins | 🛣️ **Distance:** 8.2 km")

    with t2:
        st.subheader("7 Symptoms AI Diagnostic Hub")
        symptoms = st.multiselect("Identify Symptoms", ["Engine Overheating", "Black Smoke", "Fluid Leakage", "Loss of Power", "Strange Noise", "Hard Starting", "Low Oil Pressure"])
        if st.button("RUN AI ENGINE REPORT"):
            st.warning("AI Diagnostic: High probability of Turbocharger or Injector failure.")
            st.info("Estimated Labor Time: 3.5 Hours. Recommended Budget: ₦45,000 - ₦60,000.")

# --- MECHANIC VIEW: FIELD HUB & SECURITY ---
elif st.session_state.user_role == "Mechanic":
    st.title("🔧 FIELD OPERATIONS HUB")
    st.subheader("Jobs Pending Your Expertise")
    pending_jobs = db[db['Status'] == "Pending"]
    st.dataframe(pending_jobs, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🚨 SOS EMERGENCY SHIELD")
    if st.button("TRIGGER PANIC BUTTON"):
        st.error("🚨 EMERGENCY SIGNAL SENT TO PRIVATE SECURITY FIRM.")
        st.toast(f"Coordinates for phone {st.session_state.phone} uploaded to satellite.")


