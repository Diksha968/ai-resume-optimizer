
# Resume upload API
from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
import re
from nltk.corpus import stopwords
from database import engine
from models import Base
from database import SessionLocal, engine
from models import Base, ResumeAnalysis
from utils.recommendations import generate_recommendations

Base.metadata.create_all(bind=engine)

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
    recommendations = generate_recommendations(missing)

    # Calculate ATS score
    ats_score = calculate_ats_score(
        matched,
        len(matched) + len(missing)
    )
    db = SessionLocal()

    analysis = ResumeAnalysis(
    ats_score=ats_score,
    matched_keywords=", ".join(matched[:20]),
    missing_keywords=", ".join(missing[:20])
)

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    db.close()
    return {
        "analysis_id": analysis.id,
        "ats_score": ats_score,
        "matched_keywords": matched[:20],
        "missing_keywords": missing[:20],
        "recommendations": recommendations
    }
@app.get("/history")
def get_history():

    db = SessionLocal()

    analyses = db.query(ResumeAnalysis).all()

    result = []

    for item in analyses:
        result.append({
            "id": item.id,
            "ats_score": item.ats_score,
            "matched_keywords": item.matched_keywords,
            "missing_keywords": item.missing_keywords
        })

    db.close()

    return result