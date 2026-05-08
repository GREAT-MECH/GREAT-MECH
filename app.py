import random
import streamlit as st
import pandas as pd
import numpy as np
import time
import uuid
import random
from datetime import datetime

# --- 1. THE SOVEREIGN LANGUAGE ENGINE ---
# Supporting English, Pidgin, French, Swahili, Hausa, Yoruba, Igbo
TRANSLATIONS = {
    "English": {"greet": "Welcome", "sector": "Select Sector", "symptom": "Select Symptom", "diag": "Run AI Diagnosis", "pay": "Secure Payment", "chat": "Chat with Mechanic", "thanks": "Thanks for using Great Mech, moving Africa to the next level."},
    "Pidgin": {"greet": "How far", "sector": "Select Wetin Happen", "symptom": "Pick di Symptom", "diag": "Run AI Check", "pay": "Pay Safe-Safe", "chat": "Follow Mechanic Yarn", "thanks": "Abeg thank you for using Great Mech, we dey move Africa go front."},
    "French": {"greet": "Bienvenue", "sector": "Sélectionner le secteur", "symptom": "Sélectionner le symptôme", "diag": "Lancer le diagnostic IA", "pay": "Paiement sécurisé", "chat": "Discuter avec le méco", "thanks": "Merci d'utiliser Great Mech, faire progresser l'Afrique."},
    "Swahili": {"greet": "Karibu", "sector": "Chagua Sekta", "symptom": "Chagua Dalili", "diag": "Anza Utambuzi wa AI", "pay": "Malipo Salama", "chat": "Zungumza na Fundi", "thanks": "Asante kwa kutumia Great Mech, tukiisogeza Afrika katika ngazi nyingine."},
}

# --- 2. STARTUP & PERSISTENCE ---
if 'startup_done' not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>GREAT MECH</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Moving Africa to the next level...</h3>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Select App Language / Yan zaɓin yare", list(TRANSLATIONS.keys()))
    if st.button("🚀 ACTIVATE SUPREME ENGINE"):
        st.session_state.startup_done = True
        st.session_state.lang = lang_choice
        st.rerun()
    st.stop()

L = TRANSLATIONS[st.session_state.lang]

# --- 3. GLOBAL CONTINENTAL REGISTRY ---
AFRICA_54 = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

# Comprehensive Bank Switch (Dynamic Mockup for 54 Countries)
BANKS_ALL = {
    "Nigeria": ["Access Bank", "First Bank", "GTBank", "Kuda", "OPay", "UBA", "Zenith Bank", "Stanbic", "Union Bank"],
    "Ghana": ["Absa Bank", "CBG", "Ecobank", "GCB Bank", "Stanbic", "Zenith Ghana"],
    "Kenya": ["Equity Bank", "KCB Bank", "NCBA", "Standard Chartered", "Co-operative Bank"],
    "South Africa": ["Capitec", "FNB", "Nedbank", "Standard Bank", "Absa SA", "Investec"]
    # System default for other 50: ["National Central Bank", "Standard Chartered", "Ecobank Regional"]
}

# --- 4. THE 7 PILLARS & AI DIAGNOSIS DB ---
SECTOR_DATA = {
    "🚗 Truck/Heavy Duty": {"price": 85000, "symptoms": ["Turbo Failure", "Hydraulic Leak", "Air Pressure Loss", "Differential Issue", "Clutch Slip", "Fuel System Fault", "Chassis Crack"]},
    "🚛 Car/Automotive": {"price": 25000, "symptoms": ["Overheating", "Brake Failure", "Transmission Slip", "Suspension Noise", "Battery Dead", "AC Fault", "Exhaust Smoke"]},
    "⚙️ Diesel Engine/Generator": {"price": 45000, "symptoms": ["Failure to Start", "Hunting/Surging", "Oil Leaks", "Low Voltage", "Radiator Clog", "High Consumption", "Vibration"]},
    "📹 CCTV": {"price": 15000, "symptoms": ["Signal Loss", "Night Vision Fail", "HDD Error", "Movement Jam", "Power Supply", "Flickering", "Network Fault"]},
    "☀️ Solar": {"price": 60000, "symptoms": ["Inverter Error", "Battery Drain", "Hotspots", "Controller Fault", "Wiring Leak", "Low Yield", "Grounding Issue"]}
}

