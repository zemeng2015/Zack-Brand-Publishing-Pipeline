from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS_DIR = ROOT / "content" / "items"
EXPORTS_DIR = ROOT / "exports"


def load_items() -> list[dict]:
    items: list[dict] = []
    for path in sorted(ITEMS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") == "approved" and data.get("safety_review", {}).get("approved_for_public_release") is True:
            items.append(data)
    return items


def build_plan(items: list[dict]) -> dict:
    exports = []
    for item in items:
        for platform in item["platforms"]:
            exports.append(
                {
                    "content_id": item["id"],
                    "source_project": item["source_project"],
                    "platform": platform["name"],
                    "title": platform["title"],
                    "description": platform["description"],
                    "tags": platform["tags"],
                    "scheduled_for": platform.get("scheduled_for"),
                    "assets": item.get("assets", {}),
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "publisher": "manual-or-social-auto-upload-bridge",
        "items": exports,
    }


def main() -> int:
    EXPORTS_DIR.mkdir(exist_ok=True)
    items = load_items()
    plan = build_plan(items)
    output = EXPORTS_DIR / "social-upload-plan.json"
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(plan['items'])} platform upload task(s) to {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

