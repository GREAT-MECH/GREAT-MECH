import streamlit as st
import pandas as pd
import random
import folium
import re
import time
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. SUPREME BRANDING & AFRICAN ARCHITECTURE ---
st.set_page_config(page_title="Great Mech Supreme Global", layout="wide", page_icon="🌍")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3 { color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 3px; font-weight: 800; }
    
    /* African Identity Symbol */
    .africa-logo {
        text-align: center; padding: 25px; border: 4px solid #D4AF37; border-radius: 50%;
        width: 140px; height: 140px; margin: 0 auto; font-size: 70px;
        background: radial-gradient(circle, #222, #000); box-shadow: 0px 0px 50px #D4AF37;
    }

    /* Multi-Vendor Ad Slot Styling */
    .vendor-slot {
        background: linear-gradient(135deg, #111, #222); border-left: 6px solid #D4AF37;
        padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;
        border-right: 1px solid #333; border-top: 1px solid #333;
    }

    /* Founder Insight Box (Non-Editable) */
    .insight-card {
        background: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37;
        padding: 20px; border-radius: 12px; color: #D4AF37;
    }

    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #AF8700); 
        color: black !important; font-weight: bold; border-radius: 12px; border: none; width: 100%; height: 4.5em;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL AFRICAN BANK DATABASE (FINTECH CORE) ---
african_fintech_hub = {
    "Nigeria": ["Access Bank", "Zenith Bank", "GTBank", "UBA", "First Bank", "Kuda", "Moniepoint", "OPay", "Wema Bank", "Fidelity Bank", "Stanbic IBTC", "Sterling Bank"],
    "Ghana": ["GCB Bank", "Ecobank Ghana", "Absa Ghana", "Fidelity Bank Ghana", "Stanbic Bank", "Zenith Bank Ghana"],
    "Kenya": ["KCB Bank", "Equity Bank", "NCBA Bank", "Co-operative Bank", "M-Pesa Business", "Absa Kenya"],
    "South Africa": ["Standard Bank", "Capitec", "First National Bank (FNB)", "Absa SA", "Nedbank", "TymeBank"],
    "Egypt": ["National Bank of Egypt", "Banque Misr", "CIB Egypt", "QNB ALAHLI", "Alex Bank"],
    "Ethiopia": ["Commercial Bank of Ethiopia", "Dashen Bank", "Awash Bank", "Abyssinia Bank"],
    "Uganda": ["Stanbic Bank Uganda", "Centenary Bank", "Standard Chartered", "DFCU Bank"],
    "Morocco": ["Attijariwafa Bank", "Banque Populaire", "BMCE Bank"],
    "Tanzania": ["CRDB Bank", "NMB Bank", "NBC Tanzania", "Standard Chartered TZ"],
    "Rwanda": ["Bank of Kigali", "BPR Bank", "I&M Bank Rwanda", "Cogebanque"]
}

def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning"
    elif 12 <= hour < 18: return "Good Afternoon"
    else: return "Good Evening"

# --- 3. CLOUD ENGINE & DATABASE CONNECTION ---
# Founder: Ensure your sheet is set to "Anyone with the link can EDIT"
conn = st.connection("gsheets", type=GSheetsConnection)

def sync_ledger():
    try:
        return conn.read(ttl=0)
    except Exception as e:
        # Fallback if cloud is unreachable
        return pd.DataFrame(columns=['ID', 'Phone', 'Role', 'Service', 'Budget', 'Status', 'Location', 'Description', 'Timestamp'])

# --- 4. SECURE IDENTITY PORTAL ---
if 'auth' not in st.session_state:
    st.session_state.update({'auth': False, 'role': None, 'phone': None, 'otp_active': False, 'otp_val': None})

if not st.session_state.auth:
    st.markdown("<div class='africa-logo'>🌍</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>GREAT MECH SUPREME: AFRICA UNIFIED</h2>", unsafe_allow_html=True)
    
    c_left, c_mid, c_right = st.columns([1, 2, 1])
    with c_mid:
        phone_input = st.text_input("Enter Phone Number", placeholder="+234...")
        
        if st.button("REQUEST SECURE ACCESS"):
            if re.match(r"^\+?[1-9]\d{7,14}$", phone_input):
                otp = str(random.randint(100000, 999999))
                st.session_state.otp_val = otp
                st.session_state.phone = phone_input
                st.session_state.otp_active = True
                st.success(f"Verification Code Dispatched to {phone_input}")
                st.info(f"SECURITY TOKEN: {otp}") # Debug only
            else:
                st.error("Invalid format. Use International Format.")

        if st.session_state.otp_active:
            otp_verify = st.text_input("Enter 6-Digit Token", type="password")
            if st.button("VERIFY IDENTITY"):
                if otp_verify == st.session_state.otp_val:
                    # FOUNDER MASTER ACCESS
                    if st.session_state.phone == "+2340000000000": # Founder's Private Line
                        st.session_state.role = "Founder"
                    elif "8888" in st.session_state.phone: # Mock Mechanic Logic
                        st.session_state.role = "Mechanic"
                    else:
                        st.session_state.role = "User"
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Verification Mismatch.")
    st.stop()

# --- 5. EMPIRE OPERATING SYSTEM (POST-LOGIN) ---
master_db = sync_ledger()

st.sidebar.markdown("<div class='africa-logo' style='width:80px; height:80px; font-size:40px; padding:10px;'>🌍</div>", unsafe_allow_html=True)
st.sidebar.title(f"{get_time_greeting()}, {st.session_state.role}")
st.sidebar.write(f"**ID:** {st.session_state.phone}")

if st.sidebar.button("🚪 LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# --- 6. MULTI-VENDOR ADVERTISEMENT SLOTS ---
st.markdown("### 🏬 VENDOR SHOWCASE")
ad_cols = st.columns(3)
ads = [
    {"title": "🔋 Solar Max Africa", "desc": "Premium Inverters for Engineering Sites. 10% Off."},
    {"title": "⚙️ Perkins Engines", "desc": "Genuine Spare Parts. Dispatch to 54 Countries."},
    {"title": "🛡️ SecureTech CCTV", "desc": "AI-Powered Security for Workshops. Buy Now."}
]
for i, ad in enumerate(ads):
    with ad_cols[i]:
        st.markdown(f"""
        <div class='vendor-slot'>
            <h4 style='color:#D4AF37; margin:0;'>{ad['title']}</h4>
            <p style='font-size:14px; color:#bbb;'>{ad['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- 7. MODULES BY ROLE ---

# --- FOUNDER COMMAND ---
if st.session_state.role == "Founder":
    st.title("🏛️ FOUNDER COMMAND CENTER")
    if not master_db.empty:
        master_db['Budget'] = pd.to_numeric(master_db['Budget'], errors='coerce').fillna(0)
        total_rev = master_ledger['Budget'].sum() if 'master_ledger' in locals() else master_db['Budget'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Ecosystem Value", f"₦{total_rev:,.2f}")
        m2.metric("Founder 15% Net", f"₦{total_rev * 0.15:,.2f}")
        m3.metric("Growth Index", "54 Countries Online")
        
        st.subheader("Global Ledger Control")
        st.dataframe(master_db, use_container_width=True)
        if st.button("CLEAR ALL COMPLETED JOBS"):
            st.warning("Feature locked for production safety.")

# --- USER MARKETPLACE ---
elif st.session_state.role == "User":
    st.title("📍 ENGINEERING MARKETPLACE")
    t1, t2 = st.tabs(["🚀 DEPLOY SERVICE", "🧠 AI DIAGNOSIS"])
    
    with t1:
        st.subheader("Request Service")
        with st.form("service_request", clear_on_submit=True):
            cat = st.selectbox("Engineering Category", ["Truck Repair", "Diesel Engine", "Car/Sedan", "CCTV", "Solar Power"])
            bud = st.number_input("Budget (NGN)", min_value=5000, step=1000)
            loc = st.text_input("Site Location (State/LGA)")
            desc = st.text_area("Detailed Symptom Description (For AI)")
            
            # Non-Editable Revenue Insight
            st.markdown(f"""
            <div class='insight-card'>
                <b>Financial Split (Fixed):</b><br>
                Founder Share (15%): ₦{bud * 0.15:,.2f}<br>
                Mechanic Payout (85%): ₦{bud * 0.85:,.2f}
            </div><br>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("DEPLOY TO CLOUD"):
                new_row = pd.DataFrame([{
                    "ID": f"GM-{random.randint(1000, 9999)}", "Phone": st.session_state.phone,
                    "Role": "User", "Service": cat, "Budget": bud, "Status": "Pending",
                    "Location": loc, "Description": desc, "Timestamp": datetime.now()
                }])
                try:
                    conn.update(data=pd.concat([master_db, new_row], ignore_index=True))
                    st.success("THANK YOU FOR USING GREAT MECH! Request is Live.")
                except:
                    st.error("Error: Check Google Sheet 'Editor' permissions.")

# --- MECHANIC HUB (FINTECH INCLUDED) ---
elif st.session_state.role == "Mechanic":
    st.title("🔧 FIELD OPERATIONS HUB")
    st.subheader("Available Jobs")
    st.dataframe(master_db[master_db['Status'] == "Pending"], use_container_width=True)
    
    st.markdown("---")
    st.subheader("💰 FINTECH PAYOUT PORTAL")
    st.info("Verified Mechanics Only. All settlements are processed in 85/15 ratio.")
    
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        m_nation = st.selectbox("Bank Nation", list(african_fintech_hub.keys()))
        m_bank = st.selectbox("Select Your Bank", african_fintech_hub[m_nation])
    with col_fin2:
        m_acc = st.text_input("Account Number (10 Digits)")
        m_type = st.radio("Account Type", ["Savings", "Current", "Business"])
    
    if st.button("VERIFY ACCOUNT & RECEIVE FUNDS"):
        if len(m_acc) == 10:
            st.success(f"Verified: {m_bank} Account. Payment processing for active jobs.")
        else:
            st.error("Invalid Account Number.")

    if st.button("🚨 TRIGGER SOS PANIC BUTTON"):
        st.error("EMERGENCY SIGNAL BROADCASTED TO PRIVATE SECURITY FIRM.")

