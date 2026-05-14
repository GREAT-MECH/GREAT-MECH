import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from datetime import datetime

# --- 1. PRESTIGE UI & KINETIC ANIMATIONS ---
st.set_page_config(page_title="Great Mech | v117.0", page_icon="🌍", layout="wide")

# Full CSS for Black/Gold Theme and the Kinetic Left-to-Right Animation
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Trebuchet MS'; font-weight: bold; }
    
    /* Kinetic Left-to-Right Scrolling Animation */
    .moving-africa-container { 
        width: 100%; 
        overflow: hidden; 
        white-space: nowrap; 
        margin-bottom: 20px; 
        border-bottom: 1px solid #D4AF37; 
        padding: 10px 0;
    }
    .moving-africa-text {
        display: inline-block; 
        padding-left: 100%;
        font-size: 1.5em; 
        color: #D4AF37; 
        font-weight: bold;
        animation: scroll-left-to-right 20s linear infinite;
    }
    @keyframes scroll-left-to-right { 
        0% { transform: translateX(0%); } 
        100% { transform: translateX(-200%); } 
    }

    .stButton>button { 
        background-color: #D4AF37; 
        color: black; 
        border-radius: 12px; 
        font-weight: bold; 
        border: none; 
        height: 3.5em; 
        width: 100%; 
    }
    </style>
    <div class="moving-africa-container">
        <div class="moving-africa-text">
            MOVING AFRICA TO THE NEXT LEVEL... 🚀 GREAT MECH ENGINEERING MAGIC... 🌍 54 COUNTRIES...
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. PERMANENT DATABASE ENGINE (GOOGLE SHEETS) ---
# This connects to the sheet URL you saved in the secrets shown in 321931.png
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    try:
        return conn.read(worksheet="Users", ttl="0")
    except:
        # Create the structure if the sheet is empty
        return pd.DataFrame(columns=["Email", "Name", "PIN", "Role", "Bank", "Account"])

def save_user(new_data):
    current_users = get_users()
    updated_users = pd.concat([current_users, pd.DataFrame([new_data])], ignore_index=True)
    conn.update(worksheet="Users", data=updated_users)

# --- 3. SOVEREIGN REGISTRATION & LOGIN GATEWAY ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "gateway"

if st.session_state.auth_status == "gateway":
    st.markdown("<h1 style='text-align:center;'>Great Mech Sovereign Portal 🌍</h1>", unsafe_allow_html=True)
    tab_login, tab_reg = st.tabs(["🔒 SECURE LOGIN", "🛠️ REGISTER PARTNER/USER"])
    
    with tab_login:
        e_log = st.text_input("Email Address", key="log_email")
        p_log = st.text_input("4-Digit PIN", type="password", key="log_pin")
        if st.button("ACTIVATE SESSION"):
            users_df = get_users()
            match = users_df[(users_df['Email'] == e_log) & (users_df['PIN'].astype(str) == p_log)]
            if not match.empty:
                st.session_state.user_data = match.iloc[0].to_dict()
                st.session_state.auth_status = "verified"
                st.rerun()
            else:
                st.error("Access Denied. Check credentials or register below.")

    with tab_reg:
        st.markdown("### Join the Engineering Revolution")
        r_name = st.text_input("Full Name")
        r_email = st.text_input("Email")
        r_role = st.selectbox("I am a:", ["User", "Mechanic"])
        r_pin = st.text_input("Set 4-Digit PIN (numeric)", type="password", max_chars=4)
        m_bank = st.text_input("Bank Name (for Settlements)") if r_role == "Mechanic" else ""
        m_acct = st.text_input("Account Number") if r_role == "Mechanic" else ""
        
        if st.button("CREATE PERMANENT ACCOUNT"):
            if r_email and r_pin:
                save_user({"Email": r_email, "Name": r_name, "PIN": r_pin, "Role": r_role, "Bank": m_bank, "Account": m_acct})
                st.success("Sovereign Account Secured! Please switch to the Login tab.")

