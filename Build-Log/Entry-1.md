# Build Log Entry 1 — Define the Problem Statement

## Project

Why The Code Is Like This — an evidence-backed public-repository history explorer

## Team

Anirudh, Manas, Shreya, Chirag, and Anshika

## Theme

AI and Developer Tools

## 1. Problem Statement — Version 1

Developers joining or maintaining a public software repository can read what the current code does but may not know why a design or implementation changed. Relevant context may be distributed across commits, pull requests, issues, and repository files. Searching those sources manually requires the developer to find and connect the relevant records. We want to make recent repository history easier to inspect by collecting it into a graph and returning matching records with their source links.

### Who experiences the problem?

Developers onboarding to a public codebase, open-source contributors, maintainers, and technical leads who need context before changing unfamiliar code.

### When does it occur?

The problem occurs when a developer encounters an unfamiliar module or behavior, needs to modify it, and cannot infer the historical reason from the current source alone.

### What is the cost?

The developer must search GitHub history and manually compare commits, pull requests, and issues. The time and uncertainty of this work have not been measured for this project; reduced search effort remains a hypothesis to test.

### Why is it worth exploring?

If related history and source links are easier to inspect together, a developer may recover useful context with fewer manual searches. A matching historical record is not by itself proof of intent, so the original source still needs human review.

## 2. Intended Build

The prototype accepts a public GitHub repository, fetches a bounded set of recent commits, merged pull requests, and issues, and imports normalized records into Neo4j. A developer can search the graph with a why-question and inspect matching evidence and source links; a separate Graph Explorer displays stored graph relationships.

The current query path uses keyword matching and reports matching records. It does not use an LLM to generate a historical explanation or prove why a change was made.

## 3. Leverage Map

| Task | Classification | Reason |
| --- | --- | --- |
| Fetch a bounded window of public GitHub history | Automation | The backend calls the GitHub API and normalizes records. |
| Preserve IDs, dates, authors, and source URLs | Automation | The ingestion code maps repository records into consistent fields. |
| Store entities and relationships in Neo4j | Automation | The importer creates graph records for retrieval and exploration. |
| Match a question against stored record text | Automation | The current retrieval pipeline extracts keywords and ranks matching records. |
| Format the response and display source cards | Automation | The API and frontend present matching records and links. |
| Decide whether a record explains the historical intent | Agency | Text matches can be related without establishing causation or intent. |
| Decide whether the explanation is trustworthy enough to use | Agency | The developer must inspect original sources and make the engineering decision. |

The current prototype does not perform a runtime AI summarization step. AI assistance belongs to the project workflow unless a future implementation explicitly adds and verifies it.

## 4. Human Decisions

1. **Evidence sufficiency:** decide whether the returned commit, PR, or issue actually supports the question.
2. **Historical intent:** distinguish a related record from a source that explains why the decision was made.
3. **Engineering action:** decide whether to change, preserve, or investigate the implementation further.

## 5. Initial Evidence and Claim List

### Evidence observed in the project

- prototype/backend/main.py accepts a public repository and requests up to 20 commits, 10 merged pull requests, and 15 issues for an import.
- prototype/backend/fetch_github_data.py uses the GitHub REST API and preserves record identifiers and source URLs in normalized data.
- prototype/backend/schema.cypher declares uniqueness constraints for Repository, Commit, PullRequest, Issue, Developer, and File IDs.
- prototype/backend/rag_pipeline.py searches commit, pull-request, and issue text by question keywords and returns matching records.
- prototype/frontend/index.html provides repository import and question input; prototype/frontend/graph.html presents a graph view.
- prototype/backend/data/ contains sample/final JSON files for pallets/click.

### Inference

Connecting repository records in Neo4j may make related history easier to inspect than searching each record type separately. This is a product rationale, not a measured outcome.

### Hypothesis

Developers will find relevant historical records faster when the prototype presents keyword-matched graph evidence with source links.

### Assumptions

- Recent public history contains useful context for at least some questions.
- Keyword matching can surface records worth reviewing.
- Developers will inspect the original sources before treating a match as an explanation.

## 6. Initial Why-Question Examples

- Which recent commits or pull requests mention the behavior I am investigating?
- What issue or pull request is linked to this change?
- What files were changed in matching commits?
- Does the retrieved history contain enough evidence to explain why the change was made?

These are example questions. The current implementation is more likely to retrieve useful results when the question includes distinctive words present in record text.

## 7. Initial Success Criteria

The prototype should allow a developer to import a public repository, search its stored history, inspect matching records and source links, and explore graph relationships. Whether this reduces search time or improves decision understanding remains unverified and needs user testing.