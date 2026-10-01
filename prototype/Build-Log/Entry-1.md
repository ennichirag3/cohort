# Entry-1 — Define the Problem Statement

## Project

Evidence-Backed Developer Assistant for FastAPI

## Team Member

Anirudh
Manas
Shreya
Chirag
Anshika

## Theme

AI and Developer Tools — Understanding Why the Code Is Like This

---

## 1. Problem Statement — Version 1

New developers can read existing code but often cannot recover the intent behind design and implementation decisions. Important reasoning is distributed across commits, pull requests, issues, documentation, and other repository history, making ordinary keyword search insufficient for understanding why a codebase is structured a certain way. In the FastAPI repository, developers may understand what a function, class, or module does but still struggle to understand why it was designed or changed in a particular way. We want to build an evidence-backed assistant that connects code entities to historical decisions and lets developers ask "why" questions with traceable evidence.

### Who experiences the problem?

The main users are:

* New developers learning the FastAPI codebase.
* Developers contributing to an unfamiliar part of FastAPI.
* Developers trying to understand existing design and implementation decisions.
* Developers maintaining or modifying code that was written or changed by others.

### When does the problem occur?

The problem occurs when a developer:

* Encounters unfamiliar FastAPI source code.
* Needs to modify an existing component.
* Wants to understand why a particular implementation was chosen.
* Needs historical context before making a change.
* Cannot determine the reason from the current code and documentation alone.

### What is the cost?

The developer may need to manually search through:

* Source files.
* Git commits.
* Pull requests.
* Issues.
* Documentation.

This increases the time required to understand the code and may still leave uncertainty about the original design decision.

### Why is this worth solving?

Understanding the reasoning behind existing code can help developers make changes that are consistent with the project's previous decisions. Connecting the current code with its historical evidence could reduce the effort required to recover this context and make explanations more trustworthy than explanations based only on the current source code.

---

## 2. Intended Build

We intend to build an evidence-backed developer assistant for the FastAPI GitHub repository. A developer will provide the repository and ask a natural-language "why" question about a code entity or implementation decision.

The system will follow this general flow:

GitHub Repository → History Ingestion → Graph Construction in Neo4j → Graph/RAG Retrieval → Why Question → Evidence-Backed Answer

The system will connect relevant code entities with historical information such as commits, pull requests, issues, and documentation. It will then retrieve relevant evidence and generate a concise explanation that includes the evidence chain and source links. If sufficient evidence cannot be found, the system should indicate that the available evidence is insufficient rather than inventing an explanation.

---

## 3. Leverage Map

| Task                                                               | Classification | Reason                                                                        |
| ------------------------------------------------------------------ | -------------- | ----------------------------------------------------------------------------- |
| Collect commits, pull requests, issues, and repository information | Automation     | The system can automatically collect structured repository data.              |
| Connect code entities with historical entities                     | Automation     | Graph relationships can be created automatically from repository data.        |
| Retrieve relevant historical evidence                              | Automation     | Graph and text retrieval can identify potentially relevant evidence.          |
| Summarize retrieved evidence                                       | Augmentation   | AI can help summarize multiple historical sources.                            |
| Generate an explanation for a "why" question                       | Augmentation   | AI can transform retrieved evidence into a readable explanation.              |
| Verify whether the evidence actually supports the explanation      | Agency         | A human should review whether the evidence is sufficient and relevant.        |
| Decide whether the explanation is trustworthy enough to use        | Agency         | The developer should make the final decision based on the displayed evidence. |

---

## 4. Human Decisions

The system should not completely replace developer judgment. Important human decisions include:

1. **Evidence sufficiency**
   The developer should decide whether the retrieved commits, pull requests, issues, or documentation provide enough evidence to support the explanation.

2. **Historical intent**
   The developer should determine whether the retrieved historical information actually explains the design or implementation decision being investigated.

3. **Action based on the explanation**
   The developer should decide whether to modify, reuse, or preserve the existing implementation after reviewing the explanation and evidence.

---

## 5. Initial Evidence and Claim List

The following claims will be treated as items to verify during the project:

### Evidence

* FastAPI is a public GitHub repository with a substantial development history.
* The repository contains source code and associated project information that can be analyzed.
* Git history can provide information about changes to code over time.
* Pull requests and issues can provide discussion surrounding changes.
* Documentation can provide additional context for features and design decisions.

### Inference

* Connecting current code entities with historical repository entities may make it easier to recover design context.
* A graph representation may help retrieve relationships between code, commits, pull requests, issues, and documentation.
* Combining graph retrieval with text retrieval may provide more useful context than searching source code alone.

### Hypothesis

* Developers will be able to understand selected FastAPI design and implementation decisions more effectively when the system presents relevant historical evidence together with the generated explanation.

### Assumption

* FastAPI's public repository contains enough historical evidence to answer at least some meaningful "why" questions.
* Code entities can be connected to relevant historical entities such as commits, pull requests, and issues.
* Developers will find traceable evidence useful when evaluating an AI-generated explanation.

These assumptions will be tested before the final prototype scope is frozen.

---

## 6. Initial "Why" Questions

The following questions will be considered as initial candidates for testing against the FastAPI repository:

1. Why is FastAPI's dependency injection system designed this way?
2. Why does FastAPI use Pydantic for data validation?
3. Why is a particular FastAPI implementation or function written using `async`?
4. Why was a particular internal implementation changed?
5. Why was a specific validation or serialization behavior introduced?

These are candidate questions rather than confirmed questions. The team will verify whether each question can be traced to sufficient evidence in the FastAPI repository's code and history.

---

## 7. Initial Success Criteria

The prototype should demonstrate that:

* A developer can ask a natural-language "why" question about FastAPI.
* The system can identify relevant code or repository entities.
* The system can retrieve related historical information.
* The generated answer is connected to identifiable evidence.
* Source links are provided for the evidence.
* The system indicates when sufficient evidence is not available.
* The system does not present unsupported historical intent as fact.
