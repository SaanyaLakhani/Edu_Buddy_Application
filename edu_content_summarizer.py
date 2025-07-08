import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PyPDF2 import PdfReader

#st.set_page_config(page_title="Edu Content Summarizer", layout="centered")

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
