import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CORE ENGINE CONFIG ---
st.set_page_config(page_title="Great Mech | Africa's Technical Pulse", page_icon="🌍", layout="centered")

# --- 2. GLOBAL STYLING (THE PITCH BLACK & GOLD AESTHETIC) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Branding Elements */
    .main-title { text-align: center; font-size: 48px; font-weight: 800; color: #D4AF37; letter-spacing: 4px; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 14px; color: #D4AF37; opacity: 0.8; letter-spacing: 2px; margin-top: -10px; margin-bottom: 30px; }
    
    /* Buttons & Inputs */
    .stButton>button { width: 100%; border-radius: 5px; background-color: #D4AF37; color: black; font-weight: bold; border: none; height: 3em; transition: 0.3s; }
    .stButton>button:hover { background-color: #AA8A2E; color: white; }
    
    /* Panic Button (ResQ X Style) */
    .sos-trigger { position: fixed; bottom: 20px; right: 20px; background: #FF0000; color: white; padding: 15px 25px; border-radius: 50px; font-weight: bold; z-index: 1000; text-decoration: none; box-shadow: 0 0 20px rgba(255,0,0,0.4); border: 2px solid white; }
    
    /* Clean receipt styling */
    .receipt-box { border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; background: #111; color: #EEE; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT (LOGIN & ROLES) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'role' not in st.session_state:
    st.session_state.role = "User"

# --- 4. LOGIN INTERFACE (THE FRONT GATE) ---
def login_page():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("316436.png", use_container_width=True) #
            except:
                st.image("https://img.icons8.com/isometric/512/africa.png", width=200)
            
            st.markdown("<div class='main-title'>GREAT MECH</div>", unsafe_allow_html=True)
            st.markdown("<div class='sub-title'>MOVING AFRICA TO THE NEXT LEVEL</div>", unsafe_allow_html=True)
            
            st.selectbox("Select Language", ["English", "Français", "Swahili", "Arabic", "Português"])
            
            user_mail = st.text_input("Sovereign ID (Email/Phone)")
            password = st.text_input("Security Key", type="password")
            
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("LOGIN"):
                if user_mail == "founder" and password == "greatmech2026": # Secure Founder access
                    st.session_state.auth = True
                    st.session_state.role = "Founder"
                    st.rerun()
                elif user_mail and password:
                    st.session_state.auth = True
                    st.session_state.role = "User"
                    st.rerun()
                else:
                    st.error("Please enter valid credentials.")
            
            if col_b2.button("CREATE ACCOUNT"):
                st.info("Account creation is currently reserved for authorized engineers.")

# --- 5. MAIN APPLICATION (USER INTERFACE) ---
def main_app():
    # Persistent SOS Button
    st.markdown('<a href="tel:911" class="sos-trigger">🆘 EMERGENCY SOS</a>', unsafe_allow_html=True)

    # Header
    st.markdown(f"<p style='text-align: right; color: #D4AF37;'>Role: <b>{st.session_state.role}</b> | 🔓 Secure Session</p>", unsafe_allow_html=True)
    
    if st.session_state.role == "Founder":
        st.sidebar.title("Founder Terminal")
        st.sidebar.warning("You are in Master Admin Mode.")
        if st.sidebar.button("Logout"):
            st.session_state.auth = False
            st.rerun()
        
        # Admin Stats
        st.sidebar.metric("Total Platform Revenue", "$142,500", "15% Net")
        st.sidebar.write("Police Tax (2%): **Disabled**")

    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["🛠️ Request Service", "📍 Live Radar", "🧾 Orders & Receipts"])

    with tab1:
        st.subheader("Initiate Engineering Magic")
        category = st.selectbox("Select Service Category", [
            "🚛 Heavy-Duty Truck Maintenance",
            "🚗 Luxury & Utility Car Repair",
            "⚙️ Diesel Engines & Generators",
            "📹 CCTV & Security Infrastructure",
            "☀️ Solar Energy Engineering"
        ]) #
        
        desc = st.text_area("Provide a detailed description of the mechanical issue...")
        
        st.markdown("### 🤝 Bargaining Terminal")
        mech_quote = st.number_input("Negotiated Price with Mechanic ($)", min_value=0.0, help="Enter the raw cost agreed with the on-site engineer.")
        
        if mech_quote > 0:
            # Automatic 15% Share Logic
            founder_share = mech_quote * 0.15
            final_invoice = mech_quote + founder_share
            
            st.markdown(f"""
            <div class='receipt-box'>
                <b>PROVISIONAL INVOICE</b><br>
                Service Category: {category}<br>
                Mechanic Base Cost: ${mech_quote:,.2f}<br>
                Service Platform Fee (15%): ${founder_share:,.2f}<br>
                <hr style='border:0.5px solid #D4AF37'>
                <b style='color:#D4AF37'>TOTAL PAYABLE: ${final_invoice:,.2f}</b>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("PROCEED TO PAYMENT PORTAL"):
                with st.spinner("Connecting to secure 54-country payment gateway..."):
                    time.sleep(2)
                    st.success("Payment Received Successfully!")
                    st.balloons()
                    # Generate Receipt logic
                    st.session_state.last_receipt = {
                        "cat": category,
                        "total": final_invoice,
                        "id": np.random.randint(10000, 99999)
                    }

    with tab2:
        st.subheader("Live Mechanic Radar")
        st.info("Tracking active engineers within your coordinates.")
        # Simulating user and mechanic location
        map_data = pd.DataFrame(
            np.random.randn(2, 2) / [60, 60] + [6.5244, 3.3792], 
            columns=['lat', 'lon']
        )
        st.map(map_data)

    with tab3:
        st.subheader("Transaction History")
        if 'last_receipt' in st.session_state:
            r = st.session_state.last_receipt
            st.markdown(f"""
            <div class='receipt-box'>
                <h3 style='color:#D4AF37; text-align:center;'>GREAT MECH OFFICIAL RECEIPT</h3>
                <p style='text-align:center;'>Order ID: #GM-{r['id']}</p>
                <hr>
                <b>Service:</b> {r['cat']}<br>
                <b>Status:</b> PAID IN FULL<br>
                <b>Platform Fee:</b> 15% Included<br>
                <b>Security:</b> 2% Police Tax Exempt<br>
                <hr>
                <h4 style='text-align:right;'>TOTAL: ${r['total']:,.2f}</h4>
                <p style='font-size:10px; text-align:center;'>Thank you for supporting African Engineering Magic.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("No recent transactions found.")

# --- 6. EXECUTION GATE ---
if not st.session_state.auth:
    login_page()
else:
    main_app()
            
