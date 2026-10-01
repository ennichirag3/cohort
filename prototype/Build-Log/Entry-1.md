# Build Log Entry 1: Problem Definition & Team Leverage Map

## 1. Theme
AI and Developer Tools — *Why The Code Is Like This*

## 2. Problem Statement (Version 1)
New developers can read existing code but often cannot recover the intent behind design and implementation decisions. Important reasoning is distributed across commits, pull requests, issues, and design documents, making keyword search insufficient for understanding why a codebase is structured a certain way. We want to build an evidence-backed assistant that connects code entities to historical decisions and lets developers ask why-questions with traceable evidence.

## 3. Intended Build
We are building a RAG-driven developer assistant querying a Neo4j knowledge graph containing repository commits, PRs, and issue threads. The assistant delivers zero-hallucination, evidence-backed answers to architectural questions with direct source citations.

## 4. Team Responsibilities Split (5 Members)
- **Anirudh (Product + Problem/Evidence Lead)**: Problem definition, Five Whys, assumptions, tagged claims list, problem statement iterations.
- **Manas (Technical Lead + Graph/Neo4j)**: Neo4j AuraDB schema design, Cypher queries, graph traversal, and `PROJECT_SPEC.md`.
- **Shreya (Repository Ingestion + GitHub Data)**: GitHub REST/GraphQL pipeline, data normalization, commit/PR parsing, preserving source links.
- **Anshika (RAG/AI + Evidence Answering)**: RAG pipeline (`rag_pipeline.py`), FastAPI backend (`main.py`), prompt engineering, refusal triggers.
- **Chirag (Frontend + Testing + Demo)**: Glassmorphic UI (`index.html`, `app.js`), failure case testing, stranger testing execution, README.

## 5. Task Leverage & Agency Mapping
| Task Description | Primary Lead | Leverage Type |
| :--- | :--- | :--- |
| Repository Metadata Parsing | Shreya | Automation |
| Graph Schema Definition | Manas | Augmentation |
| Zero-Temp RAG Retrieval | Anshika | Augmentation |
| User Failure Validation & Stranger Test | Chirag | Agency |
| Evidence Tagging & Claims Audit | Anirudh | Agency |

## 6. Non-Delegable Human Decisions
1. **Factual Ground Truth Verification**: Deciding whether an answer is sufficiently grounded in graph nodes or requires an explicit refusal.
2. **UI Usability Thresholds**: Judging stranger test feedback to determine if citation cards and source links provide clear lineage.
