# Build Log Entry 3: Research Briefing & Tagged Evidence List

## 1. Module Lead & Focus
- **Lead**: Anshika (AI/RAG Lead) & Anirudh (Product/Evidence Lead)
- **Focus**: Six-part prompt briefing, claim tagging, zero-temperature execution.

## 2. Six-Part Research Brief
1. **Context**: RAG pipeline connecting FastAPI to Neo4j AuraDB.
2. **Objective**: Retrieve precise subgraphs for developer questions.
3. **Task**: Convert natural language queries into Cypher statements and format LLM context.
4. **Constraints**: Zero temperature (`0.0`), explicit citation enforced, refuse if context is missing.
5. **Output**: Concise answer with evidence chain and direct GitHub URLs.
6. **Success Criteria**: 0% hallucinated design decisions.

## 3. Tagged Evidence Classification File
- `[EVIDENCE]` PR #14 merged on 2025-11-12 states: *"Replaced Redis with Memcached to lower latency spikes under high read volume."*
- `[INFERENCE]` Memcached was chosen primarily for read-heavy key-value performance based on comment threads in PR #14.
- `[HYPOTHESIS]` Switching to Memcached reduced P99 latency by 15%.
- `[ASSUMPTION]` Developers will prefer glassmorphic citation cards over raw markdown links.
