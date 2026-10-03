# Build Summary

## Theme

AI and Developer Tools — Why The Code Is Like This

## Final Problem Statement

Developers onboarding to or maintaining a public repository may need to search commits, pull requests, and issues to recover the history behind unfamiliar code. Manually connecting those records takes effort, and a related record does not necessarily explain the original intent. This project explores whether importing bounded repository history into a graph and returning source-linked matches can make that context easier to inspect.

## What Changed from Version 1

The initial framing focused on an AI assistant that would explain why code decisions were made, with FastAPI as the target repository. The implemented prototype instead accepts public GitHub repositories and focuses on locating matching history. Its included sample/final datasets use pallets/click. The current retrieval path uses keywords and does not generate an LLM-written rationale.

## What We Built

A web prototype with an Evidence Engine, Graph Explorer, and Documentation page. A user submits a public repository, the backend fetches a bounded set of recent commits, merged pull requests, and issues and imports them into Neo4j. A question is matched against stored record text; the interface displays matching records and source links. The Graph Explorer displays stored graph relationships.

The project does not prove historical intent from a text match. A developer must inspect the original sources. Claims that the prototype saves time or improves understanding still need user testing.

## Tech Stack

- **Frontend:** HTML, CSS, and vanilla JavaScript.
- **Backend:** Python FastAPI and Uvicorn.
- **Repository data:** GitHub REST API.
- **Graph database:** Neo4j with Cypher.
- **Retrieval:** deterministic keyword extraction and match scoring.
- **LLM:** no LLM call in the current runtime question path.

## Evidence Position

- **Verified in the project source:** bounded import limits, Neo4j data flow, keyword-based matching, and source-link presentation.
- **Not established:** retrieval accuracy, time saved, user satisfaction, and whether the returned records explain the original decisions.
- **Still an assumption:** recent public history and keyword matching will surface useful records for representative developer questions.

No test output, comparison study, or stranger-test notes are retained in the supplied project folder, so no testing result is claimed here.

## What We Build Next

1. Run and retain the planned import, retrieval, failure-mode, and source-link checks.
2. Conduct and document the stranger test.
3. Compare the prototype with manual GitHub search using the same questions.
4. Review missed and irrelevant matches before improving retrieval.
5. Consider generated explanations only after adding source-grounding rules and an evaluation set.