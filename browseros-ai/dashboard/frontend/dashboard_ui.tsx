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

type ThemeMode = "day" | "night";

function inferThemeByTime(now: Date): ThemeMode {
  const hour = now.getHours();
  return hour >= 7 && hour < 19 ? "day" : "night";
}

const themeTokens: Record<ThemeMode, { page: string; panel: string; text: string; muted: string; border: string }> = {
  day: {
    page: "radial-gradient(circle at top left, #f6f8ff 0%, #ebf1ff 45%, #f7fbff 100%)",
    panel: "rgba(255,255,255,.9)",
    text: "#172042",
    muted: "#4d5b88",
    border: "1px solid rgba(129, 146, 255, .25)",
  },
  night: {
    page: "radial-gradient(circle at top left, #120a2d 0%, #0a102b 45%, #060918 100%)",
    panel: "rgba(15, 18, 41, .72)",
    text: "#eef2ff",
    muted: "#b7c3ff",
    border: "1px solid rgba(113, 84, 255, .3)",
  },
};

export function DashboardUI({ initialSnapshot, onPauseAgent, onStopAgent }: DashboardUIProps) {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot>(initialSnapshot);
  const [theme, setTheme] = useState<ThemeMode>(inferThemeByTime(new Date()));

  useEffect(() => {
    ensureBrowserUIRuntime();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => setTheme(inferThemeByTime(new Date())), 60_000);
    return () => clearInterval(timer);
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

  const tokens = themeTokens[theme];

  return (
    <main
      style={{
        background: tokens.page,
        color: tokens.text,
        minHeight: "100vh",
        padding: 20,
        fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
          background: tokens.panel,
          border: tokens.border,
          borderRadius: 14,
          padding: "12px 14px",
          backdropFilter: "blur(8px)",
        }}
      >
        <div>
          <h1 style={{ margin: 0 }}>AI Browser Command Center</h1>
          <div style={{ marginTop: 6, color: tokens.muted, fontSize: 13 }}>
            Theme mode: <strong>{theme}</strong> (auto-switch based on local time)
          </div>
        </div>
        <button onClick={() => setTheme(theme === "day" ? "night" : "day")}>Toggle Theme</button>
      </header>

      <AgentPanel agents={activeAgents} onPause={handlePause} onStop={handleStop} theme={theme} />
      <TaskViewer tasks={snapshot.tasks} />
      <WorkflowBuilderPanel workflowName={workflowBuilder.name} nodes={workflowBuilder.nodes} />
      <SecurityGuardianPanel warnings={securityGuardian.warnings} />
      <MarketplacePanel agents={marketplace.agents} theme={theme} />
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
