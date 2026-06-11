def missing_skills(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))
