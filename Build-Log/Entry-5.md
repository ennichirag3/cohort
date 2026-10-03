# Build Log Entry 5 — Product-Market Fit and Single Flow

## Project Focus

State a testable product hypothesis and define one flow that matches the current repository-history prototype.

## 1. Falsifiable Hypothesis

When a developer investigates an unfamiliar public repository, the prototype’s bounded import and source-linked keyword results will help them locate a relevant commit, pull request, or issue faster than manual GitHub history search. This hypothesis will be supported only if a timed comparison shows shorter search time without a loss in source relevance; no comparison has been recorded yet.

## 2. Ideal Customer Profile

A developer or open-source contributor who:

- Works in an unfamiliar public GitHub repository.
- Needs to understand the history of a behavior or file before changing it.
- Can use public commit, pull-request, and issue history.
- Is willing to inspect original sources rather than accept a generated rationale.

Potential research/demo repositories include:

1. pallets/click — repository used in the included sample/final data.
2. fastapi/fastapi
3. pydantic/pydantic
4. encode/httpx
5. pytest-dev/pytest

These are candidate repository examples, not people contacted or evidence that the team interviewed their maintainers.

## 3. Current Substitute and Its Cost

The direct substitutes are GitHub search, commit history, pull-request and issue pages, git log, git blame, and asking a maintainer. Their actual time cost for the target users has not been measured. The evaluation should compare those workflows against the prototype using the same repository and question.

## 4. Mechanism

The backend fetches a bounded window of public commits, merged PRs, and issues, normalizes their identifiers and source links, and imports them into Neo4j. The question flow extracts keywords, searches stored record text, scores matches, and returns source records. A developer can inspect those records in Evidence Engine and explore stored relationships in Graph Explorer.

The current mechanism locates records. It does not generate an AI explanation or establish that a matching record caused a code decision.

## 5. Opportunity Estimate

No sourced user count, price, adoption rate, or willingness-to-pay estimate is present in the project files. The opportunity estimate is therefore **not calculated**. A future estimate should state its sources and assumptions using:

reachable target developers × realistic price × realistic adoption

## 6. Insight Ledger

| Insight | Origin | Type | Confidence | Consequence |
| --- | --- | --- | --- | --- |
| Source IDs and URLs are preserved through ingestion so a reviewer can return to the original record. | prototype/backend/INGESTION_CONTRACT.md, fetch_github_data.py | Implementation evidence | High for the code; runtime verification not retained | Keep source links visible and verify them during evaluation. |
| Keyword matches can locate records but do not establish the reason behind a change. | prototype/backend/rag_pipeline.py response text and query logic | Implementation evidence | High | Describe results as matching evidence and keep the developer in the judgment loop. |

## 7. Single Target Product Flow

1. Enter a public GitHub repository URL or owner/repo.
2. Import the bounded repository history into Neo4j.
3. Ask a why-question using distinctive repository terms.
4. Review matching records, source links, or the graph view.

The assessment should record import success, relevant records found, source validity, time-to-find, and whether the source actually explains the question.