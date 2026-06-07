import re
from nltk.corpus import stopwords


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

    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(job_description)

    matched = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    return list(matched), list(missing)