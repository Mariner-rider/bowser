import React from "react";

type Agent = {
  agent_name: string;
  state: "active" | "paused" | "stopped";
  active_task_id?: string | null;
};

type AgentPanelProps = {
  agents: Agent[];
  onPause: (agentName: string) => void;
  onStop: (agentName: string) => void;
export function AgentPanel({ agents, onPause, onStop, theme }: AgentPanelProps) {
  const isNight = theme === "night";

  return (
    <section style={{ marginBottom: 12 }}>
      <h2 style={{ marginBottom: 12 }}>Active Agents</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: 10,
        }}
      >
        {agents.map((agent) => (
          <div
            key={agent.agent_name}
            style={{
              border: isNight
                ? "1px solid rgba(113, 84, 255, .35)"
                : "1px solid #d8dff7",
              padding: 12,
              borderRadius: 12,
              background: isNight
                ? "rgba(25, 19, 57, .75)"
                : "rgba(255, 255, 255, .9)",
            }}
          >
            <strong style={{ fontSize: 16 }}>{agent.agent_name}</strong>

            <div style={{ marginTop: 6 }}>State: {agent.state}</div>

            <div style={{ opacity: 0.75, fontSize: 13 }}>
              Task: {agent.active_task_id ?? "None"}
            </div>

            <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
              <button
                onClick={() => onPause(agent.agent_name)}
                disabled={agent.state !== "active"}
              >
                Pause
              </button>

              <button onClick={() => onStop(agent.agent_name)}>
                Stop
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
    </section>
  );
}
