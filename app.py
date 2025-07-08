import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PyPDF2 import PdfReader
import requests
import speech_recognition as sr
from deep_translator import GoogleTranslator
import wikipedia
from openai import OpenAI
import random
import base64

# --- Streamlit Page Setup ---
st.set_page_config(page_title="EduMentor AI", layout="centered")

# --- Custom CSS for Sidebar Dropdown Styling ---
st.markdown("""
    <style>
    .sidebar .stSelectbox > div > select {
        background-color: #e0f7fa;
        color: #004d40;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #1f3c88;
        width: 100%;
        text-align: center;
    }
    .sidebar .stSelectbox > div > select:focus {
        background-color: #b2ebf2;
    }
    .sidebar .stSelectbox > div {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Dropdown Menu for Feature Selection ---
st.sidebar.markdown("<h2 style='text-align:center; color:#1f3c88;'>EduMentor AI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align:center; color:#ff4b4b;'>Select a Feature</h4>", unsafe_allow_html=True)

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Edu Content Summarizer",
        "Edu Doubt Solver",
        "Exam Paper Generator",
        "Motivational Buddy",
        "Study Planner"
    ],
    index=0,
    key="feature_select",
    help="Select a feature to get started!"
)

# --- Main Content Header ---
st.markdown("<h1 style='text-align:center; color:#1f3c88;'>EduMentor AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#ff4b4b;'>Your All-in-One Educational Companion</h4>", unsafe_allow_html=True)

# --- Edu Content Summarizer ---
if feature == "Edu Content Summarizer":
    # 🌸 Custom Styling for Soft Purple Theme
    st.markdown("""
        <style>
            body {
                background-color: #f8f3f9;
            }
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #f8f3f9 0%, #ffffff 100%);
            }
            h1, h2, h3, h4 {
                color: #6a1b9a;
            }
            .stRadio > div {
                flex-direction: row;
            }
            .stRadio label, .stMarkdown h3 {
                font-size: 16px;
                color: #4A148C;
            }
            .stRadio div[role="radiogroup"] > label {
                background-color: #f3e5f5;
                border-radius: 8px;
                padding: 4px 10px;
                margin-right: 8px;
                border: 1px solid #d1c4e9;
            }
            .stRadio div[role="radiogroup"] > label:hover {
                background-color: #ede7f6;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>📚 Edu Content Summarizer</h1>", unsafe_allow_html=True)

    @st.cache_resource
    def load_model():
        tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
        model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
        return tokenizer, model

    tokenizer, model = load_model()

    def summarize(text, length_option):
        settings = {
            "Short": {"max_length": 80, "min_length": 30},
            "Medium": {"max_length": 150, "min_length": 60},
            "Long": {"max_length": 250, "min_length": 100},
        }
        config = settings.get(length_option, settings["Medium"])
        inputs = tokenizer([text], max_length=1024, truncation=True, return_tensors="pt")
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=config["max_length"],
            min_length=config["min_length"],
            early_stopping=True,
        )
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()

    def extract_text_from_pdf(file):
        pdf = PdfReader(file)
        return "".join(page.extract_text() or "" for page in pdf.pages)

    # --------------- UI ---------------
    st.markdown("### 🎯 Choose Summary Length", unsafe_allow_html=True)
    summary_length = st.radio("", ["Short", "Medium", "Long"], index=1, horizontal=True)

    st.markdown("### ✍️ Select Input Method", unsafe_allow_html=True)
    input_method = st.radio("", ["Enter text", "Upload PDF or TXT file"], horizontal=True)

    content = ""

    if input_method == "Enter text":
        st.markdown("#### 📝 Enter Your Content")
        content = st.text_area("", height=300, placeholder="Paste your educational content here...")
    else:
        st.markdown("#### 📂 Upload File")
        uploaded_file = st.file_uploader("", type=["pdf", "txt"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                content = extract_text_from_pdf(uploaded_file)
                st.success("✅ PDF content extracted successfully!")
            else:
                content = uploaded_file.read().decode("utf-8")
                st.success("✅ Text file content loaded!")

    if content:
        st.markdown("### 🧠 Generated Summary", unsafe_allow_html=True)
        with st.spinner("Summarizing..."):
            summary = summarize(content, summary_length)
        st.success("✅ Summary ready!")
        st.markdown(f"<div style='padding: 15px; background-color: #F1F6F9; border-radius: 10px;'>{summary}</div>", unsafe_allow_html=True)
    else:
        st.info("Please enter or upload content to generate a summary.")

# --- Edu Doubt Solver ---
elif feature == "Edu Doubt Solver":
    def get_base64_of_image(image_path):
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    def set_background(image_path):
        encoded = get_base64_of_image(image_path)
        st.markdown(f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .input-box, .answer-box {{
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 15px;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }}
            </style>
        """, unsafe_allow_html=True)

    set_background("book3.jpg")
    # --------------- CONFIG ---------------- #
    OPENROUTER_API_KEY = "your-api-key"
    OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

    # --------------- FUNCTIONS ------------- #
    def transcribe_voice():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio."
            except sr.RequestError as e:
                return f"Speech recognition error: {e}"

    def translate_to_english(text):
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return text  # Fallback to original

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
            data = response.json()
            if 'choices' in data:
                return data['choices'][0]['message']['content']
            else:
                return f"API Error: {data.get('error', 'Unknown response format')}"
        except Exception as e:
            return f"API Error: {str(e)}"

    # --------------- UI STYLING ------------- #
    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 36px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            .subtitle {
                text-align: center;
                font-size: 18px;
                color: #660066;
                margin-bottom: 20px;
            }
            .input-box, .answer-box {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
            }
            .stRadio > div {
                display: flex;
                justify-content: center;
                gap: 40px;
            }
        </style>
    """, unsafe_allow_html=True)

    # --------------- UI -------------------- #
    st.markdown('<div class="title">🎓 Edu Doubt Solver</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ask questions in any language using text or voice 🎤</div>', unsafe_allow_html=True)

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

    # Language Selector
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

# --- Exam Paper Generator ---
elif feature == "Exam Paper Generator":
    # --- Custom CSS for Balanced UI ---
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #fdf1f5;  /* light pink, subtle */
        }

        .main h1 {
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            color: #d6336c;
        }

        .stTextInput > div > div > input {
            background-color: #fff;
            border: 1px solid #ccc;
            color: #136b9e;
            border-radius: 8px;
            padding: 8px;
        }

        .stButton > button {
            background-color: #136b9e;
            color: white;
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
            transition: 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #222222;
            transform: scale(1.03);
        }

        .stMarkdown h2, .stMarkdown h3 {
            color: #a61e4d;
            font-family: 'Segoe UI', sans-serif;
        }

        .stExpander {
            background-color: #fff7fa !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- OpenRouter API Setup ---
    client = OpenAI(
        api_key="your-api-key",
        base_url="https://openrouter.ai/api/v1"
    )

    # --- Question Generation Function ---
    def generate_questions_with_llm(topic, summary):
        prompt = f"""
    You are an education expert. Based on the topic: **{topic}**, and the following summary, generate 5 to 7 high-quality exam-style questions.

    Summary:
    \"\"\"
    {summary}
    \"\"\"
    Questions should:
    - Cover different subtopics
    - Be clearly worded
    - Avoid yes/no style or vague queries

    Format: 
    Q1. ...
    Q2. ...
    ...
    """
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content

    # --- Wikipedia Fetch ---
    def fetch_summary(topic):
        try:
            return wikipedia.summary(topic, sentences=5)
        except:
            return None

    # --- UI Layout ---
    st.title("🧾Exam Paper Generator")

    # Styled Subtitle
    st.markdown(
        "<h4 style='text-align: center; color: #003366;'>📚 Generate exam questions effortlessly!</h4>",
        unsafe_allow_html=True
    )

    topic = st.text_input("📘 Enter Topic (e.g. Deep Learning Neural Networks)", "")

    if st.button("Generate Questions") and topic:
        with st.spinner("Fetching content and generating questions..."):
            summary = fetch_summary(topic)
            if summary:
                questions = generate_questions_with_llm(topic, summary)
                st.subheader("📋 Generated Questions")
                st.markdown(questions)
                with st.expander("🔍 View summary used"):
                    st.write(summary)
            else:
                st.error("❌ Couldn't find Wikipedia summary for that topic.")
    else:
        st.info("👈 Enter a topic to generate questions")

# --- Motivational Buddy ---
elif feature == "Motivational Buddy":
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

# --- Study Planner ---
elif feature == "Study Planner":
    # --- Custom CSS Styling ---
    st.markdown("""
        <style>
        .main {
            background-color: #f4f6fa;
        }

        .app-title {
            font-size: 42px;
            font-weight: bold;
            color: #1f3c88;
            margin-top: -50px;
            text-align: center;
        }

        .subheader {
            font-size: 20px;
            color: #ff4b4b;
            margin-bottom: 25px;
            text-align: center;
        }

        .fun-box {
            background-color: #e0f7fa;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            color: #004d40;
            text-align: center;
            margin-top: -20px;
            margin-bottom: 15px;
        }

        .form-style {
            background-color: #ffe4e1; /* light pink */
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 5px 12px rgba(0,0,0,0.08);
        }

        .table-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
            margin-top: 20px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background-color: #1f3c88;
            color: white;
            padding: 12px;
            text-align: center !important;
        }

        td {
            padding: 12px;
            text-align: center !important;
            border-bottom: 1px solid #ddd;
        }

        </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    #st.markdown('<div class="app-title">EDUMENTOR AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">🧠 AI-Powered Study Planner..</div>', unsafe_allow_html=True)

    # --- FUN MESSAGE ---
    st.markdown('<div class="fun-box">🎯 Let’s crush your study goals! Customize and conquer. 🚀</div>', unsafe_allow_html=True)

    # --- FORM INPUT ---
    with st.form("planner_form"):
        st.markdown('<div class="form-style">', unsafe_allow_html=True)

        subjects = st.multiselect("📚 Choose Subjects", 
                                  ["Math", "Science", "English", "History", "Computer", "Hindi", "Geography"])

        total_hours = st.slider("🕒 Total Study Hours per Day", 1, 12, 5)
        start_time = st.time_input("⏰ Study Start Time", value=datetime.strptime("09:00", "%H:%M").time())

        submit_btn = st.form_submit_button("✅ Generate Study Plan")

        st.markdown('</div>', unsafe_allow_html=True)

    # --- PLAN GENERATION FUNCTION ---
    def generate_study_plan(subjects, total_hours, start_time):
        start_dt = datetime.strptime(start_time, "%H:%M")
        time_per_subject = total_hours * 60 // len(subjects)
        break_time = 15

        schedule = []
        for i, subject in enumerate(subjects):
            end_dt = start_dt + timedelta(minutes=time_per_subject)
            schedule.append({
                "Subject": subject,
                "Time Slot": f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}",
                "Details": f"Focus on key {subject} topics"
            })

            if i < len(subjects) - 1:
                break_start = end_dt
                break_end = break_start + timedelta(minutes=break_time)
                schedule.append({
                    "Subject": "Break",
                    "Time Slot": f"{break_start.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
                    "Details": "☕ Quick recharge!"
                })
                start_dt = break_end
            else:
                start_dt = end_dt

        return pd.DataFrame(schedule)

    # --- DISPLAY OUTPUT ---
    if submit_btn:
        if not subjects:
            st.warning("⚠️ Please select at least one subject.")
        else:
            df = generate_study_plan(subjects, total_hours, start_time.strftime("%H:%M"))

            st.markdown('<div class="fun-box">✅ Study Plan Ready! Time to make the most of your day 📅</div>', unsafe_allow_html=True)
            st.markdown('<div class="table-box">', unsafe_allow_html=True)
            st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
