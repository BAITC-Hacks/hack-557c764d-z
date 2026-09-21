"""Печать критичных событий и их количества, без внешних зависимостей."""

import argparse
import json
from pathlib import Path


def filter_critical(events: list[dict]) -> list[dict]:
    return [event for event in events if event["level"] == "critical"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", type=Path,
        default=Path(__file__).with_name("events.json"),
        help="JSON-массив событий с полями message и level",
    )
    args = parser.parse_args()
    try:
        events = json.loads(args.path.read_text(encoding="utf-8-sig"))
        if not isinstance(events, list) or any(
            not isinstance(event, dict)
            or not isinstance(event.get("message"), str)
            or event.get("level") not in ("info", "warn", "critical")
            for event in events
        ):
            raise ValueError("Нужен массив событий с текстом message и level: info/warn/critical")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(1, f"Не удалось прочитать события: {exc}\n")

    critical = filter_critical(events)
    for event in critical:
        print(f"{event['message']} ({event['level']})")
    print(f"критичных {len(critical)}")


if __name__ == "__main__":
    main()
