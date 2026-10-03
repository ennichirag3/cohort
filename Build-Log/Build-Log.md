# Build Log Entry 1 — Define the Problem

## Project

Why The Code Is Like This

## Theme

AI and Developer Tools

## Problem Statement

Developers working in an unfamiliar public repository may need to understand the history behind a code behavior before changing it. Relevant context can be spread across commits, pull requests, and issues, making it difficult to find and inspect the records together. This project explores whether importing a bounded set of repository history into a graph and showing source-linked matches can make that context easier to examine.

## Intended Build

Build a web prototype where a developer can:

1. Enter a public GitHub repository.
2. Import a bounded set of its recent commits, merged pull requests, and issues into Neo4j.
3. Ask a question using terms related to the code or change.
4. Review matching records and open their original GitHub sources.
5. Explore stored relationships in a graph view.

The prototype is intended to help locate evidence. It is not intended to prove historical intent or make engineering decisions.

## How the Problem Changed

The initial framing was an AI assistant that would explain why code decisions were made. The build narrowed that goal to finding and displaying matching repository history, because the current prototype uses keyword matching and does not generate an LLM explanation.

## Leverage Map

| Work | Who or what does it | Human responsibility |
| --- | --- | --- |
| Fetch bounded public GitHub history | Software | Choose the repository and decide whether the fetched scope is useful. |
| Normalize records and preserve IDs and source URLs | Software | Review the mapping and verify records against GitHub. |
| Import entities and relationships into Neo4j | Software | Review whether the graph structure represents the data correctly. |
| Match question keywords against stored records | Software | Judge whether the results are relevant or incomplete. |
| Display records, source links, and graph relationships | Software | Open original sources and interpret them. |
| Decide whether a record explains a code decision | Human | Assess whether the source supports that conclusion. |
| Decide what engineering action to take | Human | Make and review the code or architecture decision. |

## Early Assumptions

- Useful context for some questions appears in commits, merged pull requests, or issues.
- A bounded recent-history import can retrieve at least some useful records.
- Showing source links alongside matches helps a developer inspect the original evidence.
- A keyword match may be incomplete or irrelevant, so the developer must evaluate the source.

---

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

---

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

---

# Build Log Entry 4 — Unwind the Idea

## Project Focus

Test the original “AI explains why” framing against the prototype’s actual capabilities, identify objections, and state the assumptions that need testing.

## 1. Unwind: Five Whys

1. **Why did we consider building an assistant that explains code decisions?** Developers may encounter unfamiliar code and want to know why it works that way.

2. **Why is that context difficult to find?** Relevant history can be distributed across commits, pull requests, and issues.

3. **Why combine those records in one place?** A graph can represent entities and relationships, while source links let a developer inspect the original records.

4. **Why import only a bounded amount of history?** The prototype uses bounded GitHub requests and does not clone or index a repository’s complete history.

5. **Why does the current result not count as an explanation?** Retrieval is based on keyword matches. A matching record may help locate evidence, but it does not prove intent or causation.

## 2. Reframes

- **Reframe 1:** From “AI tells a developer why code is like this” to “a developer can find and inspect related repository history.”
- **Reframe 2:** From “understand the whole repository” to “search a bounded set of public commits, merged pull requests, and issues for a specific question.”

## 3. Critic Objections

| Critic | Objection | What the project should do |
| --- | --- | --- |
| Repository maintainer | Recent history may omit the older record that explains a design decision. | State the import boundary and test questions whose evidence may fall outside it. |
| Developer using the tool | Keyword matching can return irrelevant records or miss records that use different words. | Measure false matches and missed records against a known question set. |
| Evidence reviewer | A related issue or commit does not necessarily explain the original intent. | Keep source links visible and avoid presenting a match as proof. |
| Operator | GitHub rate limits, network failures, or unavailable Neo4j may prevent import or retrieval. | Record failure behavior and test it rather than assuming the services are always available. |

## 4. Three Ranked Assumptions and 48-Hour Tests

### Rank 1 — The bounded import contains useful records

**Why this ranks first:** If the relevant records are not imported, retrieval cannot find them.

