import pandas as pd

from src.anomaly_detector import train_model


def test_isolation_forest_detects_obvious_anomaly():

    normal_data = pd.DataFrame({
        "failed_login_count": [1, 2, 3, 2, 4, 1, 3, 2],
        "successful_login_count": [8, 7, 7, 8, 6, 9, 7, 8],
        "unique_users": [1, 2, 2, 1, 2, 1, 2, 2],
        "total_login_attempts": [9, 9, 10, 10, 10, 10, 10, 10],
        "failure_ratio": [0.11, 0.22, 0.30, 0.20, 0.40, 0.10, 0.30, 0.20],
        "activity_duration_seconds": [240, 220, 250, 200, 230, 260, 210, 240],
        "attempts_per_second": [0.037, 0.041, 0.040, 0.050, 0.043, 0.038, 0.048, 0.042]
    })

    model = train_model(normal_data)

    test_data = pd.DataFrame({
        "failed_login_count": [50],
        "successful_login_count": [0],
        "unique_users": [1],
        "total_login_attempts": [50],
        "failure_ratio": [1.0],
        "activity_duration_seconds": [100],
        "attempts_per_second": [0.5]
    })

    prediction = model.predict(test_data)

    assert prediction[0] == -1