import streamlit as st
import time

# --- 1. ENGINE & BRANDING CONFIG ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. THE VISION INTERFACE (CSS) ---
st.markdown("""
<style>
    /* Force pitch black background */
    .stApp { background-color: #050505; color: white; }
    
    /* Center the branding precisely */
    .brand-container { text-align: center; margin-top: -30px; }
    
    .main-title {
        font-size: 52px; font-weight: 900; color: #D4AF37;
        letter-spacing: 4px; margin-bottom: 0px;
    }
    
    .moving-africa {
        color: #D4AF37; font-size: 19px; font-weight: bold;
        text-align: center; overflow: hidden; white-space: nowrap;
        margin: 0 auto; width: fit-content; border-right: 3px solid #D4AF37;
        animation: typing 4s steps(40, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }

    /* SOS Button */
    .sos-button {
        position: fixed; bottom: 25px; right: 25px;
        background-color: #FF0000; color: white; padding: 18px 28px;
        border-radius: 50px; font-weight: bold; z-index: 9999;
        text-decoration: none; box-shadow: 0 5px 20px rgba(255,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. THE BRANDING HEADER (ERASES THE 0) ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

# This section ensures the logo is centered and no 0 is rendered
col1, col2, col3 = st.columns([0.8, 1.4, 0.8])
with col2:
    try:
        # Pulling your specific gold logo
        st.image("316436.png", use_container_width=True)
    except:
        st.image("https://img.icons8.com/isometric/512/africa.png", width=200)

st.markdown("<div class='brand-container'><div class='main-title'>GREAT MECH</div></div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00FF00; font-size:14px;'>● System Secure: 54 Countries</p>", unsafe_allow_html=True)

# --- 4. THE 5 CORE SERVICES & BARGAINING ---
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🏛️ Identity", "🛠️ Service Portal", "💳 Empire Payouts"])

with tab1:
    st.subheader("Founder's Command Entry")
    st.text_input("Full Name", placeholder="Founder Credentials")
    st.button("VERIFY SYSTEM")

with tab2:
    st.subheader("Select Service Category")
    # Added emojis and specific descriptions for core categories
    service = st.selectbox("Current Operation", [
        "🚛 Heavy Truck Maintenance", 
        "🚗 Luxury Car Repair", 
        "⚙️ Diesel Engine & Generators", 
        "📹 CCTV Surveillance Systems", 
        "☀️ Solar Power Engineering"
    ])
    
    st.text_area("Issue Description", placeholder="Describe the engineering magic needed here...")
    
    st.markdown("### 🤝 The Bargaining Stage")
    st.write("Negotiate with the mechanic before finalizing the user price.")
    mech_price = st.number_input("Mechanic's Agreed Price ($)", min_value=0.0)
    
    if mech_price > 0:
        # Founder Logic: 15% Sovereignty share
        commission = mech_price * 0.15
        total_price = mech_price + commission
        
        st.success(f"Final User Display Price: **${total_price:,.2f}**")
        st.info(f"Your 15% Share: **${commission:,.2f}** | Mechanic Gets: **${mech_price:,.2f}**")
        
        if st.button("SEND QUOTE TO USER"):
            st.toast("Transmitting to user portal...")

with tab3:
    st.subheader("Empire Revenue")
    # Ensuring 2% security fee remains removed
    st.write("Revenue streams are verified. Police/Security 2% payment is **DEACTIVATED**.")
    st.metric("Total Empire Growth", "$1,250,000", "+15%")

st.markdown("<br><p style='text-align: center; color: #333;'>Great Mech Engineering magic in progress...</p>", unsafe_allow_html=True)

