# Build Log Entry 6 — Prototype, Tests, and Reusable Workflow

## Project Focus

Record the prototype’s documented capabilities, the checks observed so far, and what remains untested.

## 1. Project Specification

The project specification is in `Build-Log/PROJECT_SPEC.md`. It describes a bounded public GitHub history evidence explorer. It does not describe a zero-hallucination answer generator.

## 2. Implemented Product Flow — Source Review

1. The frontend accepts a public repository URL or `owner/repo`.
2. FastAPI validates the repository input and starts the GitHub ingestion flow.
3. The ingestion code fetches bounded commits, merged pull requests, and issues, then imports normalized records into Neo4j.
4. The question endpoint searches Commit, PullRequest, and Issue text using extracted keywords and returns matching records with source metadata.
5. Evidence Engine displays the result cards and source links. Graph Explorer requests and displays stored graph relationships.

The active question flow returns matching records. It does not call an LLM to generate an explanation. A keyword match does not establish historical intent.

## 3. Manual Test Notes

### Manual demonstration: encode/httpx

- **Date:** 2026-10-03.
- **Repository:** `encode/httpx`.
- **Question entered:** “What changed to support chardet 6.0?”
- **Import result:** Import succeeded. Added 36 commits, 10 merged pull requests, and 15 issues.
- **Results observed:** The results included records about adapting to `chardet` 6.0, along with some records that did not appear clearly related.
- **Source links:** https://github.com/encode/httpx/commit/b5addb64f0161ff6bfe94c124ef76f6a1fba5254 The original GitHub record was opened and checked.
- **Time taken:** 4.56 seconds for [the query to return results / the import to complete — choose the one you timed].
- **Conclusion:** This was one manual demonstration. It shows that the prototype returned some relevant history, but also unrelated results. It does not establish overall retrieval accuracy or prove that the prototype is faster than manual GitHub search.

Figure 1 — Successful import and query
![alt text](<figure 1.jpeg>)
Figure 2 — Retrieved results, including relevant and unrelated records
![alt text](<figure 2.jpeg>)
Figure 3 — GitHub commit opened and verified
![alt text](<figure 3.jpeg>)

## 4. Stranger-Test Notes

No completed stranger-test record is available in the supplied project materials. No participant feedback or completion results are claimed.

To complete this test, ask at least two people unfamiliar with the project to use the flow without coaching. Record the repository and question, whether they completed import and retrieval, where they got stuck, whether results seemed relevant, whether they opened source links, and what they understood the tool could and could not conclude.

## 5. Test Plan — Not Yet Reported as Passed

- Import a valid public repository and compare returned records and source URLs with GitHub.
- Ask a question whose distinctive words appear in an imported record.
- Ask a question with no matching record.
- Ask about an entity outside the imported window.
- Try empty and unusually long questions.
- Try an invalid repository URL or malformed `owner/repo`.
- Exercise GitHub rate limits, a missing repository, network failure, or ingestion timeout.
- Check behavior when Neo4j is unavailable during import, question retrieval, or graph loading.
- Open returned source links and verify they lead to the original GitHub records.
- Conduct and document the stranger test.

The code includes some error responses, but this list describes planned checks; it is not a record that each case passed.

## 6. Important Product Limitations

- The repository import endpoint accepts public GitHub repositories.
- Import is bounded; it does not clone or index the complete repository history.
- Retrieval uses keyword matching, so relevant records can be missed and irrelevant records can match.
- The current question path returns matching records; it does not generate an LLM explanation of historical intent.
- A person must inspect the source links and judge whether a record supports a conclusion.
- Neo4j-backed features require configured credentials and an available database.

## 7. Reusable Workflow

**Input:** A public repository and a developer question.

**Process:** Fetch bounded commits, merged pull requests, and issues; normalize identifiers and source links; import records into Neo4j; search record text for question keywords.

**Verification:** Compare returned IDs and URLs with GitHub, open original sources, and judge whether they address the question. Record missing evidence and false matches.

**Output:** Matching records, source links, and graph relationships, or a no-match response. The output is not a verified explanation unless a person confirms that the original evidence supports it.

## 8. Next Build Priorities

1. Run and retain the test plan above.
2. Conduct and document the stranger test.
3. Compare the prototype with manual GitHub search using the same questions.
4. Review false positives and missed records before changing retrieval.
5. Consider generated explanations only after adding source-grounding rules and an evaluation set.
