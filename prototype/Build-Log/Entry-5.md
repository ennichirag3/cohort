# Entry 5: Glassmorphic Frontend & UI Integration

## 1. User Interface Design
- **Visual Style**: Built a modern, dark glassmorphism dashboard (`styles.css`) featuring dynamic background glow accents, frosted glass panels, and interactive hover states.
- **Components**:
  - Hero header positioned for codebase querying.
  - Interactive textarea for user "Why?" queries with quick submit actions.
  - Async loading indicator with dynamic pulse animations.
  - Synthesized Answer display panel and dynamic Evidence Chain grid.

## 2. API Consumption & Async Data Flow
- **Integration (`app.js`)**: Configured JavaScript `fetch()` requests targeting `http://127.0.0.1:8000/api/ask`.
- **Payload Structure**: Sends `POST` requests with JSON payload `{"question": "<user_input>"}`.
- **Dynamic Rendering**: Parses the API response to dynamically populate answer text and render evidence source cards (Entity Type badges, Authors, Dates, Details, and URLs).
