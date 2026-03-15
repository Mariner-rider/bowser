# Module Interfaces

This document defines minimal production-facing interfaces for each extension module.

## Shared Envelope

```ts
export interface RequestContext {
  requestId: string;
  userId?: string;
  sessionId?: string;
  traceId: string;
  timestamp: string;
  authScopes: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

export interface ModuleResult<T> {
  ok: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    retryable: boolean;
  };
  metrics?: Record<string, number>;
}
```

## `agents/`

```ts
export interface AgentPlanRequest {
  goal: string;
  constraints?: string[];
  tools?: string[];
}

export interface AgentPlan {
  planId: string;
  steps: Array<{ id: string; action: string; tool?: string }>;
}

export interface AgentOrchestrator {
  createPlan(ctx: RequestContext, req: AgentPlanRequest): Promise<ModuleResult<AgentPlan>>;
  executePlan(ctx: RequestContext, planId: string): Promise<ModuleResult<{ status: string }>>;
  runCollaboration(ctx: RequestContext, objective: string): Promise<ModuleResult<{ collaborationId: string; status: string }>>;
  getCollaborationMessages(ctx: RequestContext, collaborationId: string): Promise<ModuleResult<{ messages: unknown[] }>>;
}

export interface SecurityGuardianService {
  scanPage(ctx: RequestContext, url: string): Promise<ModuleResult<{ riskLevel: string; warnings: string[] }>>;
  scanDownload(ctx: RequestContext, filename: string, sourceUrl: string): Promise<ModuleResult<{ riskLevel: string; warnings: string[] }>>;
  scanExtensions(ctx: RequestContext): Promise<ModuleResult<{ riskLevel: string; warnings: string[] }>>;
}
```

## `llm/`

```ts
export type LLMTask = 'research' | 'coding' | 'automation' | 'summarization';

export interface GenerationRequest {
  task: LLMTask;
  prompt: string;
  modelHint?: string;
  maxTokens?: number;
  temperature?: number;
  executionMode?: "local" | "cloud" | "hybrid";
  offlineMode?: boolean;
}

export interface GenerationResponse {
  model: string;
  output: string;
  usage: { inputTokens: number; outputTokens: number };
}

export interface EmbeddingRequest {
  text: string;
  providerName?: string;
}

export interface ModelRouter {
  generate(ctx: RequestContext, req: GenerationRequest): Promise<ModuleResult<GenerationResponse>>;
  stream(ctx: RequestContext, req: GenerationRequest): AsyncIterable<string>;
  embed(ctx: RequestContext, req: EmbeddingRequest): Promise<ModuleResult<{ vector: number[] }>>;
}
```

## `memory/`

```ts
export interface MemoryWrite {
  namespace: string;
  key: string;
  value: unknown;
  ttlSeconds?: number;
}

export interface MemoryRead {
  namespace: string;
  key: string;
}

export interface KnowledgeGraphQuery {
  query: string;
  limit?: number;
}

export interface MemoryService {
  put(ctx: RequestContext, input: MemoryWrite): Promise<ModuleResult<{ version: string }>>;
  get(ctx: RequestContext, input: MemoryRead): Promise<ModuleResult<{ value: unknown }>>;
  queryGraph(ctx: RequestContext, input: KnowledgeGraphQuery): Promise<ModuleResult<{ nodes: unknown[]; edges: unknown[] }>>;
  semanticSearch(ctx: RequestContext, topic: string, query: string): Promise<ModuleResult<{ results: unknown[] }>>;
  exploreTopic(ctx: RequestContext, topic: string): Promise<ModuleResult<{ graph: unknown; stats: Record<string, number> }>>;
  summarizeTopic(ctx: RequestContext, topic: string): Promise<ModuleResult<{ summary: string }>>;
}
```

## `automation/`

```ts
export interface AutomationTask {
  objective: string;
  startUrl?: string;
  guardrails: {
    allowDomains?: string[];
    blockDomains?: string[];
    requiresConfirmation?: boolean;
  };
}

export interface AutomationRunner {
  runTask(ctx: RequestContext, task: AutomationTask): Promise<ModuleResult<{ runId: string; status: string }>>;
  stopTask(ctx: RequestContext, runId: string): Promise<ModuleResult<{ status: string }>>;
  runWorkflow(ctx: RequestContext, steps: Array<Record<string, unknown>>): Promise<ModuleResult<{ runId: string; actionsLogged: number }>>;
  createVisualWorkflow(ctx: RequestContext, name: string, nodes: Array<Record<string, unknown>>): Promise<ModuleResult<{ workflowId: string }>>;
  executeVisualWorkflow(ctx: RequestContext, workflowId: string): Promise<ModuleResult<{ runId: string; status: string }>>;
}
```

