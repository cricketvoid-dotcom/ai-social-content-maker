"use client";

import { useEffect } from "react";

export default function CreativeStudioRoute() {
  useEffect(() => {
    window.location.replace("/");
  }, []);

  return <main className="shell"><div className="container"><section className="card"><h2>Opening the unified ContentForge studio…</h2><div className="muted">The Creative Studio is now part of the main workspace.</div></section></div></main>;
}
