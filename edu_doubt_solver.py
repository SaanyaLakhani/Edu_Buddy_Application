import streamlit as st
import requests
import speech_recognition as sr
from deep_translator import GoogleTranslator
import whisper
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
import base64

# ------------------ CONFIG ------------------ #
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

# ------------------ SET BACKGROUND + CSS ------------------ #
def set_bg_from_image(img_path):
    with open(img_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown("""
    <style>
    /* Main headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0d1b5f !important;  /* Strong dark blue */
    }

    /* Subtitles or paragraph text */
    .subtitle, p, label, .css-1v0mbdj, .css-1kyxreq {
        color: #0d1b5f !important;
        font-weight: 500;
    }

    /* Sidebar title and dropdown */
    section[data-testid="stSidebar"] .css-1lcbmhc, .stSelectbox > div {
        color: #0d1b5f !important;
        font-weight: bold !important;
    }

    /* Input radio buttons and labels */
    .stRadio div[role='radiogroup'] > label {
        color: #0d1b5f !important;
        font-weight: bold !important;
    }

    /* Text input fields */
    .stTextInput input {
        background-color: #fff !important;
        color: #0d1b5f !important;
        border: 1px solid #0d1b5f !important;
        border-radius: 8px;
    }

    /* Button styling */
    .stButton > button {
        background-color: rgb(255, 0, 102) !important;  /* Deep pink */
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #880e4f !important;
    }

    </style>
""", unsafe_allow_html=True)

set_bg_from_image("book1.jpg")  # Ensure the image file is in the same directory

# ------------------ FUNCTIONS ------------------ #
def transcribe_voice():
    st.info("🎤 Listening for 5 seconds...")
    fs = 44100
    duration = 5
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        write(tmp_file.name, fs, recording)
        model = whisper.load_model("base")
        result = model.transcribe(tmp_file.name)
        return result["text"]

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def translate_from_english(text, target_lang):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

def ask_llm(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful education assistant."},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"API Error: {e}"

# ------------------ UI ------------------ #
st.markdown('<h1 style="text-align:center;">🎓 Edu Doubt Solver</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align:center;">Ask questions in any language using text or voice 🎤</h4>', unsafe_allow_html=True)

st.markdown('<div class="input-box">', unsafe_allow_html=True)

input_method = st.radio("Choose Input Method:", ["📝 Text", "🎤 Voice"])
user_question = ""

if input_method == "📝 Text":
    user_question = st.text_input("Type your question:")
elif input_method == "🎤 Voice":
    if st.button("🎙️ Start Recording"):
        user_question = transcribe_voice()
        st.success(f"Recognized: {user_question}")

st.markdown('</div>', unsafe_allow_html=True)

target_lang = st.selectbox("🌐 Choose Answer Language:", ["English", "Hindi", "Gujarati", "Marathi", "Tamil", "Telugu", "Bengali"])
lang_codes = {
    "English": "en", "Hindi": "hi", "Gujarati": "gu",
    "Marathi": "mr", "Tamil": "ta", "Telugu": "te", "Bengali": "bn"
}

if user_question:
    translated_q = translate_to_english(user_question)
    llm_response = ask_llm(translated_q)
    translated_a = translate_from_english(llm_response, lang_codes[target_lang])

    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
    st.markdown("#### ✅ Answer:")
    st.success(translated_a)
    st.markdown('</div>', unsafe_allow_html=True)

