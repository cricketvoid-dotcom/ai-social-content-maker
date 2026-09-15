# AI Social Content Maker

AI-assisted social media content planning for local businesses.

## Current version: V5 — Automation + Analytics

- Save reusable business branding profiles
- Generate an Instagram post, caption, hashtags, and CTA
- Generate reel scripts and carousel concepts
- Generate posting-time suggestions
- Build a 7-day or 30-day content calendar
- Choose a target publishing frequency from 2–7 posts/week
- Use a saved brand profile when building the calendar
- Export the branded post preview as PNG
- SQLite persistence for brand profiles
- Track impressions, reach, likes, comments, shares, saves, and clicks
- Calculate engagement and click rates
- Get rule-based performance recommendations
- Create normalized scheduling records for future publisher integrations
- Dedicated V5 Automation & Analytics dashboard at `/automation`
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `frontend/app/automation/page.tsx` — V5 analytics and scheduling dashboard
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 content generation
- `backend/app/services/brands.py` — V3 SQLite brand persistence
- `backend/app/services/calendar.py` — V4 calendar planning
- `backend/app/services/automation.py` — V5 scheduling, analytics, and recommendations

## API

- `GET /health`
- `GET /api/v1/brands`
- `POST /api/v1/brands`
- `GET /api/v1/brands/{brand_id}`
- `PUT /api/v1/brands/{brand_id}`
- `DELETE /api/v1/brands/{brand_id}`
- `POST /api/v1/generate`
- `POST /api/v1/calendar`
- `POST /api/v1/automation/schedule`
- `POST /api/v1/analytics`
- `POST /api/v1/analytics/recommendation`

## V5 notes

The scheduling endpoint creates a normalized schedule record; it does not pretend to publish directly to Instagram. Actual publishing requires an approved social-platform connection and the appropriate credentials/permissions.

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Copy `backend/.env.example` to `backend/.env` and add an AI API key when using live AI generation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` or `/automation`.

## Testing

From `backend/`:

```bash
pytest
```

The suite includes V1/V2 content, V4 calendar, and V5 automation/analytics tests. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
