import streamlit as st
import pandas as pd
import random
import base64

# Streamlit config
#st.set_page_config(page_title="Motivational Buddy", layout="centered")

# Background setup
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background(image_path):
    encoded = get_base64_of_image(image_path)
    st.markdown(f"""
    <style>
    [data-testid="stApp"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: #fff;
    }}

    .header {{
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(to right, #d4a373, #bc6c25);
        color: white;
        padding: 12px 25px;
        border-radius: 10px;
        display: inline-block;
    }}

    .subtext {{
        font-size: 18px;
        font-weight: bold;
        color: #f1f1f1;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }}

    .main-text {{
        font-size: 20px;
        font-weight: bold;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        color: #ffffff;
    }}

    .motivation-box {{
        font-size: 18px;
        font-weight: bold;
        background-color: #ffe6f0;
        color: #000000;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }}

    .stButton > button {{
        background-color: #d63384;
        color: white;
        font-weight: bold;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        transition: 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #b52c6e;
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# Set your calming background
set_background("calm.jpg")

# Load motivational quotes
df = pd.read_csv("motivational_quotes_dataset.csv")

# UI
st.markdown("""
<div style="
    background: #bc6c25;
    display: inline-block;
    padding: 8px 20px;
    border-radius: 10px;
    font-size: 24px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin: 0 auto 10px auto;
    width: fit-content;
">
Motivational Buddy Agent
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='subtext'>Get personalized encouragement when you're feeling low or overwhelmed. 🗨️</p>", unsafe_allow_html=True)

user_input = st.text_input("Tell me how you're feeling:")

if st.button("💖 Send Motivation"):
    if not user_input.strip():
        st.warning("Please share how you're feeling to receive motivation.")
    else:
        quote = df.sample(1).iloc[0]['quote']
        st.markdown(f"<div class='motivation-box'>💬 {quote}</div>", unsafe_allow_html=True)
else:
    st.markdown("<p class='main-text'>👉 Enter your feelings and receive a personalized motivational message.</p>", unsafe_allow_html=True)
