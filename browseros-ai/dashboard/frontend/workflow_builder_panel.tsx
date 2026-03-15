import React from "react";

type WorkflowNode = {
  id: string;
  label: string;
};

type WorkflowBuilderPanelProps = {
  workflowName: string;
  nodes: WorkflowNode[];
};

export function WorkflowBuilderPanel({ workflowName, nodes }: WorkflowBuilderPanelProps) {
  return (
    <section>
      <h2>Autonomous Workflow Builder</h2>
      <div>Workflow: {workflowName}</div>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
        {nodes.map((node, idx) => (
          <React.Fragment key={node.id}>
            <div style={{ border: "1px solid #ddd", padding: "8px 12px", borderRadius: 8 }}>{node.label}</div>
            {idx < nodes.length - 1 && <div style={{ alignSelf: "center" }}>↓</div>}
          </React.Fragment>
        ))}
      </div>
    </section>
  );
}
