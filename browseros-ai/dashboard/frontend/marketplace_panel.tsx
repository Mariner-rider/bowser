import React from "react";

type MarketplaceAgent = {
  name: string;
  version: string;
  description: string;
  installed: boolean;
};

type MarketplacePanelProps = {
  agents: MarketplaceAgent[];
const themeStyles = {
  night: {
    card: "linear-gradient(135deg, rgba(26,16,65,.95), rgba(14,7,46,.95))",
    border: "1px solid rgba(113, 84, 255, .3)",
    text: "#eceaff",
  },
  day: {
    card: "linear-gradient(135deg, rgba(255,255,255,.95), rgba(240,243,255,.95))",
    border: "1px solid rgba(129, 146, 255, .3)",
    text: "#172042",
  },
} as const;

export function MarketplacePanel({ agents, theme }: MarketplacePanelProps) {
  const styles = themeStyles[theme];

  return (
    <section style={{ marginTop: 16 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12,
        }}
      >
        <h2 style={{ margin: 0 }}>Marketplace</h2>
        <span style={{ fontSize: 13, color: "#6a74a0" }}>
          Discover and install quality AI agents.
        </span>
      </div>

      <div
        style={{
          padding: "10px 12px",
          borderRadius: 10,
          border: styles.border,
          background: styles.card,
          color: styles.text,
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: 12,
          }}
        >
          {agents.map((agent) => (
            <article
              key={`${agent.name}-${agent.version}`}
              style={{
                border: styles.border,
                borderRadius: 12,
                background: styles.card,
                padding: 14,
                boxShadow: "0 6px 20px rgba(0,0,0,.15)",
              }}
            >
              <div style={{ fontWeight: 700, fontSize: 16 }}>{agent.name}</div>

              <div style={{ opacity: 0.8, fontSize: 12, marginBottom: 6 }}>
                v{agent.version}
              </div>

              <div style={{ fontSize: 13, marginBottom: 10 }}>
                {agent.description}
              </div>

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span style={{ fontSize: 12, opacity: 0.7 }}>
                  ⭐ {agent.rating ?? "4.2"} • {agent.downloads ?? "2.8K"} users
                </span>

                <button
                  style={{
                    borderRadius: 8,
                    padding: "6px 10px",
                    background: agent.installed ? "#8b5cf6" : "#6366f1",
                    border: "none",
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
      </div>
    </section>
  );
}
    </section>
  );
}
