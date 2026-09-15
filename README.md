# AI Social Content Maker

AI-assisted social media content planning, optimization, analytics, and publishing infrastructure for local businesses.

## Current version: V10 — Advanced Analytics + AI Growth Engine

- Save reusable business branding profiles
- Generate Instagram posts, captions, hashtags, and CTAs
- Generate reel scripts and carousel concepts
- Build 7-day or 30-day content calendars
- Export branded post previews as PNG
- Track impressions, reach, likes, comments, shares, saves, and clicks
- Calculate engagement and click rates
- Get performance recommendations
- Create normalized scheduling records
- Optimize content using performance metrics
- Generate platform-specific content for Instagram, Facebook, YouTube Shorts, LinkedIn, and X
- Store social account connection metadata without returning authorization tokens
- Validate publishing payloads through a provider abstraction
- Safe dry-run publishing mode
- Create queued scheduler jobs with scheduled timestamps
- Retry failed jobs with a bounded three-attempt policy
- Score individual content by engagement, sharing/saving, and click signals
- Rank top-performing content and identify the strongest format
- Generate actionable growth strategy and next experiments
- Dedicated V10 AI Growth dashboard at `/growth`
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `frontend/app/platforms/page.tsx` — V7 multi-platform dashboard
- `frontend/app/connections/page.tsx` — V8 connection and publishing dashboard
- `frontend/app/growth/page.tsx` — V10 advanced analytics and AI growth dashboard
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 generation
- `backend/app/services/brands.py` — V3 SQLite branding
- `backend/app/services/calendar.py` — V4 planning
- `backend/app/services/automation.py` — V5 analytics and scheduling
- `backend/app/services/optimizer.py` — V6 performance-driven optimization
- `backend/app/services/platforms.py` — V7 platform-specific content transformation
- `backend/app/services/connections.py` — V8 connection records
- `backend/app/services/publisher.py` — V8 publishing abstraction and dry-run safety layer
- `backend/app/services/scheduler.py` — V9 queued jobs and bounded retry handling
- `backend/app/services/growth.py` — V10 growth scoring and strategy engine

## V10 API

- `POST /api/v1/growth/insights`
- Existing V1–V9 APIs remain available

V10 turns post-level performance data into deterministic growth signals. It ranks winning content, compares formats, and suggests focused experiments. It does not claim that historical metrics prove future performance; recommendations are decision-support signals that should be tested.

## Testing

From `backend/`:

```bash
pytest
```

The suite covers content generation, calendar planning, automation/analytics, V6 optimization, V7 platform transformation, V8 connection/publisher safety behavior, V9 scheduler retry behavior, and V10 growth scoring/insights. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
- V6 — Smart Content Optimizer
- V7 — Multi-Platform Content Engine
- V8 — Account Connections + Safe Publishing Pipeline
- V9 — OAuth-ready provider architecture + production scheduler core
- V10 — Advanced Analytics + AI Growth Engine
