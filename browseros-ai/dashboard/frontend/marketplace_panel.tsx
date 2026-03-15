import React, { useState } from "react";

type MarketplaceAgent = {
  name: string;
  version: string;
  description: string;
  installed: boolean;
  publisher?: string;
  priceUsd?: number;
};

type MarketplacePanelProps = {
  agents: MarketplaceAgent[];
  theme: "day" | "night";
  onPublishAgent?: (submission: {
    name: string;
    version: string;
    description: string;
    capabilities: string[];
    publisherName: string;
    priceUsd: number;
  }) => void;
};

const themeStyles = {
  night: {
    card: "linear-gradient(145deg, rgba(29,16,64,.95), rgba(13,17,42,.95))",
    border: "1px solid rgba(124, 97, 255, .35)",
    text: "#eef2ff",
    dim: "#b6c3ff",
  },
  day: {
    card: "linear-gradient(145deg, rgba(255,255,255,.98), rgba(240,244,255,.95))",
    border: "1px solid rgba(128, 145, 255, .35)",
    text: "#1f2340",
    dim: "#4b5479",
  },
} as const;

export function MarketplacePanel({ agents, theme, onPublishAgent }: MarketplacePanelProps) {
  const styles = themeStyles[theme];
  const [form, setForm] = useState({
    name: "",
    version: "1.0.0",
    description: "",
    capabilities: "research,automation",
    publisherName: "",
    priceUsd: "0",
  });

  return (
    <section style={{ marginTop: 18 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <h2 style={{ margin: 0 }}>Marketplace</h2>
          <p style={{ margin: "4px 0 0", color: styles.dim, fontSize: 13 }}>
            Discover, install, and publish high-quality AI agents.
          </p>
        </div>
        <button style={{ padding: "10px 14px", borderRadius: 10, border: styles.border, background: "#6f5dff", color: "#fff" }}>
          Request an Agent
        </button>
      </div>

      <form
        onSubmit={(event) => {
          event.preventDefault();
          onPublishAgent?.({
            name: form.name,
            version: form.version,
            description: form.description,
            capabilities: form.capabilities.split(",").map((c) => c.trim()).filter(Boolean),
            publisherName: form.publisherName,
            priceUsd: Number.parseFloat(form.priceUsd) || 0,
          });
          setForm({ ...form, name: "", description: "" });
        }}
        style={{
          marginBottom: 14,
          border: styles.border,
          borderRadius: 14,
          background: styles.card,
          color: styles.text,
          padding: 12,
          display: "grid",
          gap: 8,
        }}
      >
        <strong>Publish your own public agent</strong>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3,minmax(0,1fr))", gap: 8 }}>
          <input placeholder="Agent name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Version" value={form.version} onChange={(e) => setForm({ ...form, version: e.target.value })} />
          <input placeholder="Publisher" value={form.publisherName} onChange={(e) => setForm({ ...form, publisherName: e.target.value })} />
        </div>
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 8 }}>
          <input
            placeholder="Capabilities comma separated"
            value={form.capabilities}
            onChange={(e) => setForm({ ...form, capabilities: e.target.value })}
          />
          <input placeholder="Price USD" value={form.priceUsd} onChange={(e) => setForm({ ...form, priceUsd: e.target.value })} />
        </div>
        <button type="submit" style={{ width: "fit-content", padding: "8px 12px", borderRadius: 8 }}>
          Publish Agent
        </button>
      </form>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
        {agents.map((agent) => (
          <article
            key={`${agent.name}-${agent.version}`}
            style={{
              border: styles.border,
              borderRadius: 14,
              background: styles.card,
              color: styles.text,
              padding: 14,
              boxShadow: "0 10px 20px rgba(0,0,0,.15)",
            }}
          >
            <div style={{ fontWeight: 700, fontSize: 17 }}>{agent.name}</div>
            <div style={{ opacity: 0.85, fontSize: 12, marginBottom: 8 }}>v{agent.version}</div>
            <div style={{ color: styles.dim, fontSize: 13, minHeight: 42 }}>{agent.description}</div>
            <div style={{ fontSize: 12, color: styles.dim, marginTop: 8 }}>
              {agent.publisher ? `By ${agent.publisher}` : "Community agent"} · ${agent.priceUsd ?? 0}
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 14, alignItems: "center" }}>
              <span style={{ fontSize: 12, color: styles.dim }}>★ 4.8 · 2.6k users</span>
              <button
                style={{
                  borderRadius: 999,
                  border: "none",
                  padding: "6px 12px",
                  background: agent.installed ? "#0ea66a" : "#14b8a6",
                  color: "#fff",
                  fontWeight: 600,
                }}
              >
                {agent.installed ? "Installed" : "Install"}
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
