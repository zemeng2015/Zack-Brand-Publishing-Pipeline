# social-auto-upload Integration Plan

`dreammis/social-auto-upload` can be used as the final publishing bridge after content is approved.

This repository should remain the source of truth for:

- content items
- titles and descriptions
- tags
- script paths
- cover prompts
- review status
- release logs

`social-auto-upload` should only receive approved tasks.

## Integration Boundary

Allowed:

- export approved metadata
- copy reviewed video paths into an upload folder
- call a local upload command manually or from a scheduled local job
- record published URLs back into a release log

Not allowed:

- storing platform passwords in this repository
- committing cookies or browser profiles
- bypassing platform restrictions
- auto-publishing unreviewed AI-generated content
- uploading videos that contain private employer, customer, seller, account, or credential data

## Proposed Handoff Shape

```json
{
  "platform": "bilibili",
  "title": "跨境电商 AI 助手：从 Demo 到私有部署系统",
  "description": "拆解一个 AI Commerce Copilot 项目...",
  "tags": ["AI", "跨境电商", "AWS"],
  "video_path": "videos/final/ai-commerce-copilot.mp4",
  "cover_path": "covers/final/ai-commerce-copilot.jpg"
}
```

The exact adapter should be added only after local manual publishing works reliably.

