import React, { useEffect, useMemo, useState } from "react";

import { ensureBrowserUIRuntime } from "../../interface/capacitor_runtime";

import { AgentPanel } from "./agent_panel";
import { LogsPanel } from "./logs_panel";
import { WorkflowBuilderPanel } from "./workflow_builder_panel";
import { SecurityGuardianPanel } from "./security_guardian_panel";
import { MarketplacePanel } from "./marketplace_panel";
import { KnowledgeBrainPanel } from "./knowledge_brain_panel";
import { TaskViewer } from "./task_viewer";

type DashboardSnapshot = {
  agents: Array<{ agent_name: string; state: "active" | "paused" | "stopped"; active_task_id?: string | null }>;
  tasks: Array<{
    task_id: string;
    agent_name: string;
    description: string;
    status: string;
    progress: number;
    automation_steps: string[];
  }>;
  logs: Array<{ timestamp: string; level: string; source: string; message: string }>;
  workflowBuilder?: {
    name: string;
    nodes: Array<{ id: string; label: string }>;
  };
  securityGuardian?: {
    warnings: Array<{ risk: "low" | "medium" | "high"; message: string }>;
  };
  marketplace?: {
    agents: Array<{ name: string; version: string; description: string; installed: boolean }>;
  };
  knowledgeBrain?: {
    topic: string;
    summary: string;
    semanticResults: Array<{ title: string; source_type: string; score: number }>;
    stats: { nodes: number; relationships: number; topics: number };
  };
};

type DashboardUIProps = {
  initialSnapshot: DashboardSnapshot;
  onPauseAgent?: (agentName: string) => void;
  onStopAgent?: (agentName: string) => void;
};

export function DashboardUI({ initialSnapshot, onPauseAgent, onStopAgent }: DashboardUIProps) {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot>(initialSnapshot);

  useEffect(() => {
    ensureBrowserUIRuntime();
  }, []);

  const workflowBuilder =
    snapshot.workflowBuilder ??
    ({
      name: "Market Research",
      nodes: [
        { id: "1", label: "Search Web" },
        { id: "2", label: "Extract Data" },
        { id: "3", label: "Summarize" },
        { id: "4", label: "Generate Report" },
      ],
    } as const);

  const securityGuardian =
    snapshot.securityGuardian ??
    ({
      warnings: [{ risk: "high", message: "⚠ Possible phishing attempt" }],
    } as const);

  const marketplace =
    snapshot.marketplace ??
    ({
      agents: [
        { name: "SEO Agent", version: "1.0.0", description: "Optimize website content", installed: false },
        { name: "Stock Market Agent", version: "1.2.1", description: "Analyze market trends", installed: false },
        { name: "Coding Assistant", version: "2.0.0", description: "Generate and review code", installed: true },
      ],
    } as const);

  const knowledgeBrain =
    snapshot.knowledgeBrain ??
    ({
      topic: "AI Agents",
      summary: "Knowledge brain captures articles, papers, repositories, notes, and summaries.",
      semanticResults: [],
      stats: { nodes: 0, relationships: 0, topics: 0 },
    } as const);

  const activeAgents = useMemo(
    () => snapshot.agents.filter((agent) => agent.state === "active" || agent.state === "paused"),
    [snapshot.agents],
  );

  const handlePause = (agentName: string) => {
    onPauseAgent?.(agentName);
    setSnapshot((prev) => ({
      ...prev,
      agents: prev.agents.map((agent) =>
        agent.agent_name === agentName ? { ...agent, state: "paused" } : agent,
      ),
    }));
  };

  const handleStop = (agentName: string) => {
    onStopAgent?.(agentName);
    setSnapshot((prev) => ({
      ...prev,
      agents: prev.agents.map((agent) =>
        agent.agent_name === agentName ? { ...agent, state: "stopped" } : agent,
      ),
    }));
  };

  return (
    <main>
      <h1>Agent Monitoring Dashboard</h1>
      <AgentPanel agents={activeAgents} onPause={handlePause} onStop={handleStop} />
      <TaskViewer tasks={snapshot.tasks} />
      <WorkflowBuilderPanel workflowName={workflowBuilder.name} nodes={workflowBuilder.nodes} />
      <SecurityGuardianPanel warnings={securityGuardian.warnings} />
      <MarketplacePanel agents={marketplace.agents} />
      <KnowledgeBrainPanel
        topic={knowledgeBrain.topic}
        summary={knowledgeBrain.summary}
        semanticResults={knowledgeBrain.semanticResults}
        stats={knowledgeBrain.stats}
      />
      <LogsPanel logs={snapshot.logs} />
    </main>
  );
}
