# Build Log Entry 3 — Research Brief and Tagged Evidence

## Project Focus

Clarify what the prototype retrieves, what its records can establish, and what still needs research.

## 1. Research Question

What repository-history records can the prototype collect and retrieve for a developer question, and what can those records establish about the reason for a code change?

## 2. Six-Part Research Brief

- **Context:** The prototype is an evidence explorer for public GitHub history. It stores commits, merged pull requests, issues, and related metadata in Neo4j.
- **Objective:** Describe the available evidence path without implying that a text match establishes historical intent.
- **Task:** Review the ingestion, graph import, retrieval, and frontend source; verify one implementation claim against those files.
- **Constraints:** Use the project files as evidence; distinguish implementation facts from inference and untested product assumptions; do not invent interview or AI-output records.
- **Output:** A short description of the current evidence pipeline and a tagged claim list.
- **Success criteria:** Every implementation claim points to a project source; unknown user outcomes and missing records remain labeled as unverified.

## 3. AI Output and Verification Record

No original AI response or prompt transcript for Activity 3 is preserved in the supplied project files. This log does not reconstruct a historical response or attribute new wording to a past AI session.

**Verified implementation claim:** The repository import endpoint requests bounded history—20 commits, 10 merged pull requests, and 15 issues—then imports the normalized JSON into Neo4j. The retrieval pipeline extracts words from a question, searches commit/PR/issue text for those words, scores matches, and returns up to 10 records.  
**Sources:** prototype/backend/main.py (add_github_repository, ask_question); prototype/backend/rag_pipeline.py (extract_keywords, fetch_graph_evidence).

The returned records and links can be inspected, but a keyword match alone does not demonstrate why a change was made.  
**Source:** prototype/backend/rag_pipeline.py (make_evidence_answer).

## 4. Tagged Claims

- **[EVIDENCE]** The import endpoint requests up to 20 commits, 10 merged PRs, and 15 issues for each repository import. **Source:** prototype/backend/main.py.
- **[EVIDENCE]** Retrieval searches text fields on Commit, PullRequest, and Issue nodes and orders results by keyword match score. **Source:** prototype/backend/rag_pipeline.py.
- **[EVIDENCE]** The response builder says matching records show what was recorded and advises opening source links; it does not claim that text matching proves the reason for a change. **Source:** prototype/backend/rag_pipeline.py.
- **[INFERENCE]** Showing matched records and links together may reduce the number of separate GitHub searches needed.
- **[HYPOTHESIS]** Developers can find useful repository context faster with this flow than with manual history search. No timing comparison is recorded.
- **[ASSUMPTION]** The bounded recent-history window includes the records needed for some meaningful questions. This has not been established for a representative question set.

## 5. Evidence Still Needed

To test the hypothesis, retain a question set, query results, links opened, time-to-find measurements, and reviewer judgments on whether each source supports the answer. The supplied project files do not contain those results.