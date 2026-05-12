import streamlit as st
import time

# --- 1. GLOBAL ENGINE START ---
# This MUST be the first command to prevent the NameError
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. LANGUAGE TRANSLATION ENGINE ---
# This ensures the app actually changes when you select a language
languages = {
    "English": {
        "slogan": "Moving Africa to the next level...",
        "status": "● System Secure across 54 Countries",
        "tab1": "🏛️ Identity", "tab2": "🛠️ Service Portal", "tab3": "💰 Revenue",
        "cat": "Select Category", "desc": "Issue Description", "bargain": "Bargaining Terminal",
        "mech_p": "Mechanic Price ($)", "share": "Your 15% Share", "total": "Final User Price"
    },
    "Français": {
        "slogan": "Faire passer l'Afrique au niveau supérieur...",
        "status": "● Système sécurisé dans 54 pays",
        "tab1": "🏛️ Identité", "tab2": "🛠️ Portail de services", "tab3": "💰 Revenu",
        "cat": "Choisir une catégorie", "desc": "Description du problème", "bargain": "Terminal de négociation",
        "mech_p": "Prix du mécanicien ($)", "share": "Votre part de 15%", "total": "Prix final pour l'utilisateur"
    },
    "Swahili": {
        "slogan": "Kuiongoza Afrika katika kiwango kingine...",
        "status": "● Mfumo ni Salama katika nchi 54",
        "tab1": "🏛️ Utambulisho", "tab2": "🛠️ Huduma", "tab3": "💰 Mapato",
        "cat": "Chagua Kitengo", "desc": "Maelezo ya Tatizo", "bargain": "Eneo la Majadiliano",
        "mech_p": "Bei ya Fundi ($)", "share": "Gawio lako la 15%", "total": "Bei ya Mwisho ya Mtumiaji"
    }
}

# --- 3. PREMIUM UI STYLING (CSS) ---
st.markdown("""
<style>
    /* Kill the '0' artifact and background ghosts */
    .stApp { background-color: #050505 !important; color: white !important; }
    div.block-container { padding-top: 2rem; }
    
    .main-title {
        text-align: center; font-size: 55px; font-weight: 900; 
        color: #D4AF37; letter-spacing: 5px; margin-top: -20px;
    }
    
    .typing-text {
        color: #D4AF37; font-size: 20px; font-weight: bold; text-align: center;
        border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden;
        margin: 0 auto; width: fit-content; animation: typing 3.5s steps(30, end) infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }

    .sos-btn {
        position: fixed; bottom: 30px; right: 30px; background-color: #FF0000;
        color: white; padding: 20px 30px; border-radius: 50px; font-weight: bold;
        z-index: 9999; text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP BAR: LANGUAGE SELECTOR ---
st.markdown('<a href="tel:911" class="sos-btn">🆘 SOS PANIC</a>', unsafe_allow_html=True)

col_a, col_b = st.columns([4, 1.2])
with col_b:
    sel_lang = st.selectbox("🌐", list(languages.keys()))
    t = languages[sel_lang] # Load the chosen language dictionary

# --- 5. THE BRANDING CORE (FIXED LOGO & NO '0') ---
# Use a clear container to prevent layout leaks
with st.container():
    l_col, m_col, r_col = st.columns([1, 1.8, 1])
    with m_col:
        try:
            st.image("316436.png", use_container_width=True)
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=250)

st.markdown(f"<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='typing-text'>{t['slogan']}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#00FF00;'>{t['status']}</p>", unsafe_allow_html=True)

# --- 6. SOVEREIGN WORKFLOW ---
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.subheader("Founder's Entry")
    st.text_input("Name", placeholder="Founder Credentials")
    st.button("ENTER EMPIRE")

with tab2:
    st.subheader(t['cat'])
    # Core 5 Categories [cite: 2026-05-08]
    st.selectbox("Service", [
        "🚛 Heavy Truck", "🚗 Luxury Car", "⚙️ Diesel/Generator", 
        "📹 CCTV Systems", "☀️ Solar Engineering"
    ])
    st.text_area(t['desc'])
    
    st.markdown(f"### 🤝 {t['bargain']}")
    m_price = st.number_input(t['mech_p'], min_value=0.0)
    
    if m_price > 0:
        # Founder Share logic (15%) [cite: 2026-05-08]
        share = m_price * 0.15
        total = m_price + share
        st.info(f"{t['share']}: **${share:,.2f}**")
        st.success(f"{t['total']}: **${total:,.2f}**")

with tab3:
    st.subheader("Financial Hub")
    st.write("2% Police Payment: **REMOVED** [cite: 2026-05-08]")
    st.metric("Total Revenue Share", "$0.00", "15%")

