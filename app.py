# --- 1. PAGE CONFIG & PREMIUM STYLING ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    /* Premium Gold Title */
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #D4AF37;
        margin-top: -10px;
        letter-spacing: 2px;
    }

    /* Moving Africa Animation */
    .moving-africa {
        color: #D4AF37;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }

    /* System Status online dot */
    .status-online {
        color: #00FF00;
        font-size: 14px;
        text-align: center;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE AFRICA LOGO HEADER ---
# This section centers your golden Africa logo directly above the Great Mech title
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 0.8, 1])

with col2:
    # This uses a gold Africa map similar to your reference
    st.image("https://i.ibb.co/VWV0pXG/gold-africa-map.png", use_container_width=True)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<span class='status-online'>● System Status: All systems operational</span>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)

# --- 3. REGISTRATION PORTAL ---
# Recreating the portal from your Figma design
st.write("### Registration Portal")
with st.container():
    name = st.text_input("Full Name", placeholder="Enter your full name")
    
    # Implementing the country selection from your reference
    country = st.selectbox("Select Country", ["Nigeria 🇳🇬", "Ghana 🇬🇭", "Kenya 🇰🇪", "South Africa 🇿🇦"])
    phone = st.text_input("Phone Number", placeholder="+234 ...")
    
    st.checkbox("I accept the Terms and Privacy Policy")
    
    if st.button("ENTER EMPIRE"):
        st.success(f"Welcome, {name}. Connecting to Live Radar...")

# --- 4. PANIC BUTTON (Mechanic Safety) ---
# Persistent SOS button from your design
st.markdown("""
    <style>
    .sos-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #FF4B4B;
        color: white;
        padding: 15px 25px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    </style>
    <a href="#" class="sos-btn">🆘 SOS PANIC</a>
""", unsafe_allow_html=True)

