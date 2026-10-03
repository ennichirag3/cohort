# Build Log Entry 5 — Product-Market Fit and Single Flow

## Project Focus

State a testable product hypothesis and define one flow that matches the current repository-history prototype.

## 1. Falsifiable Hypothesis

When a developer investigates an unfamiliar public repository, the prototype’s bounded import and source-linked keyword results will help them locate a relevant commit, pull request, or issue faster than manual GitHub history search.

This hypothesis is supported only if a timed comparison shows shorter search time without a loss in source relevance. No controlled comparison has been recorded.

## 2. Ideal Customer Profile

A developer or open-source contributor who:

- Works in an unfamiliar public GitHub repository.
- Needs to inspect the history of a behavior or file before changing it.
- Can use public commit, pull-request, and issue history.
- Is willing to inspect original sources rather than accept a generated rationale.

Candidate demo repositories include `pallets/click`, `fastapi/fastapi`, `pydantic/pydantic`, `encode/httpx`, and `pytest-dev/pytest`. These are repository examples, not people interviewed or evidence of demand.

## 3. Current Substitute and Its Cost

Substitutes include GitHub search, commit history, pull-request and issue pages, `git log`, `git blame`, and asking a maintainer.

The time cost and quality of these approaches have not been measured for the target users. A fair comparison should use the same repository and question for both the prototype and manual search.

## 4. Mechanism

The backend fetches a bounded window of public commits, merged pull requests, and issues, normalizes their identifiers and source links, and imports them into Neo4j. The question flow extracts keywords, searches stored record text, scores matches, and returns source records. The Evidence Engine displays the records and links; Graph Explorer displays stored relationships.

The current mechanism locates records. It does not generate an LLM explanation or establish that a matching record caused a code decision.

## 5. Opportunity Estimate

A product-specific market size cannot be calculated from the evidence available for this project. GitHub reported more than 180 million developers and 395 million public and open-source repositories in its 2025 Octoverse report. These figures describe the wider GitHub ecosystem; they do not show how many developers investigate unfamiliar repositories or need this product. ([GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/))

The target segment’s size, how often its members face this problem, the number we could initially reach, and expected adoption are unknown. Therefore, I cannot responsibly calculate a serviceable market, adoption estimate, or revenue estimate. The GitHub totals are broad context, not this product’s addressable market.

To size the opportunity, the next step is to interview or test with developers who investigate unfamiliar public repositories, measure how often they encounter this problem, and estimate how many can be reached through a defined initial channel. Demand and willingness to pay remain unvalidated.

## 6. Insight Ledger

| Insight | Origin | Type | Confidence | Consequence |
| --- | --- | --- | --- | --- |
| The importer preserves identifiers and source metadata where available. | `prototype/backend/INGESTION_CONTRACT.md`; `prototype/backend/fetch_github_data.py` | Implementation evidence | High for source code; runtime verification is limited | Keep source links visible and verify representative records during evaluation. |
| Keyword matches can locate records but do not establish the reason behind a change. | `prototype/backend/rag_pipeline.py` and the active question flow | Implementation evidence | High | Describe results as matches and keep the developer responsible for interpretation. |
| Showing records and links together may reduce separate searches. | Product flow | Inference | Untested | Compare task time with manual GitHub search. |
| Developers may find useful context faster with this flow. | Product hypothesis | Hypothesis | Untested | Run a timed comparison before claiming time savings. |

## 7. Single Target Product Flow

1. Enter a public GitHub repository URL or `owner/repo`.
2. Import the bounded repository history into Neo4j.
3. Ask a question using distinctive terms from the repository or change.
4. Review matching records and source links, then use Graph Explorer if relationship context is useful.

The assessment should record import success, relevant records found, source validity, time-to-find, irrelevant matches, and whether each source actually addresses the question.
