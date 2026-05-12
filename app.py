import streamlit as st # FIXED: Line 1 initialization
import time

# --- 1. SOVEREIGN CONFIG ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. PREMIUM EMPIRE STYLING (CSS) ---
st.markdown("""
<style>
    /* Dark Engineering Background */
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    /* Centered Gold Title */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        color: #D4AF37;
        letter-spacing: 4px;
        margin-top: -10px;
    }

    /* Typing Animation for Slogan */
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

    /* Green System Status */
    .status-badge {
        color: #00FF00;
        font-size: 14px;
        text-align: center;
        display: block;
        margin-top: 5px;
    }

    /* Red Panic Button */
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

    /* Empire Tabs & Buttons */
    .stTabs [data-baseweb="tab"] { color: #D4AF37; font-weight: bold; }
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT SOS SYSTEM ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# --- 4. THE VISUAL ANCHOR (Africa Logo) ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.8, 1.4, 0.8])
with col2:
    # Placing your specific golden map
    try:
        st.image("316436.png", use_container_width=True)
    except:
        st.image("https://img.icons8.com/isometric/512/africa.png", width=200)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<span class='status-badge'>● System Status: Secure across 54 Countries</span>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333; margin-top: 30px;'>", unsafe_allow_html=True)

# --- 5. THE EMPIRE PORTALS ---
tab1, tab2, tab3 = st.tabs(["🏛️ Identity Verification", "🛠️ Service Portal", "💳 Empire Payouts"])

with tab1:
    st.write("### Register as a Great Mech Engineer")
    u_name = st.text_input("Full Name")
    c_code, c_phone = st.columns([1, 3])
    with c_code:
        st.selectbox("Code", ["🇳🇬 +234", "🇰🇪 +254", "🇿🇦 +27", "🇬🇭 +233"])
    with c_phone:
        st.text_input("Phone Number")
    if st.button("VERIFY IDENTITY"):
        st.success(f"Welcome, {u_name}. Sovereign credentials confirmed.")

with tab2:
    st.write("### Active Radar Diagnostic")
    cat = st.selectbox("Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    if st.button("RUN SCAN"):
        with st.status("Analyzing Engine Architecture...", expanded=True):
            time.sleep(2)
            st.image("https://img.icons8.com/wired/512/D4AF37/engine.png", width=150)
            st.warning("Anomaly detected in fuel injection system.")

with tab3:
    st.write("### Financial Command Center")
    st.info("The 2% police fee has been removed. Great Mech maintains 15% Sovereignty.")
    
    quote = st.number_input("Service Quote ($)", min_value=0.0)
    if quote > 0:
        # The 15% Calculation Logic
        founder_share = quote * 0.15
        total_payout = quote + founder_share
        
        st.metric("Your 15% Share", f"${founder_share:,.2f}")
        st.write(f"### Total Invoice to Client: **${total_payout:,.2f}**")
        
        if st.button("INITIALIZE BANK TRANSFER"):
            st.toast("Connecting to Sovereign Banking API...")
            time.sleep(2)
            st.success("Transfer sequence initiated.")

# --- 6. FOOTER ---
st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech v42.0 | African Engineering Sovereignty</p>", unsafe_allow_html=True)

