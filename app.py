import streamlit as st
import pandas as pd
import base64
import datetime
import pymysql
import pdfplumber
import re
import urllib.parse
import plotly.express as px
from streamlit_tags import st_tags
from transformers import pipeline
from sqlalchemy import create_engine
import warnings

# --- 1. SETTINGS ---
warnings.filterwarnings("ignore")
st.set_page_config(page_title="SkillSmart AI Pro", page_icon="💼", layout="wide")

# --- 2. DYNAMIC CONTENT DATABASES ---
VIDEO_LIBRARY = {
    "Data Science": "https://www.youtube.com/watch?v=ua-CiDNNj30",
    "Web Development": "https://www.youtube.com/watch?v=nu_pCVPKzTk",
    "UI/UX": "https://www.youtube.com/watch?v=c9Wg6ndoxag",
    "DevOps": "https://www.youtube.com/watch?v=hQcFE0RD0cQ",
    "General": "https://www.youtube.com/watch?v=Tt08KmFfIYQ"
}

CAREER_ADVICE = {
    "Data Science": "🚀 **AI Advice:** Focus on building a portfolio on Kaggle. Master 'Storytelling with Data' to stand out during interviews.",
    "Web Development": "🌐 **AI Advice:** Contribute to Open Source. Focus on performance optimization and 'System Design' concepts.",
    "UI/UX": "🎨 **AI Advice:** Build a case study focusing on *why* you made design choices, not just the final look. Practice accessibility.",
    "DevOps": "☁️ **AI Advice:** Get certified in AWS or Azure. Focus on Infrastructure as Code (Terraform) and security best practices."
}

SKILL_MAP = {
    "Data Science": ["Python", "Pandas", "Numpy", "Scikit-learn", "Tensorflow", "SQL", "Tableau", "Kaggle"],
    "Web Development": ["React", "JavaScript", "Node.js", "Django", "Tailwind", "Next JS", "TypeScript", "GitHub"],
    "UI/UX": ["Figma", "Adobe XD", "User Research", "Prototyping", "Wireframes", "Zeplin", "Canva"],
    "DevOps": ["Docker", "Kubernetes", "AWS", "Jenkins", "Terraform", "CI/CD", "Linux", "GCP"]
}

