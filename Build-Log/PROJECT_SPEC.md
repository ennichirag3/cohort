# PROJECT_SPEC.md

## What is this?

Why The Code Is Like This is a web prototype for importing a bounded set of public GitHub history into Neo4j and retrieving matching records for a developer question.

## Who uses it?

Developers, maintainers, and open-source contributors who need to inspect the history of an unfamiliar public repository.

## What must it do?

- Accept a public GitHub repository URL or owner/repo.
- Fetch a bounded set of recent commits, merged pull requests, and issues.
- Preserve stable IDs, authors, timestamps, changed-file metadata where available, and original source URLs.
- Import repository entities and relationships into Neo4j.
- Search Commit, PullRequest, and Issue text using question keywords.
- Return matching records and source links, and show stored relationships in Graph Explorer.
- Clearly report when no matching records are found.

## What does it not do?

- It does not index private repositories.
- It does not clone or index a repository’s complete history.
- It does not prove historical intent from text matches.
- The current rag_pipeline.py does not generate an LLM-written explanation.
- It does not make engineering decisions or modify repository source code.

## What data does it use?

Public GitHub repository metadata, commits, merged pull requests, issues, commit file paths for a bounded subset, authors, timestamps, and source URLs. An optional GITHUB_TOKEN may be used to raise GitHub API limits. Neo4j credentials are provided through environment variables and should not be committed.

## Constraints

The importer uses bounded requests to the GitHub REST API. The FastAPI import endpoint requests up to 20 commits, 10 merged pull requests, and 15 issues, with bounded detail requests. Runtime graph features require a reachable Neo4j database and configured credentials. GitHub rate limits and missing/partial history may affect results.

## Technology Stack

- **Frontend:** HTML, CSS, and vanilla JavaScript.
- **Backend:** Python FastAPI and Uvicorn.
- **Repository data:** GitHub REST API.
- **Graph store:** Neo4j with Cypher queries.
- **Retrieval:** deterministic keyword extraction, text matching, and match scoring in rag_pipeline.py.
- **LLM:** none in the current runtime question path.

## Definition of Done

A user can enter a public repository, import the bounded history, search for distinctive terms in a question, inspect matching records and original source links, and explore stored relationships. The interface reports no matches when no evidence records match. Any claim about faster research or recovered intent still requires user testing.

## What is still unknown?

- Whether users find the results faster or more useful than manual GitHub search.
- Whether the bounded window contains enough context for representative questions.
- How often keyword retrieval misses relevant history or returns irrelevant records.
- Whether users understand that a text match is not proof of historical intent.
- Whether the existing test and stranger-test claims can be supported by retained notes or screenshots.