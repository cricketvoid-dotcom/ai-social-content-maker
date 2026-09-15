# AI Social Content Maker

AI-assisted social media content planning and optimization for local businesses.

## Current version: V6 — Smart Content Optimizer

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
- Receive a stronger hook, CTA, strategy, and recommended format length
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 generation
- `backend/app/services/brands.py` — V3 SQLite branding
- `backend/app/services/calendar.py` — V4 planning
- `backend/app/services/automation.py` — V5 analytics and scheduling
- `backend/app/services/optimizer.py` — V6 performance-driven optimization

## V6 API

`POST /api/v1/optimizer`

Fields:
- `content_type`: Reel, Carousel, Post, or Story
- `title`: content title
- `metrics`: JSON string containing analytics metrics

The optimizer is intentionally deterministic and explainable. It does not invent historical performance or claim access to a social platform account.

## Testing

From `backend/`:

```bash
pytest
```

The suite covers content generation, calendar planning, automation/analytics, and V6 optimization. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
- V6 — Smart Content Optimizer
