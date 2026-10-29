import re

SKILL_KEYWORDS = {
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript"],
    "React": ["react"],
    "Next.js": ["next.js", "nextjs"],
    "Flutter": ["flutter"],
    "SQL": ["sql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Supabase": ["supabase"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Streamlit": ["streamlit"],
    "Excel": ["excel"],
    "Power BI": ["power bi", "powerbi"],
}

def extract_skills(text: str) -> list[str]:
    """Extract recognized skills from resume text."""
    normalized_text = text.lower()
    found_skills = []

    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword == "c":
                pattern = r"\bc\b"
            else:
                pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

            if re.search(pattern, normalized_text):
                found_skills.append(skill)
                break

    return found_skills