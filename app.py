# --- 1. PAGE SETUP & ERROR FIX ---
# This line must be the very first Streamlit command to avoid the NameError
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. THE SOVEREIGN DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    /* Premium Dark Mode from Figma */
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    /* Golden "Great Mech" Title Branding */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        color: #D4AF37;
        letter-spacing: 3px;
        margin-top: -20px;
    }

    /* Slogan with your established animation */
    .moving-africa {
        color: #D4AF37;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Green System Status Indicator */
    .status-badge {
        color: #00FF00;
        font-size: 14px;
        text-align: center;
        display: block;
        margin-top: 10px;
    }

    /* Gold Buttons for the Portal */
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        height: 3.5em !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. THE BRANDING HEADER (Africa Logo) ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:
    # Centering your specific Golden Africa Map
    # Note: Ensure "316436.png" is in the same GitHub folder as this app.py
    try:
        st.image("316436.png", use_container_width=True)
    except:
        # Fallback to a high-quality online gold Africa if local file is missing
        st.image("https://img.icons8.com/isometric/512/africa.png", width=150)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<span class='status-badge'>● System Status: All systems operational across 54 Nations</span>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333; margin: 30px 0;'>", unsafe_allow_html=True)

# --- 4. REGISTRATION PORTAL ---
st.markdown("### 🏛️ Registration Portal")
with st.container():
    u_name = st.text_input("Full Name", placeholder="e.g. Nwokeji Chukwuka")
    
    # Implementing the professional country selector you liked
    col_code, col_phone = st.columns([1, 3])
    with col_code:
        country_code = st.selectbox("Code", ["🇳🇬 +234", "🇰🇪 +254", "🇬🇭 +233", "🇿🇦 +27"])
    with col_phone:
        phone_num = st.text_input("Phone Number", placeholder="813 966 499")
    
    st.checkbox("I accept the Terms and Privacy Policy")
    
    if st.button("ENTER EMPIRE"):
        st.balloons()
        st.success(f"Welcome, {u_name}. Sovereign credentials verified.")

# --- 5. SOS EMERGENCY COMPONENT ---
st.markdown("""
    <style>
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
    </style>
    <a href="tel:911" class="sos-button">🆘 SOS PANIC</a>
""", unsafe_allow_html=True)

