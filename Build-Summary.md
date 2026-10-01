# Build Summary

## Theme
AI and Developer Tools — *Why The Code Is Like This*

## Final Problem Statement
Software developers onboarding to a codebase waste significant time recovering historical rationale for architectural decisions. Existing tools search code diffs but fail to link issues, PRs, and commits into a traceable decision chain. We built an evidence-backed RAG assistant that indexes Git history into a Neo4j knowledge graph, enabling developers to ask why-questions and receive answers grounded strictly in verifiable commit and PR evidence.

## What Changed from Version 1
Initial assumptions targeted broad code comments. Analysis revealed that real architectural rationale lives inside Pull Request discussion threads and issue links. We refocused the ingestion pipeline and graph schema specifically around PR-to-Commit-to-Issue relationships.

## What We Built
A single-screen Glassmorphic web application backed by FastAPI and Neo4j AuraDB. Users enter a query regarding code decisions, and the system retrieves the relevant subgraph, generating an answer with verifiable citation cards. If context is missing, it explicitly refuses to answer.

## Tech Stack
- **Frontend**: Glassmorphic HTML/CSS/JS
- **Backend**: FastAPI (Python)
- **Graph Database**: Neo4j AuraDB
- **AI Engine**: OpenAI API (`gpt-4o`) with zero-temperature guardrails

## Evidence Position
- **Proven**: Zero-temperature RAG eliminates hallucinations when backed by structured Neo4j subgraphs.
- **Assumption**: Developers will consistently write detailed PR descriptions in future projects.

## What We Build Next
1. Automated GitHub Webhooks for real-time graph updates upon PR merge.
2. Multi-repository graph querying across microservice architectures.
