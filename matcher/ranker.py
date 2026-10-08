"""Puts skill matching and TF-IDF together and ranks the resumes."""
from pathlib import Path

import pandas as pd

from .similarity import tfidf_scores, top_shared_terms
from .skills import extract_skills

# final score = 70% skill coverage + 30% text similarity
# (skills matter more, tf-idf alone gives low numbers even for good matches)
SKILL_WEIGHT = 0.7
TEXT_WEIGHT = 0.3


def read_text_files(folder):
    """Returns {filename: text} for every .txt file in a folder."""
    files = sorted(Path(folder).glob("*.txt"))
    return {f.name: f.read_text(encoding="utf-8") for f in files}


def rank_resumes(jd_text, resumes):
    """
    jd_text : the job description as a string
    resumes : dict {filename: text}
    returns : DataFrame sorted best -> worst
    """
    if not resumes:
        raise ValueError("No resumes to rank")

    names = list(resumes.keys())
    texts = [resumes[n] for n in names]

    jd_skills = extract_skills(jd_text)
    text_scores, vec, matrix = tfidf_scores(jd_text, texts)

    rows = []
    for i, name in enumerate(names):
        cv_skills = extract_skills(texts[i])
        matched = jd_skills & cv_skills
        missing = jd_skills - cv_skills
        coverage = len(matched) / len(jd_skills) if jd_skills else 0.0
        final = SKILL_WEIGHT * coverage + TEXT_WEIGHT * text_scores[i]
        rows.append({
            "resume": name,
            "final_score": round(final * 100, 1),
            "skill_match_%": round(coverage * 100, 1),
            "text_similarity_%": round(text_scores[i] * 100, 1),
            "matched_skills": ", ".join(sorted(matched)),
            "missing_skills": ", ".join(sorted(missing)),
            "top_terms": ", ".join(top_shared_terms(vec, matrix, i)),
        })

    df = pd.DataFrame(rows).sort_values("final_score", ascending=False).reset_index(drop=True)
    df.index += 1          # rank starts at 1
    df.index.name = "rank"
    return df
