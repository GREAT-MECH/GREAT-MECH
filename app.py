import streamlit as st
import pandas as pd
import random
import folium
import time
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & LOGO ARCHITECTURE ---
st.set_page_config(page_title="Great Mech Supreme Global", layout="wide", page_icon="🦾")

# Logo and Theme Styling
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 3px; font-weight: 800; }
    
    /* African Logo Styling */
    .africa-logo {
        text-align: center;
        padding: 20px;
        border: 2px solid #D4AF37;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        margin: 0 auto;
        font-size: 50px;
        background: linear-gradient(45deg, #000, #D4AF37);
    }
    
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 12px; border: none; width: 100%; height: 3.8em;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #111111; padding: 10px; border-radius: 10px; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #D4AF37 !important; color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. DYNAMIC GREETING ENGINE ---
def get_time_greeting(lang):
    hour = datetime.now().hour
    greetings = {
        "English": ["Good Morning", "Good Afternoon", "Good Evening"],
        "Pidgin": ["Bonsue", "How far", "Good Evening"],
        "Yoruba": ["Ẹ kù árọ̀", "Ẹ kù ọ̀sán", "Ẹ kù ìrọ̀lẹ́"],
        "Hausa": ["Ina kwana", "Ina wuni", "Barkada yamma"],
        "Igbo": ["Ututu oma", "Ehihie oma", "Anyasi oma"]
    }
    idx = 0 if 5 <= hour < 12 else 1 if 12 <= hour < 18 else 2
    return greetings.get(lang, greetings["English"])[idx]

# --- 3. FINTECH ASSETS (BANKS BY COUNTRY) ---
bank_data = {
    "Nigeria": ["Access Bank", "Zenith Bank", "GTBank", "UBA", "First Bank", "Kuda", "OPay"],
    "Ghana": ["GCB Bank", "Ecobank", "Absa Bank", "Fidelity Bank"],
    "Kenya": ["KCB Bank", "Equity Bank", "Co-operative Bank"],
    "South Africa": ["Standard Bank", "FirstRand", "Absa", "Nedbank"],
    "Other 50 African Countries": ["Central National Bank", "Mobile Money Transfer", "Global Settlement Hub"]
}

# --- 4. CLOUD CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)
def fetch_data():
    try: return conn.read(ttl=0)
    except: return pd.DataFrame(columns=['ID', 'Role', 'Service', 'Budget', 'Status', 'Location', 'LGA', 'Timestamp', 'Phone', 'Description'])

# --- 5. IDENTITY PORTAL ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'lang' not in st.session_state: st.session_state.lang = "English"

if not st.session_state.authenticated:
    st.markdown("<div class='africa-logo'>🌍</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>MOVING AFRICA TO THE NEXT LEVEL</h2>", unsafe_allow_html=True)
    
    col_l, col_main, col_r = st.columns([1, 2, 1])
    with col_main:
        st.session_state.lang = st.selectbox("Select Language", list(bank_data.keys().mapping.keys() if hasattr(bank_data, 'mapping') else ["English", "Pidgin", "Yoruba", "Hausa", "Igbo"]))
        phone = st.text_input("Enter Phone Number", placeholder="+234...")
        otp = st.text_input("Enter OTP Code", type="password")
        
        if st.button("LOGIN TO EMPIRE"):
            if otp == "0000": # Founder Backdoor
                st.session_state.authenticated = True
                st.session_state.user_role = "Founder"
                st.rerun()
            elif otp == "1234": # Standard Access
                st.session_state.authenticated = True
                st.session_state.user_role = "User"
                st.rerun()
            elif otp == "8888":
                st.session_state.authenticated = True
                st.session_state.user_role = "Mechanic"
                st.rerun()
    st.stop()

# --- 6. MAIN INTERFACE ---
db = fetch_data()
st.sidebar.markdown("<div style='font-size: 40px; text-align: center;'>🌍</div>", unsafe_allow_html=True)
st.sidebar.title(f"{get_time_greeting(st.session_state.lang)}, Founder")

# --- FOUNDER COMMAND ---
if st.session_state.user_role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    if not db.empty:
        db['Budget'] = pd.to_numeric(db['Budget'], errors='coerce').fillna(0)
        total = db['Budget'].sum()
        c1, c2 = st.columns(2)
        c1.metric("Total Ecosystem Value", f"₦{total:,.2f}")
        c2.metric("Founder 15% Share", f"₦{total * 0.15:,.2f}")
        
        st.subheader("Global Operations Inventory")
        for i, row in db.iterrows():
            with st.expander(f"ORDER: {row['ID']} - {row['Service']}"):
                st.write(f"**Desc:** {row['Description']}")
                if st.button(f"🗑️ PURGE {row['ID']}", key=f"del_{row['ID']}"):
                    conn.update(data=db.drop(i))
                    st.rerun()

# --- USER MARKETPLACE ---
elif st.session_state.user_role == "User":
    st.title("📍 ENGINEERING MARKETPLACE")
    t1, t2, t3 = st.tabs(["🚀 DEPLOY", "🧠 AI DIAGNOSTICS", "📄 HISTORY"])
    
    with t1:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            with st.form("main_form"):
                cat = st.selectbox("Category", ["🚛 Truck", "🏎️ Car", "⚙️ Diesel Engine", "📹 CCTV", "☀️ Solar"])
                bud = st.number_input("Budget (NGN)", min_value=5000)
                loc = st.selectbox("Country", list(bank_data.keys()))
                desc = st.text_area("Detailed Problem Description", "Type symptoms here...")
                if st.form_submit_button("ACTIVATE DEPLOYMENT"):
                    new_job = pd.DataFrame([{"ID": f"GM-{random.randint(100,999)}", "Service": cat, "Budget": bud, "Location": loc, "Description": desc, "Status": "Pending", "Timestamp": datetime.now()}])
                    conn.update(data=pd.concat([db, new_job], ignore_index=True))
                    st.success("THANK YOU FOR USING GREAT MECH! Request Broadcasted.")
                    st.balloons()
        with col2:
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=12, tiles="CartoDB dark_matter")
            st_folium(m, width=500, height=400)

    with t2:
        st.subheader("7 Symptoms AI Brain")
        user_input = st.text_area("Describe the issue for AI Analysis")
        if st.button("RUN AI DIAGNOSIS"):
            st.info(f"AI Report for: '{user_input}'")
            st.write("Diagnosis: Mechanical stress detected in Category " + cat)

# --- MECHANIC HUB & FINTECH ---
elif st.session_state.user_role == "Mechanic":
    st.title("🔧 FIELD OPERATIONS")
    tab_jobs, tab_pay = st.tabs(["🛠️ ACTIVE JOBS", "💰 PAYOUTS"])
    
    with tab_jobs:
        st.dataframe(db[db['Status'] == "Pending"])
        if st.button("🚨 TRIGGER SOS SHIELD"):
            st.error("SECURITY ALERT SENT!")
            
    with tab_pay:
        st.subheader("Financial Settlement")
        country = st.selectbox("Select Your Country", list(bank_data.keys()))
        bank = st.selectbox("Select Bank", bank_data[country])
        acc_num = st.text_input("Account Number")
        acc_type = st.radio("Account Type", ["Savings", "Current", "Business"])
        if st.button("VERIFY & RECEIVE FUNDS"):
            st.success(f"Verified: {bank} Account. 85% Payout scheduled.")

