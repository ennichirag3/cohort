const API_BASE_URL = "https://repoinsight-qjj0.onrender.com";
const API_URL = `${API_BASE_URL}/api/ask`;
const REPOSITORY_STATE_KEY = "evidenceRepositoryState";
const RESULT_STATE_KEY = "evidenceQueryResult";

function formatMarkdown(text) {
  if (!text) return "";

  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/^### (.*$)/gim,
      '<h3 style="color:#38bdf8;margin-top:16px;margin-bottom:8px;">$1</h3>')
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g,
      '<code style="background:rgba(56,189,248,.1);color:#38bdf8;padding:2px 6px;border-radius:4px;font-family:monospace;">$1</code>')
    .replace(/\n/g, "<br>");
}

function safeGitHubUrl(value) {
  try {
    const url = new URL(value);
    if (url.protocol === "https:" && url.hostname === "github.com") {
      return url.href;
    }
  } catch {
    // Ignore invalid URLs.
  }
  return "";
}

function renderQueryResult(data) {
  const resultsSection = document.getElementById("results-section");
  const answerContent = document.getElementById("answer-content");
  const sourcesContent = document.getElementById("sources-content");

  if (answerContent) {
    answerContent.innerHTML = formatMarkdown(data.answer) || "No response received.";
  }

  if (sourcesContent) {
    sourcesContent.replaceChildren();

    if (Array.isArray(data.sources) && data.sources.length > 0) {
      for (const source of data.sources) {
        const card = document.createElement("div");
        card.className = "source-card glass-card";

        const header = document.createElement("div");
        header.className = "source-header";

        const tag = document.createElement("span");
        tag.className = "source-tag";
        tag.textContent = source.entity_type || source.type || "Evidence";

        const meta = document.createElement("span");
        meta.className = "source-meta";
        meta.textContent = `${source.author || "Unknown"} • ${source.date || "N/A"}`;
        header.append(tag, meta);

        const detail = document.createElement("p");
        detail.className = "source-detail";
        detail.textContent = source.detail || source.excerpt || source.title || "";
        card.append(header, detail);

        const url = safeGitHubUrl(source.url || source.source_url || "");
        if (url) {
          const link = document.createElement("a");
          link.className = "source-link";
          link.href = url;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = "Open GitHub source →";
          card.append(link);
        }
        sourcesContent.append(card);
      }
    } else {
      const message = document.createElement("p");
      message.style.color = "#94a3b8";
      message.textContent = "No direct graph sources found for this question.";
      sourcesContent.append(message);
    }
  }

  resultsSection?.classList.remove("hidden");
}

function saveRepositoryState() {
  const status = document.getElementById("repository-status");
  const input = document.getElementById("repository-input");
  if (!status || !input) return;

  sessionStorage.setItem(REPOSITORY_STATE_KEY, JSON.stringify({
    repository: input.value,
    message: status.textContent,
    className: status.className,
  }));
}

function restorePageState() {
  const input = document.getElementById("repository-input");
  const status = document.getElementById("repository-status");
  const repositoryState = sessionStorage.getItem(REPOSITORY_STATE_KEY);

  if (repositoryState && input && status) {
    try {
      const saved = JSON.parse(repositoryState);
      input.value = saved.repository || "";
      status.textContent = saved.message || "";
      status.className = saved.className || "repo-status";
    } catch {
      sessionStorage.removeItem(REPOSITORY_STATE_KEY);
    }
  }

  const savedResult = sessionStorage.getItem(RESULT_STATE_KEY);
  if (savedResult) {
    try {
      renderQueryResult(JSON.parse(savedResult));
    } catch {
      sessionStorage.removeItem(RESULT_STATE_KEY);
    }
  }
}

async function addRepository() {
  const input = document.getElementById("repository-input");
  const button = document.getElementById("repository-submit-btn");
  const status = document.getElementById("repository-status");
  const repository = input?.value.trim();

  if (!repository) {
    status.textContent = "Enter a GitHub repository URL or owner/repo first.";
    status.className = "repo-status error";
    saveRepositoryState();
    input?.focus();
    return;
  }

  button.disabled = true;
  button.querySelector("span").textContent = "Importing…";
  status.className = "repo-status";
  status.textContent = "Fetching recent GitHub history and saving it to Neo4j. This may take a few minutes…";
  saveRepositoryState();

  try {
    const response = await fetch(`${API_BASE_URL}/api/repositories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repository }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `Server status: ${response.status}`);
    }

    const counts = data.counts || {};
    // Let Graph Explorer open the repository that was just imported.
    localStorage.setItem("lastImportedRepository", data.repository);
    status.className = "repo-status success";
    status.textContent = `${data.message} Added ${counts.commits || 0} commits, ${counts.pull_requests || 0} merged PRs, and ${counts.issues || 0} issues. You can now ask about ${data.repository}.`;
    input.value = data.repository;
    saveRepositoryState();
  } catch (error) {
    status.className = "repo-status error";
    status.textContent = `Could not add repository: ${error.message}`;
    saveRepositoryState();
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Add Repository";
  }
}

async function submitQuestion() {
  const questionInput = document.getElementById("question-input");
  const questionText = questionInput?.value.trim();

  if (!questionText) {
    alert("Please enter a question before submitting.");
    return;
  }

  sessionStorage.setItem("lastQuestion", questionText);
  const repository = localStorage.getItem("lastImportedRepository");

  const submitBtn = document.getElementById("submit-btn");
  const resultsSection = document.getElementById("results-section");
  const loadingSpinner = document.getElementById("loading-spinner");

  submitBtn.disabled = true;
  resultsSection?.classList.add("hidden");
  loadingSpinner?.classList.remove("hidden");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: questionText, repository }),
    });

    if (!response.ok) {
      throw new Error(`Server status: ${response.status}`);
    }

    const data = await response.json();

    sessionStorage.setItem(RESULT_STATE_KEY, JSON.stringify(data));
    renderQueryResult(data);
    resultsSection?.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    alert("Error communicating with backend: " + error.message);
  } finally {
    submitBtn.disabled = false;
    loadingSpinner?.classList.add("hidden");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  restorePageState();

  const repositoryInput = document.getElementById("repository-input");
  repositoryInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addRepository();
    }
  });

  const textarea = document.getElementById("question-input");

  if (!textarea) return;

  textarea.value = sessionStorage.getItem("draftQuestion") || sessionStorage.getItem("lastQuestion") || "";

  textarea.addEventListener("input", (event) => {
    sessionStorage.setItem("draftQuestion", event.target.value);
  });

  textarea.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      submitQuestion();
    }
  });
});
