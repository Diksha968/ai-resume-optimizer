
# Resume upload API
from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
import re
from nltk.corpus import stopwords

app = FastAPI()


# Home Route
@app.get("/")
def home():
    return {"message": "Resume Optimizer API is running"}


# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


# Extract keywords
def extract_keywords(text):

    # English stop words
    stop_words = set(stopwords.words('english'))

    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())

    # Remove stop words + small words
    filtered_words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    return set(filtered_words)


# Match resume with job description
def match_keywords(resume_text, job_description):

    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(job_description)

    matched = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    return list(matched), list(missing)


# ATS Score Calculation
def calculate_ats_score(matched, total_keywords):

    if total_keywords == 0:
        return 0

    score = (len(matched) / total_keywords) * 100

    return round(score, 2)


# Upload API
@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Extract resume text
    resume_text = extract_text_from_pdf(file.file)

    # Match keywords
    matched, missing = match_keywords(
        resume_text,
        job_description
    )

    # Calculate ATS score
    ats_score = calculate_ats_score(
        matched,
        len(matched) + len(missing)
    )

    return {
        "ats_score": ats_score,
        "matched_keywords": matched[:20],
        "missing_keywords": missing[:20]
    }