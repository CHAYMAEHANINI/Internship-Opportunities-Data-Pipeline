const API_URL = "http://127.0.0.1:8000/internships";

let currentPage = 1;
const limit = 5;
const searchInput = document.getElementById("search");
const searchButton = document.getElementById("search-button");
const locationInput = document.getElementById("location");
const sourceInput = document.getElementById("source");
const workModeInput = document.getElementById("work-mode");
const internshipTypeInput = document.getElementById("internship-type");
const previousButton = document.getElementById("previous-button");
const nextButton = document.getElementById("next-button");
const pageInfo = document.getElementById("page-info");


function displayInternships(internships) {

    const container = document.getElementById("internships-container");

    container.innerHTML = "";

    internships.forEach(internship => {

        const card = document.createElement("div");

        card.className = "internship-card";

        card.innerHTML = `
            <h2>${internship.title}</h2>

            <p>
                <strong>Company:</strong>
                ${internship.company || "Not specified"}
            </p>

            <p>
                <strong>Location:</strong>
                ${internship.location || "Not specified"}
            </p>

            <p>
                <strong>Work mode:</strong>
                ${internship.work_mode || "Not specified"}
            </p>

            <p>
                <strong>Type:</strong>
                ${internship.internship_type || "Not specified"}
            </p>

            <p>
                <strong>Source:</strong>
                ${internship.source}
            </p>
            
            <p>
                <strong>Skills:</strong>
                ${internship.skills || "Not specified"}
            </p>

            <p>
               <strong>Published:</strong>
               ${internship.published_at || "Not specified"}
            </p>

            <a href="${internship.url}" target="_blank">
                View Offer
            </a>
        `;

        container.appendChild(card);
    });
}

async function loadLocations() {

    const response = await fetch("http://127.0.0.1:8000/locations");

    const result = await response.json();

    result.data.forEach(location => {

        const option = document.createElement("option");

        option.value = location;
        option.textContent = location;

        locationInput.appendChild(option);
    });
}

async function loadStatistics() {

    const response = await fetch("http://127.0.0.1:8000/stats");

    const result = await response.json();

    document.getElementById("total-count").textContent =
        result.total_opportunities;

    document.getElementById("source-count").textContent =
        result.total_sources;

    document.getElementById("location-count").textContent =
        result.total_locations;
}

function buildApiUrl() {

    const search = searchInput.value;
    const location = locationInput.value;
    const source = sourceInput.value;
    const workMode = workModeInput.value;
    const internshipType = internshipTypeInput.value;

    const params = new URLSearchParams({
        search: search,
        location: location,
        source: source,
        work_mode: workMode,
        internship_type: internshipType,
        page: currentPage,
        limit: limit
    });

    return `${API_URL}?${params.toString()}`;
}

async function loadInternships() {
    
    const container = document.getElementById("internships-container");

    container.innerHTML = "<p>Loading internships...</p>";

    const url = buildApiUrl();

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Failed to fetch internships");
        }

        const result = await response.json();
 
        if (result.data.length === 0) {
           container.innerHTML = "<p>No internships found.</p>";
           document.getElementById("total-count").textContent = 0;
           return;
        }

        displayInternships(result.data);

        document.getElementById("total-count").textContent = result.total;

        pageInfo.textContent = `Page ${result.page} of ${result.total_pages}`;
        previousButton.disabled = result.page <= 1;
        nextButton.disabled = result.page >= result.total_pages;



    } catch (error) {

        console.error("Error:", error);
        container.innerHTML = "<p>Unable to load internships.</p>";

    }
}
searchButton.addEventListener("click", () => {

    currentPage = 1;

    loadInternships();

});
searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        currentPage = 1;
        loadInternships();
    }
});
previousButton.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadInternships();
    }
});

nextButton.addEventListener("click", () => {
    currentPage++;
    loadInternships();
});

loadLocations();
loadStatistics();
loadInternships();