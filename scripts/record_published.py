from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "content" / "published_log.json"


def load_log() -> dict:
    if not LOG_PATH.exists():
        return {"entries": []}
    return json.loads(LOG_PATH.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a published platform URL.")
    parser.add_argument("--content-id", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    log = load_log()
    entries = log.setdefault("entries", [])
    duplicate = next(
        (
            entry
            for entry in entries
            if entry.get("content_id") == args.content_id and entry.get("platform") == args.platform and entry.get("published_url") == args.url
        ),
        None,
    )
    if duplicate:
        print("Published URL already exists in log.")
        return 0

    entries.append(
        {
            "content_id": args.content_id,
            "platform": args.platform,
            "published_url": args.url,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "notes": args.notes,
        }
    )
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded published URL for {args.content_id} on {args.platform}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

