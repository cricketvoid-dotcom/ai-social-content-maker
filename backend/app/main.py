from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .services.content import generate_content

app = FastAPI(title="AI Social Content Maker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContentResponse(BaseModel):
    headline: str
    subheadline: str
    caption: str
    hashtags: list[str]
    cta: str
    design: dict = Field(default_factory=dict)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-social-content-maker"}


@app.post("/api/v1/generate", response_model=ContentResponse)
async def generate(
    business_type: str = Form(...),
    business_name: str = Form(""),
    product_name: str = Form(...),
    offer: str = Form(""),
    price: str = Form(""),
    location: str = Form(""),
    phone: str = Form(""),
    additional_info: str = Form(""),
    photo: UploadFile | None = File(None),
) -> ContentResponse:
    # V1 keeps image handling intentionally lightweight: the browser previews and
    # renders the uploaded photo. The AI layer receives business copy fields.
    result = await generate_content(
        business_type=business_type,
        business_name=business_name,
        product_name=product_name,
        offer=offer,
        price=price,
        location=location,
        phone=phone,
        additional_info=additional_info,
        has_photo=photo is not None,
    )
    return ContentResponse(**result)