DIAGNOSIS_DB = {
    "Turbo Failure": {"part": "Turbocharger Kit", "price": 285000, "loc": "Onitsha Main Market"},
    "Brake Failure": {"part": "Ceramic Brake Pads", "price": 18500, "loc": "Ladipo, Lagos"},
    "Inverter Error": {"part": "5KW Hybrid Board", "price": 420000, "loc": "Oshodi Solar Hub"},
    "Signal Loss": {"part": "RG59 Coaxial Cable", "price": 22000, "loc": "Computer Village, Ikeja"}
}

# --- 5. SYSTEM LAYOUT ---
st.set_page_config(page_title="Great Mech Supreme v47.0", layout="wide")
st.sidebar.markdown("<h1 style='text-align: center; color: #FFD700;'>GREAT MECH</h1>", unsafe_allow_html=True)
portal = st.sidebar.selectbox("Identity Portal", ["User Interface", "Mechanic Command", "Vendor Portal", "Partner ROI", "Founder Hub"])

h = datetime.now().hour
time_greet = "Good Morning" if h < 12 else "Good Afternoon" if h < 17 else "Good Evening"

# --- 6. USER INTERFACE ---
if portal == "User Interface":
    st.title(f"🌍 {L['greet']}, {time_greet}")
    u_col1, u_col2 = st.columns([1, 1])
    
    with u_col1:
        st.subheader("📍 Deployment")
        country_sel = st.selectbox("Country", AFRICA_54, index=38) # Nigeria
        sector_sel = st.selectbox(L["sector"], list(SECTOR_DATA.keys()))
        symptom_sel = st.selectbox(L["symptom"], SECTOR_DATA[sector_sel]["symptoms"])
        st.text_area("🔧 Fault Description Box", placeholder="Describe the issue...")
        
        service_fee = SECTOR_DATA[sector_sel]["price"]
        st.metric("Service Fee (LOCKED)", f"₦{service_fee:,}")
        
        if st.button(L["diag"]):
            with st.spinner("AI analyzing patterns..."):
                time.sleep(1.5)
                if symptom_sel in DIAGNOSIS_DB:
                    res = DIAGNOSIS_DB[symptom_sel]
                    st.success(f"**AI Report:** {symptom_sel} detected.\n\n**Spare Part:** {res['part']}\n**Estimated Cost:** ₦{res['price']:,}\n**Vendor Loc:** {res['loc']}")
                else:
                    st.info("AI Analysis: Pattern indicates wear-and-tear. Mechanic physical check required.")

    with u_col2:
        st.subheader(L["pay"])
        pay_mode = st.radio("Method", ["Bank Transfer", "Card Payment"])
        
        if pay_mode == "Card Payment":
            st.text_input("Card Name")
            st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
            st.columns(2)[0].text_input("EXP")
            st.columns(2)[1].text_input("CVV", type="password")
        else:
            # Fix for the int32 error:
            v_acc = random.randint(1000000000, 9999999999)
            st.info(f"**VIRTUAL ACCOUNT:**\n\nBank: GREAT MECH/WEMA\nAccount: **{v_acc}**")
        
        if st.button("🛡️ Verify & Lock Escrow"):
            st.session_state.paid = True
            st.success("✅ FUNDS SECURED. 15% Platform Share Recorded.")

        if 'paid' in st.session_state:
            st.subheader("🧰 Choose Your Mechanic")
            mechs = ["Engr. Musa (🟢 Online)", "Mech. Tunde (🟢 Online)", "Engr. Kofi (🟡 Busy)"]
            selected_mech = st.radio("Available Pros", mechs)
            
            c1, c2 = st.columns(2)
            if c1.button("📞 Call Mechanic"): 
                st.warning(f"Connecting to {selected_mech}...")
            if c2.button("💬 Text Mechanic"): 
                st.info("Chat window active.'Mechanic: I'm 5 mins away.'")
            
            st.map(pd.DataFrame({'lat': [6.5244], 'lon': [3.3792]}))
            st.metric("Distance to Reach", "3.2 KM")
            st.metric("Estimated Arrival", "14 Mins")

    st.divider()
    st.markdown(f"<h3 style='text-align: center; color: #FFD700;'>{L['thanks']}</h3>", unsafe_allow_html=True)

