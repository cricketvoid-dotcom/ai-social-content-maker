# AI Social Content Maker

AI-assisted social media content planning, optimization, and publishing infrastructure for local businesses.

## Current version: V8 — Account Connections + Safe Publishing Pipeline

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
- Disconnect saved accounts
- Validate publishing payloads
- Run a safe publisher dry-run that makes no external social-platform request
- Dedicated V8 account dashboard at `/connections`
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `frontend/app/platforms/page.tsx` — V7 multi-platform dashboard
- `frontend/app/connections/page.tsx` — V8 connection and publishing dashboard
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 generation
- `backend/app/services/brands.py` — V3 SQLite branding
- `backend/app/services/calendar.py` — V4 planning
- `backend/app/services/automation.py` — V5 analytics and scheduling
- `backend/app/services/optimizer.py` — V6 performance-driven optimization
- `backend/app/services/platforms.py` — V7 platform-specific content transformation
- `backend/app/services/connections.py` — V8 connection records
- `backend/app/services/publisher.py` — V8 publishing abstraction and dry-run safety layer

## V8 API

- `GET /api/v1/providers`
- `GET /api/v1/connections`
- `POST /api/v1/connections`
- `DELETE /api/v1/connections/{connection_id}`
- `POST /api/v1/publish`

V8 intentionally defaults to a **dry-run publisher**. It does not claim to publish to Instagram, Facebook, YouTube, LinkedIn, or X without the required OAuth authorization, platform-specific permissions, media handling, and approved developer configuration.

Authorization tokens are never returned by the connection API. The current V8 database stores only a short SHA-256 fingerprint and connection metadata; it is not yet a production-grade OAuth token vault.

## Platform API considerations

Platform integrations have different authorization and publishing requirements. For example, YouTube's `videos.insert` requires OAuth authorization and supports video upload, while LinkedIn's current Posts API supports creating posts with the appropriate permissions. These requirements are kept behind provider adapters instead of being hard-coded into the core content engine.

## Testing

From `backend/`:

```bash
pytest
```

The suite covers content generation, calendar planning, automation/analytics, V6 optimization, V7 platform transformation, and V8 connection/publisher safety behavior. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
- V6 — Smart Content Optimizer
- V7 — Multi-Platform Content Engine
- V8 — Account Connections + Safe Publishing Pipeline
- V9 — Approved OAuth provider adapters + production scheduler
