from src.explanation import generate_explanation


def test_generate_explanation_for_suspicious_behavior():

    row = {
        "failed_login_count": 50,
        "failure_ratio": 1.0,
        "attempts_per_second": 0.5,
        "prediction": -1
    }

    explanation = generate_explanation(row)

    assert "failed login" in explanation.lower()
    assert "failure ratio" in explanation.lower()
    assert "login frequency" in explanation.lower()
    assert "isolation forest" in explanation.lower()