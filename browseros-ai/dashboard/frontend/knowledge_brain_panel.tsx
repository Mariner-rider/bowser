import React from "react";

type SearchResult = {
  title: string;
  source_type: string;
  score: number;
};

type KnowledgeStats = {
  nodes: number;
  relationships: number;
  topics: number;
};

type KnowledgeBrainPanelProps = {
  topic: string;
  semanticResults: SearchResult[];
  stats: KnowledgeStats;
  summary: string;
};

export function KnowledgeBrainPanel({ topic, semanticResults, stats, summary }: KnowledgeBrainPanelProps) {
  return (
    <section>
      <h2>Personal AI Knowledge Brain</h2>
      <div>Topic: {topic}</div>
      <p>{summary}</p>
      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <div>Nodes: {stats.nodes}</div>
        <div>Relationships: {stats.relationships}</div>
        <div>Topics: {stats.topics}</div>
      </div>
      <h3>Semantic Search</h3>
      <ul>
        {semanticResults.map((result, index) => (
          <li key={`${result.title}-${index}`}>
            {result.title} ({result.source_type}) — similarity {result.score}
          </li>
        ))}
      </ul>
    </section>
  );
}
