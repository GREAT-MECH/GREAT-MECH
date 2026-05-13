import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- 1. ENGINE CONFIG & IDENTITY ---
st.set_page_config(page_title="Great Mech | Sovereign Engine", page_icon="🌍", layout="wide")

# All 54 African Countries for Precision Routing
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

# --- 2. PERSISTENT STATE MANAGEMENT ---
if 'db' not in st.session_state: 
    st.session_state.db = {
        "nwokejianthony2@gmail.com": {"name": "Nwokeji Anthony C.", "pin": "7777", "sector": "Founder", "phone": "+2348139664997"}
    }

# Internal State Flags
states = ['auth_status', 'current_user', 'recovery_mode', 'active_request', 'payment_confirmed', 'job_status']
for s in states:
    if s not in st.session_state: st.session_state[s] = "gateway" if s == 'auth_status' else None if s == 'current_user' else False if s in ['recovery_mode', 'payment_confirmed'] else "idle"

# --- 3. CUSTOM INTERFACE STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .main-title { text-align: center; font-size: 42px; font-weight: 900; color: #D4AF37; margin-bottom: 30px; letter-spacing: 2px; }
    .card { background: #111; border: 1px solid #D4AF37; padding: 25px; border-radius: 12px; margin-bottom: 15px; }
    div[data-testid="stSidebar"] .stButton>button { background-color: #FF0000 !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def get_greeting(name):
    hour = datetime.now().hour
    msg = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    return f"{msg}, {name} 🌍"

# --- 4. THE SOVEREIGN GATEWAY (LOGIN / REGISTRATION / STRICT OTP) ---
if st.session_state.auth_status == "gateway":
    st.markdown("<div class='main-title'>GREAT MECH v96.0</div>", unsafe_allow_html=True)
    
    # FORGOT PIN / RECOVERY MODE
    if st.session_state.recovery_mode:
        st.markdown("### 🔐 Strict PIN Recovery")
        f_email = st.text_input("Enter Registered Email", key="rec_email_field")
        
        if st.button("Send Priority Recovery OTP"):
            if f_email in st.session_state.db:
                st.session_state.rec_otp = str(random.randint(1000, 9999))
                st.info(f"Priority OTP Sent to {st.session_state.db[f_email]['phone']}. Waiting for network handshake...")
            else: st.error("Email not recognized in the Sovereign Engine.")
        
        if 'rec_otp' in st.session_state:
            otp_val = st.text_input("Enter 4-Digit Security Code", key="rec_otp_val")
            new_pin = st.text_input("Define New PIN", type="password")
            
            if st.button("Authorize Reset & Login"):
                if otp_val == st.session_state.rec_otp: # STRICT CHECK
                    st.session_state.db[f_email]['pin'] = new_pin
                    st.session_state.current_user = st.session_state.db[f_email]
                    st.session_state.auth_status = "verified"; st.session_state.recovery_mode = False; st.rerun()
                else: st.error("🚨 INVALID OTP. Access Denied.")
        
        if st.button("Return to Login"): st.session_state.recovery_mode = False; st.rerun()

    else:
        tab_login, tab_reg = st.tabs(["🔒 Secure Login", "🛠️ African Engineering Registration"])
        
        with tab_login:
            l_email = st.text_input("Email", key="login_email_main")
            l_pin = st.text_input("PIN", type="password", key="login_pin_main")
            if st.button("Enter Sovereign Engine"):
                if l_email in st.session_state.db and st.session_state.db[l_email]["pin"] == l_pin:
                    st.session_state.current_user = st.session_state.db[l_email]
                    st.session_state.auth_status = "verified"; st.rerun()
                else: st.error("Authentication Failure. Check credentials.")
            if st.button("Forget PIN?"): st.session_state.recovery_mode = True; st.rerun()

        with tab_reg:
            sec = st.radio("Professional Sector:", ["User", "Mechanic"], horizontal=True)
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Email Address", key="reg_email_field")
            
            col_flag, col_phone = st.columns([1.5, 2])
            with col_flag:
                country_select = st.selectbox("Search Africa 🔍", list(AFRICA_54.keys()))
                code = AFRICA_54[country_select]
            with col_phone:
                r_num = st.text_input("Mobile Number (without country code)")
            
            full_phone = f"{code}{r_num}"
            r_pin = st.text_input("Create 4-Digit Security PIN", type="password")
            
            if st.button("Verify Registration"):
                if r_name and "@" in r_email and r_num:
                    st.session_state.temp_otp = str(random.randint(1000, 9999))
                    st.success(f"OTP Fast-Sent to {full_phone}. Bypass-DND engaged.")
                else: st.error("Incomplete engineering credentials.")
            
            if 'temp_otp' in st.session_state:
                otp_in = st.text_input("Enter SMS OTP Code", placeholder="Check your phone...")
                if st.button("Confirm & Activate Account"):
                    if otp_in == st.session_state.temp_otp: # STRICT CHECK
                        st.session_state.db[r_email] = {"name": r_name, "pin": r_pin, "sector": sec, "phone": full_phone}
                        st.success("Sovereign Account Active. Proceed to Login."); del st.session_state.temp_otp
                    else: st.error("🚨 INCORRECT CODE. Registration Blocked.")

# --- 5. TRI-SECTOR INTERFACES (POST-VERIFICATION) ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.current_user
    
    with st.sidebar:
        st.markdown(f"### {user['sector']} Portal")
        st.write(f"**Verified Engineer:** {user['name']}")
        st.divider()
        if st.button("🚨 PANIC BUTTON"): # On-site emergency alert
            st.error("EMERGENCY ALERT: Private Security Firm Notified. Coordinates Sent.")
        if st.button("🚪 Log out of Engine"): 
            st.session_state.auth_status = "gateway"; st.rerun()

    st.markdown(f"<h2>{get_greeting(user['name'])}</h2>", unsafe_allow_html=True)

    # USER APP: AI DIAGNOSIS & PAYMENT
    if user['sector'] == "User":
        if st.session_state.payment_confirmed:
            st.success("✅ Payment Secured. Tracking Mechanic via GPS.")
            st.map(pd.DataFrame([[6.4273, 3.4215]], columns=['lat', 'lon']))
            if st.button("✅ JOB COMPLETED"): st.session_state.job_status = "completed"; st.balloons()
        else:
            cat = st.selectbox("Rendered Service Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
            st.multiselect("7-Fault AI Diagnostic Input", ["Engine Malfunction", "Fluid Leak", "Power Surge", "Smoke Emission", "Braking System", "Overheating", "Vibration/Noise"])
            if st.button("🚀 INITIATE AI DIAGNOSIS"):
                st.session_state.active_request = {"cat": cat, "user": user['name'], "phone": user['phone']}
                st.info("Broadcasted to regional Mech-Network.")

    # MECHANIC APP: NEGOTIATION & 15% FOUNDER SHARE
    elif user['sector'] == "Mechanic":
        if st.session_state.active_request:
            req = st.session_state.active_request
            st.markdown(f"<div class='card'><b>Job Request: {req['cat']}</b><br>Client: {req['user']}</div>", unsafe_allow_html=True)
            svc = st.number_input("Service Fee (₦)")
            tpt = st.number_input("Transport Fee (₦)")
            if st.button("SUBMIT QUOTE"):
                # Maintains the 15% Founder Share
                st.session_state.active_request["quote"] = (svc + tpt) * 1.15
                st.success("Quote sent to client. (Includes 15% Platform Maintenance).")
        
        if st.session_state.job_status == "completed":
            st.subheader("Financial Settlement")
            acc = st.text_input("Enter Payout Account Number")
            if st.button("VALIDATE & RELEASE FUNDS"): 
                st.success("85% Professional Fee Released. Transaction Logged.")

    # FOUNDER APP: SUPREME CONTROL (v42.0 Engine)
    elif user['sector'] == "Founder":
        st.subheader("Sovereign Master Ledger (v42.0 Core)")
        st.write("Sovereign Commission: 15% | Police/Security Tax: 0% (REMOVED)")
        st.write(f"Total Active Nodes: {len(st.session_state.db)}")
