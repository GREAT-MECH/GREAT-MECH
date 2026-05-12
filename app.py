import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. SOVEREIGN ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech | Sidebar Command", page_icon="🌍", layout="wide")

# --- 2. MASTER AESTHETIC (CSS) ---
st.markdown("""
<style>
    /* Dark Mode Sovereignty */
    .stApp { background-color: #050505; color: #FFFFFF; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #D4AF37;
        width: 350px !important;
    }
    
    /* Global Gold Accents */
    .main-title { text-align: center; font-size: 50px; font-weight: 900; color: #D4AF37; letter-spacing: 5px; margin-top: -20px; }
    .sub-title { text-align: center; font-size: 14px; color: #D4AF37; opacity: 0.8; letter-spacing: 2px; margin-bottom: 30px; }
    
    /* Panic Button Styling */
    .sos-trigger {
        display: block; text-align: center; background: #FF0000; color: white; 
        padding: 15px; border-radius: 10px; font-weight: bold; text-decoration: none;
        margin-top: 20px; border: 1px solid white; box-shadow: 0 0 15px rgba(255,0,0,0.4);
    }
    
    /* Professional Receipt */
    .receipt-card { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background: #000; color: #FFF; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION AUTHENTICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "User"

# --- 4. THE LOGIN GATEWAY ---
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("316436.png", use_container_width=True)
        except:
            st.image("https://img.icons8.com/isometric/512/africa.png", width=200)
        
        st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
        
        user = st.text_input("Sovereign ID")
        key = st.text_input("Security Key", type="password")
        
        if st.button("AUTHORIZE ACCESS"):
            if user == "founder" and key == "greatmech2026":
                st.session_state.authenticated = True
                st.session_state.user_role = "Founder"
                st.rerun()
            elif user and key:
                st.session_state.authenticated = True
                st.session_state.user_role = "User"
                st.rerun()

# --- 5. THE SIDEBAR COMMAND CENTER ---
def sidebar_navigation():
    with st.sidebar:
        # Branding in Sidebar
        try:
            st.image("316436.png", width=100)
        except:
            pass
        st.markdown("<h2 style='color:#D4AF37; margin-bottom:0;'>GREAT MECH</h2>", unsafe_allow_html=True)
        st.write(f"🌍 Status: **54 Countries Active**")
        st.write(f"👤 Role: **{st.session_state.user_role}**")
        st.divider()

        # NAVIGATION MENU
        menu = st.radio(
            "COMMAND MENU",
            ["🛠️ Service Terminal", "📡 Live Radar", "🧾 Secure Receipts", "📊 Revenue Analytics"]
        )
        
        st.divider()
        
        # FOUNDER CONTROLS (Only visible to you)
        if st.session_state.user_role == "Founder":
            st.markdown("<p style='color:#D4AF37;'><b>FOUNDER OVERRIDE</b></p>", unsafe_allow_html=True)
            st.metric("Total Platform Net (15%)", "$240,500")
            st.info("Police Tax (2%): DEACTIVATED")
        
        # LOGOUT & SOS
        if st.button("End Session"):
            st.session_state.authenticated = False
            st.rerun()
            
        st.markdown('<a href="tel:911" class="sos-trigger">🆘 SOS PANIC BUTTON</a>', unsafe_allow_html=True)
        
        return menu

# --- 6. MAIN APPLICATION MODULES ---
def main_runtime(selection):
    # Main stage branding (Centered)
    st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D4AF37;'>Engineering Magic Built for Africa</p>", unsafe_allow_html=True)
    st.divider()

    if selection == "🛠️ Service Terminal":
        st.subheader("New Engineering Request")
        col_a, col_b = st.columns(2)
        with col_a:
            cat = st.selectbox("Category", ["🚛 Truck", "🚗 Car", "⚙️ Diesel/Generator", "📹 CCTV", "☀️ Solar"])
        with col_b:
            mech_name = st.text_input("Mechanic ID/Name")
            
        desc = st.text_area("Mechanical Issue Details")
        
        st.markdown("### 🤝 Bargaining Terminal")
        price = st.number_input("Negotiated Price with Mechanic ($)", min_value=0.0)
        
        if price > 0:
            platform_fee = price * 0.15 #
            total = price + platform_fee
            st.markdown(f"""
            <div class='receipt-card'>
                <b>PROVISIONAL INVOICE</b><br>
                Service Charge: ${price:,.2f}<br>
                Founder Share (15%): ${platform_fee:,.2f}<br>
                Security/Police (2%): $0.00 (EXEMPT)<br>
                <hr>
                <h3 style='color:#D4AF37;'>TOTAL: ${total:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("PROCESS TRANSACTION"):
                st.success("Transmitting Engineering Order...")
                st.session_state.last_tx = {"cat": cat, "total": total, "id": np.random.randint(100, 999)}

    elif selection == "📡 Live Radar":
        st.subheader("Mechanic-User Synchronization")
        map_data = pd.DataFrame(
            np.random.randn(3, 2) / [50, 50] + [6.5244, 3.3792],
            columns=['lat', 'lon']
        )
        st.map(map_data)
        st.info("Currently tracking 3 mechanics in your immediate radius.")

    elif selection == "🧾 Secure Receipts":
        st.subheader("Official Transaction Records")
        if 'last_tx' in st.session_state:
            tx = st.session_state.last_tx
            st.markdown(f"""
            <div class='receipt-card'>
                <h3 style='text-align:center; color:#D4AF37;'>GREAT MECH RECEIPT</h3>
                <p style='text-align:center;'>ID: #GM-{tx['id']}</p>
                <hr>
                <b>Category:</b> {tx['cat']}<br>
                <b>Status:</b> PAID IN FULL<br>
                <b>Exemption:</b> 2% Police Payment Removed<br>
                <hr>
                <h2 style='text-align:right;'>${tx['total']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("No payment records found in this session.")

    elif selection == "📊 Revenue Analytics":
        st.subheader("Platform Sovereignty Metrics")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Active Jobs", "1,245", "Africa Wide")
        col_m2.metric("Founder Share", "15%", "Fixed")
        st.bar_chart(np.random.randn(10, 2))

# --- 7. RUNTIME EXECUTION ---
if not st.session_state.authenticated:
    login_screen()
else:
    choice = sidebar_navigation()
    main_runtime(choice)
            
