# Build Summary

## Theme
AI and Developer Tools — *Why The Code Is Like This*[span_83](start_span)[span_83](end_span)

## Final Problem Statement
Software developers onboarding to a codebase waste significant time recovering historical rationale for architectural decisions[span_84](start_span)[span_84](end_span). Existing tools search code diffs but fail to link issues, PRs, and commits into a traceable decision chain[span_85](start_span)[span_85](end_span). We built an evidence-backed RAG assistant that indexes Git history into a Neo4j knowledge graph, enabling developers to ask why-questions and receive answers grounded strictly in verifiable commit and PR evidence[span_86](start_span)[span_86](end_span).

## What Changed from Version 1
Initial assumptions targeted broad code comments[span_87](start_span)[span_87](end_span). Analysis revealed that real architectural rationale lives inside Pull Request discussion threads and issue links[span_88](start_span)[span_88](end_span). We refocused the ingestion pipeline and graph schema specifically around PR-to-Commit-to-Issue relationships[span_89](start_span)[span_89](end_span).

## What We Built
A single-screen Glassmorphic web application backed by FastAPI and Neo4j AuraDB[span_90](start_span)[span_90](end_span). Users enter a query regarding code decisions, and the system retrieves the relevant subgraph, generating an answer with verifiable citation cards[span_91](start_span)[span_91](end_span). If context is missing, it explicitly refuses to answer[span_92](start_span)[span_92](end_span).

## Tech Stack
- **Frontend**: Glassmorphic HTML/CSS/JS[span_93](start_span)[span_93](end_span)
- **Backend**: FastAPI (Python)[span_94](start_span)[span_94](end_span)
- **Graph Database**: Neo4j AuraDB[span_95](start_span)[span_95](end_span)
- **AI Engine**: OpenAI API (`gpt-4o`) with zero-temperature guardrails[span_96](start_span)[span_96](end_span)

## Evidence Position
- **Proven**: Zero-temperature RAG eliminates hallucinations when backed by structured Neo4j subgraphs[span_97](start_span)[span_97](end_span).
- **Assumption**: Developers will consistently write detailed PR descriptions in future projects[span_98](start_span)[span_98](end_span).

## What We Build Next
1. Automated GitHub Webhooks for real-time graph updates upon PR merge[span_99](start_span)[span_99](end_span).
2. Multi-repository graph querying across microservice architectures[span_100](start_span)[span_100](end_span).