## `interface/`

```ts
export interface UserCommand {
  source: 'text' | 'voice' | 'ui';
  input: string;
  locale?: string;
}

export interface StructuredCommand {
  intent: string; // e.g. "research_topic"
  entity: string; // e.g. "AI agents"
  constraints?: string[];
  metadata?: Record<string, unknown>;
}

export interface InterfaceGateway {
  ingest(ctx: RequestContext, cmd: UserCommand): Promise<ModuleResult<{ command: StructuredCommand }>>;
  route(ctx: RequestContext, command: StructuredCommand): Promise<ModuleResult<{ taskId: string; status: string }>>;
}
```

## `dashboard/`

```ts
export interface TelemetryEvent {
  type: string;
  module: string;
  severity: 'debug' | 'info' | 'warn' | 'error';
  payload: Record<string, unknown>;
}

export interface MonitoringService {
  publish(ctx: RequestContext, event: TelemetryEvent): Promise<ModuleResult<{ accepted: boolean }>>;
  getSnapshot(ctx: RequestContext): Promise<ModuleResult<{ agents: unknown[]; tasks: unknown[]; logs: unknown[] }>>;
  pauseAgent(ctx: RequestContext, agentName: string): Promise<ModuleResult<{ state: string }>>;
  stopAgent(ctx: RequestContext, agentName: string): Promise<ModuleResult<{ state: string }>>;
}
```

## `web3/`

```ts
export interface WalletConnectRequest {
  chainId: string;
  walletProvider: 'metamask' | 'walletconnect' | 'embedded';
}

export interface SignRequest {
  chainId: string;
  address: string;
  payload: string;
}

export interface Web3IdentityService {
  connectWallet(ctx: RequestContext, req: WalletConnectRequest): Promise<ModuleResult<{ address: string }>>;
  sign(ctx: RequestContext, req: SignRequest): Promise<ModuleResult<{ signature: string }>>;
  loginWithWallet(ctx: RequestContext, req: WalletConnectRequest): Promise<ModuleResult<{ token: string; did: string }>>;
  authorizeToken(ctx: RequestContext, token: string, permission: string): Promise<ModuleResult<{ allowed: boolean }>>;
}
```


## `marketplace/`

```ts
export interface MarketplaceAgentManifest {
  agentId: string;
  name: string;
  version: string;
  description: string;
  capabilities: string[];
}

export interface MarketplaceService {
  publishAgent(ctx: RequestContext, manifest: MarketplaceAgentManifest): Promise<ModuleResult<{ published: boolean }>>;
  installAgent(ctx: RequestContext, agentId: string): Promise<ModuleResult<{ installed: boolean }>>;
  listMarketplace(ctx: RequestContext): Promise<ModuleResult<{ agents: MarketplaceAgentManifest[] }>>;
}
```


## `learning/`

```ts
export interface LearningService {
  collectInteraction(ctx: RequestContext, event: Record<string, unknown>): Promise<ModuleResult<{ stored: boolean }>>;
  processFeedback(ctx: RequestContext, feedback: Record<string, unknown>): Promise<ModuleResult<{ policyScore: number }>>;
  updatePreferences(ctx: RequestContext, userId: string): Promise<ModuleResult<{ profile: Record<string, unknown> }>>;
  resetProfile(ctx: RequestContext, userId: string): Promise<ModuleResult<{ reset: boolean }>>;
  setTracking(ctx: RequestContext, enabled: boolean): Promise<ModuleResult<{ enabled: boolean }>>;
}
```


## `local_ai/`

```ts
export interface LocalAIService {
  detectEngines(ctx: RequestContext): Promise<ModuleResult<{ engines: string[] }>>;
  installModel(ctx: RequestContext, req: Record<string, unknown>): Promise<ModuleResult<{ modelId: string }>>;
  runLocalInference(ctx: RequestContext, req: { modelId: string; prompt: string; stream?: boolean }): Promise<ModuleResult<{ output: string }>>;
  queueGpuWorkload(ctx: RequestContext, workload: Record<string, unknown>): Promise<ModuleResult<{ queued: boolean }>>;
  distributedInference(ctx: RequestContext, workload: Record<string, unknown>): Promise<ModuleResult<{ dispatched: boolean; nodeId?: string }>>;
}
```

## Cross-Module Rules

- Every public method receives `RequestContext`.
- Every response uses `ModuleResult<T>`.
- High-risk actions require `riskLevel=high` and an explicit policy check.
- All modules emit telemetry events with consistent trace IDs.
