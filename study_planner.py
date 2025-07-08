import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Streamlit Page Setup ---
#st.set_page_config(page_title="EduMentor AI", layout="centered")

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
        box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
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
st.markdown('<div class="subheader">🧠 Your AI-Powered Study Planner</div>', unsafe_allow_html=True)

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
