import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. PRESTIGE UI ---
st.set_page_config(page_title="Great Mech | v126.0", page_icon="🌍")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 12px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SOVEREIGN ENGINE ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # worksheet="Users" MUST exist as a tab name on your phone sheet
    return conn.read(worksheet="Users", ttl=0)

# --- 3. GATEWAY ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    t1, t2 = st.tabs(["🔒 LOGIN", "🛠️ REGISTER"])

    with t1:
        l_email = st.text_input("Email", key="l_email")
        l_pin = st.text_input("PIN", type="password", key="l_pin")
        if st.button("ACTIVATE SESSION"):
            try:
                df = get_data()
                match = df[(df['Email'] == l_email) & (df['PIN'].astype(str) == l_pin)]
                if not match.empty:
                    st.session_state.user = match.iloc[0].to_dict()
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except Exception as e:
                st.error(f"Read Error: {e}")

    with t2:
        r_name = st.text_input("Full Name", key="r_name")
        r_email = st.text_input("Email", key="r_email")
        r_phone = st.text_input("Phone", key="r_phone")
        r_role = st.selectbox("Role", ["User", "Mechanic"], key="r_role")
        r_pin = st.text_input("PIN", type="password", max_chars=4, key="r_pin")

        if st.button("CREATE PERMANENT ACCOUNT"):
            try:
                # 1. Fetch current data
                current_df = get_data()
                
                # 2. Add new user
                new_row = pd.DataFrame([{
                    "Email": r_email, "Name": r_name, "PIN": r_pin, 
                    "Role": r_role, "Phone": r_phone
                }])
                updated_df = pd.concat([current_df, new_row], ignore_index=True)
                
                # 3. PUSH TO GOOGLE
                conn.update(worksheet="Users", data=updated_df)
                st.cache_data.clear()
                st.success("Sovereign Account Secured! Go to Login.")
            except Exception as e:
                # This will tell us the EXACT technical error
                st.error(f"Technical Block: {e}")
                st.info("Check: Tab name must be 'Users' and Secrets 'read_only = false'")

# --- 4. DASHBOARD ---
else:
    u = st.session_state.user
    st.sidebar.success(f"Verified: {u['Name']}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()
    st.markdown(f"## Great Mech Engine: Online")
    st.write(f"Welcome, {u['Name']}. Ready to move Africa to the next level.")
                
