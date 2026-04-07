import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from resume_parser import extract_resume_text
from utils import clean_text
from similarity_model import calculate_similarity
from skill_extractor import extract_skills


# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.title("🔐 Login to Resume Screener")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


# ---------------- MAIN APP ----------------
if not st.session_state.logged_in:
    login()

else:
    st.set_page_config(page_title="AI Resume Screener", layout="wide")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📄 AI Resume Screening System")
    st.markdown("### Upload resumes and get AI-based ranking 📊")

    st.divider()

    # ---------------- LOAD SKILLS ----------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    skills_path = os.path.join(BASE_DIR, "skills.txt")

    with open(skills_path, "r") as f:
        skills_list = [line.strip().lower() for line in f.readlines()]

    # ---------------- INPUT ----------------
    job_description = st.text_area("📌 Enter Job Description")

    uploaded_files = st.file_uploader(
        "📤 Upload Resumes (PDF/DOCX)",
        accept_multiple_files=True
    )

    # ---------------- PROCESS ----------------
    if uploaded_files and job_description:

        results = []

        for file in uploaded_files:
            text = extract_resume_text(file)
            cleaned_text = clean_text(text)
            score = calculate_similarity(job_description, cleaned_text)
            skills = extract_skills(cleaned_text, skills_list)

            results.append({
                "Candidate": file.name,
                "Score": score,
                "Skills": ", ".join(skills)
            })

        df = pd.DataFrame(results)

        if len(df) > 0:
            df = df.sort_values(by="Score", ascending=False)

            # ---------------- TABLE ----------------
            st.subheader("📊 Candidate Ranking")
            st.write(df)

            # ---------------- DOWNLOAD BUTTON ----------------
            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name='resume_ranking.csv',
                mime='text/csv',
            )

            st.divider()

            # ---------------- GRAPH ----------------
            st.subheader("📈 Score Visualization")

            fig, ax = plt.subplots()
            ax.barh(df["Candidate"], df["Score"])
            ax.set_xlabel("Score")
            ax.set_ylabel("Candidate")
            ax.invert_yaxis()

            st.pyplot(fig)

            st.divider()

            # ---------------- INSIGHTS ----------------
            st.subheader("💡 Insights")

            top_candidate = df.iloc[0]["Candidate"]
            top_score = df.iloc[0]["Score"]

            st.success(f"🏆 Best Candidate: {top_candidate} (Score: {top_score:.2f})")

    else:
        st.info("👆 Please upload resumes and enter job description")