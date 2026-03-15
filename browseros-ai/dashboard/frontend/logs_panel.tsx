import React from "react";

type DashboardLog = {
  timestamp: string;
  level: string;
  source: string;
  message: string;
};

type LogsPanelProps = {
  logs: DashboardLog[];
};

export function LogsPanel({ logs }: LogsPanelProps) {
  return (
    <section>
      <h2>Logs</h2>
      <ul>
        {logs.map((log, idx) => (
          <li key={`${log.timestamp}-${idx}`}>
            [{log.level.toUpperCase()}] {log.timestamp} ({log.source}) - {log.message}
          </li>
        ))}
      </ul>
    </section>
  );
}
