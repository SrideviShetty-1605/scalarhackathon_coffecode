import os
import csv
import time

LOGFILE = os.path.join(os.getcwd(), "demo", "latency_logs.csv")
os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

def log_timings(sample: str, timings: dict):
    """
    Append a row with timings to demo/latency_logs.csv
    """
    header = [
        "timestamp",
        "sample",
        "fillers_ms",
        "repetition_ms",
        "tone_ms",
        "languagetool_ms",
        "format_ms",
        "total_ms",
    ]
    write_header = not os.path.exists(LOGFILE)

    with open(LOGFILE, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(header)
        row = [
            time.time(),
            sample,
            timings.get("fillers_ms", ""),
            timings.get("repetition_ms", ""),
            timings.get("tone_ms", ""),
            timings.get("languagetool_ms", ""),
            timings.get("format_ms", ""),
            timings.get("total_ms", ""),
        ]
        w.writerow(row)
