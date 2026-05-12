import streamlit as st

# --- 1. ENGINE INITIALIZATION ---
# This must remain Line 1 to prevent NameError
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. LANGUAGE ARCHITECTURE ---
# Maps the vision across the continent
languages = {
    "English": {
        "slogan": "Moving Africa to the next level...",
        "status": "● System Secure across 54 Countries",
        "portal": "Service Portal", "revenue": "Revenue Hub",
        "cat": "Select Category", "desc": "Issue Description",
        "bargain": "Bargaining Terminal", "m_price": "Mechanic's Price ($)",
        "share": "Your 15% Share", "final": "User Display Price"
    },
    "Français": {
        "slogan": "Faire passer l'Afrique au niveau supérieur...",
        "status": "● Système sécurisé dans 54 pays",
        "portal": "Portail de services", "revenue": "Centre de revenus",
        "cat": "Choisir une catégorie", "desc": "Description du problème",
        "bargain": "Terminal de négociation", "m_price": "Prix du mécanicien ($)",
        "share": "Votre part de 15%", "final": "Prix affiché à l'utilisateur"
    }
}

# --- 3. PREMIUM INTERFACE STYLING (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-title {
        text-align: center; font-size: 58px; font-weight: 900; 
        color: #D4AF37; letter-spacing: 5px; margin-top: -30px;
    }
    .typing-box {
        color: #D4AF37; font-size: 20px; font-weight: bold; text-align: center;
        border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden;
        margin: 0 auto; width: fit-content; animation: typing 3.5s steps(30, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    .sos-btn {
        position: fixed; bottom: 30px; right: 30px; background-color: #FF0000;
        color: white; padding: 20px 30px; border-radius: 50px; font-weight: bold;
        z-index: 9999; text-decoration: none; box-shadow: 0 10px 30px rgba(255,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP BAR & SOS ---
# Panic button for on-site security
st.markdown('<a href="tel:911" class="sos-btn">🆘 SOS PANIC</a>', unsafe_allow_html=True)

col_lang_l, col_lang_r = st.columns([4, 1])
with col_lang_r:
    sel_lang = st.selectbox("🌐", list(languages.keys()))
    L = languages[sel_lang]

# --- 5. THE VISUAL CORE (LOGO & BRANDING) ---
# Erases the "0" by using a clean layout container
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        try:
            # Displays the Golden Africa Map
            st.image("316436.png", use_container_width=True)
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=250)

st.markdown(f"<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='typing-box'>{L['slogan']}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#00FF00;'>{L['status']}</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #D4AF37;'>", unsafe_allow_html=True)

# --- 6. OPERATIONAL TABS ---
tab1, tab2 = st.tabs([L['portal'], L['revenue']])

with tab1:
    st.subheader(L['cat'])
    # 5 Service Categories
    service = st.selectbox("Current Operation", [
        "🚛 Heavy Truck Maintenance", 
        "🚗 Luxury Car Repair", 
        "⚙️ Diesel Engine / Generator", 
        "📹 CCTV Systems", 
        "☀️ Solar Power Engineering"
    ])
    
    st.text_area(L['desc'], placeholder="Describe the engineering magic needed...")
    
    st.markdown(f"### 🤝 {L['bargain']}")
    m_offer = st.number_input(L['m_price'], min_value=0.0)
    
    if m_offer > 0:
        # 15% Share Logic
        commission = m_offer * 0.15
        total_user_price = m_offer + commission
        
        st.info(f"{L['share']}: **${commission:,.2f}**")
        st.success(f"{L['final']}: **${total_user_price:,.2f}**")
        
        if st.button("APPROVE & TRANSMIT"):
            st.toast("Quote sent to user portal.")

with tab2:
    st.subheader("Financial Sovereignty")
    # 2% Police fee removed
    st.warning("Police/Security 2% payment: DEACTIVATED.")
    st.metric("Empire Revenue Share", "$0.00", "15% Target")

st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech Engineering | Africa v2026</p>", unsafe_allow_html=True)
    
        
