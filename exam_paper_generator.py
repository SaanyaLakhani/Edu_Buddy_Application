import streamlit as st
import wikipedia
from openai import OpenAI  # For OpenRouter-compatible API

# --- Streamlit Page Setup ---
#st.set_page_config(page_title="Exam Paper Generator", layout="centered")

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
