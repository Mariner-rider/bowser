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
};

export function AgentPanel({ agents, onPause, onStop }: AgentPanelProps) {
  return (
    <section>
      <h2>Active Agents</h2>
      {agents.map((agent) => (
        <div key={agent.agent_name} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          <strong>{agent.agent_name}</strong>
          <div>State: {agent.state}</div>
          <div>Task: {agent.active_task_id ?? "None"}</div>
          <button onClick={() => onPause(agent.agent_name)} disabled={agent.state !== "active"}>
            Pause
          </button>
          <button onClick={() => onStop(agent.agent_name)} style={{ marginLeft: 8 }}>
            Stop
          </button>
        </div>
      ))}
    </section>
  );
}