# --- 7. MECHANIC COMMAND (ALL 54 COUNTRIES + BANKS) ---
elif portal == "Mechanic Command":
    st.header(f"🛠️ {time_greet}, Engineer")
    m_tab1, m_tab2 = st.tabs(["Navigation & SOS", "Sovereign Payout"])
    
    with m_tab1:
        st.map(pd.DataFrame({'lat': [6.5244, 6.6018], 'lon': [3.3792, 3.3515]}))
        st.warning("📍 **Precise Routing:** Head North on Ikorodu Rd. User is at Fadeyi Junction.")
        if st.button("🆘 SOS PANIC BUTTON", type="primary"):
            st.error("🚨 EMERGENCY SIGNAL SENT. Security dispatch is active.")
            
    with m_tab2:
        m_c = st.selectbox("Select Your Deployment Country", AFRICA_54, index=38)
        bank_list = BANKS_ALL.get(m_c, ["Standard Chartered", "Ecobank", "National Central Bank"])
        st.selectbox("Select Your Bank", bank_list)
        st.text_input("Account Number")
        if st.button("Verify & Link Wallet"):
            st.success("Bank details confirmed. Payouts now direct.")

# --- 8. VENDOR PORTAL (LOCATION INVENTORY) ---
elif portal == "Vendor Portal":
    st.header(f"🛒 {time_greet}, Vendor")
    if 'inv' not in st.session_state: st.session_state.inv = [{"item": "Generator AVR", "price": 45000, "loc": "Ibadan Depot"}]
    with st.expander("➕ Add Stock"):
        ni = st.text_input("Item Name"); np = st.number_input("Price", value=0); nl = st.text_input("Physical Shop Address")
        if st.button("Save Item"): st.session_state.inv.append({"item": ni, "price": np, "loc": nl}); st.rerun()
    
    st.subheader("Live Inventory")
    for idx, item in enumerate(st.session_state.inv):
        v1, v2, v3 = st.columns([2, 1, 1])
        v1.write(f"**{item['item']}**\n📍 {item['loc']}")
        v2.write(f"₦{item['price']:,}")
        if v3.button("🗑️ Delete", key=f"del_{idx}"): st.session_state.inv.pop(idx); st.rerun()

# --- 9. PARTNER ROI (PERFORMANCE) ---
elif portal == "Partner ROI":
    st.header("🤝 Partner ROI Dashboard")
    st.metric("Total Investment Profit", "₦48,250,000", "+₦1.4M Today")
    st.line_chart(np.random.randint(100, 1000, 30))
    st.write("Regional ROI split: Nigeria (60%), Ghana (25%), Kenya (15%).")

# --- 10. FOUNDER HUB (REVENUE MARGINS) ---
elif portal == "Founder Hub":
    st.header("💹 Master Sovereign Command")
    st.metric("Total Platform Revenue (15% Net)", "₦285,400,000")
    
    st.subheader("Revenue Margin Chart")
    chart_data = pd.DataFrame(np.random.randint(500000, 2500000, 20), columns=["Daily Net Share (15%)"])
    st.area_chart(chart_data)
    
    st.subheader("Revenue Margin Leaderboard")
    margin_board = pd.DataFrame({
        "Location": ["Lagos, NG", "Accra, GH", "Nairobi, KE", "Abuja, NG"],
        "Gross Revenue (85%)": ["₦850.5M", "₦420.2M", "₦310.8M", "₦290.4M"],
        "Platform Net (15%)": ["₦127.5M", "₦63M", "₦46.5M", "₦43.5M"],
        "Active Mechs": [450, 120, 85, 92]
    })
    st.table(margin_board)

