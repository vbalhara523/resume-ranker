"""TF-IDF + cosine similarity between a job description and resumes."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_scores(jd_text, resume_texts):
    """
    Fits one vectorizer on [jd] + all resumes (so they share a vocabulary)
    and returns:
      - a list of cosine similarities (one per resume)
      - the vectorizer and matrix, so we can explain the score later
    """
    docs = [jd_text] + list(resume_texts)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), lowercase=True)
    matrix = vec.fit_transform(docs)
    scores = cosine_similarity(matrix[0], matrix[1:])[0]
    return list(scores), vec, matrix


def top_shared_terms(vec, matrix, resume_index, n=5):
    """
    Which words pushed the similarity up the most?
    For each term we multiply its weight in the JD and in the resume.
    resume_index is 0-based among the resumes (row 0 of the matrix is the JD).
    """
    jd_row = matrix[0].toarray()[0]
    cv_row = matrix[resume_index + 1].toarray()[0]
    contribution = jd_row * cv_row
    terms = vec.get_feature_names_out()
    best = contribution.argsort()[::-1][:n]
    return [terms[i] for i in best if contribution[i] > 0]
