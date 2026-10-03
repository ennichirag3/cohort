# Build Log Entry 4 — Unwind the Idea

## Project

Why The Code Is Like This — an evidence-backed public-repository history explorer

## 1. Five Whys

### Why 1: Why can developers struggle with unfamiliar code?

The current source shows what the code does, but it may not show the reasoning behind a design or implementation decision.

### Why 2: Why might the reason be missing from the current source?

The discussion and record of a change may live in commits, pull requests, issues, or other repository material.

### Why 3: Why is manual search difficult?

A developer must identify useful terms and then connect records across different GitHub views.

### Why 4: Why would a connected view help?

Repository records can carry links between commits, pull requests, issues, files, and authors. A graph can make those relationships available to query and explore.

### Why 5: Why does this matter?

A developer deciding whether to change unfamiliar code benefits from inspecting its history, but must still judge whether that history actually explains the decision.

### Research Question

Can a bounded repository-history graph make it easier to locate relevant source records for a code question, while keeping the limits of those records clear?

## 2. Reframes

### Reframe 1 — From explaining code to locating historical context

**Original framing:** Developers need an AI system to explain unfamiliar code.

**Reframed problem:** Developers need a practical way to locate and inspect historical records related to unfamiliar code.

### Reframe 2 — From generated rationale to source-backed records

**Original framing:** An AI should tell the developer why a code decision was made.

**Reframed problem:** The prototype should surface related commits, pull requests, and issues with their source links; the developer decides whether they explain the reason.

This reframe matches the current implementation: rag_pipeline.py performs keyword matching and formats evidence records. It does not call an LLM to generate a rationale.

## 3. Critique from Different Perspectives

### Developer perspective

**Question:** Why not use GitHub search, commit history, or git blame?

**Concern:** Those tools are useful substitutes. The prototype only has value if its bounded import and connected view make relevant history easier to locate and inspect.

**Implication:** Compare the prototype with manual search on the same repository questions before claiming a time-saving benefit.

### Technical perspective

**Question:** Does a record that matches a question explain the decision?

**Concern:** A keyword match may be related but not causal or explanatory.

**Implication:** Preserve source URLs and IDs, describe a match as evidence to inspect, and avoid claiming that a match proves intent.

## 4. Top Three Assumptions and 48-Hour Tests

These are proposed tests, not completed research findings.

### Assumption 1 — Developers need historical context often enough to use the tool

**Impact if false:** The product may solve an infrequent problem.

**48-hour test:** Ask 2–3 developers to describe a recent instance where they searched history to understand unfamiliar code. Record the repository, sources searched, time spent, and confidence in what they found. The project folder contains no interview notes, so no result is claimed here.

### Assumption 2 — A bounded public-history import contains useful records

**Impact if false:** The selected window may omit the historical item needed to answer a question.

**48-hour test:** Prepare representative questions for a public repository, run them against the imported data, and record whether a relevant commit, PR, or issue is present. Compare misses with a wider/manual GitHub search.

### Assumption 3 — Keyword matching can retrieve records that developers consider useful

**Impact if false:** Search results may be incomplete or noisy.

**48-hour test:** Have reviewers try the same questions using the prototype and manual GitHub search. Record relevant records found, irrelevant matches, source-link correctness, and time. No comparison results are retained in the supplied project files.

## 5. Version 2 Problem Statement

Developers onboarding to or maintaining a public repository can understand what unfamiliar code currently does but may need to search commits, pull requests, and issues to recover its history. Manually connecting those records takes effort, and a related record does not necessarily explain the original intent. The prototype imports a bounded set of public repository history into Neo4j and presents keyword-matched records with source links so developers can inspect the available context. Whether this flow reduces search time or improves decisions remains to be tested.

## 6. Evidence Position

- **Evidence:** Facts visible in repository records or project source code, such as IDs, dates, changed files, descriptions, and URLs.
- **Inference:** A conclusion drawn from one or more records.
- **Hypothesis:** A proposed user or product outcome that has not been measured.
- **Assumption:** An unverified condition the product depends on.

The product should not present an inference or hypothesis as a documented historical fact.

## 7. Product Principle

> Locate the evidence first; let the developer judge what it means.

The current prototype returns matching records and links. Users should inspect original sources before treating them as an explanation.

## 8. Current Product Flow

Public GitHub repository → bounded ingestion of commits, merged PRs, and issues → normalized records imported into Neo4j → developer enters a question → keyword matching returns repository records → developer reviews record details and original source links.

The Graph Explorer separately displays stored nodes and relationships. If no matching records are found, the backend returns a no-match response.

## 9. Initial Scope Decision

The prototype accepts a public GitHub repository URL or owner/repo value. The backend requests up to 20 commits, 10 merged pull requests, and 15 issues, with bounded commit-detail and linked-issue requests. The checked-in sample/final data files use pallets/click. This is a bounded history explorer, not a complete repository index.

## 10. Activity 4 Conclusion

The project is about making related repository history easier to inspect, not automatically discovering or proving historical intent. The first prototype prioritizes:

**Bounded ingestion → graph relationships → keyword-matched records → source review**

A future generated explanation would need separate evidence-grounding and evaluation work before it could be described as reliable.