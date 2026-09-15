from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .services.brands import create_brand, delete_brand, get_brand, list_brands, update_brand
from .services.content import generate_content

app = FastAPI(title="AI Social Content Maker API", version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class BrandProfile(BaseModel):
    business_name: str = Field(min_length=1, max_length=100)
    business_type: str = Field(min_length=1, max_length=80)
    tagline: str = Field(default="", max_length=160)
    primary_color: str = Field(default="#171722", max_length=20)
    secondary_color: str = Field(default="#ffffff", max_length=20)
    accent_color: str = Field(default="#5146d8", max_length=20)
    font_family: str = Field(default="Inter", max_length=60)
    phone: str = Field(default="", max_length=40)
    location: str = Field(default="", max_length=160)
    social_handle: str = Field(default="", max_length=80)
    logo_data: str = Field(default="", max_length=2_500_000)


class BrandResponse(BrandProfile):
    id: int
    created_at: str
    updated_at: str


class ContentResponse(BaseModel):
    headline: str
    subheadline: str
    caption: str
    hashtags: list[str]
    cta: str
    design: dict = Field(default_factory=dict)
    reel_ideas: list[dict] = Field(default_factory=list)
    carousel_ideas: list[dict] = Field(default_factory=list)
    posting_suggestion: dict = Field(default_factory=dict)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-social-content-maker", "version": "3.0.0"}


@app.get("/api/v1/brands", response_model=list[BrandResponse])
def brands() -> list[dict]:
    return list_brands()


@app.post("/api/v1/brands", response_model=BrandResponse, status_code=201)
def create_brand_profile(profile: BrandProfile) -> dict:
    return create_brand(profile.model_dump())


@app.get("/api/v1/brands/{brand_id}", response_model=BrandResponse)
def read_brand(brand_id: int) -> dict:
    result = get_brand(brand_id)
    if not result:
        raise HTTPException(status_code=404, detail="Brand profile not found")
    return result


@app.put("/api/v1/brands/{brand_id}", response_model=BrandResponse)
def edit_brand(brand_id: int, profile: BrandProfile) -> dict:
    result = update_brand(brand_id, profile.model_dump())
    if not result:
        raise HTTPException(status_code=404, detail="Brand profile not found")
    return result


@app.delete("/api/v1/brands/{brand_id}")
def remove_brand(brand_id: int) -> dict:
    if not delete_brand(brand_id):
        raise HTTPException(status_code=404, detail="Brand profile not found")
    return {"deleted": True, "id": brand_id}


@app.post("/api/v1/generate", response_model=ContentResponse)
async def generate(
    business_type: str = Form(...), business_name: str = Form(""),
    product_name: str = Form(...), offer: str = Form(""), price: str = Form(""),
    location: str = Form(""), phone: str = Form(""), additional_info: str = Form(""),
    brand_id: int | None = Form(None), brand_tagline: str = Form(""),
    brand_primary_color: str = Form("#171722"), brand_secondary_color: str = Form("#ffffff"),
    brand_accent_color: str = Form("#5146d8"), brand_font_family: str = Form("Inter"),
    brand_social_handle: str = Form(""), brand_logo: str = Form(""),
    photo: UploadFile | None = File(None),
) -> ContentResponse:
    if brand_id is not None and not get_brand(brand_id):
        raise HTTPException(status_code=404, detail="Brand profile not found")
    result = await generate_content(
        include_v2=True, business_type=business_type, business_name=business_name,
        product_name=product_name, offer=offer, price=price, location=location,
        phone=phone, additional_info=additional_info, has_photo=photo is not None,
        brand_id=brand_id, brand_tagline=brand_tagline, brand_primary_color=brand_primary_color,
        brand_secondary_color=brand_secondary_color, brand_accent_color=brand_accent_color,
        brand_font_family=brand_font_family, brand_social_handle=brand_social_handle,
        brand_logo=brand_logo,
    )
    return ContentResponse(**result)
