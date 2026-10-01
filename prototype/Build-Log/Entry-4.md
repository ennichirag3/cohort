# Entry-4 — Unwind the Idea

## Project

Evidence-Backed Developer Assistant for FastAPI

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## 1. Five Whys

### Why 1: Why do developers struggle to understand unfamiliar FastAPI code?

Because the current source code shows what the system does, but it does not always explain the reasoning behind a design or implementation decision.

### Why 2: Why is the reasoning not always visible in the current code?

Because the reasoning behind changes can be distributed across commits, pull requests, issues, documentation, and other parts of the repository history.

### Why 3: Why can't developers simply search these sources manually?

Because the developer has to identify the relevant code entity first and then manually connect it with potentially related commits, pull requests, issues, and documentation.

### Why 4: Why is connecting these sources difficult?

Because the relationships between a current code entity and its historical context are not necessarily represented as one connected view that can be queried directly.

### Why 5: Why is recovering these relationships important?

Because understanding the historical context behind a design or implementation decision can help a developer understand why the current code exists before modifying it.

### Research Question

**Can relationships between code entities and repository history be represented and retrieved in a way that helps developers recover the historical context behind a design or implementation decision?**

---

## 2. Reframes

### Reframe 1 — From Code Search to Decision Recovery

Instead of treating the problem as simply finding relevant source code, the system should help developers recover the reasoning and historical context behind a particular design or implementation decision.

**Original framing:**

> Developers need help understanding unfamiliar code.

**Reframed problem:**

> Developers need a way to recover the historical context behind decisions represented in unfamiliar code.

---

### Reframe 2 — From AI Explanation to Evidence Retrieval

Instead of building an AI system that simply explains code, the system should first retrieve relevant evidence and then use AI to organize that evidence into an understandable explanation.

**Original framing:**

> AI should explain what a piece of FastAPI code does and why it exists.

**Reframed problem:**

> The system should retrieve evidence connecting the code to historical decisions and use AI to explain that evidence.

This makes the generated answer more traceable because the developer can inspect the sources used to produce it.

---

## 3. Critique from Different Perspectives

### Critique 1 — Developer Perspective

**Question:**

> Why wouldn't a developer simply use an existing AI coding assistant and ask it to explain the FastAPI code?

**Concern:**

An AI coding assistant can explain what the current code appears to do, but the developer may still need historical evidence to understand why a particular design or implementation decision was made.

**Implication:**

Our system should focus on connecting the current code to repository history rather than providing only a general code explanation.

---

### Critique 2 — Technical Perspective

**Question:**

> How do we know that a particular commit, pull request, or issue actually explains why the current code exists?

**Concern:**

A historical item may be related to a file or function without actually documenting the reason for the current implementation.

**Implication:**

The retrieval process must preserve the relationship between code entities and historical evidence and show the original sources to the developer. The system should also acknowledge when the available evidence is insufficient.

---

## 4. Top Three Assumptions

### Assumption 1 — Developers Need Historical Decision Context

**Assumption:**

Developers working with unfamiliar code will encounter situations where understanding historical context is useful.

**Impact if false:**

If developers can already understand the relevant design decisions easily from current code and documentation, the value of the proposed assistant would be lower.

**48-Hour Test:**

Talk to 2–3 developers and ask them about a recent situation where they had to understand unfamiliar code. Specifically ask whether they needed to search commits, pull requests, issues, or documentation to understand why the code was implemented a particular way.

**Evidence to collect:**

* Whether they encountered the problem.
* What sources they searched.
* How long the process took.
* Whether they were confident that they found the correct reasoning.

---

### Assumption 2 — FastAPI Contains Sufficient Historical Evidence

**Assumption:**

The FastAPI repository contains enough useful historical information to answer a meaningful set of "why" questions.

**Impact if false:**

If the repository does not contain sufficient connections between code changes and their historical explanations, the proposed evidence-backed assistant may not have enough information to produce useful answers.

**48-Hour Test:**

Select approximately 10 candidate "why" questions from the FastAPI codebase. For each question, manually investigate:

```text
Code Entity → Commit → Pull Request / Issue → Documentation
```

