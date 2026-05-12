import streamlit as st
import pandas as pd
import numpy as np

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. LANGUAGE & LOCALIZATION ---
languages = {
    "English": {
        "welcome": "Welcome back, Founder. Ready to move Africa to the next level?",
        "slogan": "Engineering Magic across 54 Countries",
        "map_header": "📍 Live Tracking: Mechanic & User Synchronization",
        "portal": "Service Portal", "revenue": "Revenue Hub",
        "cat": "Service Category", "bargain": "Bargaining Terminal",
        "mech_p": "Mechanic's Negotiated Price ($)", "share": "Founder 15% Share"
    },
    "Français": {
        "welcome": "Bon retour, Fondateur. Prêt à faire passer l'Afrique au niveau supérieur?",
        "slogan": "Magie de l'ingénierie dans 54 pays",
        "map_header": "📍 Suivi en direct : Synchronisation mécanicien et utilisateur",
        "portal": "Portail de services", "revenue": "Centre de revenus",
        "cat": "Catégorie de service", "bargain": "Terminal de négociation",
        "mech_p": "Prix négocié du mécanicien ($)", "share": "Part du fondateur 15%"
    }
}

# --- 3. SOVEREIGN INTERFACE (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-title {
        text-align: center; font-size: 55px; font-weight: 900; 
        color: #D4AF37; letter-spacing: 5px; margin-top: -30px;
    }
    .welcome-text {
        color: #D4AF37; font-size: 22px; text-align: center; font-style: italic;
        margin-bottom: 20px;
    }
    .sos-btn {
        position: fixed; bottom: 30px; right: 30px; background-color: #FF0000;
        color: white; padding: 20px 30px; border-radius: 50px; font-weight: bold;
        z-index: 9999; text-decoration: none; box-shadow: 0 10px 30px rgba(255,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP BAR: IDENTITY & LANGUAGE ---
st.markdown('<a href="tel:911" class="sos-btn">🆘 SOS PANIC</a>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 1])
with col_b:
    sel_lang = st.selectbox("🌐", list(languages.keys()))
    L = languages[sel_lang]

# --- 5. BRANDING & WELCOME (PURGING THE 0) ---
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        try:
            st.image("316436.png", use_container_width=True) #
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=250)

st.markdown(f"<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='welcome-text'>{L['welcome']}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#00FF00;'>● {L['slogan']}</p>", unsafe_allow_html=True)

# --- 6. COMMAND TABS ---
tab1, tab2, tab3 = st.tabs(["🗺️ Radar & Map", L['portal'], L['revenue']])

with tab1:
    st.subheader(L['map_header'])
    # Mock data for Mechanic/User tracking
    map_data = pd.DataFrame(
        np.random.randn(2, 2) / [50, 50] + [6.5244, 3.3792], # Defaulting near Lagos/Africa context
        columns=['lat', 'lon']
    )
    st.map(map_data)
    st.info("Mechanic (Blue Dot) is currently 2.4km from User location.")

with tab2:
    st.subheader(L['cat'])
    # The 5 core categories
    service = st.selectbox("Current Operation", [
        "🚛 Truck Maintenance", "🚗 Car Repair", "⚙️ Diesel/Generator", 
        "📹 CCTV Systems", "☀️ Solar Engineering"
    ])
    st.text_area("Engineering Description", placeholder="Enter specific fix details...")
    
    st.markdown(f"### 🤝 {L['bargain']}")
    m_price = st.number_input(L['m_price'], min_value=0.0)
    
    if m_price > 0:
        # Founder 15% Share
        commission = m_price * 0.15
        total = m_price + commission
        st.write(f"**{L['share']}:** ${commission:,.2f}")
        st.success(f"**Final Display Price:** ${total:,.2f}")
        
        if st.button("SEND TO USER FOR PAYMENT"):
            st.toast("Transmitting funds request...")

with tab3:
    st.subheader("Empire Revenue")
    st.warning("2% Police/Security Payment: REMOVED")
    st.metric("15% Platform Growth", "$0.00", "54 Countries")

st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech Engineering | African Magic Built Here</p>", unsafe_allow_html=True)
    
