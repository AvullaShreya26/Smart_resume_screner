import streamlit as st
import pandas as pd
import plotly.express as px

from modules.pdf_reader import extract_text
from modules.preprocessing import preprocess_text
from modules.skill_extractor import extract_skills
from modules.similarity import get_similarity_score
from modules.recommendations import missing_skills


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.big-title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:white;
    margin-bottom:0px;
}

.sub-title{
    text-align:center;
    color:#B0B3B8;
    font-size:18px;
    margin-bottom:30px;
}

.metric-card{
    background:linear-gradient(135deg,#667eea,#764ba2);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    box-shadow:0px 4px 15px rgba(0,0,0,0.3);
}

.skill-box{
    display:inline-block;
    background:#1f77b4;
    color:white;
    padding:8px 15px;
    border-radius:20px;
    margin:5px;
    font-size:14px;
}

.missing-box{
    display:inline-block;
    background:#d62728;
    color:white;
    padding:8px 15px;
    border-radius:20px;
    margin:5px;
    font-size:14px;
}

.section-card{
    padding:20px;
    border-radius:15px;
    background:#1A1D24;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class='big-title'>
🚀 AI Resume ATS Analyzer
</div>

<div class='sub-title'>
Smart Resume Screening System 
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INPUT AREA
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"]
    )

with col2:
    jd_text = st.text_area(
        "💼 Paste Job Description",
        height=250
    )

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        st.stop()

    if jd_text.strip() == "":
        st.error("Please paste a job description.")
        st.stop()

    # -------------------------
    # READ RESUME
    # -------------------------
    resume_text = extract_text(uploaded_file)

    # -------------------------
    # PREPROCESS
    # -------------------------
    clean_resume = preprocess_text(resume_text)
    clean_jd = preprocess_text(jd_text)

    # -------------------------
    # SCORE
    # -------------------------
    score = get_similarity_score(
        clean_resume,
        clean_jd
    )

    # -------------------------
    # SKILLS
    # -------------------------
    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(jd_text)

    missing = missing_skills(
        resume_skills,
        jd_skills
    )

    # -------------------------
    # SCORE SECTION
    # -------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='metric-card'>
            <h1>{score}%</h1>
            <h3>ATS Match Score</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.progress(int(score))

    # -------------------------
    # SCORE MESSAGE
    # -------------------------
    if score >= 80:
        st.success(
            "Excellent Match! Resume strongly aligns with the Job Description."
        )

    elif score >= 60:
        st.warning(
            "Moderate Match. Consider improving missing skills."
        )

    else:
        st.error(
            "Low Match Score. Resume requires significant improvement."
        )

    # -------------------------
    # SKILLS SECTION
    # -------------------------
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Skills Found")

        if len(resume_skills) == 0:
            st.info("No skills detected.")

        for skill in resume_skills:
            st.markdown(
                f"""
                <span class='skill-box'>
                {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

    with col2:

        st.subheader("❌ Missing Skills")

        if len(missing) == 0:
            st.success(
                "No missing skills detected."
            )

        for skill in missing:
            st.markdown(
                f"""
                <span class='missing-box'>
                {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

    # -------------------------
    # CHART
    # -------------------------
    st.markdown("---")

    st.subheader("📊 Skill Analysis")

    matched_count = len(resume_skills)
    missing_count = len(missing)

    chart_df = pd.DataFrame(
        {
            "Category": [
                "Matched Skills",
                "Missing Skills"
            ],
            "Count": [
                matched_count,
                missing_count
            ]
        }
    )

    fig = px.pie(
        chart_df,
        names="Category",
        values="Count",
        hole=0.55,
        title="Resume vs Job Description Skill Match"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # SUMMARY
    # -------------------------
    st.markdown("---")

    st.subheader("📋 Analysis Summary")

    st.write(
        f"""
        - ATS Match Score: **{score}%**
        - Skills Found: **{len(resume_skills)}**
        - Required Skills: **{len(jd_skills)}**
        - Missing Skills: **{len(missing)}**
        """
    )

    if len(missing) > 0:

        st.subheader(
            "🎯 Recommended Skills To Learn"
        )

        for skill in missing:
            st.write(f"• {skill}")

    else:
        st.success(
            "Your resume covers all detected job requirements."
        )