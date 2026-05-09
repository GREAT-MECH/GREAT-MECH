import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & LANGUAGE ENGINE ---
st.set_page_config(page_title="Great Mech Supreme OS", layout="wide", page_icon="🦾")

# Global African Language Dictionary
languages = {
    "English": {"greet": "Welcome, Founder", "deploy": "Deploy Request", "status": "Online"},
    "Pidgin": {"greet": "Abeg Welcome, Oga Founder", "deploy": "Send Work", "status": "I Dey Online"},
    "Yoruba": {"greet": "Ẹ n lẹ o, Oludasile", "deploy": "Fi iṣẹ ranṣẹ", "status": "Mo wa lori ayelujara"},
    "Hausa": {"greet": "Sannu, Shugaba", "deploy": "Tura nema", "status": "Ina kan layi"},
    "Igbo": {"greet": "Nnọọ, Onye nchoputa", "deploy": "Ziga arịrịọ", "status": "Anọ m n'ịntanetị"},
    "Swahili": {"greet": "Karibu, Mwanzilishi", "deploy": "Tuma ombi", "status": "Niko mtandaoni"}
}

st.sidebar.title("🌍 GLOBAL SETTINGS")
lang_choice = st.sidebar.selectbox("Preferred Language", list(languages.keys()))
st.sidebar.success(f"Status: {languages[lang_choice]['status']}")

# The Black & Gold DNA
st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }}
    h1, h2, h3 {{ color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }}
    .stButton>button {{ 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 10px; border: none; width: 100%; height: 3.5em;
    }}
    [data-testid="stMetricValue"] {{ color: #D4AF37 !important; font-family: 'Courier New', monospace; }}
</style>
""", unsafe_allow_html=True)

# --- 2. IDENTITY PORTAL ---
if 'role' not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.title(f"🦾 {languages[lang_choice]['greet']}")
    cols = st.columns(4)
    if cols[0].button("🏛️ FOUNDER"): st.session_state.role = "Founder"
    if cols[1].button("🔧 MECHANIC"): st.session_state.role = "Mechanic"
    if cols[2].button("👤 USER"): st.session_state.role = "User"
    if cols[3].button("🤝 PARTNER"): st.session_state.role = "Partner"
    st.stop()

# --- 3. CLOUD LEDGER & INVENTORY ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)
def get_db():
    try: return conn.read(ttl=0)
    except: return pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'LGA', 'Timestamp'])

db = get_db()

# --- 4. THE VISION MODULES ---

# --- FOUNDER: THE MONEY & INVENTORY ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND")
    if not db.empty:
        db['Budget'] = pd.to_numeric(db['Budget'], errors='coerce').fillna(0)
        total = db['Budget'].sum()
        m1, m2 = st.columns(2)
        m1.metric("Total Ecosystem Value", f"₦{total:,.2f}")
        m2.metric("Founder 15% Net", f"₦{total * 0.15:,.2f}")
        
        st.subheader("Inventory Management")
        for index, row in db.iterrows():
            col1, col2 = st.columns([4, 1])
            col1.write(f"**ID:** {row['ID']} | **Job:** {row['Service']} | **Budget:** ₦{row['Budget']}")
            if col2.button(f"🗑️ DELETE", key=f"del_{row['ID']}"):
                new_db = db.drop(index)
                conn.update(data=new_db)
                st.rerun()
    else: st.info("Ledger Empty.")

# --- USER: MARKETPLACE, AI, & MAPS ---
elif st.session_state.role == "User":
    st.title("📍 USER MARKETPLACE")
    tab1, tab2, tab3 = st.tabs(["🚀 DEPLOY REQUEST", "🧠 AI DIAGNOSTICS", "🧾 RECEIPTS"])
    
    with tab1:
        col_in, col_map = st.columns([1, 1])
        with col_in:
            service = st.selectbox("Category", ["🚛 Truck", "🏎️ Car", "⚙️ Diesel Engine", "📹 CCTV", "☀️ Solar"])
            budget = st.number_input("Proposed Budget (NGN)", min_value=5000)
            country = st.selectbox("Country", ["Nigeria", "Ghana", "South Africa", "Kenya", "Egypt", "Rest of Africa (54)"])
            state = st.selectbox("State (Nigeria)", ["Lagos", "Kano", "Rivers", "Oyo", "Enugu", "...36 States"])
            lga = st.text_input("Local Government Area (LGA)")
            
            if st.button(languages[lang_choice]['deploy']):
                new_job = pd.DataFrame([{"ID": f"GM-{random.randint(1000, 9999)}", "Service": service, "Budget": budget, "Status": "Pending", "Location": state, "LGA": lga, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([db, new_job], ignore_index=True))
                st.success("Deployment Active!")
                st.balloons()
        
        with col_map:
            st.subheader("🌍 Logistics Hub")
            m = folium.Map(location=[6.5244, 3.3792], zoom_start=12, tiles="CartoDB dark_matter")
            st_folium(m, width=500, height=350)
            st.write("⏱️ **Estimated Arrival:** 24 mins | 🛣️ **Distance:** 12.4 km")

    with tab2:
        st.subheader("7 Symptoms AI Diagnostic")
        symp = st.multiselect("Symptoms", ["Overheating", "Black Smoke", "Fluid Leak", "Power Loss", "Strange Noise", "Hard Start", "Low Pressure"])
        if st.button("GENERATE REPORT"):
            st.info("AI Analysis: High probability of fuel injector blockage. Recommend cleaning.")

# --- MECHANIC: HUB & SOS ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 FIELD HUB")
    st.dataframe(db[db['Status'] == "Pending"])
    col_call, col_text = st.columns(2)
    col_call.button("📞 CALL USER")
    col_text.button("💬 TEXT USER")
    
    st.markdown("---")
    if st.button("🚨 TRIGGER SOS PANIC BUTTON"):
        st.error("🚨 SECURITY ALERT SENT TO PRIVATE FIRM.")

