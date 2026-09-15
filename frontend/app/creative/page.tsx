"use client";

import { FormEvent, useState } from "react";

type Reel = { title: string; hook: string; script: string[]; duration: string };
type Content = { headline: string; subheadline: string; caption: string; hashtags: string[]; cta: string; reel_ideas: Reel[] };

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CreativeStudio() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [generatedImage, setGeneratedImage] = useState("");
  const [businessName, setBusinessName] = useState("Chai & Chill Café");
  const [businessType, setBusinessType] = useState("Café");
  const [productName, setProductName] = useState("Special Masala Chai");
  const [offer, setOffer] = useState("Buy 2 Get 1 Free");
  const [prompt, setPrompt] = useState("Warm natural café lighting, clean premium composition, realistic Instagram product photography");
  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function selectFile(next: File | null) {
    setFile(next); setGeneratedImage("");
    if (next) setPreview(URL.createObjectURL(next)); else setPreview("");
  }

  async function run(e: FormEvent) {
    e.preventDefault();
    if (!file) return setError("Upload a photo first.");
    setLoading(true); setError(""); setContent(null);
    try {
      const imageData = new FormData();
      imageData.append("image", file); imageData.append("prompt", prompt);
      imageData.append("business_name", businessName); imageData.append("product_name", productName);
      const imageResponse = await fetch(`${API_URL}/api/v1/creative/image`, { method: "POST", body: imageData });
      if (!imageResponse.ok) throw new Error(await imageResponse.text() || "Image generation failed");
      const imageResult = await imageResponse.json(); setGeneratedImage(imageResult.image_data);

      const contentData = new FormData();
      contentData.append("business_type", businessType); contentData.append("business_name", businessName);
      contentData.append("product_name", productName); contentData.append("offer", offer);
      contentData.append("additional_info", "Create social content around the uploaded product photo and marketing image.");
      const contentResponse = await fetch(`${API_URL}/api/v1/generate`, { method: "POST", body: contentData });
      if (!contentResponse.ok) throw new Error(await contentResponse.text() || "Content generation failed");
      setContent(await contentResponse.json());
    } catch (err) { setError(err instanceof Error ? err.message : "Something went wrong."); }
    finally { setLoading(false); }
  }

  return <main className="shell"><div className="container">
    <header className="topbar"><div className="logo">ContentForge</div><a className="badge" href="/">← Main studio</a></header>
    <section className="hero"><h1>AI Creative Studio</h1><p>Upload an ordinary business photo. AI turns it into a polished marketing image and creates the social content around it.</p></section>
    <div className="grid">
      <section className="card"><h2>1. Give AI the raw photo</h2><div className="muted">Use a normal phone photo. The original subject is preserved.</div>
        <form className="form" onSubmit={run}>
          <div className="field"><label>Business name</label><input value={businessName} onChange={e => setBusinessName(e.target.value)} /></div>
          <div className="row"><div className="field"><label>Business type</label><input value={businessType} onChange={e => setBusinessType(e.target.value)} /></div><div className="field"><label>Product / service</label><input value={productName} onChange={e => setProductName(e.target.value)} /></div></div>
          <div className="field"><label>Offer</label><input value={offer} onChange={e => setOffer(e.target.value)} /></div>
          <div className="field"><label>Creative direction</label><textarea value={prompt} onChange={e => setPrompt(e.target.value)} /></div>
          <div className="field"><label>Raw photo</label><input type="file" accept="image/png,image/jpeg,image/webp" onChange={e => selectFile(e.target.files?.[0] || null)} /></div>
          {preview && <img src={preview} alt="Original upload" style={{ width: "100%", maxHeight: 360, objectFit: "cover", borderRadius: 16 }} />}
          {error && <div className="error">{error}</div>}
          <button className="primary" disabled={loading || !file}>{loading ? "AI is creating everything…" : "✨ Create marketing content"}</button>
        </form>
      </section>
      <section className="card"><h2>2. AI marketing image</h2><div className="muted">Enhanced/generated result from the uploaded photo.</div>
        <div style={{ marginTop: 18 }}>{generatedImage ? <img src={generatedImage} alt="AI generated marketing image" style={{ width: "100%", borderRadius: 18, display: "block" }} /> : <div className="preview" style={{ minHeight: 420, display: "grid", placeItems: "center", padding: 30 }}><span className="muted">Your AI image will appear here.</span></div>}</div>
        {content && <div className="results" style={{ marginTop: 22 }}><div className="result-box"><strong>{content.headline}</strong><p>{content.subheadline}</p><p>{content.caption}</p><div className="tags">{content.hashtags.map(h => <span className="tag" key={h}>{h}</span>)}</div><p><b>CTA:</b> {content.cta}</p></div></div>}
      </section>
    </div>
    {content && <section className="card" style={{ marginTop: 22 }}><h2>3. Reel script generator</h2><div className="muted">The same business brief becomes ready-to-shoot reel concepts.</div><div className="results" style={{ marginTop: 18 }}>{content.reel_ideas.map((r, index) => <article className="result-box" key={`${r.title}-${index}`}><strong>{r.title}</strong><p><b>Duration:</b> {r.duration}</p><p><b>Hook:</b> {r.hook}</p><ol>{r.script.map((line, i) => <li key={i}>{line}</li>)}</ol></article>)}</div></section>}
  </div></main>;
}
