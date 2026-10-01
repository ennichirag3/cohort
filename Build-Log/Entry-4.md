# Build Log Entry 4: Unwinding the Idea & Problem Statement V2

## 1. Module Lead & Focus
- **Lead**: Anirudh (Product Lead)
- **Focus**: Five Whys, Critic Objections, Top Assumptions, Problem Statement V2.

## 2. Five Whys Analysis
1. *Why do developers write code that violates past architectural patterns?* They don't know why the original code was written that way.
2. *Why don't they know?* Design context is hidden inside closed PRs and commit logs.
3. *Why can't they find it using standard search?* Keyword search returns file locations, not historical intent.
4. *Why is historical intent hard to query?* Git history treats changes as text diffs, not connected graph entities.
5. *Why haven't tools fixed this?* Existing tools index current code states rather than historical relationships. **(Research Focus)**

## 3. Critic Objections & Mitigation
- **Technical Lead Objection**: *"Developers won't trust an AI that guesses design reasons."*
  - *Mitigation*: System strictly returns *"Insufficient context in knowledge graph"* when graph evidence is absent.
- **Operator Objection**: *"Maintaining a Neo4j graph for every repo is too complex."*
  - *Mitigation*: Automated GitHub Actions pipeline ingests metadata incrementally.

## 4. Top 3 Assumptions & 48-Hour Tests
1. **Assumption**: PR body texts contain enough design context.
   - *Test*: Audit 50 PRs in the target repo for explicit rationale.
2. **Assumption**: Zero-temperature LLMs will not hallucinate missing PR links.
   - *Test*: Query 20 non-existent features and check for 100% refusal rate.
3. **Assumption**: External developers can navigate citation cards without training.
   - *Test*: Run stranger tests with 2 peer developers.

## 5. Problem Statement Version 2
Software developers onboarding to a codebase waste significant time recovering historical rationale for architectural decisions. Existing tools search code diffs but fail to link issues, PRs, and commits into a traceable decision chain. We are building an evidence-backed RAG assistant that indexes Git history into a Neo4j knowledge graph, enabling developers to ask why-questions and receive answers grounded strictly in verifiable commit and PR evidence.
