# Entry 2: Neo4j Schema & Data Ingestion Plan

## 1. Graph Entity Schema
- **Nodes**: `:Commit`, `:PullRequest`, `:Issue`, `:Decision`
- **Properties**: `hash`/`id`, `message`/`summary`/`title`, `author`, `date`, `url`
- **Relationships**: 
  - `(:Commit)-[:RESOLVES]->(:Issue)`
  - `(:PullRequest)-[:MERGES]->(:Commit)`
  - `(:Decision)-[:DOCUMENTED_IN]->(:PullRequest)`

## 2. Environment Configuration
Database credentials and URI are stored securely in `.env`:
- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
