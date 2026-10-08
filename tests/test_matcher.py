import pytest

from matcher.ranker import rank_resumes
from matcher.skills import extract_skills


def test_extracts_basic_skills():
    found = extract_skills("I know Python, SQL and Git.")
    assert {"python", "sql", "git"} <= found


def test_aliases_work():
    # "sklearn" should count as scikit-learn, "ml" as machine learning
    found = extract_skills("Used sklearn for ML projects")
    assert "scikit-learn" in found
    assert "machine learning" in found


def test_cpp_is_not_confused_with_c():
    assert "c++" in extract_skills("Programming in C++")


def test_no_partial_word_matches():
    # "javascript" contains "java" but should not count as java
    found = extract_skills("Built a site with JavaScript")
    assert "javascript" in found
    assert "java" not in found


def test_empty_text_has_no_skills():
    assert extract_skills("") == set()


JD = "Looking for a Python intern with FastAPI, SQL and pytest experience."


def test_best_resume_is_ranked_first():
    resumes = {
        "good.txt": "Python developer. Built FastAPI services with SQL and pytest tests.",
        "bad.txt": "Mechanical engineering student using AutoCAD and MATLAB.",
    }
    df = rank_resumes(JD, resumes)
    assert df.iloc[0]["resume"] == "good.txt"
    assert df.index[0] == 1


def test_missing_skills_are_reported():
    resumes = {"half.txt": "I know Python and SQL."}
    df = rank_resumes(JD, resumes)
    assert "pytest" in df.iloc[0]["missing_skills"]
    assert "fastapi" in df.iloc[0]["missing_skills"]


def test_scores_between_0_and_100():
    resumes = {"a.txt": "Python FastAPI SQL pytest", "b.txt": "nothing relevant here"}
    df = rank_resumes(JD, resumes)
    assert df["final_score"].between(0, 100).all()


def test_no_resumes_raises_error():
    with pytest.raises(ValueError):
        rank_resumes(JD, {})
