from src.risk_scoring import calculate_risk_score, get_severity


def test_high_risk_behavior():

    row = {
        "failed_login_count": 50,
        "failure_ratio": 1.0,
        "attempts_per_second": 0.5,
        "prediction": -1
    }

    score = calculate_risk_score(row)

    assert score == 100
    assert get_severity(score) == "CRITICAL"


def test_low_risk_behavior():

    row = {
        "failed_login_count": 1,
        "failure_ratio": 0.1,
        "attempts_per_second": 0.01,
        "prediction": 1
    }

    score = calculate_risk_score(row)

    assert score == 0
    assert get_severity(score) == "LOW"