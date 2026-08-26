# log_util.py
# A homemade logger. Modernized 2024.
# The logging module felt like "too much magic" in 2013.

import time

LOG_LINES: list[str] = []   # module-level buffer; cleared after each flush_log call


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to a file, then clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
