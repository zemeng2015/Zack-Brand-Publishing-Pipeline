# Zack Brand Publishing Pipeline

A lightweight content operations workflow for turning technical projects into publishable personal-brand assets.

This project is designed for Zack Wang's AI engineering brand:

- portfolio-backed technical writing
- short video scripts
- platform-specific metadata
- human review before publishing
- safe handoff to publishing tools such as `social-auto-upload`

It does not store social platform passwords, cookies, tokens, browser profiles, or private session data.

## Why This Exists

Personal technical branding should not be random posting.

The goal is to build a repeatable workflow:

```text
Project progress or AI topic
  -> content brief
  -> blog outline
  -> short video script
  -> cover image prompt
  -> platform metadata
  -> human approval
  -> publish queue
  -> release log
```

## Core Workflow

1. Create an item in `content/items/`.
2. Fill in title, audience, source project, formats, platform metadata, and safety notes.
3. Run validation:

```bash
python scripts/validate_queue.py
```

4. Review `publish_queue/approved/`.
5. Export approved items to the future upload bridge:

```bash
python scripts/export_social_upload_plan.py
```

6. Publish manually or connect the exported plan to an automation tool.

## Content Status

Use these statuses:

- `draft`: idea is being shaped
- `needs_review`: content is ready for human review
- `approved`: safe to publish
- `published`: already published
- `archived`: not worth publishing

Only `approved` items are exported for publishing.

## Safety Rules

Do not commit:

- social platform cookies
- login passwords
- API tokens
- browser profiles
- customer data
- private employer code
- private seller data
- unreleased credentials or screenshots

For AI/e-commerce projects, content must clearly avoid claiming unsafe integrations, guaranteed profit, official platform partnership, or live account automation unless those facts are explicitly true and safe to disclose.

## Suggested Brand Pillars

- Enterprise AI delivery
- AI evaluation and observability
- AWS-backed AI systems
- Developer productivity
- Local/private AI tools for business operators
- Productized lead-generation systems

## Current Integrations

This repository currently produces a platform-neutral upload plan.

Future integrations can include:

- `dreammis/social-auto-upload`
- GitHub Actions scheduled content checks
- personal homepage updates
- newsletter drafts
- YouTube/Bilibili/Xiaohongshu metadata generation

