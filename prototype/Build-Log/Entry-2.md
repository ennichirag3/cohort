# Entry 2: Knowledge Graph Schema & Data Ingestion Pipeline

## 1. Module Overview & Primary Lead
- **Module Lead**: Manas (Tech & Neo4j Lead)
- **Co-Lead / Contributor**: Anirudh (Data & Ingestion Lead)
- **Collaborators**: Anshika (RAG Integration), Chirag (UI Query Mapping), Shreya (Data Quality & Validation)

---

## 2. Graph Database Architecture & Schema Design
To provide factual, source-backed explanations for code decisions, the system models Git metadata and developer discussions in **Neo4j AuraDB**.

### Node Labels
- `:Commit`: Represents Git commits containing commit hash, author, timestamp, and message.
- `:PullRequest`: Represents GitHub PRs with PR ID, title, body, and status.
- `:Issue`: Represents issues with issue ID, title, description, and state.
- `:Developer`: Represents contributors/authors involved in discussions and changes.
- `:File`: Represents code files or modules modified in commits.

### Relationship Types
- `(:Developer)-[:AUTHORED]->(:Commit)`
- `(:Commit)-[:MERGED_INTO]->(:PullRequest)`
- `(:PullRequest)-[:CLOSES]->(:Issue)`
- `(:Commit)-[:MODIFIED]->(:File)`
- `(:Developer)-[:COMMENTED_ON]->(:PullRequest)`

---

## 3. Data Ingestion Pipeline & Parsing
- **Extraction**: GitHub REST/GraphQL APIs extract commits, issues, pull requests, and file diffs.
- **Parsing & Cleaning**: Unstructured PR descriptions and commit messages are parsed and normalized into structured JSON formats.
- **Neo4j Ingestion**: Cypher `MERGE` queries import nodes and relationships deterministically to avoid duplicate records.

---

## 4. Query Optimization & Retrieval
- Created constraints on unique properties (`Commit.hash`, `PullRequest.id`, `Issue.id`).
- Formulated optimized Cypher lookup templates for common developer queries (e.g., *"Why was this file modified?"* or *"Which PR closed Issue #42?"*).
