import pandas as pd

from src.data_processor import create_features


def test_create_features():

    events = [
        {
            "timestamp": "Aug 22 18:10:00",
            "event_type": "failed_login",
            "username": "root",
            "ip": "192.168.1.10",
            "status": "failure"
        },
        {
            "timestamp": "Aug 22 18:11:00",
            "event_type": "failed_login",
            "username": "root",
            "ip": "192.168.1.10",
            "status": "failure"
        },
        {
            "timestamp": "Aug 22 18:12:00",
            "event_type": "successful_login",
            "username": "root",
            "ip": "192.168.1.10",
            "status": "success"
        }
    ]

    df = pd.DataFrame(events)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%b %d %H:%M:%S"
    )

    features = create_features(df)

    row = features.iloc[0]

    assert row["failed_login_count"] == 2
    assert row["successful_login_count"] == 1
    assert row["total_login_attempts"] == 3
    assert row["unique_users"] == 1
    assert row["failure_ratio"] == 2 / 3