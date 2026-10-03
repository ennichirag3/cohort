# Build Log Entry 2 — 4D Check and Delegation Map

## Project Focus

Define how the prototype collects and represents repository evidence, and identify which judgments remain human-led.

## 1. 4D Check

| 4D area | Project application | Check |
| --- | --- | --- |
| **Description** | The prototype fetches a bounded set of public commits, merged pull requests, and issues, stores them in Neo4j, and searches record text for question keywords. | Describe the behavior as evidence retrieval. Do not describe it as an AI explanation of historical intent. |
| **Discernment** | Records returned by matching text may be relevant, irrelevant, or incomplete. | Compare a result with its GitHub source and decide whether it actually supports the question. |
| **Delegation** | Software handles bounded fetching, normalization, graph import, keyword matching, and display. People choose repositories, review data and relationships, interpret evidence, and choose engineering actions. | Keep decisions about intent and action with a person. |
| **Diligence** | Records should preserve stable IDs, authors, timestamps, and original source URLs where available. | Verify representative records against GitHub, inspect graph relationships, and report missing or ambiguous evidence. |

## 2. Delegation Map

| Task | Delegation | Reason |
| --- | --- | --- |
| Fetch commits, pull requests, and issues | Software automation | The code makes bounded GitHub API requests after a person selects a repository. |
| Normalize records and preserve source metadata | Shared | Code creates the normalized records; a person should review the mapping and lineage. |
| Import records and relationships into Neo4j | Software automation with human review | Code writes the graph; a person checks whether the schema and relationships are appropriate. |
| Search record text for question keywords | Software automation | Current retrieval uses deterministic keyword matching. |
| Decide whether a match answers the question | Human-led | A text match does not establish that a record supports the question. |
| Judge historical intent or evidence sufficiency | Human-led | The graph does not prove causation or intent by itself. |
| Choose or implement a code change | Human-led | Engineering decisions are outside the prototype’s retrieval flow. |

## 3. Review Checkpoints

These are team responsibilities, not claims that the reviews have been completed.

1. **Ingestion review — Shreya, ingestion lead:** compare normalized records with GitHub and check IDs, dates, authors, and source URLs.
2. **Graph review — Manas, technical/Neo4j lead:** inspect node constraints and relationships against the schema, importer, and retrieval queries.
3. **Evidence review — Anshika and Anirudh, AI/RAG and product/evidence leads:** inspect returned records and check that explanations do not overstate what matching text proves.
4. **Frontend and testing — Chirag:** review the user flow, source links, graph display, and test observations.

## 4. Diligence Checklist

Before relying on an imported result:

1. Compare a normalized record with its GitHub source.
2. Verify its ID, author, date, and source URL where those fields are available.
3. Inspect the Neo4j relationships used by graph and retrieval queries.
4. Open the source link and check whether the original record supports the question.
5. Record missing or ambiguous evidence instead of filling gaps with assumptions.

## 5. Review Status

The project files do not contain a completed review record for each checkpoint. This entry documents the planned responsibilities and review method; it does not claim that every review was completed.
