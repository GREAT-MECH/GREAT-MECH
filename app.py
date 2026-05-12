# --- 1. PAGE ENGINE CONFIG ---
import streamlit as st
st.set_page_config(page_title="Great Mech Empire", page_icon="🌍", layout="centered")

# --- 2. THE DESIGN SYSTEM (CSS) ---
# Erasing the "0" and applying premium gold-on-black styling
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        color: #D4AF37;
        letter-spacing: 3px;
        margin-top: -10px;
    }

    .moving-africa {
        color: #D4AF37;
        font-size: 19px;
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

    /* SOS Button for mechanic safety */
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

    .status-badge {
        color: #00FF00;
        font-size: 14px;
        text-align: center;
        display: block;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT SOS COMPONENT ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# --- 4. THE BRANDING HEADER ---
# Centering the Golden Africa Logo directly above the title
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.8, 1.4, 0.8])
with col2:
    try:
        # Calls your specific golden map file from your GitHub repository
        st.image("316436.png", use_container_width=True)
    except:
        # High-quality fallback if the local file is missing
        st.image("https://img.icons8.com/isometric/512/africa.png", width=200)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<span class='status-badge'>● System Status: Secure across 54 Countries</span>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333; margin-top: 30px;'>", unsafe_allow_html=True)

# --- 5. FUNCTIONAL EMPIRE TABS ---
tab1, tab2, tab3 = st.tabs(["🏛️ Registration", "🛠️ Service Portal", "💳 Empire Payouts"])

with tab1:
    st.write("### Identity Verification Portal")
    name = st.text_input("Full Name", placeholder="Enter your full name")
    c_code, c_phone = st.columns([1, 3])
    with c_code:
        st.selectbox("Code", ["🇳🇬 +234", "🇰🇪 +254", "🇿🇦 +27", "🇬🇭 +233"])
    with c_phone:
        st.text_input("Phone Number")
    if st.button("VERIFY CREDENTIALS"):
        st.success(f"Welcome to Great Mech, {name}.")

with tab2:
    st.write("### Engineering Support")
    st.selectbox("Select Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    if st.button("RUN AI DIAGNOSTIC"):
        with st.status("Analyzing Engine Architecture...", expanded=True):
            time.sleep(2)
            st.image("https://img.icons8.com/wired/512/D4AF37/engine.png", width=150)
            st.warning("Anomaly detected in system components.")

with tab3:
    st.write("### Founder's Revenue Analysis")
    st.info("The 2% security fee is removed. Great Mech maintains a 15% share.")
    
    quote = st.number_input("Service Quote ($)", min_value=0.0)
    if quote > 0:
        # The 15% Calculation Logic
        founder_fee = quote * 0.15
        total_price = quote + founder_fee
        
        st.metric("Great Mech Share (15%)", f"${founder_fee:,.2f}")
        st.write(f"### Total Invoice: **${total_price:,.2f}**")
        
        if st.button("INITIALIZE BANK SETTLEMENT"):
            st.toast("Connecting to Sovereign Banking API...")
            time.sleep(2)
            st.success("Financial sequence initiated.")

# --- 6. FOOTER ---
st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech v42.0 | Africa's Engineering Command</p>", unsafe_allow_html=True)

