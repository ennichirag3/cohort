# Entry 6: System Testing, Failure Analysis & Demo Verification

## 1. Test Results Matrix

| Test Case | Query Input | Expected Outcome | Actual System Response | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Valid Query** | "Why was Neo4j chosen over PostgreSQL for indexing repository entities?" | Returns evidence-backed explanation with sources. | Returned synthesized answer with graph sources. | PASS |
| **Missing Evidence** | "Why did we switch our frontend framework from Vue to Svelte in 2022?" | Triggers strict fallback statement: "Insufficient evidence in repository history..." | Returned exact fallback string without hallucinating. | PASS |
| **Edge Case** | [Empty String Query] | Prevents dispatch and handles gracefully via API validation. | Handled gracefully without server crash. | PASS |

---

## 2. Guardrail & Fallback Verification
- Verified that when no relevant records are returned from Neo4j, the system strictly outputs: `"Insufficient evidence in repository history to answer this question."`

---

## 3. Stranger Testing Feedback
- Peers praised the clean dark glassmorphism interface and the structured separation between the LLM's answer and the individual evidence cards.
