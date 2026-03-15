# memory

Persistent and session memory services plus knowledge graph retrieval.

## Responsibilities
- User/session memory storage.
- Embedding + retrieval orchestration.
- Knowledge graph query/update interfaces.

## Framework Layout
- `core/memory_manager.py`: unified memory orchestration API (`store_memory`, `search_memory`, `retrieve_context`) plus agent-compatible `remember`/`recall`.
- `core/short_term_memory.py`: bounded recent-memory buffer.
- `core/long_term_memory.py`: namespace-aware long-term store.
- `vector/embedding_service.py`: deterministic embedding generation service.
- `vector/vector_store.py`: vector index with semantic `similarity_search`.
- `graph/knowledge_graph.py`: entity/relationship graph operations.
- `graph/entity_extractor.py`: lightweight entity extraction pipeline.

- `brain/personal_knowledge_brain.py`: personal knowledge brain for capture, semantic search, topic linking/exploration, and automatic summarization.
