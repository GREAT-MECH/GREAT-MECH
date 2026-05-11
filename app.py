# --- 1. SOVEREIGN PAGE CONFIG ---
# Must be the very first line to prevent the NameError you encountered.
st.set_page_config(
    page_title="Great Mech Empire", 
    page_icon="🌍", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. THE DESIGN SYSTEM (CSS) ---
# Translating your Figma vision (Black & Gold) into live code.
st.markdown("""
<style>
    /* Premium Background */
    .stApp {
        background-color: #050505;
        color: #FFFFFF;
    }
    
    /* Golden "Great Mech" Title */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        color: #D4AF37;
        letter-spacing: 3px;
        margin-top: -20px;
    }

    /* Typing Animation for Slogan */
    .moving-africa {
        color: #D4AF37;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        overflow: hidden;
        white-space: nowrap;
        margin: 0 auto;
        width: fit-content;
        border-right: 3px solid #D4AF37;
        animation: typing 4s steps(40, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }

    /* Red Panic Button Styling */
    .sos-button {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background-color: #FF0000;
        color: white;
        padding: 18px 28px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 5px 20px rgba(255, 0, 0, 0.4);
        text-decoration: none;
        z-index: 9999;
    }

    /* Gold Buttons */
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        height: 3.5em !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFD700 !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT SOS COMPONENT ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# --- 4. BRANDING HEADER (African Logo) ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    # This calls your specific golden logo file from your repo
    try:
        st.image("316436.png", use_container_width=True)
    except:
        # Fallback if image isn't found
        st.image("https://img.icons8.com/isometric/512/africa.png", width=150)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF00; font-size: 14px;'>● System Status: Secure across 54 Countries</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333; margin-bottom: 40px;'>", unsafe_allow_html=True)

# --- 5. APP NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏛️ Registration", "🛠️ Deploy Service", "💰 Founder Command"])

# TAB 1: REGISTRATION PORTAL
with tab1:
    st.subheader("Enter the Empire")
    name = st.text_input("Full Name", placeholder="e.g. John Doe")
    c_code, c_phone = st.columns([1, 3])
    with c_code:
        country = st.selectbox("Code", ["🇳🇬 +234", "🇰🇪 +254", "🇿🇦 +27", "🇬🇭 +233", "🇪🇬 +20"])
    with c_phone:
        phone = st.text_input("Phone Number")
    
    st.checkbox("I accept the Terms and Privacy Policy")
    if st.button("VERIFY CREDENTIALS"):
        st.success(f"Welcome, {name}. Your account is now active.")

# TAB 2: SERVICE DEPLOYMENT
with tab2:
    st.subheader("Request Engineering Support")
    category = st.selectbox("Select Service Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    problem = st.text_area("Describe the Issue", placeholder="e.g. Engine misfire in Cylinder 3")
    
    if st.button("GENERATE AI DIAGNOSTIC"):
        st.info("Analyzing system architecture...")
        # Visual diagram placeholder
        st.image("https://img.icons8.com/wired/512/D4AF37/engine.png", width=200)
        st.write("**Diagnostic Result:** Potential fuel injector misfire detected.")

# TAB 3: FOUNDER COMMAND (Commission Logic)
with tab3:
    st.subheader("Revenue Analysis")
    st.info("The 2% security fee has been removed. Great Mech maintains a 15% commission.")
    
    mech_quote = st.number_input("Mechanic's Repair Quote ($)", min_value=0.0)
    transport_fee = st.number_input("Transport/Logistic Fee ($)", min_value=0.0)
    
    if mech_quote > 0:
        # The 15% Sovereignty Calculation
        subtotal = mech_quote + transport_fee
        commission = subtotal * 0.15
        total_payout = subtotal + commission
        
        st.markdown(f"""
        ### Financial Breakdown
        * **Base Service Cost:** ${subtotal:,.2f}
        * **Great Mech Fee (15%):** ${commission:,.2f}
        ---
        ## **Total User Payment: ${total_payout:,.2f}**
        """)

# --- 6. FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #555;'>Great Mech v42.0 | Proprietary Engineering Software</p>", unsafe_allow_html=True)

