def calculate_ats_score(matched, total_keywords):

    if total_keywords == 0:
        return 0

    score = (len(matched) / total_keywords) * 100

    return round(score, 2)