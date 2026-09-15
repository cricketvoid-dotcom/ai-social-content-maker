# AI Social Content Maker

AI-assisted social media content planning for local businesses.

## Current version: V4 — Content Calendar

- Save reusable business branding profiles
- Generate an Instagram post, caption, hashtags, and CTA
- Generate reel scripts and carousel concepts
- Generate posting-time suggestions
- Build a 7-day or 30-day content calendar
- Choose a target publishing frequency from 2–7 posts/week
- Use a saved brand profile when building the calendar
- Export the branded post preview as PNG
- SQLite persistence for brand profiles
- Local deterministic fallback when no AI API key is configured

## Architecture

- `frontend/` — Next.js + React + TypeScript web app
- `backend/` — FastAPI API
- `backend/app/services/content.py` — V1/V2 content generation
- `backend/app/services/brands.py` — V3 SQLite brand persistence
- `backend/app/services/calendar.py` — V4 calendar planning

## API

- `GET /health`
- `GET /api/v1/brands`
- `POST /api/v1/brands`
- `GET /api/v1/brands/{brand_id}`
- `PUT /api/v1/brands/{brand_id}`
- `DELETE /api/v1/brands/{brand_id}`
- `POST /api/v1/generate`
- `POST /api/v1/calendar`

### Calendar request fields

`business_type`, `business_name`, `product_name`, `offer`, `days` (7 or 30 in the UI), `start_date` (optional ISO date), `frequency` (2–7), and optional `brand_id`.

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

Open `http://localhost:3000`.

## Testing

From `backend/`:

```bash
pytest
```

The test suite covers V1/V2 content shape and V4 calendar output. Live dependency installation/build execution may require a network-enabled development environment.

## Product roadmap

- V1 — Core MVP
- V2 — Content AI
- V3 — Business Branding
- V4 — Content Calendar
- V5 — Automation + analytics
