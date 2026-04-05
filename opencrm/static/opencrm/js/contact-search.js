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
    const tagsApiUrl = tagSelect.dataset.url;
    fetch(tagsApiUrl)
        .then((res) => res.json())
        .then((tags) => {
            tagSelect.innerHTML = '<option value="">All</option>';
            tags.forEach((tag) => {
                const option = document.createElement("option");
                option.value = tag.name;
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
        resultsList.style.display = "none"; // hide when no query
        return;
    }

    fetch(`${apiUrl}?${queryString}`)
        .then((res) => {
            if (!res.ok) throw new Error("Network error");
            return res.json();
        })
        .then((results) => {
            if (results.length === 0) {
                resultsList.innerHTML = `<li class="list-group-item">No results found</li>`;
            } else {
                resultsList.innerHTML = results
                    .map((c) => {
                        let hoverText = "";
                        if (c.email) hoverText += `Email: ${c.email}\n`;
                        if (c.phonenumber)
                            hoverText += `Phone: ${c.phonenumber}\n`;
                        if (c.tags.length)
                            hoverText += `Tags: ${c.tags.join(", ")}\n`;
                        if (c.last_contacted)
                            hoverText += `Last Contacted: ${new Date(c.last_contacted).toLocaleDateString()}\n`;

                        return `
                        <li class="list-group-item" title="${hoverText.trim()}">
                            <a href="${c.contact_url}" class="text-decoration-none">
                                ${c.fullname}${c.company ? " - " + c.company : ""}
                            </a>
                        </li>`;
                    })
                    .join("");
            }
            resultsList.style.display = "block"; // show results
        })
        .catch((err) => {
            console.error(err);
            resultsList.innerHTML =
                "<li class='list-group-item text-danger'>Error loading results</li>";
            resultsList.style.display = "block";
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

// --- Show results only when input is focused ---
input.addEventListener("focus", () => {
    if (resultsList.innerHTML.trim() !== "") {
        resultsList.style.display = "block";
    }
});

// --- Hide results when clicking outside ---
document.addEventListener("click", (event) => {
    if (!input.contains(event.target) && !resultsList.contains(event.target)) {
        resultsList.style.display = "none";
    }
});
