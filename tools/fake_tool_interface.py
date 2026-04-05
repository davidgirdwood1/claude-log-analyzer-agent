from pathlib import Path
from typing import List


def _read_lines(log_path: str) -> List[str]:
    path = Path(log_path)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")
    return path.read_text(encoding="utf-8").splitlines()


def get_recent_logs(log_path: str, lines: int = 50) -> str:
    """Return the newest N lines from a log file."""
    data = _read_lines(log_path)
    return "\n".join(data[-lines:])



def get_service_logs(log_path: str, service: str, lines: int = 50) -> str:
    """Return matching lines for a service or keyword, up to N most recent matches."""
    data = _read_lines(log_path)
    matches = [line for line in data if service in line]
    return "\n".join(matches[-lines:])



def search_logs(log_path: str, pattern: str, lines: int = 50) -> str:
    """Return matching lines for an arbitrary pattern, up to N most recent matches."""
    data = _read_lines(log_path)
    matches = [line for line in data if pattern.lower() in line.lower()]
    return "\n".join(matches[-lines:])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fake tool interface for log retrieval")
    parser.add_argument("tool", choices=["get_recent_logs", "get_service_logs", "search_logs"])
    parser.add_argument("log_path")
    parser.add_argument("--lines", type=int, default=50)
    parser.add_argument("--service", default="")
    parser.add_argument("--pattern", default="")
    args = parser.parse_args()

    if args.tool == "get_recent_logs":
        print(get_recent_logs(args.log_path, args.lines))
    elif args.tool == "get_service_logs":
        if not args.service:
            raise SystemExit("--service is required for get_service_logs")
        print(get_service_logs(args.log_path, args.service, args.lines))
    elif args.tool == "search_logs":
        if not args.pattern:
            raise SystemExit("--pattern is required for search_logs")
        print(search_logs(args.log_path, args.pattern, args.lines))
