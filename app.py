import streamlit as st
import time

# --- 1. GLOBAL ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. ELIMINATE THE "0" & DEFINE PREMIUM STYLE (CSS) ---
st.markdown("""
<style>
    /* Kill the artifact "0" and force pitch black */
    .stApp { background-color: #050505; color: white; }
    
    /* Clean Top-Bar for Language */
    .top-bar { display: flex; justify-content: flex-end; padding: 10px; }

    /* Branding Alignment */
    .brand-header { text-align: center; margin-top: -50px; }
    
    .main-title {
        font-size: 58px; font-weight: 900; color: #D4AF37;
        letter-spacing: 5px; margin-bottom: 0px; text-transform: uppercase;
    }
    
    .moving-africa {
        color: #D4AF37; font-size: 20px; font-weight: bold;
        text-align: center; border-right: 3px solid #D4AF37;
        white-space: nowrap; overflow: hidden; margin: 0 auto;
        width: fit-content; animation: typing 3.5s steps(30, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }

    /* SOS Button */
    .sos-button {
        position: fixed; bottom: 30px; right: 30px;
        background-color: #FF0000; color: white; padding: 20px 30px;
        border-radius: 50px; font-weight: bold; z-index: 9999;
        text-decoration: none; box-shadow: 0 10px 30px rgba(255,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. TOP LEVEL: LANGUAGE & SECURITY ---
st.markdown('<a href="tel:911" class="sos-button">🆘 SOS PANIC</a>', unsafe_allow_html=True)

col_lang_left, col_lang_right = st.columns([4, 1])
with col_lang_right:
    # Preferred Language Selection
    st.selectbox("🌐 Language", ["English", "Français", "Português", "Arabic", "Swahili"])

# --- 4. THE VISUAL CORE (GOLDEN AFRICA LOGO) ---
# We use a container to ensure no stray characters (like 0) can leak out
with st.container():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        # Using your specific gold map file
        try:
            st.image("316436.png", use_container_width=True)
        except:
            # High-fidelity backup if file is not in directory
            st.image("https://img.icons8.com/isometric/512/africa.png", width=250)

st.markdown("<div class='brand-header'><div class='main-title'>GREAT MECH</div></div>", unsafe_allow_html=True)
st.markdown("<div class='moving-africa'>Moving Africa to the next level... 🌍</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00FF00; font-weight:bold;'>● System Secure across 54 Countries</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #D4AF37;'>", unsafe_allow_html=True)

# --- 5. THE WORKFLOW PORTALS ---
tabs = st.tabs(["🏛️ Identity Verification", "🛠️ Service Portal", "💰 Empire Revenue"])

with tabs[0]:
    st.write("### Engineer & Founder Onboarding")
    st.text_input("Sovereign Name", placeholder="Founder Credentials")
    st.button("AUTHORIZE ACCESS")

with tabs[1]:
    st.write("### Operational Categories")
    # 5 Core Services with Emojis
    service = st.selectbox("Select Service", [
        "🚛 Heavy Duty Truck Maintenance",
        "🚗 Luxury & Utility Car Repair",
        "⚙️ Diesel Engine & Power Generators",
        "📹 CCTV & Security Systems",
        "☀️ Solar Energy Engineering"
    ])
    
    st.text_area("Detailed Issue Description", placeholder="Describe the mechanical or technical requirements...")
    
    st.markdown("#### 🤝 Mechanic Bargaining Terminal")
    mech_offer = st.number_input("Negotiated Price with Mechanic ($)", min_value=0.0, step=10.0)
    
    if mech_offer > 0:
        # Maintain 15% share logic
        founder_commission = mech_offer * 0.15
        user_total = mech_offer + founder_commission
        
        st.info(f"Great Mech Share (15%): **${founder_commission:,.2f}**")
        st.success(f"Final Price to Display to User: **${user_total:,.2f}**")
        
        if st.button("LOCK PRICE & NOTIFY USER"):
            st.toast("Updating User Portal...")

with tabs[2]:
    st.write("### Financial Sovereignty")
    st.warning("Police/Security 2% payment successfully REMOVED from all cycles.")
    
    col_met1, col_met2 = st.columns(2)
    col_met1.metric("Current Revenue Share", "$45,200", "15%")
    col_met2.metric("Total Jobs Completed", "1,204", "All 54 Countries")

st.markdown("<br><p style='text-align: center; color: #555;'>Great Mech Engineering | Africa's Future Built Here</p>", unsafe_allow_html=True)

