import React from "react";

type SecurityWarning = {
  risk: "low" | "medium" | "high";
  message: string;
};

type SecurityGuardianPanelProps = {
  warnings: SecurityWarning[];
};

export function SecurityGuardianPanel({ warnings }: SecurityGuardianPanelProps) {
  return (
    <section>
      <h2>AI Privacy + Security Guardian</h2>
      {warnings.length === 0 ? (
        <div>No active security alerts.</div>
      ) : (
        <ul>
          {warnings.map((warning, index) => (
            <li key={`${warning.message}-${index}`}>
              {warning.risk === "high" ? "⚠" : "ℹ"} [{warning.risk.toUpperCase()}] {warning.message}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
