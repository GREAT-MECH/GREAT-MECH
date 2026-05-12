import streamlit as st
import time

# --- 1. CONFIGURE PAGE ---
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

# --- 8. INPUT FIELD ---
user_input = st.text_input("Your Ideas for Innovation:", placeholder="Share your thoughts...")

# --- 9. LOADING ANIMATION ---
if st.button("Submit"):
    with st.spinner('Processing your input...'):
        time.sleep(2) # Simulate processing time
    st.success(f"Thank you for your input: '{user_input}'")

# --- 10. ADDITIONAL CONTENT ---
st.subheader("Our Services")
st.write("We provide solutions in engineering, technology development, and much more.")

# --- 11. FOOTER ---
st.markdown("""
<style>
footer {
    display: none;
}
</style>
""", unsafe_allow_html=True)

### Key Features of the Updated Code:
