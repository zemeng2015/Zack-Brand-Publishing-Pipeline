from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS_DIR = ROOT / "content" / "items"
PUBLISHED_LOG_PATH = ROOT / "content" / "published_log.json"
VALID_STATUSES = {"draft", "needs_review", "approved", "published", "archived"}
VALID_FORMATS = {"blog", "short_video", "long_video", "linkedin_post", "github_readme", "homepage_case"}
REQUIRED_FIELDS = {
    "id",
    "status",
    "source_project",
    "audience",
    "brand_pillar",
    "title",
    "formats",
    "platforms",
    "safety_review",
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]+$")


def fail(path: Path, message: str) -> str:
    return f"{path.relative_to(ROOT)}: {message}"


def validate_item(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [fail(path, f"invalid JSON: {exc}")]

    missing = sorted(REQUIRED_FIELDS - data.keys())
    if missing:
        errors.append(fail(path, f"missing fields: {', '.join(missing)}"))

    item_id = data.get("id")
    if not isinstance(item_id, str) or not ID_PATTERN.match(item_id):
        errors.append(fail(path, "id must be lowercase kebab-case"))

    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(fail(path, f"status must be one of: {', '.join(sorted(VALID_STATUSES))}"))

    title = data.get("title", {})
    if not isinstance(title, dict) or not title.get("zh") or not title.get("en"):
        errors.append(fail(path, "title.zh and title.en are required"))

    formats = data.get("formats", [])
    if not isinstance(formats, list) or not formats:
        errors.append(fail(path, "formats must be a non-empty list"))
    else:
        invalid_formats = [value for value in formats if value not in VALID_FORMATS]
        if invalid_formats:
            errors.append(fail(path, f"invalid formats: {', '.join(invalid_formats)}"))

    platforms = data.get("platforms", [])
    if not isinstance(platforms, list) or not platforms:
        errors.append(fail(path, "platforms must be a non-empty list"))
    else:
        for index, platform in enumerate(platforms):
            for field in ("name", "title", "description", "tags"):
                if field not in platform:
                    errors.append(fail(path, f"platforms[{index}] missing {field}"))
            if "tags" in platform and not isinstance(platform["tags"], list):
                errors.append(fail(path, f"platforms[{index}].tags must be a list"))

    review = data.get("safety_review", {})
    if not isinstance(review, dict):
        errors.append(fail(path, "safety_review must be an object"))
    else:
        if "approved_for_public_release" not in review:
            errors.append(fail(path, "safety_review.approved_for_public_release is required"))
        if not review.get("notes"):
            errors.append(fail(path, "safety_review.notes is required"))
        if status == "approved" and review.get("approved_for_public_release") is not True:
            errors.append(fail(path, "approved items require safety_review.approved_for_public_release=true"))

    assets = data.get("assets", {})
    if isinstance(assets, dict):
        for label, value in assets.items():
            asset_path = ROOT / value
            if value and not asset_path.exists():
                errors.append(fail(path, f"asset {label} not found: {value}"))

    return errors


def validate_published_log() -> list[str]:
    if not PUBLISHED_LOG_PATH.exists():
        return [f"content/published_log.json: file is required"]

    try:
        data = json.loads(PUBLISHED_LOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"content/published_log.json: invalid JSON: {exc}"]

    entries = data.get("entries")
    if not isinstance(entries, list):
        return ["content/published_log.json: entries must be a list"]

    errors: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for index, entry in enumerate(entries):
        for field in ("content_id", "platform", "published_url", "published_at"):
            if not entry.get(field):
                errors.append(f"content/published_log.json: entries[{index}] missing {field}")
        key = (entry.get("content_id", ""), entry.get("platform", ""), entry.get("published_url", ""))
        if key in seen:
            errors.append(f"content/published_log.json: duplicate entry for {key[0]} on {key[1]}")
        seen.add(key)
    return errors


def main() -> int:
    item_paths = sorted(ITEMS_DIR.glob("*.json"))
    if not item_paths:
        print("No content items found.")
        return 1

    errors: list[str] = []
    for path in item_paths:
        errors.extend(validate_item(path))
    errors.extend(validate_published_log())

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {len(item_paths)} content item(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
