const list = document.getElementById("tasks");
const apiUrl = list.dataset.url; // <-- get URL from template

function timeUntil(dueDateStr) {
    if (!dueDateStr) return "No due date";

    const now = new Date();
    const due = new Date(dueDateStr);
    const diffMs = due - now;

    if (diffMs <= 0) return "Overdue";

    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor((diffMs / (1000 * 60 * 60)) % 24);
    const diffMinutes = Math.floor((diffMs / (1000 * 60)) % 60);

    if (diffDays > 0) return `in ${diffDays} day${diffDays > 1 ? "s" : ""}`;
    if (diffHours > 0) return `in ${diffHours} hour${diffHours > 1 ? "s" : ""}`;
    return `in ${diffMinutes} min${diffMinutes > 1 ? "s" : ""}`;
}

function renderTasks(tasks) {
    if (!tasks.length) {
        list.innerHTML = `
            <li class="list-group-item text-muted">
                No upcoming tasks
            </li>`;
        return;
    }

    list.innerHTML = tasks
        .map((t) => {
            const timeText = timeUntil(t.due_date);

            // Badge color depending on urgency
            let badgeClass = "bg-secondary";
            if (timeText === "Overdue") {
                badgeClass = "bg-danger";
            } else if (timeText.includes("min") || timeText.includes("hour")) {
                badgeClass = "bg-warning text-dark";
            }

            return `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    
                    <div>
                        <a href="${t.contact_url}" class="fw-semibold text-decoration-none">
                            ${t.contact_name}
                        </a>
                        <span class="text-muted">•</span>
                        <a href="${t.task_url}" class="text-decoration-none">
                            ${t.task_text}
                        </a>
                    </div>

                    <span class="badge ${badgeClass}" title="${t.due_date}">
                        ${timeText}
                    </span>

                </li>
            `;
        })
        .join("");
}

// --- Fetch tasks ---
function loadTasks() {
    fetch(apiUrl)
        .then((res) => {
            if (!res.ok) throw new Error("Network error");
            return res.json();
        })
        .then(renderTasks)
        .catch((err) => {
            console.error(err);
            list.innerHTML = `
                <li class="list-group-item text-danger">
                    Error loading tasks
                </li>`;
        });
}

// Initial load
loadTasks();
