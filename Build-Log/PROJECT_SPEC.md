# PROJECT_SPEC.md

## What Is This?

Why The Code Is Like This is a web prototype for importing a bounded set of public GitHub history into Neo4j and retrieving matching records for a developer’s question.

## Who Uses It?

Developers, maintainers, and open-source contributors who need to inspect the history of an unfamiliar public repository.

## What Must It Do?

- Accept a public GitHub repository URL or `owner/repo`.
- Fetch a bounded set of commits, merged pull requests, and issues.
- Preserve stable IDs, authors, timestamps, changed-file metadata where available, and original source URLs.
- Import repository entities and relationships into Neo4j.
- Search Commit, PullRequest, and Issue text using question keywords.
- Return matching records and source links.
- Show stored relationships in Graph Explorer.
- Clearly report when no matching records are found.

## What Does It Not Do?

- It does not index private repositories.
- It does not clone or index a repository’s complete history.
- It does not prove historical intent from text matches.
- The current question flow does not generate an LLM-written explanation.
- It does not make engineering decisions or modify repository source code.

## What Data Does It Use?

Public GitHub repository metadata, commits, merged pull requests, issues, changed-file paths where available, authors, timestamps, and source URLs. An optional `GITHUB_TOKEN` can raise GitHub API limits. Neo4j credentials are supplied through environment variables and must not be committed.

## Constraints

The importer uses bounded requests to the GitHub REST API. The FastAPI import endpoint requests up to 20 commits, 10 merged pull requests, and 15 issues, with bounded detail requests. GitHub rate limits and partial history can affect the results. Runtime graph features require a reachable Neo4j database and configured credentials.

## Technology Stack and Reasons

- **Frontend — HTML, CSS, and vanilla JavaScript:** provides the Evidence Engine and Graph Explorer as a lightweight browser interface without requiring a frontend framework.
- **Backend — Python, FastAPI, and Uvicorn:** handles HTTP requests, input validation, GitHub ingestion, and Neo4j-backed retrieval in the project’s Python environment.
- **Repository data — GitHub REST API:** supplies public repository metadata, commits, pull requests, and issues from their original source.
- **Graph store — Neo4j and Cypher:** represents repository entities and their relationships so the application can query and display graph structure.
- **Retrieval — deterministic keyword extraction and match scoring:** makes it possible to find records containing question terms without claiming generated reasoning. This approach is simple to inspect, but can miss relevant records or return noisy matches.
- **LLM — not used by the current runtime question path:** LLM-related packages in the dependency list do not mean the active question flow calls an LLM.

## Definition of Done

A user can enter a public repository, import bounded history, search for distinctive terms in a question, inspect matching records and original source links, and explore stored relationships. The interface reports when no evidence records match. Claims about faster research or recovered intent require user testing.

## What Is Still Unknown?

- Whether users find results faster or more useful than manual GitHub search.
- Whether the bounded history contains enough context for representative questions.
- How often keyword retrieval misses relevant history or returns irrelevant records.
- Whether users understand that a text match is not proof of historical intent.
- Whether the planned test cases and stranger test have been completed and retained.
