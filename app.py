import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Great Mech Global", layout="wide", page_icon="🦾")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # We use ttl=0 to ensure we always get the freshest data from the cloud
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=['ID', 'Service', 'Budget', 'Status', 'Location', 'Timestamp'])

# Load the current ledger
if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- APP INTERFACE ---
st.title("🦾 GREAT MECH SUPREME")

tab1, tab2 = st.tabs(["🚀 Deploy Job", "📊 Global Ledger"])

with tab1:
    with st.form("job_form"):
        service = st.selectbox("Category", ["Diesel Engine", "Solar Power", "Truck Repair"])
        budget = st.number_input("Budget (NGN)", min_value=5000)
        submit = st.form_submit_button("DEPLOY TO CLOUD")
        
        if submit:
            new_entry = pd.DataFrame([{
                "ID": f"GM-{random.randint(1000, 9999)}",
                "Service": service,
                "Budget": budget,
                "Status": "Pending",
                "Location": "Lagos",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            try:
                # Attempt to update Google Sheets
                updated_df = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                conn.update(data=updated_df)
                st.session_state.db = updated_df
                st.success("Vision Unified: Job Saved to Google Cloud!")
                st.balloons()
            except Exception as e:
                # If Google blocks the write, we save it locally so the Founder can see it
                st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                st.warning("Local Save: App is live, but check Google Sheet 'Editor' permissions.")

with tab2:
    st.subheader("Current Empire Volume")
    st.dataframe(st.session_state.db, use_container_width=True)

