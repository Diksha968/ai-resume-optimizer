def generate_recommendations(missing_skills):

    recommendations = []

    skill_tips = {
        "python": "Highlight Python projects and experience.",
        "django": "Mention Django applications you have built.",
        "fastapi": "Include FastAPI APIs or backend projects.",
        "react": "Add React frontend projects.",
        "mysql": "Mention database design and SQL experience.",
        "postgresql": "Show PostgreSQL usage in projects.",
        "mongodb": "Include NoSQL database experience.",
        "docker": "Add Docker containerization experience.",
        "aws": "Mention AWS cloud services and deployments.",
        "git": "Include Git and GitHub collaboration experience.",
    }

    for skill in missing_skills:
        if skill in skill_tips:
            recommendations.append(skill_tips[skill])

    return recommendations