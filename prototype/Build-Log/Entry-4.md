# Entry 4: Claims Classification, Guardrails & Faithfulness Evaluation

## 1. Module Overview & Primary Lead
- **Module Lead**: Shreya (Evaluation & Security Lead)
- **Co-Lead / Contributor**: Anshika (AI & RAG Lead)
- **Collaborators**: Anirudh (Ground Truth Dataset Curation), Chirag (Failure Case Logging), Manas (Graph Traceability)

---

## 2. Claims Classification Framework
To guarantee factual explanations, generated responses undergo automated claim verification before being returned to the user:

- **Source-Grounded Claims**: Statements directly linked to a specific commit hash, PR number, or issue ID (e.g., *"PR #14 replaced Redis with Memcached due to latency"*).
- **Inferred Architectural Context**: Analytical statements synthesizing graph relationships.
- **Ungrounded / Hallucinated Claims**: Any claim lacking a corresponding node or relationship in the retrieved Neo4j subgraph.

---

## 3. Evaluation Metrics & Benchmark Dataset
A curated test suite of developer queries is used to evaluate pipeline performance:

1. **Faithfulness Score**: Measures whether the LLM output strictly adheres to the retrieved graph facts without adding unverified details.
2. **Citation Accuracy**: Verifies that every commit, PR, or issue reference correctly points to an existing record in Neo4j.
3. **Refusal Precision**: Assesses the system's ability to correctly respond with *"Insufficient context"* when graph data is missing, avoiding speculative answers.

---

## 4. Automated Guardrail Verification Pipeline
- **Traceability Verification**: Cross-checks extracted entities in the answer against graph retrieval outputs.
- **Post-Generation Filtering**: Automatically flags or strips unverified claims prior to sending the response payload to the UI.
