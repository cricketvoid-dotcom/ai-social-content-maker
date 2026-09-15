# AI Social Content Maker

ContentForge is an AI-assisted social media content maker for local businesses. It turns one business brief into an Instagram post, caption, reels, carousels, and a reusable visual brand identity.

## Versions

### V1 — Core MVP
- Enter business/product details
- Upload a product photo
- Generate an Instagram post concept
- Generate caption, hashtags, and CTA
- Export the post as a PNG

### V2 — Content AI
- 3 reel concepts with hooks, scripts, and durations
- 2 carousel concepts with slide-by-slide structure
- Posting-day, time, and frequency suggestions
- AI provider with deterministic local fallback

### V3 — Business Branding
- Save multiple business brand profiles in SQLite
- Business name/type and tagline
- Primary, secondary, and accent colors
- Preferred font
- Phone, location, and social handle
- Logo upload with a 1.5 MB client-side limit
- Select a saved brand and reuse it for future generations
- Branded live post preview and PNG export
- Brand identity is included in AI generation context
- Brand CRUD API with automated persistence tests

## Architecture

- `frontend/` — Next.js web app
- `backend/` — FastAPI API
- `backend/app/services/content.py` — content generation and fallback logic
- `backend/app/services/brands.py` — SQLite brand persistence
- `backend/tests/` — backend tests

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

## Brand API

- `GET /api/v1/brands` — list saved profiles
- `POST /api/v1/brands` — create a profile
- `GET /api/v1/brands/{id}` — read a profile
- `PUT /api/v1/brands/{id}` — replace/update a profile
- `DELETE /api/v1/brands/{id}` — delete a profile

The SQLite database is created automatically at `backend/contentforge.db` (or the path supplied by `BRAND_DB_PATH`).

## Implementation note

The visual post is rendered with HTML/CSS instead of asking an image model to draw text. This keeps prices, business names, offers, contact information, and branding sharp and reliable. Logo data is stored in the local SQLite profile for this MVP; production deployment should move binary assets to object storage.
