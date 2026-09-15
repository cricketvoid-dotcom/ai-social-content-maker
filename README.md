# AI Social Content Maker

V1 MVP for creating Instagram-ready promotional content for local businesses.

## V1 goals

- Enter business/product details
- Upload a product photo
- Generate a polished Instagram post concept
- Generate caption, hashtags, and CTA
- Export the post as a 1080x1080 PNG

## Architecture

- `frontend/` — Next.js web app
- `backend/` — FastAPI API
- AI provider is isolated behind a small service layer so it can be swapped later.

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

## V1 implementation note

The visual is rendered with HTML/CSS and browser canvas instead of asking an image model to draw text. This keeps prices, business names, offers, and contact information sharp and reliable.