Record whether useful evidence explaining the decision can be found.

**Evidence to collect:**

* Candidate question.
* Relevant file/function/class.
* Related commit.
* Related pull request or issue, if available.
* Whether the historical source actually explains the decision.
* Source link.

---

### Assumption 3 — Code Entities Can Be Connected to Historical Entities

**Assumption:**

It is technically possible to establish useful relationships between FastAPI code entities and repository history.

**Impact if false:**

If reliable relationships cannot be established, the Neo4j graph and retrieval process may produce irrelevant or misleading evidence.

**48-Hour Test:**

Manually select several FastAPI examples and create relationships such as:

```text
Repository
    ↓
File
    ↓
Function / Class
    ↓
Commit
    ↓
Pull Request / Issue
    ↓
Documentation
```

Test whether these relationships can be represented as graph nodes and edges and whether they can be queried to retrieve relevant historical context.

**Evidence to collect:**

* Code entity.
* Historical entity.
* Relationship between them.
* Evidence supporting the relationship.
* Whether the relationship can be retrieved through a graph query.

---

## 5. Version 2 Problem Statement

Developers working on unfamiliar parts of the FastAPI codebase may understand what existing code does but struggle to recover the reasoning behind particular design and implementation decisions. Relevant context can be distributed across source code, commits, pull requests, issues, and documentation, requiring developers to manually search and connect these sources without a single view of the relationships between them. This can make understanding historical intent time-consuming and uncertain.

The proposed solution is an evidence-backed developer assistant that connects FastAPI code entities with relevant repository history and allows developers to ask natural-language "why" questions. The system will retrieve related historical evidence and present a concise explanation together with an evidence chain and source links. When sufficient evidence cannot be found, the system should clearly indicate the uncertainty instead of generating an unsupported explanation.

---

## 6. Evidence Position

The project should distinguish between:

* **Evidence:** Information directly retrieved from FastAPI source code, commits, pull requests, issues, documentation, or other repository sources.
* **Inference:** A conclusion derived from multiple pieces of retrieved evidence.
* **Hypothesis:** A proposed explanation that still needs verification.
* **Assumption:** A belief about the problem or solution that must be tested.

The assistant should not present an inference or hypothesis as a documented historical fact.

---

## 7. Product Principle

The core principle of the system is:

> **Retrieve evidence first, explain second.**

The LLM should use retrieved repository evidence to construct the answer rather than relying only on its general knowledge of FastAPI.

Every answer should therefore aim to provide:

1. A concise explanation.
2. The relevant code entity.
3. Historical evidence supporting the explanation.
4. Links to the original sources.
5. An indication of uncertainty when evidence is incomplete.

---

## 8. Proposed Product Flow

The initial product flow is:

```text
Developer
    ↓
FastAPI Repository + "Why" Question
    ↓
Identify Relevant Code Entity
    ↓
Retrieve Related Graph Entities
    ↓
Retrieve Commits / PRs / Issues / Documentation
    ↓
Evidence Filtering
    ↓
LLM Explanation
    ↓
Answer + Evidence Chain + Source Links
```

If the system cannot find sufficient evidence, the flow should instead produce:

```text
Insufficient Evidence
        +
Available Related Sources
        +
Uncertainty Explanation
```

rather than generating an unsupported historical explanation.

---

## 9. Initial Scope Decision

For the first prototype, the system should focus on a limited portion of the FastAPI repository rather than attempting to ingest the entire repository immediately.

The initial scope should include:

* Selected FastAPI source files or modules.
* Their relevant Git commits.
* Related pull requests where available.
* Related issues where available.
* Relevant documentation.
* A small set of verified "why" questions.

This allows the team to test whether the core idea works before expanding the graph and retrieval scope.

---

## 10. Activity 4 Conclusion

The main insight from the Five Whys and reframing exercise is that the project is not primarily about generating another AI explanation of source code. The central problem is recovering and connecting the historical evidence behind existing code decisions.

Therefore, the prototype should prioritize:

**Code-to-history relationships → Evidence retrieval → Traceable explanation**

rather than:

**Code → Generic AI explanation**
