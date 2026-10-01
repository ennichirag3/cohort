# Entry 3: RAG Prompt Engineering & Claims Classification

## 1. Six-Part RAG Prompt Brief

- **Role**: Technical Documentation & Architecture Assistant.
- **Task**: Answer developer "Why?" queries regarding software architecture decisions using only retrieved Neo4j knowledge graph context.
- **Context**: Dynamically injected Cypher graph traversal records (Commits, Pull Requests, Issues, Architectural Decisions).
- **Constraints**: 
  1. Rely strictly on the provided evidence.
  2. Do NOT invent, assume, or speculate on historical repository details.
  3. If evidence is missing or insufficient, output EXACTLY: *"Insufficient evidence in repository history to answer this question."*
- **Output Format**: Structured, clear explanation categorized into direct evidence and inference, followed by source citations.
- **Examples**: Provided reference questions regarding technology stack choices and refactoring decisions.

---

## 2. Sample Output Generation Log

**User Question**: 
> *"Why was Neo4j chosen over PostgreSQL for indexing repository entities?"*

**Synthesized LLM Output**:
> Neo4j was selected over PostgreSQL to natively store and query multi-hop relationships between commits, pull requests, issues, and architectural decisions without requiring costly relational JOIN operations.

---

## 3. Tagged Claims Classification

- **[EVIDENCE]**: PR #42 explicitly documents graph traversal performance benchmarks comparing Neo4j and PostgreSQL.
- **[INFERENCE]**: The engineering team prioritized query performance for multi-hop entity relations over familiar SQL relational patterns.
- **[HYPOTHESIS]**: Future repository scaling will yield greater graph traversal performance advantages as the codebase grows.
- **[ASSUMPTION]**: PostgreSQL relational join overhead would have become a performance bottleneck at current repository scale.
