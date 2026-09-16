"use client";

import { ChangeEvent, useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Reel = {
  number: number; day: string; slot: number; title: string; type: string; hook: string;
  scene_by_scene: string[]; script: string; cta: string; caption: string; hashtags: string[]; duration: string;
};
type CreativeContent = {
  headline: string; subheadline: string; caption: string; hashtags: string[]; cta: string; reel_ideas: Reel[];
};

const initial = { businessName: "", businessType: "", phone: "", address: "", additionalInfo: "", productName: "", offer: "" };

export default function Home() {
  const [form, setForm] = useState(initial);
  const [creativeFile, setCreativeFile] = useState<File | null>(null);
  const [creativePreview, setCreativePreview] = useState("");
  const [creativeImage, setCreativeImage] = useState("");
  const [creativeContent, setCreativeContent] = useState<CreativeContent | null>(null);
  const [creativePrompt, setCreativePrompt] = useState("Premium realistic marketing photography. Improve lighting, sharpness, composition and background while preserving the exact product.");
  const [reelsPerWeek, setReelsPerWeek] = useState(3);
  const [maxReelsPerDay, setMaxReelsPerDay] = useState(1);
  const [imageLoading, setImageLoading] = useState(false);
  const [reelLoading, setReelLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => () => { if (creativePreview) URL.revokeObjectURL(creativePreview); }, [creativePreview]);
  function update(key: keyof typeof initial, value: string) { setForm((old) => ({ ...old, [key]: value })); }
  function onCreativeFile(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    if (creativePreview) URL.revokeObjectURL(creativePreview);
    setCreativeFile(file); setCreativePreview(file ? URL.createObjectURL(file) : ""); setCreativeImage(""); setCreativeContent(null); setError("");
  }

  async function generateImage() {
    if (!creativeFile) { setError("Upload a product photo first."); return; }
    if (!form.businessName.trim() || !form.businessType.trim() || !form.productName.trim()) { setError("For the marketing image, complete Business Name, Business Type, and Product / Service in Step 1."); return; }
    setImageLoading(true); setError(""); setCreativeImage("");
    try {
      const imageData = new FormData();
      imageData.append("image", creativeFile);
      imageData.append("prompt", creativePrompt);
      imageData.append("business_name", form.businessName.trim());
      imageData.append("product_name", form.productName.trim());
      const response = await fetch(`${API_URL}/api/v1/creative/image`, { method: "POST", body: imageData });
      if (!response.ok) throw new Error((await response.text()) || "Image generation failed");
      const result = await response.json();
      setCreativeImage(result.image_data);
    } catch (err) { setError(err instanceof Error ? err.message : "Image generation failed."); }
    finally { setImageLoading(false); }
  }

  async function generateReels() {
    const missing: string[] = [];
    if (!form.businessName.trim()) missing.push("Business Name");
    if (!form.businessType.trim()) missing.push("Business Type");
    if (missing.length) {
      setError(`Complete these Business Information fields in Step 1 first: ${missing.join(", ")}.`);
      return;
    }

    setReelLoading(true); setError(""); setCreativeContent(null);
    try {
      // Every Reel is generated from the complete Step 1 business context.
      // Product/service is optional for Reels; the AI can still use the business
      // name, type, location, phone, offer and additional information.
      const contentData = new FormData();
      contentData.append("business_type", form.businessType.trim());
      contentData.append("business_name", form.businessName.trim());
      contentData.append("product_name", form.productName.trim());
      contentData.append("offer", form.offer.trim());
      contentData.append("price", "");
      contentData.append("location", form.address.trim());
      contentData.append("phone", form.phone.trim());
      contentData.append("additional_info", form.additionalInfo.trim());
      contentData.append("reels_per_week", String(reelsPerWeek));
      contentData.append("max_reels_per_day", String(maxReelsPerDay));
      const response = await fetch(`${API_URL}/api/v1/generate`, { method: "POST", body: contentData });
      if (!response.ok) throw new Error((await response.text()) || "Reel generation failed");
      setCreativeContent(await response.json());
    } catch (err) { setError(err instanceof Error ? err.message : "Reel generation failed."); }
    finally { setReelLoading(false); }
  }

  return (
    <main className="shell"><div className="container">
      <header className="topbar"><div className="logo">ContentForge</div><span className="badge">AI Social Content Maker</span></header>
      <section className="hero"><h1>Create professional social content in one simple workflow.</h1><p>1. Business information → 2. Marketing image → 3. Business-specific Reel plan.</p></section>

      <section className="card"><div className="section-head"><div><h2>1️⃣ Business Information</h2><div className="muted">This is the foundation for everything ContentForge creates. Reel ideas, hooks, scripts, CTAs, captions and hashtags are generated around this business context.</div></div></div>
        <div className="form">
          <div className="row"><Field label="Business name *" value={form.businessName} onChange={(v) => update("businessName", v)} placeholder="e.g. Urban Threads" required /><Field label="Business type *" value={form.businessType} onChange={(v) => update("businessType", v)} placeholder="e.g. Clothing brand" required /></div>
          <div className="row"><Field label="Contact number" value={form.phone} onChange={(v) => update("phone", v)} placeholder="e.g. 98765 43210" /><Field label="Address / location" value={form.address} onChange={(v) => update("address", v)} placeholder="e.g. Vasant Kunj, New Delhi" /></div>
          <div className="field"><label>Product / service</label><input value={form.productName} onChange={(e) => update("productName", e.target.value)} placeholder="e.g. Oversized Black Hoodie / Haircut / Home Bakery" /></div>
          <div className="field"><label>Offer or price</label><input value={form.offer} onChange={(e) => update("offer", e.target.value)} placeholder="e.g. ₹999, 20% off, Free delivery" /></div>
          <div className="field"><label>Additional business information <span className="muted">(optional)</span></label><textarea value={form.additionalInfo} onChange={(e) => update("additionalInfo", e.target.value)} placeholder="Opening hours, delivery details, special features, target customers, website, social handle, unique selling points, etc." /></div>
        </div>
      </section>

      <section className="card" style={{ marginTop: 22 }}><div className="section-head"><div><h2>2️⃣ ✨ AI Image Generation</h2><div className="muted">Use the business and product information above to turn an ordinary product photo into a professional marketing image.</div></div></div>
        <div className="form">
          <div className="field"><label>Creative direction</label><textarea value={creativePrompt} onChange={(e) => setCreativePrompt(e.target.value)} placeholder="Describe the visual style, setting, mood or campaign direction you want." /></div>
          <div className="field"><label>Product photo *</label><input type="file" accept="image/png,image/jpeg,image/webp" onChange={onCreativeFile} /></div>
          {creativePreview && <div><div className="muted" style={{ marginBottom: 8 }}>Original photo</div><img src={creativePreview} alt="Original product" style={{ width: "100%", maxHeight: 360, objectFit: "cover", borderRadius: 16 }} /></div>}
          <button className="primary" disabled={imageLoading || reelLoading || !creativeFile} onClick={generateImage}>{imageLoading ? "Creating professional image…" : "✨ Generate Marketing Image"}</button>
        </div>
      </section>

      <section className="card" style={{ marginTop: 22 }}><div className="section-head"><div><h2>3️⃣ 🎬 Reel Schedule & Ideas</h2><div className="muted">Set your posting schedule. Then AI creates exactly that many simple Reels specifically from the business information in Step 1.</div></div></div>
        <div className="form">
          <div className="row">
            <Field label="How many Reels per week? *" value={String(reelsPerWeek)} onChange={(v) => setReelsPerWeek(Math.max(1, Math.min(21, Number(v) || 1)))} placeholder="e.g. 5" required />
            <Field label="Maximum Reels per day *" value={String(maxReelsPerDay)} onChange={(v) => setMaxReelsPerDay(Math.max(1, Math.min(3, Number(v) || 1)))} placeholder="e.g. 1" required />
          </div>
          <div className="muted">Example: 5 Reels/week + maximum 1/day = Monday to Friday. The schedule is generated across Monday–Sunday without exceeding your daily limit.</div>
          {error && <div className="error">{error}</div>}
          <button className="primary" disabled={reelLoading || imageLoading} onClick={generateReels}>{reelLoading ? "Creating business-specific Reel plan…" : "🎬 Generate Reel Plan"}</button>
        </div>
      </section>

      {(creativeImage || creativeContent) && <section className="card" style={{ marginTop: 22 }}><div className="section-head"><div><h2>Generated Content</h2><div className="muted">Results created from your business workflow.</div></div></div>
        {creativeImage && <img src={creativeImage} alt="AI generated marketing image" style={{ width: "100%", maxHeight: 700, objectFit: "contain", borderRadius: 18, display: "block", background: "#f4f4f5" }} />}
        {creativeContent && <div className="results" style={{ marginTop: 20 }}>
          <div className="result-box"><strong>{creativeContent.headline}</strong><p>{creativeContent.subheadline}</p><p>{creativeContent.caption}</p><div className="tags">{creativeContent.hashtags.map((h) => <span className="tag" key={h}>{h}</span>)}</div><p><b>CTA:</b> {creativeContent.cta}</p></div>
          <div className="result-box"><strong>🎬 Your Business-Specific Reel Plan</strong><p className="muted">{creativeContent.reel_ideas.length} Reels created from your Step 1 business information and Step 3 schedule.</p>
            {creativeContent.reel_ideas.map((reel) => <article key={`${reel.number}-${reel.day}-${reel.slot}`} style={{ marginTop: 18, paddingTop: 16, borderTop: "1px solid #e5e7eb" }}>
              <p><b>Reel {reel.number} — {reel.day}</b> · {reel.duration}</p>
              <p><b>💡 Idea:</b> {reel.title}</p>
              <p><b>🪝 Hook:</b> {reel.hook}</p>
              <p><b>🎥 Scenes:</b></p><ol>{reel.scene_by_scene.map((line, i) => <li key={i}>{line}</li>)}</ol>
              <p><b>🗣️ Script:</b> {reel.script}</p>
              <p><b>📢 CTA:</b> {reel.cta}</p>
              <p><b>📝 Caption:</b> {reel.caption}</p>
              <div><b>#️⃣ Hashtags:</b> <span className="tags">{reel.hashtags.map((h) => <span className="tag" key={h}>{h}</span>)}</span></div>
            </article>)}
          </div>
        </div>}
      </section>}
    </div></main>
  );
}

function Field({ label, value, onChange, placeholder, required }: { label: string; value: string; onChange: (v: string) => void; placeholder: string; required?: boolean }) {
  return <div className="field"><label>{label}</label><input required={required} type={label.toLowerCase().includes("how many") || label.toLowerCase().includes("maximum") ? "number" : "text"} min={1} max={21} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} /></div>;
}
