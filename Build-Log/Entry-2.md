# Build Log Entry 2 — 4D Check and Delegation Map

## Project Focus

Define how the repository-history assistant should collect and represent evidence, and specify which decisions remain human-led.

## 1. Delegation

The implementation automates public GitHub data retrieval, normalization, Neo4j import, keyword matching, and presentation of matching records. AI tools may assist with drafting or reviewing project materials, but the current prototype/backend/rag_pipeline.py does not call an LLM. Humans choose the repository and scope, review schema and source lineage, judge whether matches support a question, and decide what engineering action to take.

## 2. Description — Six-Part Brief

- **Context:** Repository rationale is spread across commits, merged pull requests, issues, and changed-file metadata.
- **Objective:** Let a developer inspect relevant recent history and its source links in one prototype.
- **Task:** Fetch bounded GitHub history, normalize stable IDs and metadata, import it into Neo4j, and retrieve records whose text matches a question.
- **Constraints:** Public repositories only; bounded API calls; preserve original IDs, dates, and source URLs; keep credentials out of source; do not treat keyword matches as proof of intent.
- **Output:** Matching repository records, source links, and a graph view of stored relationships.
- **Success criteria:** A developer can import a public repository, retrieve relevant records for a specific question, open original sources, and recognize when the available evidence is insufficient.

## 3. Discernment

Review any AI-assisted planning or generated code against the repository files and the observed application behavior. Check that IDs, dates, authors, URLs, and relationships agree with the GitHub records; check that retrieval returns actual source records; and verify that response text does not claim the records prove more than they do. A passing technical response is not enough if its sources do not support the interpretation.

The project files do not include a completed AI-output review record, so this entry defines the review method rather than claiming a review was completed.

## 4. Diligence

Before relying on an imported result:

1. Compare a normalized record with its GitHub source.
2. Verify the record ID, author/date fields, and source URL.
3. Inspect the Neo4j relationships used by the query.
4. Open source links and check whether the cited text supports the question.
5. Record missing or ambiguous evidence instead of filling gaps with assumptions.

## 5. Activity 1 Task Map

| Task | Delegation | Reason |
| --- | --- | --- |
| Fetch commits, pull requests, and issues | Software automation, not AI | The ingestion code makes bounded API requests after a person selects a repository. |
| Normalize and connect repository records | Shared | Code creates the structure; a person should review mappings and relationships. |
| Search graph records for question terms | Software automation, not AI | Current retrieval is deterministic keyword matching. |
| Interpret whether a source answers the question | Human-led | The product presents records; a person evaluates what the source supports. |
| Judge historical intent and sufficiency | Human-led | The graph does not establish causation from text matches alone. |
| Choose a code change | Human-led | This is an engineering judgment beyond the prototype’s output. |

## 6. Review Checkpoints

1. **Ingestion review — Shreya, ingestion lead:** compare normalized JSON with GitHub source records and verify IDs and URLs.
2. **Graph review — Manas, technical/Neo4j lead:** inspect node constraints and relationships against schema.cypher, import_sample.py, and retrieval queries.
3. **Evidence review — Anshika and Anirudh, AI/RAG and product/evidence leads:** inspect returned records and confirm that response language does not overstate what matching text proves.

Chirag leads the frontend and testing work. These are responsibility assignments from the team guide; this log does not claim that each checkpoint has a retained completion record.

## 7. Items That Still Need Verification

- Whether the selected history window contains enough context for realistic why-questions.
- Whether keyword matching is sufficiently useful compared with manual GitHub search.
- Whether the source links and relationships remain accurate after import.
- Whether users understand the limitation between “matching record” and “documented reason.”