import pandas as pd


def events_to_dataframe(events):
    df = pd.DataFrame(events)
    df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%b %d %H:%M:%S"
)

    print(df)

    print("Events per IP:")
    print(df.groupby("ip").size())

    failed = df[df["status"] == "failure"]
    print("Failed logins per IP:")
    print(failed.groupby("ip").size())

    success = df[df["status"] == "success"]
    print("Successful logins per IP:")
    print(success.groupby("ip").size())

    return df


def create_features(df):

    # Create 5-minute time windows
    df["time_window"] = df["timestamp"].dt.floor("5min")

    # Group events by IP and time window
    feature_df = df.groupby(["ip", "time_window"]).agg(
    failed_login_count=("status", lambda x: (x == "failure").sum()),
    successful_login_count=("status", lambda x: (x == "success").sum()),
    unique_users=("username", "nunique"),
    activity_duration_seconds=(
        "timestamp",
        lambda x: (x.max() - x.min()).total_seconds()
    )
).reset_index()

    # Total login attempts
    feature_df["total_login_attempts"] = (
        feature_df["failed_login_count"] +
        feature_df["successful_login_count"]
    )

    # Failure ratio
    feature_df["failure_ratio"] = (
        feature_df["failed_login_count"] /
        feature_df["total_login_attempts"]
    )

    # Avoid division by zero
    # A 5-minute window contains 300 seconds
    WINDOW_SECONDS = 5 * 60
    feature_df["attempts_per_second"] = (
    feature_df["total_login_attempts"] /
    WINDOW_SECONDS
)

    return feature_df

def prepare_ml_data(feature_df):
    feature_columns = [
        "failed_login_count",
        "successful_login_count",
         "unique_users",
        "total_login_attempts",
        "failure_ratio",
        "activity_duration_seconds",
        "attempts_per_second"
    ]

    X = feature_df[feature_columns]

    return X