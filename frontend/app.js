const API = (() => {
  const host = window.location.hostname;
  if (host === "127.0.0.1" || host === "localhost") {
    return "http://127.0.0.1:5000/api";
  }
  return "/api";
})();

let updatesCache = [];
let deadlinesCache = [];

async function fetchJSON(path) {
  try {
    const response = await fetch(`${API}${path}`);
    if (!response.ok) {
      const errorPayload = await response.json().catch(() => ({}));
      throw new Error(errorPayload.error || `${response.status} ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("API error", error);
    return { error: error.message };
  }
}

function setDailyKitendawili() {
  const riddles = [
    { q: "Haba na haba...", a: "Hujaza kibaba" },
    { q: "Mti wangu una matawi mengi...", a: "Ulimi" },
    { q: "Nyumba yangu haina mlango...", a: "Yai" },
    { q: "Kuku wangu ametaga mayai juu ya mti...", a: "Embe" },
    { q: "Adui wa mtu ni nani?", a: "Mtu mwenyewe" }
  ];

  const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
  const riddle = riddles[dayOfYear % riddles.length];
  const target = document.getElementById("daily-riddle");
  if (target) {
    target.textContent = `${riddle.q} → ${riddle.a}`;
  }
}

function activateSection(section) {
  document.querySelectorAll(".section").forEach((node) => {
    node.classList.toggle("active", node.id === `section-${section}`);
  });
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.section === section);
  });

  if (section === "dashboard") loadDashboard();
  if (section === "updates") loadUpdates();
  if (section === "deadlines") loadDeadlines();
  if (section === "users") loadUsers();
}

function createCard({ title, subtitle = "", body = "", footer = "" }) {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `
    <span class="card-title">${title}</span>
    <span class="card-subtitle">${subtitle}</span>
    <span class="card-text">${body}</span>
    <div class="card-footer">${footer}</div>
  `;
  return card;
}

function formatDate(value) {
  if (!value) return "Unknown";
  try {
    return new Date(value).toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric"
    });
  } catch {
    return value;
  }
}

function showMessage(container, message) {
  if (container) {
    container.innerHTML = `<div class="placeholder-card">${message}</div>`;
  }
}

function setRefreshTimestamp() {
  const timestamp = document.getElementById("refresh-timestamp");
  if (!timestamp) return;
  const time = new Date();
  timestamp.textContent = time.toLocaleString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    day: "2-digit",
    month: "short"
  });
}

function normalizeQuery(value) {
  return (value || "").trim().toLowerCase();
}

function matchesQuery(item, query, fields) {
  if (!query) return true;
  return fields.some((field) => {
    const value = (item[field] || "").toString().toLowerCase();
    return value.includes(query);
  });
}

function sortByDate(items, key, desc = false) {
  return [...items].sort((a, b) => {
    const dateA = new Date(a[key] || 0).valueOf();
    const dateB = new Date(b[key] || 0).valueOf();
    return desc ? dateB - dateA : dateA - dateB;
  });
}

async function renderSection(containerId, data, renderItem, emptyMessage) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (data.error) {
    showMessage(container, `Unable to load content: ${data.error}`);
    return;
  }

  if (!data.length) {
    showMessage(container, emptyMessage);
    return;
  }

  container.innerHTML = "";
  data.forEach((item) => container.appendChild(renderItem(item)));
}

async function loadDashboard() {
  const deadlinesContainer = document.getElementById("dash-deadlines");
  const updatesContainer = document.getElementById("dash-updates");
  const usersCount = document.querySelector("#stat-users .stat-num");
  const projectsCount = document.querySelector("#stat-projects .stat-num");
  const deadlinesCount = document.querySelector("#stat-deadlines .stat-num");
  const urgentBadge = document.getElementById("urgent-count");

  if (deadlinesContainer) deadlinesContainer.innerHTML = "Loading...";
  if (updatesContainer) updatesContainer.innerHTML = "Loading...";

  const [deadlinesResponse, updatesResponse, usersResponse] = await Promise.all([
    fetchJSON("/deadlines?status=urgent"),
    fetchJSON("/updates?county=National"),
    fetchJSON("/users")
  ]);

  if (deadlinesResponse.error) {
    showMessage(deadlinesContainer, `Unable to load deadlines: ${deadlinesResponse.error}`);
  } else if (!deadlinesResponse.length) {
    showMessage(deadlinesContainer, "No urgent deadlines available.");
  } else if (deadlinesContainer && urgentBadge) {
    const sortedDeadlines = sortByDate(deadlinesResponse, "due_date");
    urgentBadge.textContent = `${deadlinesResponse.length} urgent`;
    deadlinesContainer.innerHTML = "";
    sortedDeadlines.slice(0, 3).forEach((deadline) => {
      deadlinesContainer.appendChild(
        createCard({
          title: deadline.title,
          subtitle: `${deadline.source || "Unknown source"} • ${deadline.county || "Unknown county"}`,
          body: `Due ${formatDate(deadline.due_date)} — ${deadline.status || "Unknown"}`,
          footer: deadline.description || "No extra details."
        })
      );
    });
  }

  if (updatesResponse.error) {
    showMessage(updatesContainer, `Unable to load updates: ${updatesResponse.error}`);
  } else if (!updatesResponse.length) {
    showMessage(updatesContainer, "No civic updates found.");
  } else if (updatesContainer) {
    const sortedUpdates = sortByDate(updatesResponse, "published_date", true);
    updatesCache = sortedUpdates;
    updatesContainer.innerHTML = "";
    sortedUpdates.slice(0, 3).forEach((update) => {
      updatesContainer.appendChild(
        createCard({
          title: update.title,
          subtitle: `${update.category || "General"} • ${update.county || "Kenya"}`,
          body: update.summary || "No summary available.",
          footer: `${formatDate(update.published_date)} • ${update.admin_name || "Staff"}`
        })
      );
    });
  }

  const projectCount = Array.isArray(deadlinesResponse)
    ? new Set(deadlinesResponse.map((deadline) => deadline.source || "Unknown")).size
    : "—";

  if (usersCount) usersCount.textContent = usersResponse.error ? "—" : usersResponse.length;
  if (projectsCount) projectsCount.textContent = typeof projectCount === "number" ? projectCount : "—";
  if (deadlinesCount) deadlinesCount.textContent = deadlinesResponse.error ? "—" : deadlinesResponse.length;
  setRefreshTimestamp();
}

async function applyUpdatesFilter(query) {
  const filtered = updatesCache.filter((update) =>
    matchesQuery(update, normalizeQuery(query), ["title", "category", "county", "summary"])
  );
  await renderSection(
    "updates-list",
    filtered,
    (update) =>
      createCard({
        title: update.title || "Untitled update",
        subtitle: `${update.category || "General"} • ${update.county || "Kenya"}`,
        body: update.summary || "No summary available.",
        footer: `${formatDate(update.published_date)} • ${update.admin_name || "Staff"}`
      }),
    "No updates match your search."
  );
}

async function loadUpdates() {
  const updates = await fetchJSON("/updates");
  updatesCache = sortByDate(Array.isArray(updates) ? updates : [], "published_date", true);
  await applyUpdatesFilter(document.getElementById("updates-search")?.value || "");
}

async function applyDeadlinesFilter(query) {
  const filtered = deadlinesCache.filter((deadline) =>
    matchesQuery(deadline, normalizeQuery(query), ["title", "source", "county", "description", "status"])
  );
  await renderSection(
    "deadlines-list",
    filtered,
    (deadline) =>
      createCard({
        title: deadline.title || "Untitled deadline",
        subtitle: `${deadline.source || "Unknown source"} • ${deadline.county || "Unknown county"}`,
        body: `${deadline.description || "No description."} — due ${formatDate(deadline.due_date)}`,
        footer: `Status: ${deadline.status || "Unknown"}`
      }),
    "No deadlines match your search."
  );
}

async function loadDeadlines() {
  const deadlines = await fetchJSON("/deadlines");
  deadlinesCache = sortByDate(Array.isArray(deadlines) ? deadlines : [], "due_date");
  await applyDeadlinesFilter(document.getElementById("deadlines-search")?.value || "");
}

async function loadUsers() {
  const users = await fetchJSON("/users");
  await renderSection(
    "users-list",
    Array.isArray(users) ? users.sort((a, b) => (a.name || "").localeCompare(b.name || "")) : [],
    (user) =>
      createCard({
        title: user.name || "Unnamed user",
        subtitle: `${user.email || "No email"} • ${user.county || "Unknown"}`,
        body: `Subscriptions: ${user.saved_categories?.join(", ") || "No subscriptions"}`,
        footer: `Bookmarks: ${user.bookmarked_updates?.join(", ") || "No bookmarks"}`
      }),
    "No users registered."
  );
}

function setupNavigation() {
  document.querySelectorAll(".nav-btn").forEach((button) => {
    button.addEventListener("click", () => activateSection(button.dataset.section));
  });

  document.getElementById("refresh-updates")?.addEventListener("click", loadUpdates);
  document.getElementById("refresh-deadlines")?.addEventListener("click", loadDeadlines);
  document.getElementById("refresh-users")?.addEventListener("click", loadUsers);
  document.getElementById("refresh-dashboard-updates")?.addEventListener("click", loadDashboard);
  document.getElementById("updates-search")?.addEventListener("input", (event) => applyUpdatesFilter(event.target.value));
  document.getElementById("deadlines-search")?.addEventListener("input", (event) => applyDeadlinesFilter(event.target.value));
}

function init() {
  setupNavigation();
  setDailyKitendawili();
  loadDashboard();
}

document.addEventListener("DOMContentLoaded", init);
