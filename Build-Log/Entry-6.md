# Build Log Entry 6: Testing, Failure Modes & Stranger Test Findings

## 1. Module Lead & Focus
- **Lead**: Chirag (Frontend/QA Lead) & Shreya (Ingestion/Testing)
- **Focus**: System testing, stranger testing, failure mode handling.

## 2. Failure Mode & Edge Case Testing Results
- **Unsupported Question (No Graph Context)**: Successfully returned *"Insufficient context in knowledge graph to answer this query"*.
- **Empty / Very Long Inputs**: Sanitized gracefully by client-side JS (`app.js`) without backend crash.
- **API / Database Timeout**: Rendered glassmorphic error banner with retry options.

## 3. Stranger Test Execution
- **Participants**: Two peer developers unfamiliar with the project.
- **Feedback Received**:
  1. Requested direct links on citation cards to open GitHub commits directly in a new tab.
  2. Suggested adding prompt templates for new users.
- **Fixes Applied**: Added target `_blank` hyperlinked cards in `app.js` and quick-select question pills on the dashboard.
