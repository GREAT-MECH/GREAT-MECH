# --- 1. SOVEREIGN PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Great Mech Empire", 
    page_icon="🌍", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. THE DESIGN SYSTEM (CSS) ---
# Translating Figma UI
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    
    .main-title {
        text-align: center; font-size: 52px; font-weight: 900;
        color: #D4AF37; letter-spacing: 3px; margin-top: -20px;
    }
    
    .moving-africa {
        color: #D4AF37; font-size: 20px; font-weight: bold; text-align: center;
        overflow: hidden; white-space: nowrap; margin: 0 auto;
        width: fit-content; border-right: 3px solid #D4AF37;
        animation: typing 4s steps(40, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }

    .sos-button {
        position: fixed; bottom: 25px; right: 25px;
        background-color: #FF0000; color: white; padding: 18px 28px;
        border-radius: 50px; font-weight: bold; z-index: 9999;
        box-shadow: 0 5px 20px rgba(255, 0, 0, 0.4); text-decoration: none;
    }

    .stButton>button {
        width: 100%; background-color: #D4AF37 !important;
        color: black !important; font-weight: bold !important;
        border-radius: 10px !important; border: none !important;
        height: 3.5em !important; transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT EMERGENCY SYSTEM ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# --- 4. BRANDING HEADER ---
col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    try:
        # Calls your specific golden logo file
        st.image("316436.png", use_container_width=True)
    except:
        st.image("https://img.icons8.com/isometric/512/africa.png", width=150)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF00; font-size: 14px;'>● System Status: Secure across 54 Countries</p>", unsafe_allow_html=True)

# --- 5. APP NAVIGATION (Tab System) ---
tab1, tab2, tab3 = st.tabs(["🏛️ Registration", "🛠️ Service Portal", "💳 Empire Payouts"])

# TAB 1: LOGIN & REGISTRATION
with tab1:
    st.subheader("Sovereign Identity Verification")
    u_name = st.text_input("Full Name", placeholder="Enter your full name")
    c_code, c_phone = st.columns([1, 3])
    with c_code:
        country = st.selectbox("Code", ["🇳🇬 +234", "🇰🇪 +254", "🇿🇦 +27", "🇬🇭 +233", "🇪🇬 +20"])
    with c_phone:
        phone = st.text_input("Phone Number")
    
    st.checkbox("I accept the Terms and Privacy Policy")
    if st.button("ENTER EMPIRE"):
        st.success(f"Welcome to Great Mech, {u_name}.")

# TAB 2: LIVE ENGINEERING RADAR
with tab2:
    st.subheader("Diagnostic Deployment")
    cat = st.selectbox("Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    problem = st.text_area("Issue Description")
    
    if st.button("SCAN SYSTEM"):
        with st.status("Running AI Diagnostic...", expanded=True):
            time.sleep(2)
            st.write("Checking system integrity...")
            time.sleep(1)
            st.image("https://img.icons8.com/wired/512/D4AF37/engine.png", width=200)
            st.warning("Anomaly detected: Fuel Injector Resistance High.")

# TAB 3: BANKING & PAYOUTS (Commission Logic)
with tab3:
    st.subheader("Financial Command Center")
    st.write("---")
    
    # Banking Integration Infrastructure
    st.markdown("#### Real-Time Payment Settlement")
    bank_name = st.selectbox("Select Payout Bank", ["Zenith Bank", "Kuda", "Standard Chartered", "M-Pesa"])
    acc_num = st.text_input("Account Number / Wallet ID")
    
    st.write("---")
    # 15% Sovereignty Calculation (2% Police Fee Removed as requested)
    base_quote = st.number_input("Mechanic's Service Quote ($)", min_value=0.0)
    transport = st.number_input("Logistics/Transport Fee ($)", min_value=0.0)
    
    if base_quote > 0:
        subtotal = base_quote + transport
        founder_fee = subtotal * 0.15 # 15% Maintained
        total_price = subtotal + founder_fee
        
        col_a, col_b = st.columns(2)
        col_a.metric("Base Cost", f"${subtotal:,.2f}")
        col_b.metric("Founder Share (15%)", f"${founder_fee:,.2f}", delta_color="normal")
        
        st.info(f"### Total Client Invoice: ${total_price:,.2f}")
        
        if st.button("TRIGGER BANK TRANSFER"):
            st.toast("Connecting to Payment Gateway...")
            time.sleep(2)
            st.success(f"Transfer of ${founder_fee:,.2f} initiated to {bank_name} account {acc_num[-4:]}")

# --- 6. FOOTER ---
st.markdown("<br><hr><p style='text-align: center; color: #444;'>Great Mech v42.0 | African Engineering Sovereignty</p>", unsafe_allow_html=True)

