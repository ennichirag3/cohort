# Build Log Entry 1 — Define the Problem

## Project

Why The Code Is Like This

## Theme

AI and Developer Tools

## Problem Statement

Developers working in an unfamiliar public repository may need to understand the history behind a code behavior before changing it. Relevant context can be spread across commits, pull requests, and issues, making it difficult to find and inspect the records together. This project explores whether importing a bounded set of repository history into a graph and showing source-linked matches can make that context easier to examine.

## Intended Build

Build a web prototype where a developer can:

1. Enter a public GitHub repository.
2. Import a bounded set of its recent commits, merged pull requests, and issues into Neo4j.
3. Ask a question using terms related to the code or change.
4. Review matching records and open their original GitHub sources.
5. Explore stored relationships in a graph view.

The prototype is intended to help locate evidence. It is not intended to prove historical intent or make engineering decisions.

## How the Problem Changed

The initial framing was an AI assistant that would explain why code decisions were made. The build narrowed that goal to finding and displaying matching repository history, because the current prototype uses keyword matching and does not generate an LLM explanation.

## Leverage Map

| Work | Who or what does it | Human responsibility |
| --- | --- | --- |
| Fetch bounded public GitHub history | Software | Choose the repository and decide whether the fetched scope is useful. |
| Normalize records and preserve IDs and source URLs | Software | Review the mapping and verify records against GitHub. |
| Import entities and relationships into Neo4j | Software | Review whether the graph structure represents the data correctly. |
| Match question keywords against stored records | Software | Judge whether the results are relevant or incomplete. |
| Display records, source links, and graph relationships | Software | Open original sources and interpret them. |
| Decide whether a record explains a code decision | Human | Assess whether the source supports that conclusion. |
| Decide what engineering action to take | Human | Make and review the code or architecture decision. |

## Early Assumptions

- Useful context for some questions appears in commits, merged pull requests, or issues.
- A bounded recent-history import can retrieve at least some useful records.
- Showing source links alongside matches helps a developer inspect the original evidence.
- A keyword match may be incomplete or irrelevant, so the developer must evaluate the source.
