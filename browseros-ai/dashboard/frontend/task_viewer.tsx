import React from "react";

type Task = {
  task_id: string;
  agent_name: string;
  description: string;
  status: string;
  progress: number;
  automation_steps: string[];
};

type TaskViewerProps = {
  tasks: Task[];
};

export function TaskViewer({ tasks }: TaskViewerProps) {
  return (
    <section>
      <h2>Task Progress</h2>
      {tasks.map((task) => (
        <div key={task.task_id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          <strong>{task.description}</strong>
          <div>Agent: {task.agent_name}</div>
          <div>Status: {task.status}</div>
          <div>Progress: {task.progress}%</div>
          <div>
            Automation Steps:
            <ul>
              {task.automation_steps.map((step, idx) => (
                <li key={`${task.task_id}-${idx}`}>{step}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}
    </section>
  );
}
