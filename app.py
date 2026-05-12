import streamlit as st
import pandas as pd
import numpy as np

# --- 1. ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. STABILIZED LANGUAGE ENGINE ---
languages = {
    "English": {
        "welcome": "Welcome back, Founder. Ready to move Africa to the next level?",
        "slogan": "Engineering Magic across 54 Countries",
        "map_header": "📍 Live Tracking: Mechanic & User Synchronization",
        "portal": "Service Portal", "revenue": "Revenue Hub",
        "cat": "Service Category", "bargain": "Bargaining Terminal",
        "m_price": "Mechanic's Negotiated Price ($)", 
        "share": "Founder 15% Share", "final": "Final Display Price"
    },
    "Français": {
        "welcome": "Bon retour, Fondateur. Prêt à faire passer l'Afrique au niveau supérieur?",
        "slogan": "Magie de l'ingénierie dans 54 pays",
        "map_header": "📍 Suivi en direct : Synchronisation mécanicien et utilisateur",
        "portal": "Portail de services", "revenue": "Centre de revenus",
        "cat": "Catégorie de service", "bargain": "Terminal de négociation",
        "m_price": "Prix négocié du mécanicien ($)", 
        "share": "Part du fondateur 15%", "final": "Prix final affiché"
    }
}

# --- 3. PREMIUM UI STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: white; }
    .main-title { text-align: center; font-size: 55px; font-weight: 900; color: #D4AF37; letter-spacing: 5px; margin-top: -30px; }
    .welcome-text { color: #D4AF37; font-size: 22px; text-align: center; font-style: italic; margin-bottom: 20px; }
    .sos-btn { position: fixed; bottom: 30px; right: 30px; background-color: #FF0000; color: white; padding: 20px 30px; border-radius: 50px; font-weight: bold; z-index: 9999; text-decoration: none; box-shadow: 0 10px 30px rgba(255,0,0,0.5); }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP BAR & SOS ---
st.markdown('<a href="tel:911" class="sos-btn">🆘 SOS PANIC</a>', unsafe_allow_html=True)
col_a, col_b = st.columns([4, 1.2])
with col_b:
    sel_lang = st.selectbox("🌐 Language", list(languages.keys()))
    L = languages[sel_lang]

# --- 5. LOGO & GREETING ---
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        try:
            # Attempt to load your custom logo
            st.image("316436.png", use_container_width=True)
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=220)

st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='welcome-text'>{L['welcome']}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#00FF00;'>● {L['slogan']}</p>", unsafe_allow_html=True)

# --- 6. CORE TABS ---
tab1, tab2, tab3 = st.tabs(["🗺️ Radar", L['portal'], L['revenue']])

with tab1:
    st.subheader(L['map_header'])
    # Live tracking map (Simulated for 54 countries)
    map_data = pd.DataFrame(
        np.random.randn(2, 2) / [50, 50] + [6.5244, 3.3792], 
        columns=['lat', 'lon']
    )
    st.map(map_data)
    st.info("Mechanic and User connection established.")

with tab2:
    st.subheader(L['cat'])
    # The 5 Core Categories
    service = st.selectbox("Current Operation", [
        "🚛 Truck Maintenance", "🚗 Car Repair", "⚙️ Diesel/Generator", 
        "📹 CCTV Systems", "☀️ Solar Engineering"
    ])
    st.text_area("Fix Details", placeholder="Enter specific fix details...")
    
    st.markdown(f"### 🤝 {L['bargain']}")
    # Fixed the KeyError by using the correct mapped key
    m_price = st.number_input(L['m_price'], min_value=0.0)
    
    if m_price > 0:
        # Founder 15% Share logic
        commission = m_price * 0.15
        total = m_price + commission
        st.write(f"**{L['share']}:** ${commission:,.2f}")
        st.success(f"**{L['final']}:** ${total:,.2f}")

with tab3:
    st.subheader("Empire Revenue")
    st.warning("Police/Security 2% payment: REMOVED")
    st.metric("Total Platform Revenue", "$0.00", "15% Share")

st.markdown("<br><p style='text-align: center; color: #444;'>Great Mech Engineering | Africa v2026</p>", unsafe_allow_html=True)
    
