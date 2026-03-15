import React from "react";

type MarketplaceAgent = {
  name: string;
  version: string;
  description: string;
  installed: boolean;
};

type MarketplacePanelProps = {
  agents: MarketplaceAgent[];
};

export function MarketplacePanel({ agents }: MarketplacePanelProps) {
  return (
    <section>
      <h2>AI Marketplace (Agent App Store)</h2>
      {agents.map((agent) => (
        <div key={`${agent.name}-${agent.version}`} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          <strong>{agent.name}</strong> <span>v{agent.version}</span>
          <div>{agent.description}</div>
          <button>{agent.installed ? "Installed" : "Install"}</button>
        </div>
      ))}
    </section>
  );
}
