import streamlit as st
import time

# --- 1. CONFIGURE THE PAGE ---
st.set_page_config(page_title="Great Mech", page_icon="🌍", layout="centered")

# --- 2. DEFINE STYLES ---
st.markdown("""
<style>
body {
    background-color: #101010;
    color: #FFD700;
}
h1 {
    font-size: 2.5em;
    text-align: center;
    font-weight: bold;
}
.sidebar .sidebar-content {
    background-color: #333;
}
footer {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# --- 3. LANGUAGE TRANSLATION DATA ---
languages = {
    "English": {"slogan": "Moving Africa to the next level..."},
    "French": {"slogan": "Faire avancer l'Afrique au niveau supérieur..."},
    "Spanish": {"slogan": "Llevando a África al siguiente nivel..."}
}

# --- 4. SIDEBAR FOR LANGUAGE SELECTION ---
st.sidebar.header("Select Language")
selected_language = st.sidebar.selectbox("Choose a language", options=list(languages.keys()))

# --- 5. DISPLAY SELECTED LANGUAGE SLOGAN ---
slogan = languages[selected_language]['slogan']
st.title(slogan)

# --- 6. LOGO DISPLAY ---
st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://example.com/africa_logo.png" alt="Africa Logo" style='width: 200px;'>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 7. APP DESCRIPTION ---
st.write("Welcome to Great Mech! We are dedicated to innovation and improvement in technology.")
st.write("Here, we aim to provide resources and support for advancing various fields within Africa.")

# --- 8. INPUT FIELD FOR USER IDEAS ---
user_input = st.text_input("Your Ideas for Innovation:", placeholder="Share your thoughts...")

# --- 9. SUBMIT BUTTON WITH PROCESSING ANIMATION ---
if st.button("Submit"):
    if user_input: # Check if input is not empty
        with st.spinner('Processing your input...'):
            time.sleep(2) # Simulate processing time
        st.success(f"Thank you for your input: '{user_input}'")
    else:
        st.error("Please enter your ideas before submitting.")

# --- 10. ADDITIONAL CONTENT ---
st.subheader("Our Services")
st.write("We provide solutions in engineering, technology development, and much more.")
st.write("Explore innovative technologies, workshops, and partnerships designed to elevate African enterprises.")

# --- 11. COLLECT USER FEEDBACK ---
if st.button("Give Feedback"):
    feedback = st.text_area("Your Feedback:", placeholder="What do you think about Great Mech?")
    if st.button("Submit Feedback"):
        with st.spinner('Submitting feedback...'):
            time.sleep(2)
        st.success("Your feedback has been submitted. Thank you!")

# --- 12. CONCLUSION AND FUTURE PLANS ---
st.markdown("""
We are continuously working to improve our platform. Stay tuned for updates and new features!
""")

# --- 13. FOOTER --- 
st.markdown("""
<div style='text-align: center;'>
    <small>&copy; 2026 Great Mech. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)
