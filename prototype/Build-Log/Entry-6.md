# Entry 6: Stranger Testing, User Feedback & Final Refinement

## 1. Module Overview & Primary Lead
- **Module Lead**: Chirag (Frontend & QA Lead)
- **Co-Lead / Contributor**: Shreya (Evaluation & Security Lead)
- **Collaborators**: Anshika (Prompt & Guardrail Refinement), Anirudh (Query Log Analysis), Manas (Graph Query Tuning)

---

## 2. Stranger Testing Methodology
To evaluate system usability and response clarity without bias, the project was tested by external developers ("strangers") who had no prior exposure to the codebase or graph schema.

- **Participant Group**: External peer developers and engineers outside the core team.
- **Test Protocol**: Testers were given open-ended architectural queries regarding repo history without guidance on how to phrase their questions.
- **Observation Focus**: System latency, response comprehensibility, clarity of commit/PR citations, and UI navigation intuitiveness.

---

## 3. Key Findings & User Feedback
1. **Citation Clarity**: Testers appreciated source-backed answers but requested direct external links on PR and Commit cards for faster verification.
2. **Handling Unclear Queries**: Broad queries (e.g., *"Why is the backend like this?"*) produced generic context; users preferred suggested query templates.
3. **Response Speed**: High graph traversal depth occasionally caused slight UI delays during context fetching.

---

## 4. System Refinements & Final Implementation
Based on feedback, the team executed the following final updates:

- **Frontend (`app.js`)**: Added interactive query suggestions and direct hyperlink formatting on retrieved node cards.
- **RAG & Cypher Optimization (`rag_pipeline.py`)**: Restructured Cypher traversal depth limits to reduce latency by keeping query execution lightweight.
- **Guardrail Fine-Tuning**: Enhanced refusal triggers so that ambiguous inputs prompt the user for clarification instead of attempting broad inference.
