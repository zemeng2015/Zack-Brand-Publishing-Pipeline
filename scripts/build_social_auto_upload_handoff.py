from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "exports" / "social-upload-plan.json"
HANDOFF_DIR = ROOT / "exports" / "social-auto-upload"
HANDOFF_PATH = HANDOFF_DIR / "upload_tasks.json"


def main() -> int:
    if not PLAN_PATH.exists():
        print("Upload plan not found. Run scripts/export_social_upload_plan.py first.")
        return 1

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    tasks = []
    for item in plan.get("items", []):
        assets = item.get("assets", {})
        tasks.append(
            {
                "platform": item["platform"],
                "title": item["title"],
                "description": item["description"],
                "tags": item["tags"],
                "video_path": assets.get("video_path", ""),
                "cover_path": assets.get("cover_path", ""),
                "scheduled_for": item.get("scheduled_for"),
                "content_id": item["content_id"],
                "source_project": item["source_project"],
                "manual_review_required": True,
            }
        )

    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    HANDOFF_PATH.write_text(json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(tasks)} social-auto-upload handoff task(s) at {HANDOFF_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

