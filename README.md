# AI Social Content Maker

AI-assisted social media content planning and optimization for local businesses.

## Current version: V7 — Multi-Platform Content Engine

- Save reusable business branding profiles
- Generate Instagram posts, captions, hashtags, and CTAs
- Generate reel scripts and carousel concepts
- Build 7-day or 30-day content calendars
- Export branded post previews as PNG
- Track impressions, reach, likes, comments, shares, saves, and clicks
- Calculate engagement and click rates
- Get performance recommendations
- Create normalized scheduling records
- Optimize a content idea using its performance metrics
- Generate platform-specific content for Instagram, Facebook, YouTube Shorts, LinkedIn, and X
- Platform-aware text limits, formats, CTAs, and hashtag suggestions
- Dedicated V7 dashboard at `/platforms`
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `frontend/app/platforms/page.tsx` — V7 multi-platform dashboard
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 generation
- `backend/app/services/brands.py` — V3 SQLite branding
- `backend/app/services/calendar.py` — V4 planning
- `backend/app/services/automation.py` — V5 analytics and scheduling
- `backend/app/services/optimizer.py` — V6 performance-driven optimization
- `backend/app/services/platforms.py` — V7 platform-specific content transformation

## V7 API

`POST /api/v1/platforms`

Fields:
- `business_name`: business name
- `topic`: campaign/topic
- `base_caption`: optional starting caption
- `platform_list`: comma-separated platform names

Supported platforms: Instagram, Facebook, YouTube Shorts, LinkedIn, X.

V7 generates content variations locally and does not claim access to any user's social account. Live publishing requires each platform's approved developer access, OAuth/authorization, and applicable permissions.

## Testing

From `backend/`:

```bash
pytest
```

The suite covers content generation, calendar planning, automation/analytics, V6 optimization, and V7 platform transformation. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
- V6 — Smart Content Optimizer
- V7 — Multi-Platform Content Engine
