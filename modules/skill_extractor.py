import pandas as pd

skills_df = pd.read_csv("data/skills.csv")
SKILLS = skills_df["skill"].tolist()

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)
    return list(set(found))
