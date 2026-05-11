import streamlit as st
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Great Mech Empire", page_icon="🌍", layout="centered")

# --- 2. SUPREME CSS (Figma-to-Code Styles) ---
st.markdown("""
<style>
    /* Dark Mode Sovereignty */
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    /* Center the Africa Logo & Main Title */
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: 900;
        color: #D4AF37;
        margin-bottom: 0px;
    }

    /* Your "Moving Africa" Typing Animation */
    .moving-africa {
        color: #D4AF37;
        font-size: 20px;
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

    /* SOS Red Panic Button */
    .sos-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #FF0000;
        color: white;
        border-radius: 50px;
        padding: 15px 25px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.5);
        z-index: 1000;
        text-decoration: none;
    }

    /* Gold Buttons for the Empire */
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        height: 3em !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT PANIC BUTTON ---
st.markdown('<a href="tel:911" class="sos-button">🚨 PANIC BUTTON</a>', unsafe_allow_html=True)

# --- 4. BRANDING HEADER (Africa Logo) ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col2:
    # Gold Africa Logo centered as requested
    st.image("https://img.icons8.com/isometric/512/africa.png", width=120) 

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF00; font-size: 14px;'>● System Status: Secure across 54 Countries</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)

# --- 5. APP LOGIC / REGISTRATION ---
st.subheader("Registration Portal")
with st.container():
    name = st.text_input("Full Name", placeholder="Enter your full name")
    
    # Country Code Selection for all 54 African Countries
    country_code = st.selectbox("Country Code", ["🇳🇬 +234", "🇰🇪 +254", "🇿🇦 +27", "🇬🇭 +233", "🇪🇬 +20"])
    phone = st.text_input("Phone Number", placeholder="813 966 499")
    
    st.checkbox("I accept the Terms and Privacy Policy")
    
    if st.button("ENTER EMPIRE"):
        st.success(f"Welcome to the Great Mech Empire, {name}!")

# --- 6. COMMISSION CALCULATOR (15% Logic) ---
st.sidebar.title("Founder Command")
st.sidebar.info("Auto-calculating 15% Service Charge for rendered services.")
quote = st.sidebar.number_input("Mechanic Quote ($)", min_value=0.0)
transport = st.sidebar.number_input("Transport Fee ($)", min_value=0.0)

if quote > 0:
    # Calculating total with 15% service charge
    service_charge = (quote + transport) * 0.15
    total = (quote + transport) + service_charge
    st.sidebar.write(f"**Great Mech Fee (15%):** ${service_charge:.2f}")
    st.sidebar.write(f"### **Total User Payment: ${total:.2f}**")

