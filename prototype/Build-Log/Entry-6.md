# Build Log Entry 6: Testing, Failure Modes & Stranger Test Findings

## 1. Module Lead & Focus
- **Lead**: Chirag (Frontend/QA Lead) & Shreya (Ingestion/Testing)[span_61](start_span)[span_61](end_span)
- **Focus**: System testing, stranger testing, failure mode handling[span_62](start_span)[span_62](end_span).

## 2. Failure Mode & Edge Case Testing Results
- **Unsupported Question (No Graph Context)**: Successfully returned *"Insufficient context in knowledge graph to answer this query"*[span_63](start_span)[span_63](end_span).
- **Empty / Very Long Inputs**: Sanitized gracefully by client-side JS (`app.js`) without backend crash[span_64](start_span)[span_64](end_span).
- **API / Database Timeout**: Rendered glassmorphic error banner with retry options[span_65](start_span)[span_65](end_span).

## 3. Stranger Test Execution
- **Participants**: Two peer developers unfamiliar with the project[span_66](start_span)[span_66](end_span).
- **Feedback Received**:
  1. Requested direct links on citation cards to open GitHub commits directly in a new tab[span_67](start_span)[span_67](end_span).
  2. Suggested adding prompt templates for new users[span_68](start_span)[span_68](end_span).
- **Fixes Applied**: Added target `_blank` hyperlinked cards in `app.js` and quick-select question pills on the dashboard[span_69](start_span)[span_69](end_span).