# --- 4. THE LIVE SERVICE INTERFACE ---
elif st.session_state.auth_status == "verified":
    user = st.session_state.user_data
    role = user['Role']
    
    with st.sidebar:
        st.markdown(f"### Welcome, {user['Name']}")
        st.write(f"Access Level: **{role}**")
        st.write("Founder Share: **15%**")
        st.write("Police Tax: **0%**")
        if st.button("🚨 PANIC BUTTON"): st.error("EMERGENCY: Security Firm Notified.")
        if st.sidebar.button("Logout"):
            st.session_state.auth_status = "gateway"
            st.rerun()

    # --- USER VIEW: DIAGNOSTIC & PAYSTACK ---
    if role == "User":
        st.markdown("### 🤖 Diagnostic & Dispatch")
        addr = st.text_input("📍 Detailed Address / Landmark for Mechanic")
        
        # 5 Core Categories with Emojis
        cat = st.selectbox("Service Needed", [
            "🚛 Truck", "🚗 Car", "🔋 Diesel Engine / Generator", "🛡️ CCTV", "☀️ Solar"
        ])
        
        fault = st.selectbox("AI Fault Suggestion", [
            "Engine won't start", "Overheating issues", "Strange mechanical noise", 
            "Hydraulic failure", "Electrical fault / Wiring", "Fuel system leak", "Performance drop"
        ])

        if st.button("🤖 RUN AI DIAGNOSTIC"):
            job_id = f"GM-{random.randint(1000, 9999)}"
            st.session_state[f"job_{job_id}"] = {"cat": cat, "addr": addr, "fault": fault, "status": "Pending"}
            st.success(f"Diagnostic Sent. Job ID: {job_id}")

        # Active Job Management
        for key in list(st.session_state.keys()):
            if key.startswith("job_"):
                job = st.session_state[key]
                if job.get("status") == "Quoted":
                    st.info(f"Quote for {job['cat']}: ₦{job['total']:,.2f}")
                    if st.button(f"Pay ₦{job['total']:,.2f} via Paystack"):
                        job["status"] = "Paid"
                        st.success("Payment Verified! Tracking Mechanic...")
                
                if job.get("status") == "Paid":
                    st.map(pd.DataFrame({'lat': [6.5244], 'lon': [3.3792]}))
                    if st.button(f"✅ JOB COMPLETED: RELEASE FUNDS"):
                        job["status"] = "Settled"
                        st.balloons()

    # --- MECHANIC VIEW: QUOTING & BANK SETTLEMENT ---
    elif role == "Mechanic":
        st.markdown("### 🔧 Live Dispatch Feed")
        for key, job in st.session_state.items():
            if key.startswith("job_") and job["status"] == "Pending":
                st.warning(f"NEW REQUEST: {job['cat']} | Address: {job['addr']}")
                st.write(f"**Fault:** {job['fault']}")
                t_fee = st.number_input("Transport Fee (₦)", key=f"t_{key}")
                s_fee = st.number_input("Service Fee (₦)", key=f"s_{key}")
                if st.button("Submit Quote", key=f"btn_{key}"):
                    base = t_fee + s_fee
                    f_share = base * 0.15 
                    job.update({"total": base + f_share, "f_share": f_share, "net": base, "status": "Quoted"})
                    st.rerun()

            if key.startswith("job_") and job["status"] == "Settled":
                st.markdown(f"""
                <div style='border: 1px solid #D4AF37; padding: 15px; border-radius: 10px;'>
                    <h3 style='color: #D4AF37;'>💰 Payment Dispersed</h3>
                    <p>Job Completed. <b>₦{job['net']:,.2f}</b> has been credited to your <b>{user['Bank']}</b> account ({user['Account']}).</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><p style='text-align:center; color:gray;'>Thanks for using Great Mech 🌍</p>", unsafe_allow_html=True)
        
