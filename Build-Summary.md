# Build Summary

## Theme

AI and Developer Tools — Why The Code Is Like This

## Final Problem Statement

Developers working in unfamiliar public repositories may need to search commits, pull requests, and issues to recover the history behind code. Connecting those records takes effort, and a related record does not necessarily explain the original intent. This project explores whether a graph of repository history can make relevant, source-linked records easier to inspect.

## What Changed from Version 1

The initial concept proposed an AI assistant for explaining FastAPI design decisions. The implemented prototype accepts public GitHub repositories and locates matching history using keywords; it does not generate an LLM-written rationale. The included normalized dataset is for `pallets/click`.

## What We Built

A web prototype with an Evidence Engine, Graph Explorer, and Documentation page. It imports up to 20 commits, 10 merged pull requests, and 15 issues into Neo4j, then displays keyword-matched records and source links. Developers inspect the sources themselves; a text match does not prove historical intent.

## Tech Stack

- **Frontend — HTML, CSS, and vanilla JavaScript:** a lightweight browser interface without a frontend framework.
- **Backend — Python, FastAPI, and Uvicorn:** handles API requests, validation, ingestion, and retrieval in the project’s Python stack.
- **Repository data — GitHub REST API:** retrieves public history from its original source.
- **Graph database — Neo4j and Cypher:** stores entities and relationships for graph queries and exploration.
- **Retrieval — keyword extraction and match scoring:** provides inspectable deterministic matching, though it can miss relevant records or return noise. No LLM is called by the runtime question path.

## Evidence Position

- **Confirmed in source:** bounded import, Neo4j data flow, keyword matching, and source-link presentation.
- **Manual demonstration:** `encode/httpx` imported with 36 commits, 10 merged pull requests, and 15 issues. The chardet 6.0 query returned 10 records, including related records and noise; one linked commit was opened and verified. A 4.56-second query time was recorded in one run.
- **Exploratory stranger test:** two computer science students completed the flow. One found the graph useful but thought it covered all repository history; the other reported relevant and irrelevant results. This small test does not establish general usability or retrieval accuracy.
- **Opportunity scenario (assumption-based, not validated):** GitHub reported 180M+ developers in 2025. If 1% fit this use case and an initial 0.1% of that segment were reachable/adoptable, the scenario is 1.8M potential-fit developers and 1,800 early users. These rates are assumptions, not measured demand; no revenue estimate is claimed. [Source](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- **Still unproven:** faster search than GitHub, systematic retrieval quality, broad user satisfaction, and willingness to pay.

## What We Would Build Next

Run broader user and retrieval evaluations, including a comparison with manual GitHub search. Improving retrieval is worth pursuing if it repeatedly surfaces relevant sources and helps developers find them faster without reducing source relevance. Consider generated explanations only after source-grounding rules and an evaluation set are in place.