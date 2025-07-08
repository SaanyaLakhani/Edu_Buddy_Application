EDUMENTOR AI PROJECT
====================

PROJECT OVERVIEW:
-----------------
EduMentor AI is an all-in-one educational web application designed to assist students in their learning journey. Built using Streamlit, it integrates five powerful features: Edu Content Summarizer, Edu Doubt Solver, Exam Paper Generator, Motivational Buddy, and Study Planner. The application leverages machine learning, natural language processing, and external APIs to provide a comprehensive educational toolset for students, educators, and lifelong learners. The goal is to create a user-friendly platform that enhances productivity, clarifies doubts, generates study materials, and boosts motivation.

FILES INCLUDED:
---------------
1. app.py – Main Streamlit application integrating all features
2. edu_content_summarizer.py – Script for summarizing educational content
3. edu_doubt_solver.py – Script for answering questions in multiple languages using text or voice input
4. exam_paper_generator.py – Script for generating exam-style questions based on a topic
5. motivational_buddy.py – Script for providing motivational quotes based on user input
6. study_planner.py – Script for creating personalized study schedules
7. motivational_quotes_dataset.csv – Dataset containing motivational quotes and associated keywords
8. book1.jpg – Background image for Edu Doubt Solver
9. book3.jpg – Alternative background image for Edu Doubt Solver
10. calm.jpg – Background image for Motivational Buddy
11. README.txt – This file

FEATURE DESCRIPTIONS:
---------------------
1. **Edu Content Summarizer**:
   - Purpose: Summarizes educational content from text or uploaded PDF/TXT files.
   - Technology: Uses the `sshleifer/distilbart-cnn-12-6` model from Hugging Face for summarization.
   - Input: Text input or file upload (PDF/TXT).
   - Options: Short, Medium, or Long summary lengths.
   - Output: Concise summary displayed in a styled container.
   - Dependencies: transformers, PyPDF2, streamlit.

2. **Edu Doubt Solver**:
   - Purpose: Answers educational questions in multiple languages via text or voice input.
   - Technology: Integrates OpenRouter API (Mistral-7B-Instruct model), Google Translator for multilingual support, and Whisper/SpeechRecognition for voice input.
   - Input: Text or voice (5-second audio recording).
   - Languages Supported: English, Hindi, Gujarati, Marathi, Tamil, Telugu, Bengali.
   - Output: Answers in the selected language, displayed in a styled container.
   - Dependencies: streamlit, requests, deep_translator, whisper, speech_recognition, sounddevice, scipy.

3. **Exam Paper Generator**:
   - Purpose: Generates 5–7 exam-style questions based on a user-specified topic.
   - Technology: Fetches topic summaries from Wikipedia and uses OpenRouter API (Mistral-7B-Instruct model) to generate questions.
   - Input: Topic entered by the user (e.g., "Deep Learning Neural Networks").
   - Output: List of formatted questions with an expandable summary of the Wikipedia content used.
   - Dependencies: streamlit, wikipedia, openai.

4. **Motivational Buddy**:
   - Purpose: Provides personalized motivational quotes based on user-described feelings.
   - Technology: Uses a CSV dataset of motivational quotes, randomly selected based on user input.
   - Input: Text describing the user’s feelings (e.g., "tired," "stressed").
   - Output: A motivational quote displayed in a styled box.
   - Dependencies: streamlit, pandas.

5. **Study Planner**:
   - Purpose: Creates a customized daily study schedule based on user preferences.
   - Technology: Generates a timetable using pandas DataFrame, incorporating subjects, study hours, and breaks.
   - Input: Subjects (multiselect), total study hours (slider), and start time.
   - Output: A formatted table with subject time slots and break periods.
   - Dependencies: streamlit, pandas.