**48-hour test:** Select three public repositories and five specific questions per repository. For each question, identify a relevant record manually in GitHub, import the bounded history, and check whether that record is present.

**Measure:** Number of known relevant records present in the import.

**Evidence that supports the assumption:** The bounded import includes relevant records for a useful portion of the questions.

### Rank 2 — Keyword matching surfaces the relevant records

**Why this ranks second:** Records can be present in Neo4j but still fail to appear in results.

**48-hour test:** Run the same 15 questions through the prototype. Have a reviewer compare the top results with the records found manually.

**Measure:** Relevant records in the top results, irrelevant results, and questions with no relevant result.

**Evidence that supports the assumption:** Relevant records appear consistently near the top without an unacceptable amount of unrelated noise.

### Rank 3 — Developers benefit from source-linked results

**Why this ranks third:** Even accurate retrieval may not improve the developer’s task enough to justify using another tool.

**48-hour test:** Ask two or more people unfamiliar with the project to answer repository-history questions using the prototype, then using manual GitHub search, or in the reverse order.

**Measure:** Completion time, source relevance, errors, and whether participants can explain the evidence limits.

**Evidence that supports the assumption:** Participants can find relevant source records more quickly without losing confidence in source relevance.

No results from these proposed tests are claimed in this entry.

## 5. Problem Statement V2

Developers investigating an unfamiliar public repository may need to locate history relevant to a code behavior before making a change. The relevant context can be spread across commits, merged pull requests, and issues. This prototype imports a bounded set of those records into Neo4j and returns keyword-matched records with source links, so developers can inspect the evidence themselves. It does not establish historical intent from text matches.

## 6. Evidence Principles

- A matching record is a lead to inspect, not proof of intent.
- Source IDs and URLs should be preserved where available.
- Missing evidence should be reported rather than guessed.
- User benefit and retrieval quality need evaluation before they can be claimed.

---

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

**Method: top-down, illustrative scenario (not validated demand).** GitHub reported more than 180 million developers on its platform in its 2025 Octoverse report ([source](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)). This is a broad ecosystem ceiling, not the number of people who need this product.

For a first-pass planning estimate, assume **1%** of those developers regularly investigate unfamiliar public repositories and fit the target use case: 180,000,000 × 1% = **1,800,000 potential-fit developers**. Assume an initial reachable/adoptable share of **0.1%** of that group: 1,800,000 × 0.1% = **1,800 possible early users**. Both percentages are assumptions with no market survey behind them; treat the result as a scenario for planning, not a measured market size or forecast. No revenue estimate is made because willingness to pay and pricing have not been tested.

Early product evidence is limited to two computer science students who tried the flow using `fastapi/fastapi` and `encode/httpx`. Both completed it; feedback included relevant and irrelevant results and a misunderstanding about the history window. This pilot does not validate the market assumptions or establish product effectiveness.

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

---

# Build Log Entry 6 — Prototype, Tests, and Reusable Workflow

## Project Focus

Record the prototype’s documented capabilities, observed checks, and remaining unknowns.

## 1. Project Specification

The full project specification is included in this compiled Build Log under the heading `PROJECT_SPEC.md`.

# PROJECT_SPEC.md

#### What Is This?

Why The Code Is Like This is a web prototype for importing a bounded set of public GitHub history into Neo4j and retrieving matching records for a developer’s question.

#### Who Uses It?

Developers, maintainers, and open-source contributors who need to inspect the history of an unfamiliar public repository.

#### What Must It Do?

- Accept a public GitHub repository URL or `owner/repo`.
- Fetch a bounded set of commits, merged pull requests, and issues.
- Preserve stable IDs, authors, timestamps, changed-file metadata where available, and original source URLs.
- Import repository entities and relationships into Neo4j.
- Search Commit, PullRequest, and Issue text using question keywords.
- Return matching records and source links.
- Show stored relationships in Graph Explorer.
- Clearly report when no matching records are found.

#### What Does It Not Do?

- It does not index private repositories.
- It does not clone or index a repository’s complete history.
- It does not prove historical intent from text matches.
- The current question flow does not generate an LLM-written explanation.
- It does not make engineering decisions or modify repository source code.

