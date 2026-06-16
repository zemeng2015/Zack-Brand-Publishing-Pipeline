# Public Release Review

Content ID: `2026-06-17-ai-commerce-copilot`

## Decision

`NEEDS_HUMAN_REVIEW`

## Review Checklist

- [ ] No real seller data is shown.
- [ ] No account credentials, cookies, tokens, browser profiles, or session data are shown.
- [ ] No private employer code or customer data is shown.
- [ ] No real platform mutation is claimed.
- [ ] No official Temu partnership or authorization is claimed.
- [ ] No guaranteed revenue, profit, GMV, traffic, ranking, or listing success is claimed.
- [ ] Screenshots, if added later, use mock or redacted data.
- [ ] Video narration says "demo", "concept", or "private/local deployment" where needed.
- [ ] Platform descriptions do not imply unsafe automation.
- [ ] Final video and cover image have been manually reviewed.

## Allowed Public Claims

- The project explores an AI commerce operations assistant.
- The workflow includes scoring, quote priority, drafts, approval gates, audit evidence, and private/local deployment.
- The engineering focus is safe, auditable enterprise AI delivery.
- AI suggestions stay behind human review boundaries.

## Claims To Avoid

- "Official Temu integration"
- "Automatically operates seller accounts"
- "Guaranteed profit"
- "Guaranteed listing success"
- "Real-time platform sync"
- "Fully autonomous seller bot"

## Approval Instructions

Only after the checklist is complete:

1. Update `content/items/2026-06-17-ai-commerce-copilot.json`.
2. Set `status` to `approved`.
3. Set `safety_review.approved_for_public_release` to `true`.
4. Run:

```bash
python scripts/validate_queue.py
python scripts/export_social_upload_plan.py
python scripts/build_social_auto_upload_handoff.py
```

