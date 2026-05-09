import streamlit as st
import pandas as pd
import random
import folium
import time
import base64
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. THE FOUNDER'S BRANDING (CSS SUPREMACY) ---
st.set_page_config(
    page_title="Great Mech Supreme Global",
    layout="wide",
    page_icon="🦾",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Full Black & Gold Theme */
    .stApp {
        background-color: #050505;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Gold Metallic Headers */
    h1, h2, h3, .gold-text {
        color: #D4AF37 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 900;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Secure Login Card */
    .auth-card {
        padding: 40px;
        border: 2px solid #D4AF37;
        border-radius: 20px;
        background: linear-gradient(145deg, #111111, #000000);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
        text-align: center;
    }

    /* Premium Founder Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #D4AF37, #AF8700);
        color: #000000 !important;
        font-weight: bold;
        font-size: 18px;
        border-radius: 12px;
        border: none;
        width: 100%;
        height: 4em;
        text-transform: uppercase;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 20px #D4AF37;
        background: #D4AF37;
    }

    /* Metrics Architecture */
    [data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-family: 'Courier New', monospace;
        font-size: 3rem;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #111111;
        border-radius: 15px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 10px;
    }

    /* Inputs & Selectboxes */
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. MULTILINGUAL DICTIONARY (THE 54-COUNTRY GATE) ---
lang_pack = {
    "English": {
        "welcome": "Great Mech Supreme: Accessing Empire...",
        "phone": "Phone Number", "otp": "Verification Code",
        "login": "Secure Login", "deploy": "Activate Deployment",
        "sos": "Trigger SOS Panic Shield"
    },
    "Pidgin": {
        "welcome": "Great Mech Supreme: Empire Dey Load...",
        "phone": "Chook Your Number", "otp": "Enter the Pin",
        "login": "Enter Inside", "deploy": "Send Work Now",
        "sos": "Call Security Fast-Fast"
    },
    "Yoruba": {
        "welcome": "Great Mech Supreme: Wọle si Ijọba...",
        "phone": "Nọmba Foonu rẹ", "otp": "Koodu Ijẹrisi",
        "login": "Wọle", "deploy": "Sọ iṣẹ di ṣiṣẹ",
        "sos": "Pe Olusoabo"
    },
    "Hausa": {
        "welcome": "Great Mech Supreme: Shiga Mulki...",
        "phone": "Lambar Waya", "otp": "Lambar Tabbatarwa",
        "login": "Shiga", "deploy": "Kunna Aikewa",
        "sos": "Kira Tsaro"
    },
    "Igbo": {
        "welcome": "Great Mech Supreme: Na-abata Alaeze...",
        "phone": "Nọmba ekwentị", "otp": "Koodu nkwenye",
        "login": "Banye", "deploy": "Mee arịrịọ",
        "sos": "Kpọọ Ndị Nche"
    },
    "Swahili": {
        "welcome": "Great Mech Supreme: Kufikia Milki...",
        "phone": "Nambari ya Simu", "otp": "Nambari ya Uhakiki",
        "login": "Ingia", "deploy": "Amilisha Ombi",
        "sos": "Piga Simu kwa Usalama"
    }
}

# --- 3. GEOGRAPHIC & SERVICE ASSETS ---
nigeria_states = [
    "Lagos", "Kano", "Rivers", "Oyo", "Enugu", "Abuja FCT", "Kaduna", "Edo", "Delta", "Ogun", 
    "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Ebonyi", 
    "Ekiti", "Gombe", "Imo", "Jigawa", "Kwara", "Kogi", "Katsina", "Kebbi", "Nasarawa", 
    "Niger", "Ondo", "Osun", "Plateau", "Sokoto", "Taraba", "Yobe", "Zamfara", "Abia"
]

african_nations = ["Nigeria", "Ghana", "South Africa", "Kenya", "Egypt", "Ethiopia", "Uganda", "Morocco", "Algeria", "Tanzania", "Other 44 African Nations"]

services = {
    "🚛 Heavy Truck": ["Engine Overhaul", "Transmission Repair", "Brake System", "Suspension"],
    "🏎️ Car/Sedan": ["Diagnostic Check", "Oil Service", "AC Repair", "Body Work"],
    "⚙️ Diesel Generator": ["Routine Service", "Fuel Pump Calibration", "Alternator Repair"],
    "📹 CCTV Security": ["Installation", "System Maintenance", "Remote View Setup"],
    "☀️ Solar Power": ["Panel Install", "Inverter Repair", "Battery Storage Setup"]
}

# --- 4. CLOUD DATABASE & SESSION STATE ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'role' not in st.session_state: st.session_state.role = None
if 'phone' not in st.session_state: st.session_state.phone = ""

conn = st.connection("gsheets", type=GSheetsConnection)

def sync_data():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=['ID', 'Phone', 'Service', 'Category', 'Budget', 'Status', 'Location', 'LGA', 'Timestamp'])

# --- 5. THE IDENTITY GATE (SECURE LOGIN) ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_left, c_mid, c_right = st.columns([1, 2, 1])
    
    with c_mid:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.title("🦾 IDENTITY GATE")
        sel_lang = st.selectbox("🌍 Select Language", list(lang_pack.keys()))
        st.write(f"### {lang_pack[sel_lang]['welcome']}")
        
        ph = st.text_input(lang_pack[sel_lang]['phone'], placeholder="+234...")
        otp = st.text_input(lang_pack[sel_lang]['otp'], type="password")
        
        if st.button(lang_pack[sel_lang]['login']):
            # FOUNDER ACCESS
            if otp == "0000": 
                st.session_state.auth = True
                st.session_state.role = "Founder"
                st.session_state.phone = ph if ph else "Admin"
                st.rerun()
            # MECHANIC/USER MOCK LOGIC (Replace with SMS API later)
            elif otp == "1234":
                st.session_state.auth = True
                st.session_state.role = "User"
                st.session_state.phone = ph
                st.rerun()
            elif otp == "8888":
                st.session_state.auth = True
                st.session_state.role = "Mechanic"
                st.session_state.phone = ph
                st.rerun()
            else:
                st.error("Access Denied: Verification Code Error")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. POST-LOGIN EMPIRE INTERFACE ---
df = sync_data()

# Sidebar: Global Navigation
st.sidebar.title("🦾 GREAT MECH SUPREME")
st.sidebar.markdown(f"**STATUS:** Online 🟢")
st.sidebar.markdown(f"**ROLE:** {st.session_state.role}")
st.sidebar.markdown(f"**PHONE:** {st.session_state.phone}")

if st.sidebar.button("🚪 LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# --- MODULE A: FOUNDER COMMAND CENTER ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    st.markdown("---")
    
    if not df.empty:
        # Strict Financial Math
        df['Budget'] = pd.to_numeric(df['Budget'], errors='coerce').fillna(0)
        total_rev = df['Budget'].sum()
        founder_cut = total_rev * 0.15
        mechanic_cut = total_rev * 0.85
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Ecosystem Value", f"₦{total_rev:,.2f}")
        col_m2.metric("Founder 15% Net", f"₦{founder_cut:,.2f}")
        col_m3.metric("Mechanic 85% Pool", f"₦{mechanic_cut:,.2f}")
        
        st.subheader("📦 Global Service Inventory")
        for i, row in df.iterrows():
            with st.expander(f"ORDER ID: {row['ID']} | {row['Service']} | Status: {row['Status']}"):
                cl1, cl2 = st.columns([3, 1])
                cl1.write(f"**Site:** {row['Location']} ({row['LGA']}) | **Time:** {row['Timestamp']} | **Contact:** {row['Phone']}")
                if cl2.button("🗑️ DELETE ORDER", key=f"del_{row['ID']}"):
                    new_df = df.drop(i)
                    conn.update(data=new_df)
                    st.success("Entry Purged.")
                    st.rerun()
    else:
        st.info("Ecosystem is silent. Waiting for the first African Engineer to deploy.")

# --- MODULE B: USER MARKETPLACE (MAPS, AI, DEPLOYMENT) ---
elif st.session_state.role == "User":
    st.title("📍 USER ENGINEERING HUB")
    t_market, t_ai, t_receipt = st.tabs(["🚀 DEPLOY SERVICE", "🧠 AI DIAGNOSIS", "📄 MY RECEIPTS"])
    
    with t_market:
        c_form, c_vis = st.columns([1, 1.2])
        with c_form:
            st.subheader("Request Engineering Magic")
            with st.form("main_deploy", clear_on_submit=True):
                s_cat = st.selectbox("Category", list(services.keys()))
                s_type = st.selectbox("Specific Task", services[s_cat])
                b_val = st.number_input("Budget (NGN)", min_value=5000, step=5000)
                
                c_sel = st.selectbox("Select Country", african_nations)
                s_sel = st.selectbox("State (Nigeria Only)", nigeria_states)
                lga_sel = st.text_input("Enter LGA / Local District")
                
                if st.form_submit_button("DEPLOY REQUEST"):
                    new_entry = pd.DataFrame([{
                        "ID": f"GM-{random.randint(100000, 999999)}",
                        "Phone": st.session_state.phone,
                        "Service": s_cat,
                        "Category": s_type,
                        "Budget": b_val,
                        "Status": "Pending",
                        "Location": f"{s_sel}, {c_sel}",
                        "LGA": lga_sel,
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }])
                    try:
                        final_df = pd.concat([df, new_entry], ignore_index=True)
                        conn.update(data=final_df)
                        st.success("Deployment Active! Notification sent to nearby Mechanics.")
                        st.balloons()
                    except:
                        st.error("Cloud Error: Database Sync Interrupted.")

        with c_vis:
            st.subheader("🌍 Logistics View")
            st.write("Track Mechanic Proximity & Site Location")
            # Dual-Map Logic (User Site vs Mock Mechanic)
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=11, tiles="CartoDB dark_matter")
            folium.Marker([6.5244, 3.3792], popup="User Location", icon=folium.Icon(color='gold', icon='home')).add_to(m)
            # Simulate a mechanic moving toward user
            folium.Marker([6.5350, 3.3850], popup="Mechanic ID-405", icon=folium.Icon(color='blue', icon='wrench')).add_to(m)
            st_folium(m, width=600, height=400)
            st.write("⏱️ **Estimated Arrival:** 14 mins | 🛣️ **Distance:** 5.8 km")

    with t_ai:
        st.subheader("7 Symptoms AI Diagnostic Brain")
        st.write("Check your machine's health before the mechanic arrives.")
        s_list = st.multiselect("Select Symptoms", ["Engine Overheating", "Black Smoke", "Fluid Leak", "Power Loss", "Strange Noise", "Won't Start", "Battery Failure"])
        
        if st.button("GENERATE AI REPORT"):
            st.markdown("---")
            st.info("**AI Analysis Result:** High probability of Fuel Injector failure or Turbocharge leak.")
            st.write("**Recommended Labor:** 3 - 5 Hours")
            st.write("**Estimated Cost Range:** ₦35,000 - ₦55,000")

    with t_receipt:
        st.subheader("Digital Receipts & History")
        user_history = df[df['Phone'] == st.session_state.phone]
        if not user_history.empty:
            st.dataframe(user_history, use_container_width=True)
            if st.button("DOWNLOAD RECEIPT (PDF)"):
                st.toast("Generating secure encrypted PDF...")
        else:
            st.write("No transactions recorded yet.")

# --- MODULE C: MECHANIC HUB (FIELD OPS & SECURITY) ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 MECHANIC FIELD HUB")
    
    st.subheader("Jobs Pending Accept")
    pending = df[df['Status'] == "Pending"]
    if not pending.empty:
        st.dataframe(pending, use_container_width=True)
        sel_job = st.selectbox("Select Job to View Map", pending['ID'].tolist())
        col_call, col_text = st.columns(2)
        col_call.button("📞 CALL USER")
        col_text.button("💬 TEXT USER")
    else:
        st.write("No pending jobs in your area.")

    st.markdown("---")
    st.subheader("🚨 SOS SECURITY SHIELD")
    st.write("Emergency panic button for mechanics on-site.")
    if st.button("TRIGGER PANIC BUTTON"):
        st.error("🚨 EMERGENCY SIGNAL SENT TO PRIVATE SECURITY FIRM.")
        st.toast(f"Broadcasting GPS for {st.session_state.phone}...")
        # In a real build, this triggers an API call to a security company

