const input = document.getElementById("contact-search");
const resultsList = document.getElementById("contact-results");
const apiUrl = input.dataset.url;

let debounceTimer; // store the timer

input.addEventListener("input", () => {
    const query = input.value;

    // clear previous timer
    clearTimeout(debounceTimer);

    // set a new timer
    debounceTimer = setTimeout(async () => {
        if (query.length < 1) {
            resultsList.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(
                `${apiUrl}?q=${encodeURIComponent(query)}`,
            );
            if (!response.ok) throw new Error("Network error");
            const results = await response.json();

            resultsList.innerHTML = results
                .map(
                    (c) => `
            <li>
                <a href="${c.contact_url}">
                    ${c.fullname}${c.company ? " - " + c.company : ""}
                </a>
            </li>
            `,
                )
                .join("");
        } catch (err) {
            console.error(err);
            resultsList.innerHTML = "<li>Error loading results</li>";
        }
    }, 200); // 500ms debounce
});
