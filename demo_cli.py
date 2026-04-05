import argparse
from tools.fake_tool_interface import get_recent_logs, get_service_logs, search_logs


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo CLI for the fake log tool interface")
    parser.add_argument("--tool", required=True, choices=["get_recent_logs", "get_service_logs", "search_logs"])
    parser.add_argument("--log", required=True, help="Path to a log file")
    parser.add_argument("--lines", type=int, default=50)
    parser.add_argument("--service", default="")
    parser.add_argument("--pattern", default="")
    args = parser.parse_args()

    if args.tool == "get_recent_logs":
        result = get_recent_logs(args.log, args.lines)
    elif args.tool == "get_service_logs":
        if not args.service:
            raise SystemExit("--service is required for get_service_logs")
        result = get_service_logs(args.log, args.service, args.lines)
    else:
        if not args.pattern:
            raise SystemExit("--pattern is required for search_logs")
        result = search_logs(args.log, args.pattern, args.lines)

    print("=" * 80)
    print(f"Tool used: {args.tool}")
    print(f"Log file: {args.log}")
    print("=" * 80)
    print(result)
    print("=" * 80)
    print("Paste the output above into Claude and ask it to analyze the logs.")


if __name__ == "__main__":
    main()
