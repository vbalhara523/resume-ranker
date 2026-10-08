"""
Skill extraction.

SKILLS maps a skill name -> list of ways people write it.
I kept the list small on purpose (tech skills for CS internships), it is easy to extend.
"""
import re

SKILLS = {
    "python": ["python"],
    "c++": ["c++"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "sql": ["sql", "mysql", "postgresql"],
    "sqlite": ["sqlite"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "machine learning": ["machine learning", "ml"],
    "nlp": ["nlp", "natural language processing"],
    "data analysis": ["data analysis", "data analytics"],
    "data cleaning": ["data cleaning", "data cleansing"],
    "eda": ["eda", "exploratory data analysis"],
    "regex": ["regex", "regular expressions"],
    "rest api": ["rest api", "rest apis", "restful"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "git": ["git", "github"],
    "docker": ["docker"],
    "linux": ["linux"],
    "pytest": ["pytest", "unit testing", "unit tests"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "reactjs"],
    "oop": ["oop", "object-oriented", "object oriented"],
    "dsa": ["dsa", "data structures", "algorithms"],
    "streamlit": ["streamlit"],
    "matplotlib": ["matplotlib"],
    "excel": ["excel"],
    "agile": ["agile", "scrum"],
}


def _pattern(alias):
    # lookarounds instead of \b so that "c++" and "scikit-learn" work properly
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])")


_PATTERNS = {skill: [_pattern(a) for a in aliases] for skill, aliases in SKILLS.items()}


def extract_skills(text):
    """Returns the set of known skills that appear in the text."""
    text = text.lower()
    found = set()
    for skill, patterns in _PATTERNS.items():
        if any(p.search(text) for p in patterns):
            found.add(skill)
    return found
