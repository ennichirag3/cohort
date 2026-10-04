# Why The Code Is Like This

**A source-linked explorer for the history behind public GitHub repositories.** Import a bounded set of commits, merged pull requests, and issues into Neo4j, ask a question, and inspect matching records and their original sources.

[Open the hosted app](https://cohort-do0y.onrender.com) · [Read the project guide](PROJECT_GUIDE.md) · [Read the build summary](Build-Summary.md) · [Read the build log](Build-Log/Build-Log.md)

## What the prototype does

1. Accepts a public GitHub repository URL or `owner/repo`.
2. Imports a bounded set of recent commits, merged pull requests, and issues into Neo4j.
3. Searches the imported text for keywords from a developer’s question.
4. Shows matching records with GitHub source links and a graph view of repository relationships.

The current retrieval uses keyword matching and scoring. It does not generate an LLM-written explanation or prove why a code change was made. Review the linked GitHub sources before drawing conclusions.

## Start here

- **Project guide:** [PROJECT_GUIDE.md](PROJECT_GUIDE.md) explains the product flow, architecture, graph, API, local setup, deployment, evidence, and limitations.
- **Prototype setup:** [prototype/README.md](prototype/README.md) has the setup instructions for running the app.
- **Build Log:** [Build-Log/Build-Log.md](Build-Log/Build-Log.md) documents the six assessment entries and supporting screenshots.
- **Build Summary:** [Build-Summary.md](Build-Summary.md) summarizes the problem, implementation, evidence position, and next steps.

## Repository layout

```text
prototype/       Application source and setup README
Build-Log/       Six-entry process log and supporting screenshots
Build-Summary.md One-page project summary
PROJECT_GUIDE.md Detailed guide to the project and its operation
```

## Technology

- **Frontend:** HTML, CSS, and vanilla JavaScript
- **Backend:** Python, FastAPI, and Uvicorn
- **Repository data:** GitHub REST API
- **Graph store:** Neo4j and Cypher
- **Retrieval:** deterministic keyword extraction, matching, and scoring

For local requirements, environment configuration, and run commands, see [prototype/README.md](prototype/README.md).