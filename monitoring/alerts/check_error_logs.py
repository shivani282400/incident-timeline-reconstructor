"""Simple monitoring script for detecting ERROR log entries."""

import logging
from pathlib import Path
import sys


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger(__name__)


def main() -> int:
    """Scan a log file and report whether ERROR entries exist."""
    log_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tests/testdata/sample_logs.txt")

    if not log_file.exists():
        print(f"CRITICAL: log file missing - {log_file}")
        LOGGER.error("Monitoring failed because the log file does not exist: %s", log_file)
        return 2

    error_lines = []
    with log_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            if " ERROR " in line:
                error_lines.append(line.strip())

    if not error_lines:
        print(f"OK: no ERROR entries found in {log_file}")
        LOGGER.info("No ERROR entries found in %s", log_file)
        return 0

    print(f"CRITICAL: {len(error_lines)} ERROR entries found in {log_file}")
    for entry in error_lines:
        print(entry)
    LOGGER.warning("Detected %s ERROR entries in %s", len(error_lines), log_file)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
