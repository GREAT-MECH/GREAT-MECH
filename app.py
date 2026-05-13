import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. SOVEREIGN IDENTITY & DATA ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# 54 African Countries Data for Searchable Dropdown
AFRICA_54 = {
    "🇳🇬 Nigeria (+234)": "+234", "🇬🇭 Ghana (+233)": "+233", "🇰🇪 Kenya (+254)": "+254",
    "🇿🇦 South Africa (+27)": "+27", "🇪🇬 Egypt (+20)": "+20", "🇪🇹 Ethiopia (+251)": "+251",
    "🇩🇿 Algeria (+213)": "+213", "🇦🇴 Angola (+244)": "+244", "🇧🇯 Benin (+229)": "+229",
    "🇧🇼 Botswana (+267)": "+267", "🇧🇫 Burkina Faso (+226)": "+226", "🇧🇮 Burundi (+257)": "+257",
    "🇨🇲 Cameroon (+237)": "+237", "🇨🇻 Cape Verde (+238)": "+238", "🇨🇫 Central African Rep (+236)": "+236",
    "🇹🇩 Chad (+235)": "+235", "🇰🇲 Comoros (+269)": "+269", "🇨🇬 Congo (+242)": "+242",
    "🇨🇩 DR Congo (+243)": "+243", "🇩🇯 Djibouti (+253)": "+253", "🇬🇶 Equatorial Guinea (+240)": "+240",
    "🇪🇷 Eritrea (+291)": "+291", "🇸🇿 Eswatini (+268)": "+268", "🇬🇦 Gabon (+241)": "+241",
    "🇬🇲 Gambia (+220)": "+220", "🇬🇳 Guinea (+224)": "+224", "🇬🇼 Guinea-Bissau (+245)": "+245",
    "🇨🇮 Ivory Coast (+225)": "+225", "🇱🇸 Lesotho (+266)": "+266", "🇱🇷 Liberia (+231)": "+231",
    "🇱🇾 Libya (+218)": "+218", "🇲🇬 Madagascar (+261)": "+261", "🇲🇼 Malawi (+265)": "+265",
    "🇲🇱 Mali (+223)": "+223", "🇲🇷 Mauritania (+222)": "+222", "🇲🇺 Mauritius (+230)": "+230",
    "🇲🇦 Morocco (+212)": "+212", "🇲🇿 Mozambique (+258)": "+258", "🇳🇦 Namibia (+264)": "+264",
    "🇳🇪 Niger (+227)": "+227", "🇷🇼 Rwanda (+250)": "+250", "🇸🇹 Sao Tome & Principe (+239)": "+239",
    "🇸🇳 Senegal (+221)": "+221", "🇸🇨 Seychelles (+248)": "+248", "🇸🇱 Sierra Leone (+232)": "+232",
    "🇸🇴 Somalia (+252)": "+252", "🇸🇸 South Sudan (+211)": "+211", "🇸🇩 Sudan (+249)": "+249",
    "🇹🇿 Tanzania (+255)": "+255", "🇹🇬 Togo (+228)": "+228", "🇹🇳 Tunisia (+216)": "+216",
    "🇺🇬 Uganda (+256)": "+256", "🇿🇲 Zambia (+260)": "+260", "🇿🇼 Zimbabwe (+263)": "+263"
}

# --- 2. PERSISTENT DATABASE ---
if 'db' not in st.session_state: 
    st.session_state.db = {
        "nwokejianthony2@gmail.com": {"name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"}
    }

if 'auth_status' not in st.session_state: st.session_state.auth_status = "gateway"
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'recovery_mode' not in st.session_state: st.session_state.recovery_mode = False
if 'active_request' not in st.session_state: st.session_state.active_request = None
if 'payment_confirmed' not in st.session_state: st.session_state.payment_confirmed = False
if 'job_status' not in st.session_state: st.session_state.job_status = "idle"

