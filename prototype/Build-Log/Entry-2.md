# Build Log Entry 2: 4D Check & Delegation Mapping

## 1. Module Lead & Focus
- **Lead**: Manas (Technical Lead) & Shreya (Ingestion Lead)
- **Focus**: Repository representation, Neo4j schema design, 4D Framework.

## 2. 4D Framework Breakdown
- **Delegation**: AI is delegated Cypher query generation and data transformation; humans retain schema validation and entity linking logic.
- **Description**:
  - **Context**: Large Git history with scattered architectural decisions.
  - **Objective**: Map entities (`:Commit`, `:PullRequest`, `:Issue`, `:Developer`, `:File`) in Neo4j with directional relationships.
  - **Constraints**: Preserved source IDs, URLs, and timestamps without credential exposure.
- **Discernment**: AI Cypher outputs are evaluated against Neo4j schema constraints and execution speed.
- **Diligence**: Every ingested entity is verified against raw GitHub REST/GraphQL API outputs.

## 3. Review Checkpoints
1. **Raw Ingestion Review (Shreya)**: Validating JSON outputs from GitHub API before database loading.
2. **Graph Consistency Check (Manas)**: Verifying `MERGE` constraints in Neo4j to prevent duplicate node creation.
3. **Retrieval Lineage Review (Anshika & Anirudh)**: Testing Cypher traversals against known PR-to-issue links.
