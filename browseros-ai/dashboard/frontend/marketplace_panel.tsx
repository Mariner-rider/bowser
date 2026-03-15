import React from "react";

type MarketplaceAgent = {
  name: string;
  version: string;
  description: string;
  installed: boolean;
};

type MarketplacePanelProps = {
  agents: MarketplaceAgent[];
  theme: "day" | "night";
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

export function MarketplacePanel({ agents, theme }: MarketplacePanelProps) {
  const styles = themeStyles[theme];

  return (
    <section style={{ marginTop: 18 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <h2 style={{ margin: 0 }}>Marketplace</h2>
          <p style={{ margin: "4px 0 0", color: styles.dim, fontSize: 13 }}>
            Discover and install high-quality AI agents.
          </p>
        </div>
        <button style={{ padding: "10px 14px", borderRadius: 10, border: styles.border, background: "#6f5dff", color: "#fff" }}>
          Request an Agent
        </button>
      </div>

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
