# Build Log Entry 3 — Research Brief and Tagged Evidence

## Project Focus

Clarify what the prototype retrieves, what its records can establish, and what still needs research.

## 1. Research Question

What repository-history records can the prototype collect and retrieve for a developer’s question, and what can those records establish about the reason for a code change?

## 2. Six-Part Research Brief

- **Context:** Repository rationale can be spread across commits, merged pull requests, issues, and changed-file metadata.
- **Objective:** Describe the current evidence path without implying that a text match proves historical intent.
- **Task:** Review the ingestion, graph import, retrieval, and frontend implementation; verify an implementation claim against the project source.
- **Constraints:** Use project files and observed behavior as evidence. Distinguish implementation facts from inference and untested assumptions. Do not invent interview or AI-output records.
- **Output:** A description of the current retrieval flow and a tagged list of evidence, inferences, hypotheses, and assumptions.
- **Success criteria:** Implementation claims point to project sources; unknown user outcomes and missing records are identified as unverified.

## 3. Output

The current flow accepts a public GitHub repository, imports a bounded set of history into Neo4j, and lets a user search stored commit, pull-request, and issue text using question keywords. The Evidence Engine displays matching records with source links. The Graph Explorer displays stored graph relationships.

The output is a set of matching records for a person to inspect. It is not a verified explanation of why a change happened.

No original AI response or prompt transcript for this activity is preserved in the supplied project materials. This entry does not reconstruct one.

## 4. Verified Implementation Claim

The repository import endpoint requests up to 20 commits, 10 merged pull requests, and 15 issues. The question retrieval code extracts keywords, searches text on Commit, PullRequest, and Issue nodes, scores matching records, and returns up to 10 results.

**Sources:** `prototype/backend/main.py` (repository import and question endpoints); `prototype/backend/rag_pipeline.py` (keyword extraction and graph retrieval).

The active question flow displays matching records and source links. A keyword match alone does not demonstrate why a code change was made. The current question path does not call an LLM to write an explanation.

**Sources:** `prototype/backend/main.py`; `prototype/backend/rag_pipeline.py`.

## 5. Tagged Claims

- **[EVIDENCE]** The import endpoint requests up to 20 commits, 10 merged pull requests, and 15 issues for a repository import. **Source:** `prototype/backend/main.py`.
- **[EVIDENCE]** Retrieval searches text on Commit, PullRequest, and Issue nodes and ranks records using keyword matches. **Source:** `prototype/backend/rag_pipeline.py`.
- **[EVIDENCE]** The question response returns matching records and source metadata for display. **Source:** `prototype/backend/main.py`; `prototype/frontend/app.js`.
- **[EVIDENCE]** The active question path does not generate an LLM-written rationale. **Source:** `prototype/backend/main.py`; `prototype/backend/rag_pipeline.py`.
- **[INFERENCE]** Showing matches and source links together may reduce the number of separate GitHub searches a developer needs to perform.
- **[HYPOTHESIS]** Developers can find relevant repository context faster with this flow than with manual GitHub search. No timed comparison has been recorded.
- **[ASSUMPTION]** A bounded recent-history window contains useful records for some developer questions. This has not been established across a representative question set.

## 6. Evidence Still Needed

A useful evaluation would retain the question set, import counts, query results, source links opened, time-to-find measurements, and reviewer judgments about whether each source supports the question. The available project materials do not contain a systematic evaluation of this kind.
