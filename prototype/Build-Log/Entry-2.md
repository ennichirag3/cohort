# Build Log Entry 2: 4D Check & Delegation Mapping

## 1. Module Lead & Focus
- **Lead**: Manas (Technical Lead) & Shreya (Ingestion Lead)[span_17](start_span)[span_17](end_span)
- **Focus**: Repository representation, Neo4j schema design, 4D Framework[span_18](start_span)[span_18](end_span).

## 2. 4D Framework Breakdown
- **Delegation**: AI is delegated Cypher query generation and data transformation; humans retain schema validation and entity linking logic[span_19](start_span)[span_19](end_span).
- **Description**:
  - **Context**: Large Git history with scattered architectural decisions[span_20](start_span)[span_20](end_span).
  - **Objective**: Map entities (`:Commit`, `:PullRequest`, `:Issue`, `:Developer`, `:File`) in Neo4j with directional relationships[span_21](start_span)[span_21](end_span).
  - **Constraints**: Preserved source IDs, URLs, and timestamps without credential exposure[span_22](start_span)[span_22](end_span).
- **Discernment**: AI Cypher outputs are evaluated against Neo4j schema constraints and execution speed.
- **Diligence**: Every ingested entity is verified against raw GitHub REST/GraphQL API outputs[span_23](start_span)[span_23](end_span).

## 3. Review Checkpoints
1. **Raw Ingestion Review (Shreya)**: Validating JSON outputs from GitHub API before database loading[span_24](start_span)[span_24](end_span).
2. **Graph Consistency Check (Manas)**: Verifying `MERGE` constraints in Neo4j to prevent duplicate node creation[span_25](start_span)[span_25](end_span).
3. **Retrieval Lineage Review (Anshika & Anirudh)**: Testing Cypher traversals against known PR-to-issue links[span_26](start_span)[span_26](end_span).