#### What Data Does It Use?

Public GitHub repository metadata, commits, merged pull requests, issues, changed-file paths where available, authors, timestamps, and source URLs. An optional `GITHUB_TOKEN` can raise GitHub API limits. Neo4j credentials are supplied through environment variables and must not be committed.

#### Constraints

The importer uses bounded requests to the GitHub REST API. The FastAPI import endpoint requests up to 20 commits, 10 merged pull requests, and 15 issues, with bounded detail requests. GitHub rate limits and partial history can affect the results. Runtime graph features require a reachable Neo4j database and configured credentials.

#### Technology Stack and Reasons

- **Frontend — HTML, CSS, and vanilla JavaScript:** provides the Evidence Engine and Graph Explorer as a lightweight browser interface without requiring a frontend framework.
- **Backend — Python, FastAPI, and Uvicorn:** handles HTTP requests, input validation, GitHub ingestion, and Neo4j-backed retrieval in the project’s Python environment.
- **Repository data — GitHub REST API:** supplies public repository metadata, commits, pull requests, and issues from their original source.
- **Graph store — Neo4j and Cypher:** represents repository entities and their relationships so the application can query and display graph structure.
- **Retrieval — deterministic keyword extraction and match scoring:** makes it possible to find records containing question terms without claiming generated reasoning. This approach is simple to inspect, but can miss relevant records or return noisy matches.
- **LLM — not used by the current runtime question path:** LLM-related packages in the dependency list do not mean the active question flow calls an LLM.

#### Definition of Done

A user can enter a public repository, import bounded history, search for distinctive terms in a question, inspect matching records and original source links, and explore stored relationships. The interface reports when no evidence records match. Claims about faster research or recovered intent require user testing.

#### What Is Still Unknown?

- Whether users find results faster or more useful than manual GitHub search.
- Whether the bounded history contains enough context for representative questions.
- How often keyword retrieval misses relevant history or returns irrelevant records.
- Whether users understand that a text match is not proof of historical intent.
- The remaining technical test cases and comparison with manual GitHub search are unverified. Two exploratory stranger-test sessions are recorded in this Build Log, but they do not establish general usability.

## 2. Implemented Product Flow — Source Review

1. The frontend accepts a public repository URL or `owner/repo`.
2. FastAPI validates the repository input and starts the GitHub ingestion flow.
3. The ingestion code fetches bounded commits, merged pull requests, and issues, then imports normalized records into Neo4j.
4. The question endpoint searches Commit, PullRequest, and Issue text using extracted keywords and returns matching records with source metadata.
5. Evidence Engine displays result cards and source links. Graph Explorer requests and displays stored graph relationships.

The active question flow returns matching records. It does not call an LLM to generate an explanation. A keyword match does not establish historical intent.

## 3. Manual Test Notes

### Manual demonstration: encode/httpx

- **Date:** 2026-10-03.
- **Repository:** `encode/httpx`.
- **Question entered:** “What changed to support chardet 6.0?”
- **Import result:** Import succeeded. Added 36 commits, 10 merged pull requests, and 15 issues.
- **Results observed:** The app reported 10 matching records. Results included a commit and pull request titled “Adapt test_response_decode_text_using_autodetect for chardet 6.0,” along with records that did not appear clearly related.
- **Source verification:** Opened and checked the linked commit: https://github.com/encode/httpx/commit/b5addb64f0161ff6bfe94c124ef76f6a1fba5254. The commit updates a test assertion to accept `ISO-8859-1` or `WINDOWS-1252`.
- **Time taken:** 4.56 seconds from submitting the query to seeing the result output. This is one observed run, not a performance comparison.
- **Conclusion:** This demonstration returned some relevant history and some unrelated results. It does not establish overall retrieval accuracy or prove that the prototype is faster than manual GitHub search.

![Figure 1 — Successful import and query](<figure 1.jpeg>)

*Figure 1. The repository import succeeded and shows the question used.*

![Figure 2 — Retrieved evidence results](<figure 2.jpeg>)