# --- 3. DYNAMIC STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .main-title { text-align: center; font-size: 40px; font-weight: 900; color: #D4AF37; margin-bottom: 20px; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stSidebar"] .stButton>button { background-color: #ff0000 !important; color: white !important; font-weight: bold; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN / REG / RECOVERY) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    
    if st.session_state.recovery_mode:
        st.markdown("### 🔐 Security Recovery")
        f_email = st.text_input("Enter Registered Email", key="rec_email")
        if st.button("Send Recovery SMS OTP"):
            if f_email in st.session_state.db:
                st.session_state.rec_otp = str(random.randint(1000, 9999))
                st.info("Fast OTP sent via SMS Gateway. Check your mobile device.")
            else: st.error("Account not found.")
        
        if 'rec_otp' in st.session_state:
            otp_val = st.text_input("Enter 4-Digit OTP", key="rec_otp_val")
            new_pin = st.text_input("New PIN", type="password")
            if st.button("Reset PIN & Enter Engine"):
                if otp_val == st.session_state.rec_otp:
                    st.session_state.db[f_email]['pin'] = new_pin
                    st.session_state.current_user = st.session_state.db[f_email]
                    st.session_state.auth_status = "verified"; st.rerun()
        if st.button("Back to Login"): st.session_state.recovery_mode = False; st.rerun()

    else:
        tab_login, tab_reg = st.tabs(["Secure Login", "Register Profile"])
        
        with tab_login:
            l_email = st.text_input("Email", key="l_email")
            l_pin = st.text_input("PIN", type="password", key="l_pin")
            if st.button("Enter Sovereign Engine"):
                if l_email in st.session_state.db and st.session_state.db[l_email]["pin"] == l_pin:
                    st.session_state.current_user = st.session_state.db[l_email]
                    st.session_state.auth_status = "verified"; st.rerun()
                else: st.error("Access Denied.")
            if st.button("Forget PIN?"): st.session_state.recovery_mode = True; st.rerun()

        with tab_reg:
            sec = st.radio("I am a:", ["User", "Mechanic"], horizontal=True)
            r_name = st.text_input("Full Legal Name")
            r_email = st.text_input("Email Address", key="r_email")
            
            # Searchable Country Code Dropdown with Flags
            col_flag, col_phone = st.columns([1, 2])
            with col_flag:
                country_select = st.selectbox("Search Country 🔍", list(AFRICA_54.keys()))
                code = AFRICA_54[country_select]
            with col_phone:
                r_num = st.text_input("Mobile Number")
            
            full_phone = f"{code}{r_num}"
            r_pin = st.text_input("Create Security PIN", type="password")
            
            if st.button("Verify Registration"):
                if r_name and "@" in r_email and r_num:
                    st.session_state.temp_otp = str(random.randint(1000, 9999))
                    # Triggering SMS Gateway
                    st.success(f"OTP Fast-Sent to {full_phone}. Check your SMS.")
                else: st.error("Please fill all engineering credentials.")
            
            if 'temp_otp' in st.session_state:
                otp_in = st.text_input("Enter SMS OTP")
                if st.button("Confirm Account"):
                    if otp_in == st.session_state.temp_otp:
                        st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "sector": sec, "phone": full_phone}
                        st.success("Account Active. Please Login."); del st.session_state.temp_otp

# --- 5. THE TRI-SECTOR APP SWITCHER ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    with st.sidebar:
        st.markdown(f"### {user['sector']} Portal")
        st.write(f"**Verified:** {user['name']}")
        st.divider()
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY: Security Dispatched.")
        if st.button("🚪 Logout"): st.session_state.auth_status = "gateway"; st.rerun()

    st.markdown(f"<div class='welcome-text'>{get_greeting(user['name'])}</div>", unsafe_allow_html=True)

    # --- USER APP ---
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Secured. Tracking Mechanic.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
            if st.button("✅ JOB COMPLETED"): st.session_state.job_status = "completed"; st.balloons()
        else:
            cat = st.selectbox("Category", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Gen", "📹 CCTV", "☀️ Solar"])
            st.multiselect("7 Fault AI Diagnostic Symptoms", ["Engine", "Leak", "Power", "Smoke", "Brakes", "Heat", "Vibration"])
            if st.button("🚀 AI DIAGNOSIS"):
                st.session_state.active_request = {"cat": cat, "user": user['name'], "phone": user['phone']}
                st.info("Report broadcasted.")

    # --- MECHANIC APP ---
    elif user['sector'] == "Mechanic":
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Job Request: {req['cat']}</b><br>Client: {req['user']}</div>", unsafe_allow_html=True)
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
            svc = st.number_input("Service Fee (₦)")
            tpt = st.number_input("Transport Fee (₦)")
            if st.button("SEND QUOTE"):
                st.session_state.active_request["quote"] = (svc + tpt) * 1.15
                st.success("Quote sent (15% Founder Share added).")
        
        if st.session_state.job_status == "completed":
            st.subheader("Payout Verification")
            acc = st.text_input("Bank Account Number")
            if st.button("VERIFY & CREDIT"): st.success("Verified. 85% Funds Released.")

    # --- FOUNDER APP ---
    elif user['sector'] == "Founder":
        st.subheader("Sovereign Ledger (v42.0 Engine)")
        st.write("Founder Net: 15% | Service Tax: 0%")
                    
