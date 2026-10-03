# Build Log Entry 6 — Prototype, Tests, and Reusable Workflow

## Project Focus

Record the prototype’s documented capabilities, define its test coverage, and distinguish source-code behavior from test results.

## 1. Project Specification

The project specification is in Build-Log/PROJECT_SPEC.md. It describes an evidence explorer for bounded public GitHub history, rather than a zero-hallucination AI answer generator.

## 2. Implemented Product Flow (Source Review)

The current files implement these parts of the flow:

1. The frontend accepts a public repository URL or owner/repo.
2. FastAPI validates the input and calls the GitHub ingestion script.
3. The ingestion script fetches bounded commits, merged PRs, and issues, then the importer writes records to Neo4j.
4. The question endpoint searches Commit, PullRequest, and Issue text by extracted keywords and returns matching records with source metadata.
5. Evidence Engine renders result cards; Graph Explorer requests and displays stored graph relationships.

The response builder explicitly says matching records do not prove why a change was made. The current rag_pipeline.py has no LLM call. Although LLM-related packages appear in requirements.txt, their presence in the dependency list is not evidence that the runtime query path uses them.

## 3. Test Plan and Evidence Status

The supplied project folder does not include a test suite, test output, screenshots, or a completed test-results record. The following cases should be run and recorded; they are not reported here as passed:

- A valid repository import with expected counts and source URLs.
- A why-question whose distinctive words appear in an imported record.
- A question with no matching record.
- A question about an entity absent from the imported window.
- Empty and very long question inputs.
- Invalid repository URL or malformed owner/repo.
- GitHub rate limit, missing repository, network failure, or ingestion timeout.
- Neo4j unavailable during import, query, or graph loading.
- Open a returned source link and check that it is the original GitHub record.
- Have two people unfamiliar with the project complete the flow without coaching.

The code defines some failure responses, including invalid-input errors, GitHub import errors, database errors, and a timeout. This describes implemented error handling; it does not establish that the cases have been exercised successfully.

## 4. Stranger-Test Record

An earlier version of this entry reported two peer testers and specific feedback, but no interview notes, screenshots, or test artifacts are present in the supplied project folder. The reported findings therefore remain unverified. The current prototype/frontend/app.js contains clickable GitHub source links that open in a new tab; it does not contain the earlier entry’s claimed quick-select prompt pills. Do not treat that earlier claim as an implemented feature or verified test result.

## 5. Important Product Limitations

- Only public GitHub repositories are accepted by the repository import endpoint.
- Import is bounded; it does not clone or index the full repository history.
- Retrieval uses keyword overlap, so relevant records can be missed and irrelevant records can match.
- The current answer reports matching records; it does not generate an LLM explanation of historical intent.
- A person must inspect source links and judge whether a record supports a conclusion.
- Neo4j-backed behavior requires configured credentials and a reachable database.

## 6. Reusable Workflow

**Input:** Public repository URL and a developer question.

**Process:** Fetch a bounded set of commits, merged pull requests, and issues; normalize identifiers and source links; import records into Neo4j; search record text for question keywords.

**Verification:** Compare returned IDs and URLs with GitHub, open the original sources, and decide whether they actually address the question. Record missing evidence and false matches.

**Output:** Matching records, source links, and graph relationships, plus a clear no-match response when no records match. The output is not a verified explanation unless a person confirms that the original evidence supports it.

## 7. Next Build Priorities

1. Run and retain the test matrix above.
2. Conduct and document the stranger test.
3. Measure the prototype against manual GitHub search.
4. Improve retrieval only after reviewing false positives and missed records.
5. Consider an LLM explanation only with source-grounding rules and an evaluation set.