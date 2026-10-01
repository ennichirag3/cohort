# Build Log Entry 4: Unwinding the Idea & Problem Statement V2

## 1. Module Lead & Focus
- **Lead**: Anirudh (Product Lead)[span_35](start_span)[span_35](end_span)
- **Focus**: Five Whys, Critic Objections, Top Assumptions, Problem Statement V2[span_36](start_span)[span_36](end_span).

## 2. Five Whys Analysis
1. *Why do developers write code that violates past architectural patterns?* They don't know why the original code was written that way[span_37](start_span)[span_37](end_span).
2. *Why don't they know?* Design context is hidden inside closed PRs and commit logs[span_38](start_span)[span_38](end_span).
3. *Why can't they find it using standard search?* Keyword search returns file locations, not historical intent[span_39](start_span)[span_39](end_span).
4. *Why is historical intent hard to query?* Git history treats changes as text diffs, not connected graph entities[span_40](start_span)[span_40](end_span).
5. *Why haven't tools fixed this?* Existing tools index current code states rather than historical relationships[span_41](start_span)[span_41](end_span). **(Research Focus)**

## 3. Critic Objections & Mitigation
- **Technical Lead Objection**: *"Developers won't trust an AI that guesses design reasons."*
  - *Mitigation*: System strictly returns *"Insufficient context in knowledge graph"* when graph evidence is absent[span_42](start_span)[span_42](end_span).
- **Operator Objection**: *"Maintaining a Neo4j graph for every repo is too complex."*
  - *Mitigation*: Automated GitHub Actions pipeline ingests metadata incrementally[span_43](start_span)[span_43](end_span).

## 4. Top 3 Assumptions & 48-Hour Tests
1. **Assumption**: PR body texts contain enough design context[span_44](start_span)[span_44](end_span).
   - *Test*: Audit 50 PRs in the target repo for explicit rationale.
2. **Assumption**: Zero-temperature LLMs will not hallucinate missing PR links[span_45](start_span)[span_45](end_span).
   - *Test*: Query 20 non-existent features and check for 100% refusal rate[span_46](start_span)[span_46](end_span).
3. **Assumption**: External developers can navigate citation cards without training[span_47](start_span)[span_47](end_span).
   - *Test*: Run stranger tests with 2 peer developers[span_48](start_span)[span_48](end_span).

## 5. Problem Statement Version 2
Software developers onboarding to a codebase waste significant time recovering historical rationale for architectural decisions[span_49](start_span)[span_49](end_span). Existing tools search code diffs but fail to link issues, PRs, and commits into a traceable decision chain[span_50](start_span)[span_50](end_span). We are building an evidence-backed RAG assistant that indexes Git history into a Neo4j knowledge graph, enabling developers to ask why-questions and receive answers grounded strictly in verifiable commit and PR evidence[span_51](start_span)[span_51](end_span).
