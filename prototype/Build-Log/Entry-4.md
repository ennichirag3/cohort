# Entry 4: Backend API Architecture & Integration

## 1. Endpoint Contract
- **Route**: `POST /api/ask`
- **Request Payload**: `{"question": "string"}`
- **Response Structure**:
  ```json
  {
    "question": "string",
    "answer": "string",
    "evidence_found": true,
    "sources": []
  }
