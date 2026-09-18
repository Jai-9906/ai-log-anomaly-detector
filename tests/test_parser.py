from src.parser import parse_log_line


def test_failed_login_parsing():

    line = (
        "Aug 22 18:11:10 server sshd[1008]: "
        "Failed password for root from 192.168.1.20 "
        "port 54328 ssh2"
    )

    event = parse_log_line(line)

    assert event is not None
    assert event["event_type"] == "failed_login"
    assert event["username"] == "root"
    assert event["ip"] == "192.168.1.20"
    assert event["status"] == "failure"