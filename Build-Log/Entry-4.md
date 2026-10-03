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
