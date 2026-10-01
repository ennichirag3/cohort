# Build Log Entry 4 — Unwind the Idea

**Project:** Evidence-Backed Developer Assistant for FastAPI
**Activity:** 4

---

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

### Critique 1 — User / Developer Perspective

**Question:**

> Why wouldn't a developer simply use an existing AI coding assistant and ask it to explain the FastAPI code?

**Concern:**

An AI coding assistant can explain what the current code appears to do, but the developer may still need historical evidence to understand why a particular design or implementation decision was made.

**Implication:**

The proposed system should focus on connecting the current code to repository history rather than providing only a general code explanation.

---

### Critique 2 — Technical Lead Perspective

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

If developers can already understand relevant design decisions easily from current code and documentation, the value of the proposed assistant would be lower.

**48-Hour Test:**

Talk to 2–3 developers and ask about situations where they had to understand unfamiliar code. Specifically ask whether they needed to search commits, pull requests, issues, or documentation to understand why the code was implemented in a particular way.

**Evidence to collect:**

* Whether they encountered the problem.
* What sources they searched.
* How long the process took.
* Whether they were confident that they found the correct reasoning.

---

### Assumption 2 — The Selected FastAPI Repository Contains Sufficient Evidence

**Assumption:**

The selected FastAPI repository contains enough relevant historical information to answer at least some meaningful "why" questions.

**Impact if false:**

If relevant historical evidence cannot be found or connected to the current code, the evidence-backed assistant may not be able to produce reliable answers.

**48-Hour Test:**

Test approximately 10 candidate "why" questions against the selected FastAPI repository. For each question, investigate whether the relevant code can be connected to commits, pull requests, issues, or documentation that provide useful evidence.

Record:

* The question.
* Relevant code entity.
* Related commit.
* Related pull request or issue, if available.
* Whether the source actually helps explain the decision.
* Source link.
* Whether the evidence is sufficient, partial, or insufficient.

This test will determine which questions should be included in the prototype.

---

### Assumption 3 — Code Entities Can Be Connected to Historical Entities

**Assumption:**

Useful relationships can be established between FastAPI code entities and historical repository entities.

**Impact if false:**

If reliable relationships cannot be established, the Neo4j graph may not provide useful evidence for the retrieval process.

**48-Hour Test:**

Manually trace several examples using:

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

Check whether these relationships can be represented and retrieved using the proposed graph structure.

**Evidence to collect:**

* Code entity.
* Historical entity.
* Relationship between them.
* Evidence supporting the relationship.
* Whether the relationship can be retrieved through a graph query.

---

## 5. Version 2 Problem Statement

Developers working on unfamiliar parts of a public codebase may understand what existing code does but struggle to recover the reasoning behind particular design and implementation decisions. Relevant context can be distributed across source code, commits, pull requests, issues, and documentation, requiring developers to manually search and connect these sources. This can make understanding historical context time-consuming and uncertain.

For the PS1 prototype, the selected repository is **FastAPI**. The proposed system will investigate whether connecting FastAPI code entities with relevant repository history can help developers answer natural-language "why" questions. The system will retrieve available evidence and present a concise explanation together with an evidence chain and source links; when sufficient evidence cannot be found, it should explicitly indicate that the evidence is insufficient.

---

## 6. Evidence Position

At this stage, the following distinctions will be maintained:

* **Evidence:** Information directly obtained from FastAPI source code, commits, pull requests, issues, documentation, or other repository sources.
* **Inference:** A conclusion derived from multiple pieces of retrieved evidence.
* **Hypothesis:** A proposed explanation that still requires verification.
* **Assumption:** A belief about the problem or solution that is being tested.

The project should not treat an inferred or hypothesized explanation as a documented historical fact.

---

## 7. Product Principle

The proposed product principle is:

> **Retrieve evidence first, explain second.**

The LLM should use retrieved repository evidence to construct the answer rather than relying only on its general knowledge.

The prototype should aim to provide:

1. A concise explanation.
2. The relevant FastAPI code entity.
3. The historical evidence supporting the explanation.
4. Links to the original sources.
5. An indication of uncertainty when the available evidence is incomplete.

---

## 8. Proposed Product Flow

For the selected FastAPI repository, the proposed flow is:

```text
FastAPI Repository
        ↓
Repository / History Ingestion
        ↓
Identify Relevant Code Entity
        ↓
Retrieve Related Graph Entities
        ↓
Retrieve Commits / PRs / Issues / Documentation
        ↓
Evidence Retrieval
        ↓
Developer "Why?" Question
        ↓
LLM Explanation
        ↓
Answer + Evidence Chain + Source Links
```

If sufficient evidence cannot be found:

```text
Insufficient Evidence
        +
Available Related Sources
        +
Uncertainty Explanation
```

The system should not generate an unsupported historical explanation.

---

## 9. Initial Scope Decision

The PS1 build will use **FastAPI as the selected public repository**. The team will initially work with a limited and testable subset of the repository rather than attempting to process the entire repository history.

The initial scope will be determined after testing the candidate "why" questions and identifying which questions have sufficient evidence.

The prototype will focus on:

* Selected FastAPI source files or modules.
* Relevant Git commits.
* Related pull requests where available.
* Related issues where available.
* Relevant documentation.
* A small set of "why" questions for which the evidence can be verified.

The scope can be expanded only after the initial flow is shown to work.

---

## 10. Activity 4 Conclusion

The Five Whys and reframing exercise indicate that the central problem is not simply generating an AI explanation of source code. The proposed value lies in helping developers recover historical context and supporting the explanation with traceable repository evidence.

The selected FastAPI repository will therefore be used to test whether this approach is practical. The results of the assumption tests will determine which questions and repository data should be included in the prototype.

The intended direction is:

**Code-to-history relationships → Evidence retrieval → Traceable explanation**
