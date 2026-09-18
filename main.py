from sklearn.metrics import classification_report, confusion_matrix

from src.parser import parse_log_file
from src.data_processor import (
    events_to_dataframe,
    create_features,
    prepare_ml_data
)
from src.anomaly_detector import train_model
from src.risk_scoring import calculate_risk_score, get_severity
from src.explanation import generate_explanation


# Known anomalous IPs in our synthetic dataset
ANOMALOUS_IPS = {
    "192.168.1.200",
    "192.168.1.201",
    "192.168.1.202",
    "192.168.1.203"
}


# Step 1: Parse the log file
events = parse_log_file("data/synthetic.log")


# Step 2: Convert parsed events into a DataFrame
df = events_to_dataframe(events)


# Step 3: Create ML features
features = create_features(df)

print("\nML Features:")
print(features)


# Step 4: Create ground-truth labels
results = features.copy()

results["actual"] = results["ip"].apply(
    lambda ip: -1 if ip in ANOMALOUS_IPS else 1
)


# Step 5: Prepare numerical data for the ML model
X = prepare_ml_data(features)

print("\nML Input:")
print(X)


# Step 6: Train Isolation Forest using normal behavior only
normal_mask = results["actual"] == 1

X_train = X[normal_mask]

model = train_model(X_train)


# Step 7: Detect anomalies on all behavior
predictions = model.predict(X)
scores = model.decision_function(X)

print("\nDetection Summary:")

print(
    f"Total windows: {len(predictions)}"
)

print(
    f"Detected anomalies: {(predictions == -1).sum()}"
)

print(
    f"Detected normal windows: {(predictions == 1).sum()}"
)


# Step 8: Add model predictions to results
results["prediction"] = predictions
results["anomaly_score"] = scores


# Step 9: Calculate risk score
results["risk_score"] = results.apply(
    calculate_risk_score,
    axis=1
)


# Step 10: Determine severity
results["severity"] = results["risk_score"].apply(
    get_severity
)


# Step 11: Generate explanation
results["explanation"] = results.apply(
    generate_explanation,
    axis=1
)


# Step 12: Evaluate the model
print("\nEvaluation:")

print(
    classification_report(
        results["actual"],
        results["prediction"],
        target_names=["Anomaly", "Normal"]
    )
)


# Step 13: Create security report
anomalies = results[
    results["prediction"] == -1
].copy()


# Sort anomalies by risk score
anomalies = anomalies.sort_values(
    by="risk_score",
    ascending=False
)


# Step 14: Display clean security report

print("\n")
print("=" * 60)
print("              AI LOG ANOMALY DETECTOR")
print("=" * 60)

print(f"Total Windows      : {len(results)}")
print(f"Detected Anomalies : {len(anomalies)}")
print(f"Normal Windows     : {(results['prediction'] == 1).sum()}")


print("\n" + "-" * 60)
print("TOP SUSPICIOUS ACTIVITY")
print("-" * 60)


if len(anomalies) == 0:

    print("No suspicious activity detected.")

else:

    print(
        anomalies[
            [
                "ip",
                "time_window",
                "risk_score",
                "severity"
            ]
        ].head(10).to_string(index=False)
    )


print("\n" + "-" * 60)
print("SUSPICIOUS ACTIVITY DETAILS")
print("-" * 60)


if len(anomalies) == 0:

    print("No anomalies to explain.")

else:

    for _, row in anomalies.head(10).iterrows():

        print(f"\nIP Address : {row['ip']}")
        print(f"Time       : {row['time_window']}")
        print(f"Risk Score : {row['risk_score']}/100")
        print(f"Severity   : {row['severity']}")
        print(f"Reason     : {row['explanation']}")


print("\n" + "=" * 60)
print("                    REPORT COMPLETE")
print("=" * 60)

# Step 15: Display detected anomalies
print("\nDetected Anomalies:")

anomalies = results[
    results["prediction"] == -1
]

print(
    anomalies[
        [
            "ip",
            "time_window",
            "failed_login_count",
            "successful_login_count",
            "unique_users",
            "failure_ratio",
            "attempts_per_second",
            "risk_score",
            "severity"
        ]
    ].to_string(index=False)
)