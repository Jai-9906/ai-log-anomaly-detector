import re


def parse_log_line(line):
    ip_match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
    timestamp_match = re.search(
    r"^(\w+ \d+ \d+:\d+:\d+)",
    line
)

    if "Failed password" in line:
        username_match = re.search(r"Failed password for (\w+) from", line)

        if username_match and ip_match and timestamp_match:
         username = username_match.group(1)
         ip = ip_match.group()
         timestamp = timestamp_match.group(1)

        event = {
    "timestamp": timestamp,
    "event_type": "failed_login",
    "username": username,
    "ip": ip,
    "status": "failure"
}

        return event

    elif "Accepted password" in line:
        username_match = re.search(r"for (\w+) from", line)

    if username_match and ip_match and timestamp_match:
       username = username_match.group(1)
       ip = ip_match.group()
       timestamp = timestamp_match.group(1)

    event = {
        "timestamp": timestamp,
        "event_type": "successful_login",
        "username": username,
        "ip": ip,
        "status": "success"
    }

    return event

    return None


def parse_log_file(filepath):
    events = []

    with open(filepath, "r") as file:
        for line in file:
            event = parse_log_line(line.strip())

            if event is not None:
                events.append(event)

    return events