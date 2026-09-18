# AI Log Anomaly Detector

An AI-assisted cybersecurity tool that analyzes authentication logs, extracts behavioral features, and uses Isolation Forest to identify unusual login activity.

## Overview

Security logs contain valuable information about authentication activity, but manually analyzing large numbers of log entries can be difficult.

This project processes Linux-style authentication logs and groups login activity into time windows. It then extracts behavioral features such as failed login count, failure ratio, unique users, and login frequency.

An Isolation Forest model is used to identify behavior that differs significantly from the learned normal pattern.

The detected behavior is then assigned a custom risk score and severity level, along with an explanation of the factors that contributed to the result.

> An anomaly indicates unusual behavior; it does not automatically mean that an attack has occurred.

## Problem Statement

Large volumes of authentication logs make it difficult to manually identify unusual login behavior.

Traditional rule-based detection can identify known patterns using fixed thresholds, but it may not detect unusual combinations of otherwise normal-looking behavior.

This project explores an ML-based approach for detecting anomalous authentication behavior from security logs.

## Solution

The system follows this pipeline:

Security Logs  
↓  
Log Parser  
↓  
Structured Events  
↓  
Feature Extraction  
↓  
Time-Window Feature Dataset  
↓  
Isolation Forest  
↓  
Anomaly Detection  
↓  
Risk Scoring  
↓  
Severity + Explanation  
↓  
Security Report

## Features

- Linux-style authentication log parsing
- Failed and successful login detection
- IP and username extraction
- 5-minute time-window analysis
- Behavioral feature engineering
- Isolation Forest anomaly detection
- Normal-behavior-based model training
- Custom risk scoring
- Severity classification
- Human-readable anomaly explanations
- Precision, recall and F1 evaluation
- Confusion matrix
- Automated tests using pytest
- Command-line security report

## Machine Learning Approach

### Isolation Forest

The project uses Isolation Forest, an unsupervised anomaly-detection algorithm.

The basic idea is that unusual observations are easier to isolate from the rest of the data than normal observations.

The model learns patterns from normal authentication behavior and assigns anomaly predictions to new observations.

The predictions are:

- `1` → Normal
- `-1` → Anomaly

The Isolation Forest decision score is used as an anomaly indicator. It is not a probability and should not be interpreted as a percentage risk.

## Feature Engineering

Authentication events are grouped into 5-minute windows for each source IP.

The following features are extracted:

| Feature | Description |
|---|---|
| `failed_login_count` | Number of failed login attempts |
| `successful_login_count` | Number of successful login attempts |
| `unique_users` | Number of distinct usernames involved |
| `total_login_attempts` | Total login attempts |
| `failure_ratio` | Proportion of attempts that failed |
| `activity_duration_seconds` | Time span of activity inside the window |
| `attempts_per_second` | Login activity frequency |

These features convert raw text logs into numerical data that can be processed by the ML model.

## Risk Scoring

The ML prediction and behavioral indicators are combined into a custom risk score from 0 to 100.

The score considers factors such as:

- Number of failed login attempts
- Failure ratio
- Login frequency
- Isolation Forest anomaly prediction

The score is then mapped to custom severity levels:

| Score | Severity |
|---|---|
| 0–29 | LOW |
| 30–59 | MEDIUM |
| 60–79 | HIGH |
| 80–100 | CRITICAL |

These thresholds are project-specific heuristics and are not intended to represent a formal industry risk standard.

## Example Detection

A behavior such as:

- 50 failed login attempts
- 0 successful logins
- 100% failure ratio
- High login frequency

can be identified as unusual by the system and receive a high risk score.

The system also provides an explanation describing the factors that contributed to the assessment.

## Project Structure

```text
ai-anomaly-log-detector/
│
├── data/
│   ├── sample.log
│   └── synthetic.log
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── data_processor.py
│   ├── anomaly_detector.py
│   ├── risk_scoring.py
│   └── explanation.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_data_processor.py
│   ├── test_risk_scoring.py
│   └── test_anomaly_detector.py
│
├── main.py
├── generate_logs.py
├── pytest.ini
└── README.md

