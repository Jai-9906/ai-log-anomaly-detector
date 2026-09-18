import random
from datetime import datetime, timedelta

def generate_normal_event(ip, username, timestamp):
    if random.random() < 0.8:
        event = "Accepted password"
    else:
        event = "Failed password"

    return f"{timestamp.strftime('%b %d %H:%M:%S')} server sshd[1000]: {event} for {username} from {ip} port 54321 ssh2"

def generate_normal_logs():
    logs = []

    ips = [
    f"192.168.1.{i}"
    for i in range(10, 60)
]

    usernames = ["jai", "alice", "bob", "admin"]

    timestamp = datetime(2026, 8, 22, 18, 10, 0)

    for _ in range(1000):
        ip = random.choice(ips)
        username = random.choice(usernames)

        timestamp += timedelta(seconds=random.randint(5, 60))

        logs.append(
            generate_normal_event(ip, username, timestamp)
        )

    return logs

def generate_anomalous_logs():
    logs = []

    # --------------------------------------------------
    # Anomaly 1: Many failed logins
    # --------------------------------------------------
    ip = "192.168.1.200"
    username = "root"

    timestamp = datetime(2026, 8, 22, 19, 0, 0)

    for _ in range(50):
        logs.append(
            f"{timestamp.strftime('%b %d %H:%M:%S')} "
            f"server sshd[2000]: Failed password for {username} "
            f"from {ip} port 54321 ssh2"
        )

        timestamp += timedelta(seconds=random.randint(1, 3))


    # --------------------------------------------------
    # Anomaly 2: Many different usernames
    # --------------------------------------------------
    ip = "192.168.1.201"

    usernames = [
        "root",
        "admin",
        "alice",
        "bob",
        "jai",
        "guest",
        "test",
        "user1",
        "user2",
        "developer"
    ]

    timestamp = datetime(2026, 8, 22, 20, 0, 0)

    for _ in range(30):
        username = random.choice(usernames)

        logs.append(
            f"{timestamp.strftime('%b %d %H:%M:%S')} "
            f"server sshd[2001]: Failed password for {username} "
            f"from {ip} port 54321 ssh2"
        )

        timestamp += timedelta(seconds=random.randint(5, 15))


    # --------------------------------------------------
    # Anomaly 3: Very rapid login attempts
    # --------------------------------------------------
    ip = "192.168.1.202"
    username = "admin"

    timestamp = datetime(2026, 8, 22, 21, 0, 0)

    for _ in range(40):
        logs.append(
            f"{timestamp.strftime('%b %d %H:%M:%S')} "
            f"server sshd[2002]: Failed password for {username} "
            f"from {ip} port 54321 ssh2"
        )

        timestamp += timedelta(milliseconds=500)


    # --------------------------------------------------
    # Anomaly 4: Combination of suspicious behavior
    # --------------------------------------------------
    ip = "192.168.1.203"

    usernames = ["root", "admin", "test"]

    timestamp = datetime(2026, 8, 22, 22, 0, 0)

    for _ in range(45):
        username = random.choice(usernames)

        logs.append(
            f"{timestamp.strftime('%b %d %H:%M:%S')} "
            f"server sshd[2003]: Failed password for {username} "
            f"from {ip} port 54321 ssh2"
        )

        timestamp += timedelta(seconds=random.randint(1, 2))


    return logs

normal_logs = generate_normal_logs()
anomalous_logs = generate_anomalous_logs()

all_logs = normal_logs + anomalous_logs

random.shuffle(all_logs)

with open("data/synthetic.log", "w") as file:
    for log in all_logs:
        file.write(log + "\n")

print(f"Generated {len(all_logs)} log entries.")