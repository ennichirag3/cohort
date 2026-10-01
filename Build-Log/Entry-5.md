# Build Log Entry 5: Product-Market Fit & Single Flow Definition

## 1. Module Lead & Focus
- **Lead**: Chirag (Frontend Lead) & Anirudh (Product Lead)
- **Focus**: Falsifiable hypothesis, ICP, mechanism, and target product flow.

## 2. Falsifiable Hypothesis
If a developer is given a why-question assistant backed by a Neo4j Git graph, they will identify architectural reasons in under 2 minutes with 100% citation accuracy, compared to spending 15+ minutes searching GitHub PRs manually.

## 3. Ideal Customer Profile (ICP) & Substitutes
- **ICP**: Software Engineers, Open-Source Contributors, Technical Leads.
- **Current Substitutes**: Manual `git blame`, GitHub PR search, asking senior engineers on Slack.
- **Cost of Substitute**: Hours of lost engineering velocity and redundant code refactors.

## 4. Single Target Product Flow
1. Developer enters a public GitHub repo URL and a why-question into the UI.
2. System queries Neo4j AuraDB for matching commits, PRs, and issues.
3. RAG pipeline generates a source-grounded response with citation cards.
4. Developer clicks a citation card to inspect the exact GitHub source commit/PR.
