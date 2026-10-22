import streamlit as st
import pdfplumber
import base64
from database_config import get_connection, load_shared_engines

def run_candidate_portal():
    classifier, translator = load_shared_engines()
    st.title("🎯 Candidate Career Intelligence")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file:
        # 1. VIEW PDF
        with st.expander("📄 View Uploaded Resume"):
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
            uploaded_file.seek(0) # Reset file pointer

        # 2. DATA EXTRACTION
        with pdfplumber.open(uploaded_file) as pdf:
            text = " ".join([p.extract_text() for p in pdf.pages if p.extract_text()])

        with st.spinner('AI performing deep analysis...'):
            # 3. CATEGORY & ROLE
            roles = ["Data Science", "Web Development", "DevOps", "Cybersecurity"]
            tiers = ["Beginner", "Intermediate", "Advanced Technocrat"]
            
            res_role = classifier(text, roles)
            res_tier = classifier(text, tiers)
            
            role = res_role['labels'][0]
            tier = res_tier['labels'][0]
            score = round(res_role['scores'][0] * 100, 2)

            # 4. SKILL DETECTION (Dynamic set based on role)
            skill_bank = {
                "Data Science": ["Python", "Machine Learning", "SQL", "Pandas", "Tableau"],
                "Web Development": ["React", "Node.js", "CSS", "JavaScript", "MongoDB"]
            }.get(role, ["Leadership", "Communication", "Problem Solving"])
            
            skill_res = classifier(text, skill_bank, multi_label=True)
            detected = [s for s, sc in zip(skill_res['labels'], skill_res['scores']) if sc > 0.5]
            lacking = list(set(skill_bank) - set(detected))

        # --- DISPLAY RESULTS ---
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Category", tier)
        c2.metric("Role Match", role)
        c3.metric("Industry Score", f"{score}%")

        st.subheader("🤖 AI Insights")
        st.info(f"As an {tier} in {role}, you show strong potential in {', '.join(detected[:2])}.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.success(f"✅ Skills Detected: {', '.join(detected)}")
        with col_b:
            st.error(f"❌ Skills Lacking: {', '.join(lacking)}")

        # 5. DYNAMIC VIDEO RECOMMENDATIONS
        st.subheader("📚 Personalized Learning Roadmap")
        for skill in lacking:
            st.write(f"**Improve your {skill} skills:**")
            st.video(f"https://www.youtube.com/results?search_query=learn+{skill}+for+{tier}")

        # 6. LOG DATA FOR ADMIN
        if st.button("Confirm Analysis & Apply to Featured Roles"):
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("INSERT INTO recruitment_analytics (candidate_name, predicted_domain, technocrat_tier, score) VALUES (%s, %s, %s, %s)",
                            (uploaded_file.name, role, tier, score))
            conn.commit()
            st.balloons()