*Figure 2. The app returned 10 records, including relevant and unrelated results.*

![Figure 3 — Verified GitHub commit](<figure 3.jpeg>)

*Figure 3. The linked commit was opened and checked on GitHub.*

## 4. Stranger-Test Notes

Two computer science students unfamiliar with the project tried the flow on 2026-10-03. These were exploratory sessions, not a controlled usability study.

### Participant 1

- **Repository and query:** `fastapi/fastapi`; “test”.
- **Completed import and retrieval:** Yes.
- **Relevant results found:** Yes.
- **Opened and checked source links:** Yes.
- **Time taken:** 1 minute 2 seconds.
- **Where they got stuck:** None observed.
- **Understanding of the tool:** The participant thought the tool could read all commits, pull requests, and issues. This indicates the bounded import scope needs to be made clearer.
- **Feedback:** The graph made the repository easier to visualize.

### Participant 2

- **Repository and query:** `encode/httpx`; “What changed to support chardet 6.0?”
- **Completed import and retrieval:** Yes.
- **Relevant results found:** Yes.
- **Opened and checked source links:** Not recorded.
- **Time taken:** 1 minute 32 seconds.
- **Where they got stuck:** None observed.
- **Understanding of the tool:** The participant understood that it imports repository history, shows matching records, and links to GitHub sources.
- **Feedback:** The participant found relevant results, but also some irrelevant results for natural-language queries.

These two observations are exploratory. They do not establish general user satisfaction, retrieval accuracy, or faster performance than manual GitHub search.

## 5. Test Plan and Status

| Check | Status | Observation |
| --- | --- | --- |
| Import a valid public repository | **Tested once** | `encode/httpx` imported successfully: 36 commits, 10 merged pull requests, and 15 issues. |
| Ask a question using distinctive words from an imported record | **Tested once** | “What changed to support chardet 6.0?” returned 10 records, including related commit and pull-request records, plus unrelated results. |
| Compare returned records and links with GitHub | **Partially tested** | Opened and verified one commit source link. The full result set was not checked. |
| Ask a question with no matching record | **Not tested** | No result recorded. |
| Ask about an entity outside the imported history window | **Not tested** | No result recorded. |
| Try empty and unusually long questions | **Not tested** | No result recorded. |
| Try an invalid repository URL or malformed `owner/repo` | **Not tested** | No result recorded. |
| Check GitHub rate limits, missing repository, network failure, or ingestion timeout | **Not tested** | No result recorded. |
| Check behavior when Neo4j is unavailable | **Not tested** | No result recorded. |
| Conduct and document the stranger test | **Conducted once (2 participants)** | Exploratory observations are recorded in Section 4; they are not a general usability evaluation. |

The encode/httpx run was one manual technical demonstration. Two exploratory participant sessions are also recorded above. Most technical failure cases remain untested.

## 6. Important Product Limitations

- The repository import endpoint accepts public GitHub repositories.
- Import is bounded; it does not clone or index the complete repository history.
- Retrieval uses keyword matching, so relevant records can be missed and irrelevant records can match.
- The current question path returns matching records; it does not generate an LLM explanation of historical intent.
- A person must inspect source links and judge whether a record supports a conclusion.
- Neo4j-backed features require configured credentials and an available database.

## 7. Reusable Workflow

**Input:** A public repository and a developer question.

**Process:** Fetch bounded commits, merged pull requests, and issues; normalize identifiers and source links; import records into Neo4j; search record text for question keywords.

**Verification:** Compare returned IDs and URLs with GitHub, open original sources, and judge whether they address the question. Record missing evidence and false matches.

**Output:** Matching records, source links, and graph relationships, or a no-match response. The output is not a verified explanation unless a person confirms that the original evidence supports it.

## 8. Next Build Priorities

1. Run and retain the remaining technical checks in Section 5.
2. Repeat the exploratory test with more participants and make the bounded import scope clearer.
3. Compare the prototype with manual GitHub search using the same questions and assess relevance as well as time.
4. Review false positives and missed records before changing retrieval.
5. Consider generated explanations only after adding source-grounding rules and an evaluation set.
