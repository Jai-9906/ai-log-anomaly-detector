def calculate_risk_score(row):
    score = 0

    if row["failed_login_count"] >= 10:
        score += 30

    if row["failure_ratio"] >= 0.8:
        score += 25

    if row["attempts_per_second"] >= 0.1:
        score += 30

    if row["prediction"] == -1:
        score += 15

    return min(score, 100)

def get_severity(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"