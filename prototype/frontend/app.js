const API_URL = "http://127.0.0.1:8000/api/ask";

async function submitQuestion() {
  const questionInput = document.getElementById("question-input");
  const questionText = questionInput.value.trim();
  
  if (!questionText) {
    alert("Please enter a question before submitting.");
    return;
  }

  // Clear window.name draft upon submission
  window.name = "";

  const submitBtn = document.getElementById("submit-btn");
  const resultsSection = document.getElementById("results-section");
  const loadingSpinner = document.getElementById("loading-spinner");
  const answerContent = document.getElementById("answer-content");
  const sourcesContent = document.getElementById("sources-content");

  submitBtn.disabled = true;
  resultsSection.classList.add("hidden");
  loadingSpinner.classList.remove("hidden"); // Correctly reveals the loading spinner

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: questionText }),
    });

    if (!response.ok) {
      throw new Error(`Server status: ${response.status}`);
    }

    const data = await response.json();
    answerContent.textContent = data.answer || "No response received.";

    sourcesContent.innerHTML = "";
    if (data.sources && data.sources.length > 0) {
      data.sources.forEach((source) => {
        const card = document.createElement("div");
        card.className = "source-card glass-card";
        card.innerHTML = `
          <span class="source-tag">${source.entity_type || 'Evidence Node'}</span>
          <div class="source-meta">${source.author || 'Unknown'} • ${source.date || 'N/A'}</div>
          <p class="source-detail">${source.detail || ''}</p>
          ${source.url ? `<a class="source-link" href="${source.url}" target="_blank" rel="noopener noreferrer">Open Source Commit →</a>` : ''}
        `;
        sourcesContent.appendChild(card);
      });
    } else {
      sourcesContent.innerHTML = `<p style="color: var(--text-muted); grid-column: 1 / -1;">No direct graph sources found for this question.</p>`;
    }

    resultsSection.classList.remove("hidden");
  } catch (error) {
    alert("Error communicating with backend: " + error.message);
  } finally {
    submitBtn.disabled = false;
    loadingSpinner.classList.add("hidden");
  }
}

// Window Name State Persistence across page navigation
document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("question-input");

  if (textarea) {
    // 1. Restore text from window.name when returning to the page
    if (window.name && window.name.trim() !== "") {
      textarea.value = window.name;
    }

    // 2. Continuously save text to window.name on every keystroke
    textarea.addEventListener("input", (e) => {
      window.name = e.target.value;
    });

    // 3. Keyboard shortcut (Cmd+Enter or Ctrl+Enter to submit)
    textarea.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        submitQuestion();
      }
    });
  }
});