# --- 3. UTILS & AI ---
@st.cache_resource
def load_ai():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_data(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def get_skills(text):
    found = []
    all_skills = [s for sublist in SKILL_MAP.values() for s in sublist]
    for s in set(all_skills):
        if re.search(r'\b' + re.escape(s) + r'\b', text, re.IGNORECASE):
            found.append(s)
    return sorted(list(set(found)))

def calculate_tier(text, found_skills):
    text_lower = text.lower()
    # Check for Years of Experience using Regex
    exp_match = re.search(r'(\d+)\s*(?:\+)?\s*(?:year|yr)', text_lower)
    years = int(exp_match.group(1)) if exp_match else 0
    
    # Keywords
    adv_keys = ['senior', 'lead', 'architect', 'manager', 'head', 'principal']
    beg_keys = ['intern', 'fresher', 'student', 'trainee', 'junior']
    
    has_adv = any(word in text_lower for word in adv_keys)
    has_beg = any(word in text_lower for word in beg_keys)

    if years >= 6 or (years >= 3 and has_adv):
        return "Advanced 🏆", "#1f77b4"
    elif 2 <= years < 6 or (years < 3 and has_adv) or (len(found_skills) > 5):
        return "Intermediate ⚡", "#ff7f0e"
    else:
        return "Beginner 🌱", "#2ca02c"

# --- 4. DATABASE ---
def init_db():
    conn = pymysql.connect(host='localhost', user='root', password='Admin12@', autocommit=True)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS cv")
    cursor.execute("USE cv")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            ID INT NOT NULL AUTO_INCREMENT,
            Email_ID VARCHAR(500),
            resume_score INT,
            Timestamp VARCHAR(50),
            Predicted_Field VARCHAR(100),
            Category VARCHAR(100),
            Actual_skills TEXT,
            PRIMARY KEY (ID)
        )
    """)
    return conn, cursor

# --- 5. RUN APP ---
def run():
    try:
        conn, cursor = init_db()
    except Exception as e:
        st.error(f"DB Error: {e}")
        return

    st.sidebar.markdown("## 🤖 SkillSmart Pro")
    side_opt = st.sidebar.radio("Navigation", ["User Analysis", "Admin Insights"])

    if side_opt == "User Analysis":
        st.title("🚀 Smart Career Profiler")
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")
        
        if uploaded_file:
            with st.spinner("AI analyzing your profile..."):
                raw_text = extract_data(uploaded_file)
                classifier = load_ai()
                res = classifier(raw_text[:1500], list(SKILL_MAP.keys()))
                field = res['labels'][0]
                
                email = re.search(r'[\w\.-]+@[\w\.-]+', raw_text)
                email = email.group(0) if email else "Not Found"
                found_skills = get_skills(raw_text)
                
                # New Category Logic
                tier_label, tier_color = calculate_tier(raw_text, found_skills)
                score = min(len(found_skills) * 10 + 25, 100)

                # --- DASHBOARD HEADER ---
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.metric("Predicted Role", field)
                with c2: 
                    st.markdown("**Profile Category**")
                    st.markdown(f"<p style='color:{tier_color}; font-size:24px; font-weight:bold; margin-top:-15px;'>{tier_label}</p>", unsafe_allow_html=True)
                with c3: st.metric("Profile Strength", f"{score}%")
                with c4: st.metric("Contact Info", email[:18])

                st.markdown("---")

                # --- AI CAREER ADVICE ---
                st.subheader("💡 Personal AI Insights")
                col_adv, col_job = st.columns([2, 1])
                with col_adv:
                    st.markdown(f"""
                    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #7101FF;">
                        <p style="color:#31333F; font-size:18px;">{CAREER_ADVICE.get(field)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_job:
                    search_query = urllib.parse.quote(f"{field} jobs")
                    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
                    st.write("Ready to apply?")
                    st.link_button("🔍 Find Jobs on LinkedIn", linkedin_url, use_container_width=True)

                st.markdown("---")

                # --- DYNAMIC LEARNING & SKILLS ---
                col_v, col_s = st.columns([1.2, 1])
                with col_v:
                    st.subheader(f"🎥 Recommended for {field}")
                    video_url = VIDEO_LIBRARY.get(field, VIDEO_LIBRARY["General"])
                    st.video(video_url)
                
                with col_s:
                    st.subheader("🛠️ Skills Detected")
                    st_tags(label="", text="", value=found_skills, key="tags")
                    
                    target = SKILL_MAP.get(field, [])
                    missing = [s for s in target if s not in found_skills]
                    if missing:
                        st.write("📈 **Bridge the Gap:**")
                        st.write(", ".join([f"`{m}`" for m in missing[:4]]))

                st.markdown("---")

                # --- PREVIEW ---
                with st.expander("🔍 View Analyzed Resume"):
                    uploaded_file.seek(0)
                    base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)

                # DB SAVE
                ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("USE cv")
                cursor.execute(
                    "INSERT INTO user_data (Email_ID, resume_score, Timestamp, Predicted_Field, Category, Actual_skills) VALUES (%s,%s,%s,%s,%s,%s)",
                    (email, score, ts, field, tier_label, str(found_skills))
                )
                st.balloons()

    elif side_opt == "Admin Insights":
        st.title("🔐 Admin Management")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Access Logs") and user == "admin" and pw == "admin123":
            # Using urllib.parse to handle '@' in password for SQLAlchemy
            encoded_pw = urllib.parse.quote_plus("Admin12@")
            engine = create_engine(f"mysql+pymysql://root:{encoded_pw}@localhost/cv")
            df = pd.read_sql("SELECT * FROM user_data", con=engine)
            
            st.dataframe(df, use_container_width=True)
            if not df.empty:
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.plotly_chart(px.pie(df, names='Predicted_Field', title='Domain Split', hole=0.4))
                with col_c2:
                    st.plotly_chart(px.bar(df, x='Category', title='Experience Levels', color='Category'))

    conn.close()

if __name__ == "__main__":
    run()