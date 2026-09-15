"use client";

import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import { toPng } from "html-to-image";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Reel = { title: string; hook: string; script: string[]; duration: string };
type Carousel = { title: string; slides: string[] };
type Result = {
  headline: string; subheadline: string; caption: string; hashtags: string[]; cta: string;
  design: { brand: string; price: string; location: string; phone: string; has_photo: boolean };
  reel_ideas: Reel[]; carousel_ideas: Carousel[];
  posting_suggestion: { best_days: string[]; best_time: string; frequency: string; tip: string };
};

const initial = { businessType: "", businessName: "", productName: "", offer: "", price: "", location: "", phone: "", additionalInfo: "" };

export default function Home() {
  const [form, setForm] = useState(initial); const [photo, setPhoto] = useState("");
  const [result, setResult] = useState<Result | null>(null); const [loading, setLoading] = useState(false); const [error, setError] = useState("");
  useEffect(() => () => { if (photo) URL.revokeObjectURL(photo); }, [photo]);
  function update(key: keyof typeof initial, value: string) { setForm((old) => ({ ...old, [key]: value })); }
  function onPhoto(e: ChangeEvent<HTMLInputElement>) { const file = e.target.files?.[0]; if (!file) return; if (photo) URL.revokeObjectURL(photo); setPhoto(URL.createObjectURL(file)); }
  async function generate(e: FormEvent) {
    e.preventDefault(); setLoading(true); setError("");
    try {
      const data = new FormData(); Object.entries(form).forEach(([key, value]) => data.append(key.replace(/[A-Z]/g, (m) => `_${m.toLowerCase()}`), value));
      const input = document.querySelector<HTMLInputElement>("#photo"); if (input?.files?.[0]) data.append("photo", input.files[0]);
      const response = await fetch(`${API_URL}/api/v1/generate`, { method: "POST", body: data });
      if (!response.ok) throw new Error((await response.text()) || "Generation failed"); setResult(await response.json());
    } catch (err) { setError(err instanceof Error ? err.message : "Something went wrong"); } finally { setLoading(false); }
  }
  async function downloadPost() { const node = document.getElementById("post-preview"); if (!node) return; const dataUrl = await toPng(node, { pixelRatio: 2, cacheBust: true }); const a = document.createElement("a"); a.download = "instagram-post.png"; a.href = dataUrl; a.click(); }
  async function copy(text: string) { await navigator.clipboard.writeText(text); }

  return <main className="shell"><div className="container">
    <header className="topbar"><div className="logo">ContentForge</div><span className="badge">V2 • Content AI</span></header>
    <section className="hero"><h1>One product. A week of content ideas.</h1><p>Generate an Instagram post, caption, reels, carousel concepts, and a practical posting suggestion from the same business brief.</p></section>
    <div className="grid">
      <section className="card"><h2>Business details</h2><div className="muted">Tell ContentForge what you are promoting.</div>
        <form className="form" onSubmit={generate}>
          <div className="row"><Field label="Business type *" value={form.businessType} onChange={(v) => update("businessType", v)} placeholder="e.g. Cafe, Salon, Gym" required /><Field label="Business name" value={form.businessName} onChange={(v) => update("businessName", v)} placeholder="e.g. Bean & Brew" /></div>
          <Field label="Product / service *" value={form.productName} onChange={(v) => update("productName", v)} placeholder="e.g. Cold Coffee" required />
          <div className="row"><Field label="Offer" value={form.offer} onChange={(v) => update("offer", v)} placeholder="e.g. Buy 1 Get 1" /><Field label="Price" value={form.price} onChange={(v) => update("price", v)} placeholder="e.g. ₹149" /></div>
          <div className="row"><Field label="Location" value={form.location} onChange={(v) => update("location", v)} placeholder="e.g. Connaught Place" /><Field label="Phone" value={form.phone} onChange={(v) => update("phone", v)} placeholder="e.g. 98765 43210" /></div>
          <div className="field"><label htmlFor="additional_info">Extra information</label><textarea id="additional_info" value={form.additionalInfo} onChange={(e) => update("additionalInfo", e.target.value)} placeholder="Opening hours, special details, delivery info..." /></div>
          <div className="field"><label htmlFor="photo">Product photo</label><div className="upload"><input id="photo" type="file" accept="image/png,image/jpeg,image/webp" onChange={onPhoto} /></div></div>
          {error && <div className="error">{error}</div>}<button className="primary" disabled={loading || !form.businessType || !form.productName}>{loading ? "Creating your content…" : "✨ Generate V2 Content"}</button>
        </form>
      </section>
      <section className="card"><h2>Post preview</h2><div className="muted">Your original V1 export still works.</div>
        <div className="preview-wrap" style={{ marginTop: 18 }}><div id="post-preview" className="preview">{photo && <img src={photo} alt="Product preview" />}<div className="overlay" />{result?.design.price && <div className="price">{result.design.price}</div>}<div className="post-copy"><div className="post-brand">{result?.design.brand || form.businessName || form.businessType || "Your Business"}</div><h3>{result?.headline || form.offer || form.productName || "Your next post"}</h3><p>{result?.subheadline || "Your offer, ready for Instagram."}</p></div></div></div>
        {result && <div className="results"><div className="actions"><button className="secondary" onClick={downloadPost}>Download PNG</button><button className="secondary" onClick={() => copy(result.caption)}>Copy caption</button></div><div className="result-box"><strong>Caption</strong><p>{result.caption}</p></div><div className="result-box"><strong>Hashtags</strong><div className="tags">{result.hashtags.map((tag) => <span className="tag" key={tag}>{tag}</span>)}</div></div></div>}
      </section>
    </div>
    {result && <section className="card" style={{ marginTop: 22 }}><h2>V2 content ideas</h2><div className="muted">Turn the same product brief into reels and carousels.</div>
      <div className="results"><div className="result-box"><strong>Reel ideas</strong>{result.reel_ideas.map((r) => <article key={r.title} style={{ marginBottom: 17 }}><p><b>{r.title}</b> · {r.duration}</p><p>Hook: {r.hook}</p><ol>{r.script.map((line, i) => <li key={i}>{line}</li>)}</ol></article>)}</div>
      <div className="result-box"><strong>Carousel ideas</strong>{result.carousel_ideas.map((c) => <article key={c.title} style={{ marginBottom: 14 }}><p><b>{c.title}</b></p><ol>{c.slides.map((s, i) => <li key={i}>{s}</li>)}</ol></article>)}</div>
      <div className="result-box"><strong>Posting suggestion</strong><p><b>{result.posting_suggestion.frequency}</b> · {result.posting_suggestion.best_time}</p><p>Best days: {result.posting_suggestion.best_days.join(", ")}</p><p>{result.posting_suggestion.tip}</p></div></div>
    </section>}
  </div></main>;
}

function Field({ label, value, onChange, placeholder, required }: { label: string; value: string; onChange: (v: string) => void; placeholder: string; required?: boolean }) {
  return <div className="field"><label>{label}</label><input required={required} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} /></div>;
}