SETUP INSTRUCTIONS:
-------------------
1. **Install Required Python Libraries**:
   Install the necessary dependencies using pip:
   ```bash
   pip install streamlit pandas numpy transformers PyPDF2 requests deep_translator wikipedia-api openai speechrecognition whisper sounddevice scipy
   ```

2. **Ensure Files are in the Same Directory**:
   Place the following files in the project folder:
   - app.py
   - edu_content_summarizer.py
   - edu_doubt_solver.py
   - exam_paper_generator.py
   - motivational_buddy.py
   - study_planner.py
   - motivational_quotes_dataset.csv
   - book1.jpg
   - book3.jpg
   - calm.jpg

3. **Run the Streamlit App**:
   Execute the following command in your terminal:
   ```bash
   streamlit run app.py
   ```

4. **Access the Application**:
   - The app will open in your default browser.
   - Use the sidebar dropdown to select a feature (e.g., Study Planner, Edu Doubt Solver).
   - Follow the on-screen prompts to interact with each feature.

WEB APPLICATION FEATURES:
-------------------------
- **Unified Interface**: A single Streamlit app (`app.py`) integrates all features with a clean, modern UI.
- **Sidebar Navigation**: Select features using a dropdown menu in the sidebar.
- **Custom Styling**: Each feature has tailored CSS for a visually appealing and consistent experience:
  - Edu Content Summarizer: Soft purple gradient theme.
  - Edu Doubt Solver: Book-themed background with white input/output boxes.
  - Exam Paper Generator: Light pink theme with styled inputs and buttons.
  - Motivational Buddy: Calming background with motivational quote display.
  - Study Planner: Light blue and pink theme with interactive forms and tables.
- **Responsive Design**: Optimized for both desktop and mobile use.
- **Interactive Inputs**: Includes sliders, dropdowns, text inputs, file uploads, and voice recording.
- **Multilingual Support**: Edu Doubt Solver supports multiple Indian languages for accessibility.

DEPENDENCIES:
-------------
- Python 3.8+
- streamlit
- pandas
- numpy
- transformers
- PyPDF2
- requests
- deep_translator
- wikipedia-api
- openai
- speechrecognition
- whisper
- sounddevice
- scipy

PROJECT OUTPUT:
---------------
- **Edu Content Summarizer**: Generates concise summaries of educational content for quick review.
- **Edu Doubt Solver**: Provides accurate, multilingual answers to educational queries, supporting both text and voice inputs.
- **Exam Paper Generator**: Creates high-quality exam questions for practice and assessment.
- **Motivational Buddy**: Delivers motivational quotes to boost morale during study sessions.
- **Study Planner**: Produces structured study schedules to optimize time management.

LIMITATIONS:
------------
- **Edu Doubt Solver**: Voice recognition accuracy depends on audio quality and may struggle with heavy accents or background noise.
- **Exam Paper Generator**: Relies on Wikipedia for summaries; may fail for obscure topics or require disambiguation.
- **Motivational Buddy**: Limited to predefined quotes; does not use LLM for dynamic motivation.
- **Internet Dependency**: Features like Exam Paper Generator and Edu Doubt Solver require internet access for API calls.

FUTURE IMPROVEMENTS:
--------------------
- Add offline support for summarization and doubt-solving using local models.
- Enhance Motivational Buddy with LLM-generated personalized messages.
- Expand Study Planner to include task prioritization and progress tracking.
- Improve voice recognition for Edu Doubt Solver with advanced models.
- Add export options for generated study plans and exam papers (e.g., PDF, CSV).

CONCLUSION:
-----------
EduMentor AI is a versatile educational tool designed to empower students by streamlining study processes, clarifying doubts, generating practice questions, and providing motivation. By combining machine learning, NLP, and a user-friendly Streamlit interface, it offers a practical solution for modern learning needs. This project showcases the integration of multiple technologies to create a cohesive, deployable application for educational purposes.

Developed as part of a Machine Learning and Web Development portfolio project by Saanya lakhani. Feel free to use for any Educational Projects.
