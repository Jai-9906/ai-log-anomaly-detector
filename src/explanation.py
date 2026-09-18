def generate_explanation(row):
    reasons = []

    if row["failed_login_count"] >= 10:
        reasons.append("High number of failed login attempts")

    if row["failure_ratio"] >= 0.8:
        reasons.append("Very high failure ratio")

    if row["attempts_per_second"] >= 0.1:
        reasons.append("High login frequency")

    if row["prediction"] == -1:
        reasons.append("Isolation Forest detected unusual behavior")

    if not reasons:
        reasons.append("No suspicious behavior detected")

    return "; ".join(reasons)