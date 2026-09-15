"use client";

import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import { toPng } from "html-to-image";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Result = {
  headline: string;
  subheadline: string;
  caption: string;
  hashtags: string[];
  cta: string;
  design: { brand: string; price: string; location: string; phone: string; has_photo: boolean };
};

const initial = { businessType: "", businessName: "", productName: "", offer: "", price: "", location: "", phone: "", additionalInfo: "" };

export default function Home() {
  const [form, setForm] = useState(initial);
  const [photo, setPhoto] = useState<string>("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => () => { if (photo) URL.revokeObjectURL(photo); }, [photo]);

  function update(key: keyof typeof initial, value: string) { setForm((old) => ({ ...old, [key]: value })); }

  function onPhoto(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    if (photo) URL.revokeObjectURL(photo);
    setPhoto(URL.createObjectURL(file));
  }

  async function generate(e: FormEvent) {
    e.preventDefault();
    setLoading(true); setError("");
    try {
      const data = new FormData();
      Object.entries(form).forEach(([key, value]) => data.append(key.replace(/[A-Z]/g, (m) => `_${m.toLowerCase()}`), value));
      const input = document.querySelector<HTMLInputElement>("#photo");
      if (input?.files?.[0]) data.append("photo", input.files[0]);
      const response = await fetch(`${API_URL}/api/v1/generate`, { method: "POST", body: data });
      if (!response.ok) throw new Error((await response.text()) || "Generation failed");
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally { setLoading(false); }
  }

  async function downloadPost() {
    const node = document.getElementById("post-preview");
    if (!node) return;
    const dataUrl = await toPng(node, { pixelRatio: 2, cacheBust: true });
    const a = document.createElement("a"); a.download = "instagram-post.png"; a.href = dataUrl; a.click();
  }

  async function copy(text: string) { await navigator.clipboard.writeText(text); }

  return (
    <main className="shell">
      <div className="container">
        <header className="topbar"><div className="logo">ContentForge</div><span className="badge">V1 MVP</span></header>
        <section className="hero"><h1>Turn one product into a post people want to stop for.</h1><p>Enter a few business details, add a photo, and generate an Instagram-ready promotional post with caption, hashtags, and a clear call to action.</p></section>
        <div className="grid">
          <section className="card">
            <h2>Business details</h2><div className="muted">The more context you give, the better the copy.</div>
            <form className="form" onSubmit={generate}>
              <div className="row"><Field label="Business type *" value={form.businessType} onChange={(v) => update("businessType", v)} placeholder="e.g. Cafe, Salon, Gym" required /><Field label="Business name" value={form.businessName} onChange={(v) => update("businessName", v)} placeholder="e.g. Bean & Brew" /></div>
              <Field label="Product / service *" value={form.productName} onChange={(v) => update("productName", v)} placeholder="e.g. Cold Coffee" required />
              <div className="row"><Field label="Offer" value={form.offer} onChange={(v) => update("offer", v)} placeholder="e.g. Buy 1 Get 1" /><Field label="Price" value={form.price} onChange={(v) => update("price", v)} placeholder="e.g. ₹149" /></div>
              <div className="row"><Field label="Location" value={form.location} onChange={(v) => update("location", v)} placeholder="e.g. Connaught Place" /><Field label="Phone" value={form.phone} onChange={(v) => update("phone", v)} placeholder="e.g. 98765 43210" /></div>
              <div className="field"><label htmlFor="additional_info">Extra information</label><textarea id="additional_info" value={form.additionalInfo} onChange={(e) => update("additionalInfo", e.target.value)} placeholder="Opening hours, special details, delivery info..." /></div>
              <div className="field"><label htmlFor="photo">Product photo</label><div className="upload"><input id="photo" type="file" accept="image/png,image/jpeg,image/webp" onChange={onPhoto} /></div></div>
              {error && <div className="error">{error}</div>}
              <button className="primary" disabled={loading || !form.businessType || !form.productName}>{loading ? "Creating your post…" : "✨ Generate Instagram Post"}</button>
            </form>
          </section>

          <section className="card">
            <h2>Your result</h2><div className="muted">Preview, copy the text, or export the square post.</div>
            <div className="preview-wrap" style={{ marginTop: 18 }}>
              <div id="post-preview" className="preview">
                {photo && <img src={photo} alt="Product preview" />}
                <div className="overlay" />
                {result?.design.price && <div className="price">{result.design.price}</div>}
                <div className="post-copy"><div className="post-brand">{result?.design.brand || form.businessName || form.businessType || "Your Business"}</div><h3>{result?.headline || form.offer || form.productName || "Your next post"}</h3><p>{result?.subheadline || "Your offer, ready for Instagram."}</p></div>
              </div>
            </div>
            {result && <div className="results">
              <div className="actions"><button className="secondary" onClick={downloadPost}>Download PNG</button><button className="secondary" onClick={() => copy(result.caption)}>Copy caption</button></div>
              <div className="result-box"><strong>Caption</strong><p>{result.caption}</p></div>
              <div className="result-box"><strong>Hashtags</strong><div className="tags">{result.hashtags.map((tag) => <span className="tag" key={tag}>{tag}</span>)}</div></div>
              <div className="result-box"><strong>Call to action</strong><p>{result.cta}</p></div>
            </div>}
          </section>
        </div>
      </div>
    </main>
  );
}

function Field({ label, value, onChange, placeholder, required }: { label: string; value: string; onChange: (v: string) => void; placeholder: string; required?: boolean }) {
  return <div className="field"><label>{label}</label><input required={required} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} /></div>;
}
