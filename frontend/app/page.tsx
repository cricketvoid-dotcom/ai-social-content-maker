"use client";

import { ChangeEvent, useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Reel = { title: string; hook: string; script: string[]; duration: string };
type CreativeContent = {
  headline: string;
  subheadline: string;
  caption: string;
  hashtags: string[];
  cta: string;
  reel_ideas: Reel[];
};

const initial = {
  businessName: "",
  businessType: "",
  phone: "",
  address: "",
  additionalInfo: "",
  productName: "",
  offer: "",
};

export default function Home() {
  const [form, setForm] = useState(initial);
  const [creativeFile, setCreativeFile] = useState<File | null>(null);
  const [creativePreview, setCreativePreview] = useState("");
  const [creativeImage, setCreativeImage] = useState("");
  const [creativeContent, setCreativeContent] = useState<CreativeContent | null>(null);
  const [creativePrompt, setCreativePrompt] = useState(
    "Premium realistic marketing photography. Improve lighting, sharpness, composition and background while preserving the exact product."
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => () => {
    if (creativePreview) URL.revokeObjectURL(creativePreview);
  }, [creativePreview]);

  function update(key: keyof typeof initial, value: string) {
    setForm((old) => ({ ...old, [key]: value }));
  }

  function onCreativeFile(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    if (creativePreview) URL.revokeObjectURL(creativePreview);
    setCreativeFile(file);
    setCreativePreview(file ? URL.createObjectURL(file) : "");
    setCreativeImage("");
    setCreativeContent(null);
    setError("");
  }

  async function generate() {
    if (!creativeFile) {
      setError("Upload a product photo first.");
      return;
    }
    if (!form.businessName || !form.businessType || !form.productName) {
      setError("Please enter business name, business type and product/service.");
      return;
    }

    setLoading(true);
    setError("");
    setCreativeImage("");
    setCreativeContent(null);

    try {
      const imageData = new FormData();
      imageData.append("image", creativeFile);
      imageData.append("prompt", creativePrompt);
      imageData.append("business_name", form.businessName);
      imageData.append("product_name", form.productName);

      const imageResponse = await fetch(`${API_URL}/api/v1/creative/image`, {
        method: "POST",
        body: imageData,
      });
      if (!imageResponse.ok) {
        throw new Error((await imageResponse.text()) || "Image generation failed");
      }

      const imageResult = await imageResponse.json();
      setCreativeImage(imageResult.image_data);

      const contentData = new FormData();
      contentData.append("business_type", form.businessType);
      contentData.append("business_name", form.businessName);
      contentData.append("product_name", form.productName);
      contentData.append("offer", form.offer);
      contentData.append("price", "");
      contentData.append("location", form.address);
      contentData.append("phone", form.phone);
      contentData.append("additional_info", form.additionalInfo);

      const contentResponse = await fetch(`${API_URL}/api/v1/generate`, {
        method: "POST",
        body: contentData,
      });
      if (!contentResponse.ok) {
        throw new Error((await contentResponse.text()) || "Content generation failed");
      }

      const contentResult = await contentResponse.json();
      setCreativeContent(contentResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <div className="container">
        <header className="topbar">
          <div className="logo">ContentForge</div>
          <span className="badge">AI Social Content Maker</span>
        </header>

        <section className="hero">
          <h1>Create professional social content in one simple workflow.</h1>
          <p>Enter the business details, upload a product photo, and let AI create the marketing image and social content.</p>
        </section>

        <section className="card">
          <div className="section-head">
            <div>
              <h2>Business Information</h2>
              <div className="muted">Only the basic information needed to create accurate content.</div>
            </div>
          </div>

          <div className="form">
            <div className="row">
              <Field label="Business name *" value={form.businessName} onChange={(v) => update("businessName", v)} placeholder="e.g. Urban Threads" required />
              <Field label="Business type *" value={form.businessType} onChange={(v) => update("businessType", v)} placeholder="e.g. Clothing brand" required />
            </div>
            <div className="row">
              <Field label="Contact number" value={form.phone} onChange={(v) => update("phone", v)} placeholder="e.g. 98765 43210" />
              <Field label="Address" value={form.address} onChange={(v) => update("address", v)} placeholder="e.g. Vasant Kunj, New Delhi" />
            </div>
            <div className="field">
              <label>Additional information <span className="muted">(optional)</span></label>
              <textarea value={form.additionalInfo} onChange={(e) => update("additionalInfo", e.target.value)} placeholder="Opening hours, delivery details, special features, website, social handle, etc." />
            </div>
          </div>
        </section>

        <section className="card" style={{ marginTop: 22 }}>
          <div className="section-head">
            <div>
              <h2>✨ AI Image Generation</h2>
              <div className="muted">Upload an ordinary product photo and turn it into a professional marketing image.</div>
            </div>
          </div>

          <div className="form">
            <div className="row">
              <Field label="Product / service *" value={form.productName} onChange={(v) => update("productName", v)} placeholder="e.g. Oversized Black Hoodie" required />
              <Field label="Offer or price" value={form.offer} onChange={(v) => update("offer", v)} placeholder="e.g. ₹999 or 20% off" />
            </div>

            <div className="field">
              <label>Creative direction</label>
              <textarea value={creativePrompt} onChange={(e) => setCreativePrompt(e.target.value)} />
            </div>

            <div className="field">
              <label>Product photo *</label>
              <input type="file" accept="image/png,image/jpeg,image/webp" onChange={onCreativeFile} />
            </div>

            {creativePreview && (
              <div>
                <div className="muted" style={{ marginBottom: 8 }}>Original photo</div>
                <img src={creativePreview} alt="Original product" style={{ width: "100%", maxHeight: 360, objectFit: "cover", borderRadius: 16 }} />
              </div>
            )}

            {error && <div className="error">{error}</div>}

            <button className="primary" disabled={loading || !creativeFile} onClick={generate}>
              {loading ? "AI is creating your content…" : "✨ Generate Marketing Content"}
            </button>
          </div>
        </section>

        {(creativeImage || creativeContent) && (
          <section className="card" style={{ marginTop: 22 }}>
            <div className="section-head">
              <div>
                <h2>Generated Content</h2>
                <div className="muted">Your upgraded image and ready-to-use social content.</div>
              </div>
            </div>

            {creativeImage && (
              <img src={creativeImage} alt="AI generated marketing image" style={{ width: "100%", maxHeight: 700, objectFit: "contain", borderRadius: 18, display: "block", background: "#f4f4f5" }} />
            )}

            {creativeContent && (
              <div className="results" style={{ marginTop: 20 }}>
                <div className="result-box">
                  <strong>{creativeContent.headline}</strong>
                  <p>{creativeContent.subheadline}</p>
                  <p>{creativeContent.caption}</p>
                  <div className="tags">{creativeContent.hashtags.map((h) => <span className="tag" key={h}>{h}</span>)}</div>
                  <p><b>CTA:</b> {creativeContent.cta}</p>
                </div>

                <div className="result-box">
                  <strong>Reel ideas</strong>
                  {creativeContent.reel_ideas.map((reel, index) => (
                    <article key={`${reel.title}-${index}`} style={{ marginTop: 14 }}>
                      <p><b>{reel.title}</b> · {reel.duration}</p>
                      <p>Hook: {reel.hook}</p>
                      <ol>{reel.script.map((line, i) => <li key={i}>{line}</li>)}</ol>
                    </article>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}

function Field({ label, value, onChange, placeholder, required }: { label: string; value: string; onChange: (v: string) => void; placeholder: string; required?: boolean }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input required={required} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    </div>
  );
}
