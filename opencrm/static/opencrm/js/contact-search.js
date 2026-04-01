// contact-search.js
const input = document.getElementById("contact-search");
const resultsList = document.getElementById("contact-results");
const apiUrl = input.dataset.url;

// Filter inputs
const openTasksCheckbox = document.getElementById("filter-open-tasks");
const daysInput = document.getElementById("filter-days");
const tagSelect = document.getElementById("filter-tag");

let debounceTimer;

// --- Load all tags dynamically ---
if (tagSelect) {
    const tagsApiUrl = tagSelect.dataset.url; // e.g., set data-url="{% url 'opencrm:all_tags_api' %}" in HTML
    fetch(tagsApiUrl)
        .then((res) => res.json())
        .then((tags) => {
            // Clear existing options except "All"
            tagSelect.innerHTML = '<option value="">All</option>';
            tags.forEach((tag) => {
                const option = document.createElement("option");
                option.value = tag.name; // or tag.id if using IDs
                option.textContent = tag.name;
                tagSelect.appendChild(option);
            });
        })
        .catch((err) => console.error("Failed to load tags:", err));
}

// --- Build query parameters for the API call ---
function buildQueryParams() {
    const params = new URLSearchParams();

    if (input.value) params.append("q", input.value);
    if (openTasksCheckbox && openTasksCheckbox.checked)
        params.append("has_open_tasks", "1");
    if (daysInput && daysInput.value)
        params.append("not_contacted_days", daysInput.value);
    if (tagSelect && tagSelect.value) params.append("tag", tagSelect.value);

    return params.toString();
}

// --- Fetch and display results ---
function fetchResults() {
    const queryString = buildQueryParams();

    if (!queryString.includes("q") || input.value.length < 1) {
        resultsList.innerHTML = "";
        return;
    }

    fetch(`${apiUrl}?${queryString}`)
        .then((res) => {
            if (!res.ok) throw new Error("Network error");
            return res.json();
        })
        .then((results) => {
            // Inside your fetchResults mapping
            resultsList.innerHTML = results
                .map((c) => {
                    // Build the hover text
                    let hoverText = "";
                    if (c.email) hoverText += `Email: ${c.email}\n`;
                    if (c.phonenumber) hoverText += `Phone: ${c.phonenumber}\n`;
                    if (c.tags.length)
                        hoverText += `Tags: ${c.tags.join(", ")}\n`;
                    if (c.last_contacted)
                        hoverText += `Last Contacted: ${new Date(c.last_contacted).toLocaleDateString()}\n`;

                    return `
        <li title="${hoverText.trim()}">
            <a href="${c.contact_url}">
                ${c.fullname}${c.company ? " - " + c.company : ""}
            </a>
        </li>
        `;
                })
                .join("");
        })
        .catch((err) => {
            console.error(err);
            resultsList.innerHTML = "<li>Error loading results</li>";
        });
}

// --- Debounced search on typing ---
input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(fetchResults, 200);
});

// --- Update search when filters change ---
if (openTasksCheckbox)
    openTasksCheckbox.addEventListener("change", fetchResults);
if (daysInput)
    daysInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchResults, 200);
    });
if (tagSelect) tagSelect.addEventListener("change", fetchResults);
