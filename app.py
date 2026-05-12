import streamlit as st # FIXED: Must be Line 1 to prevent NameError
import time

# --- 1. SOVEREIGN ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech Empire", page_icon="🌍", layout="centered")

# --- 2. PREMIUM DESIGN SYSTEM (CSS) ---
# Erased the "0" and applied the Figma Engineering Dashboard aesthetic
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

# --- 3. PERSISTENT PANIC BUTTON ---
# Emergency alert for mechanics on-site [cite: 2026-04-30]
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# --- 4. BRANDING HEADER ---
# Centering the Golden Africa Logo
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.8, 1.4, 0.8])
with col2:
    try:
        # Calls your specific golden map asset
        st.image("316436.png", use_container_width=True)
    except:
        st.image("https://img.icons8.com/isometric/512/africa.png", width=200)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<span class='status-badge'>● System Status: Secure across 54 Countries</span>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333; margin-top: 30px;'>", unsafe_allow_html=True)

# --- 5. FUNCTIONAL PORTALS ---
tab1, tab2, tab3 = st.tabs(["🏛️ Identity", "🛠️ Service Radar", "💳 Command Payouts"])

with tab1:
    st.write("### Founder's Verification")
    name = st.text_input("Full Name", placeholder="Founder Credentials")
    if st.button("ENTER EMPIRE"):
        st.success(f"Welcome back, Founder {name}.")

with tab2:
    st.write("### Engineering Support")
    category = st.selectbox("Category", ["Truck", "Car", "Diesel Engine/Generator", "CCTV", "Solar"])
    if st.button("RUN DIAGNOSTIC"):
        with st.status("Analyzing Engine Architecture...", expanded=True):
            time.sleep(1)
            st.warning("Diagnostic complete: Optimization required.")

with tab3:
    st.write("### Revenue Command")
    # 2% Security removed. 15% Founder commission maintained [cite: 2026-05-08]
    st.info("Great Mech Fee: 15% Sovereignty share.")
    quote = st.number_input("Mechanic Quote ($)", min_value=0.0)
    if quote > 0:
        commission = quote * 0.15
        total = quote + commission
        st.metric("Your 15% Share", f"${commission:,.2f}")
        st.write(f"### Total Invoice: **${total:,.2f}**")

# --- 6. FOOTER ---
st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech v42.0 | African Engineering Sovereignty</p>", unsafe_allow_html=True)

