const apiInput = document.querySelector("#apiBase");
const jobText = document.querySelector("#jobText");
const scanLimit = document.querySelector("#scanLimit");
const topN = document.querySelector("#topN");
const useLlm = document.querySelector("#useLlm");
const button = document.querySelector("#rankButton");
const statusEl = document.querySelector("#status");
const cardsEl = document.querySelector("#cards");
const jobTitleEl = document.querySelector("#jobTitle");
const resultCountEl = document.querySelector("#resultCount");

const storedApi = localStorage.getItem("recruitrankai_api_base");
apiInput.value = storedApi || window.RECRUITRANKAI_API_BASE || "";

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderResults(payload) {
  jobTitleEl.textContent = payload.job?.title || "Ranked shortlist";
  resultCountEl.textContent = `${payload.count || 0} candidates`;
  cardsEl.innerHTML = "";

  for (const [index, item] of (payload.results || []).entries()) {
    const skills = [
      ...(item.matched_skills || []),
      ...(item.missing_skills || []).map((skill) => `Missing: ${skill}`),
    ].slice(0, 8);
    const skillHtml = skills.map((skill) => `<span class="chip">${escapeHtml(skill)}</span>`).join("");
    const llm = item.llm_review?.summary ? `<p class="reason">Brain: ${escapeHtml(item.llm_review.summary)}</p>` : "";

    cardsEl.insertAdjacentHTML(
      "beforeend",
      `
      <article class="card">
        <div class="card-top">
          <div>
            <h3>#${index + 1} ${escapeHtml(item.name || "Unnamed Candidate")}</h3>
            <p class="meta">${escapeHtml(item.candidate_id)} / ${escapeHtml(item.headline)} / ${escapeHtml(item.location)}</p>
          </div>
          <div class="score">${Math.round((item.score || 0) * 100)}%</div>
        </div>
        <p class="reason">${escapeHtml((item.reasons || []).join(" "))}</p>
        ${llm}
        <div class="chips">${skillHtml}</div>
      </article>
      `,
    );
  }
}

button.addEventListener("click", async () => {
  const apiBase = apiInput.value.trim().replace(/\/$/, "");

  if (!apiBase) {
    statusEl.textContent = "Add your deployed API base URL first.";
    return;
  }

  localStorage.setItem("recruitrankai_api_base", apiBase);
  statusEl.textContent = "Ranking candidates...";
  button.disabled = true;

  try {
    const response = await fetch(`${apiBase}/rank`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_text: jobText.value,
        scan_limit: Number(scanLimit.value),
        top_n: Number(topN.value),
        use_llm: useLlm.checked,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error ${response.status}`);
    }

    const payload = await response.json();
    renderResults(payload);
    statusEl.textContent = "Shortlist ready.";
  } catch (error) {
    statusEl.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
