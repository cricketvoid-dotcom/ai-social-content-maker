"use client";

import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Row = { content_type: string; title: string; reach: number; likes: number; comments: number; shares: number; saves: number; clicks: number };

export default function GrowthPage() {
  const [rows, setRows] = useState<Row[]>([
    { content_type: "Reel", title: "Example Reel", reach: 1000, likes: 60, comments: 8, shares: 20, saves: 20, clicks: 10 },
  ]);
  const [result, setResult] = useState<any>(null);
  const [busy, setBusy] = useState(false);

  const addRow = () => setRows([...rows, { content_type: "Post", title: "New content", reach: 0, likes: 0, comments: 0, shares: 0, saves: 0, clicks: 0 }]);
  const update = (i: number, key: keyof Row, value: string) => setRows(rows.map((r, n) => n === i ? { ...r, [key]: key === "content_type" || key === "title" ? value : Number(value) || 0 } : r));

  const analyze = async () => {
    setBusy(true);
    try {
      const res = await fetch(`${API}/api/v1/growth/insights`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(rows) });
      setResult(await res.json());
    } finally { setBusy(false); }
  };

  return <main className="min-h-screen bg-slate-950 text-white p-6 md:p-10">
    <div className="mx-auto max-w-6xl space-y-8">
      <a href="/" className="text-sm text-cyan-300">← Back to Content Maker</a>
      <header><p className="text-sm uppercase tracking-[0.25em] text-cyan-300">V10 • AI Growth Engine</p><h1 className="mt-2 text-4xl font-bold">Find what actually grows the account.</h1><p className="mt-3 max-w-2xl text-slate-300">Paste post-level performance data and get a ranked view of winning formats, growth signals, and the next experiments to run.</p></header>
      <section className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 shadow-xl">
        <div className="mb-4 flex items-center justify-between"><h2 className="text-xl font-semibold">Performance dataset</h2><button onClick={addRow} className="rounded-lg bg-white px-3 py-2 text-sm font-semibold text-slate-900">+ Add post</button></div>
        <div className="space-y-3 overflow-x-auto">
          {rows.map((r, i) => <div key={i} className="grid min-w-[1100px] grid-cols-9 gap-2">
            <select value={r.content_type} onChange={e => update(i, "content_type", e.target.value)} className="rounded-lg bg-slate-800 p-2"><option>Reel</option><option>Carousel</option><option>Post</option><option>Story</option></select>
            <input value={r.title} onChange={e => update(i, "title", e.target.value)} placeholder="Title" className="rounded-lg bg-slate-800 p-2" />
            {(["reach","likes","comments","shares","saves","clicks"] as const).map(k => <input key={k} type="number" value={r[k]} onChange={e => update(i, k, e.target.value)} placeholder={k} className="rounded-lg bg-slate-800 p-2" />)}
            <button onClick={() => setRows(rows.filter((_, n) => n !== i))} className="rounded-lg border border-red-900 px-2 text-red-300">Remove</button>
          </div>)}
        </div>
        <button disabled={busy} onClick={analyze} className="mt-5 rounded-xl bg-cyan-300 px-5 py-3 font-bold text-slate-950 disabled:opacity-50">{busy ? "Analyzing…" : "Analyze growth"}</button>
      </section>
      {result && <section className="grid gap-5 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><p className="text-slate-400">Posts analyzed</p><p className="mt-2 text-3xl font-bold">{result.posts_analyzed}</p></div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><p className="text-slate-400">Best format</p><p className="mt-2 text-3xl font-bold">{result.best_format}</p></div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><p className="text-slate-400">Strategy</p><p className="mt-2 text-sm text-slate-200">{result.strategy}</p></div>
        <div className="md:col-span-2 rounded-2xl border border-slate-800 bg-slate-900 p-5"><h2 className="text-xl font-semibold">Top performers</h2><div className="mt-4 space-y-3">{result.top_posts.map((p: any, i: number) => <div key={i} className="flex items-center justify-between rounded-xl bg-slate-800 p-3"><span>{p.title} <span className="text-slate-400">({p.content_type})</span></span><strong>{p.score}</strong></div>)}</div></div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><h2 className="text-xl font-semibold">Next tests</h2><ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-slate-300">{result.next_tests.map((x: string) => <li key={x}>{x}</li>)}</ul></div>
      </section>}
    </div>
  </main>;
}
