import re
from nltk.corpus import stopwords
from utils.recommendations import extract_skills


def extract_keywords(text):

    stop_words = set(stopwords.words("english"))

    words = re.findall(r"\b\w+\b", text.lower())

    filtered_words = [
        word
        for word in words
        if word not in stop_words and len(word) > 2
    ]

    return set(filtered_words)


def match_keywords(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills


    return list(matched), list(missing)