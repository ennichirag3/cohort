# Build Summary

## Theme

AI and Developer Tools — Why The Code Is Like This

## Final Problem Statement

Developers working in unfamiliar public repositories may need to search commits, pull requests, and issues to recover the history behind code. Connecting those records takes effort, and a related record does not necessarily explain the original intent. This project explores whether a graph of repository history can make relevant, source-linked records easier to inspect.

## What Changed from Version 1

The initial concept proposed an AI assistant for explaining FastAPI design decisions. The implemented prototype accepts public GitHub repositories and focuses on locating matching history. Its included sample data is for pallets/click. The current retrieval path uses keywords; it does not generate an LLM-written rationale.

## What We Built

A web prototype with an Evidence Engine, Graph Explorer, and Documentation page. It imports up to 20 commits, 10 merged pull requests, and 15 issues into Neo4j. A question is matched against stored record text, and the frontend presents matching records and source links. The Graph Explorer displays stored relationships. Developers must inspect the original sources; a text match does not prove historical intent.

## Tech Stack

- **Frontend:** HTML, CSS, and vanilla JavaScript.
- **Backend:** Python FastAPI and Uvicorn.
- **Repository data:** GitHub REST API.
- **Graph database:** Neo4j with Cypher.
- **Retrieval:** keyword extraction and match scoring; no LLM call in the runtime question path.

## Evidence Position

- **Confirmed in source:** bounded import, Neo4j data flow, keyword matching, and source-link presentation.
- **Not measured:** retrieval accuracy, time saved, user satisfaction, or whether results explain the original decisions.
- **Still an assumption:** recent public history and keyword matching will surface useful records for representative questions.

One manual demonstration using `encode/httpx` and a question about the `chardet` 6.0 change surfaced a related commit and pull request, along with noisy results. Exact import counts, task timing, and a complete source-link audit were not retained. No systematic evaluation or stranger-test record is available.

## What We Build Next

1. Run and record import, retrieval, failure-mode, and source-link checks.
2. Conduct the stranger test and compare the prototype with manual GitHub search.
3. Review missed and irrelevant matches before considering an evidence-grounded LLM explanation.
