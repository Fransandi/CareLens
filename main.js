// Wait for the DOM to fully load before executing the script
document.addEventListener("DOMContentLoaded", () => {
  let index = parseInt(getQueryParam("patient") || "1"); // Get the patient index from the query parameter or default to 1
  if (index) {
    loadFiles(index); // Load patient data for the selected index
  }
  generatePatientButtons(index); // Generate buttons for selecting patients
  setupTabs(); // Set up tab navigation functionality
});

// Get a query parameter value from the URL
function getQueryParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

// Set a query parameter in the URL without reloading the page
function setQueryParam(key, value) {
  const url = new URL(window.location);
  url.searchParams.set(key, value);
  window.history.pushState({}, "", url);
}

// Set up tab navigation functionality
function setupTabs() {
  document.querySelectorAll('[id^="tab"]').forEach((tab) => {
    tab.addEventListener("click", () => {
      // Hide all tab content sections
      document
        .querySelectorAll(".tab-content")
        .forEach((tc) => tc.classList.add("hidden"));
      // Remove the "active" class from all tabs
      document
        .querySelectorAll('[id^="tab"]')
        .forEach((t) => t.classList.remove("active"));
      // Show the selected tab's content and mark the tab as active
      const tabId = tab.id.replace("tab", "");
      document
        .getElementById(tabId.charAt(0).toLowerCase() + tabId.slice(1))
        .classList.remove("hidden");
      tab.classList.add("active");
    });
  });
}

// Load patient data from a JSON file and populate the UI
async function loadFiles(index) {
  try {
    // Fetch the JSON file for the selected patient
    const responseJson = await fetch(
      `data/llm_responses/patient_${index}.json`
    ).then((r) => r.json());

    // Update the summary section with the patient's medical history
    document.getElementById("summaryTitle").textContent = `Patient ${index}`;
    document.getElementById("summaryText").textContent = responseJson.summary;

    // Clear the responses container
    const responsesContainer = document.getElementById("responses");
    responsesContainer.innerHTML = "";

    // Populate the responses section with questions and answers
    responseJson.questions.forEach((qa) => {
      const card = document.createElement("div");
      card.className = "card";

      // Create the card header with the question title and possible answers
      const cardHeader = document.createElement("div");
      cardHeader.className = "flex items-center justify-between pb-2";

      const questionTitle = document.createElement("h2");
      questionTitle.className = "card-title";
      questionTitle.textContent = `${qa.id}. ${qa.question}`;

      const badgesContainer = document.createElement("div");
      badgesContainer.className = "flex flex-wrap justify-end gap-2 mt-2";
      qa.possible_answers.forEach((answer) => {
        const badge = document.createElement("div");
        badge.className =
          "inline-block bg-gray-200 text-gray-800 text-sm font-medium px-2.5 py-0.5 rounded";
        badge.textContent = answer;
        badgesContainer.appendChild(badge);
      });

      cardHeader.appendChild(questionTitle);
      cardHeader.appendChild(badgesContainer);
      card.appendChild(cardHeader);

      // Create the answers container with demographic badges and reasoning
      const answersContainer = document.createElement("div");
      answersContainer.className = "space-y-3";

      qa.answers.forEach(({ gender, race, income, answer, reasoning }) => {
        const blockContainer = document.createElement("div");
        blockContainer.className =
          "pl-1 rounded bg-gradient-to-b from-blue-600 to-violet-700";

        const block = document.createElement("div");
        block.className = "bg-gray-100 p-4 roundedshadow-md";

        // Generate demographic badges dynamically
        const badgesHTML = [gender, race, income]
          .map((part) => {
            const label = part.toLowerCase();
            const labelColorMap = {
              male: "blue",
              female: "pink",
              white: "gray",
              black: "indigo",
              hispanic: "orange",
              high: "green",
              low: "red",
            };
            const colorClass = labelColorMap[label] || "gray";
            return `<div class="inline-block bg-${colorClass}-200 text-${colorClass}-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded capitalize">${label} ${
              ["High", "Low"].includes(part) ? "Income" : ""
            }</div>`;
          })
          .join("");

        // Populate the block with the answer, reasoning, and badges
        block.innerHTML = `<div class="text-gray-800 text-xl mb-2">${answer}</div><div class="text-gray-600 mb-2">${reasoning}</div><div class="flex flex-wrap gap-1">${badgesHTML}</div>`;
        blockContainer.appendChild(block);
        answersContainer.appendChild(blockContainer);
      });

      card.appendChild(answersContainer);
      responsesContainer.appendChild(card);
    });

    // Populate the charts section with demographic and aggregated charts
    populateCharts(responseJson, index);
  } catch (err) {
    // Display an error message if the data fails to load
    document.getElementById("main").innerHTML =
      "<p class='text-red-600'>❌ Error loading patient data.</p>";
  }
}

// Generate buttons for selecting patients
function generatePatientButtons(currentIndex) {
  const patientButtonsContainer = document.getElementById("patientButtons");
  for (let i = 1; i <= 10; i++) {
    const btn = document.createElement("button");
    btn.textContent = `Patient ${i}`;
    btn.className = `px-3 py-1 rounded text-sm font-medium shadow transition ${
      i === currentIndex
        ? "bg-blue-600 text-white"
        : "bg-white text-blue-700 border border-blue-200 hover:bg-blue-100"
    }`;
    btn.addEventListener("click", () => {
      if (i !== currentIndex) {
        setQueryParam("patient", i); // Update the query parameter
        location.reload(); // Reload the page to load the selected patient's data
      }
    });
    patientButtonsContainer.appendChild(btn);
  }
}

// Populate the charts section with demographic and aggregated charts
function populateCharts(responseJson, index) {
  const chartsSection = document.getElementById("charts");
  chartsSection.innerHTML = "";

  // Loop through the first 5 questions and generate charts
  responseJson.questions.slice(0, 5).forEach((qa) => {
    const questionContainer = document.createElement("div");
    questionContainer.className = "card";
    chartsSection.appendChild(questionContainer);

    // Add a title for the question
    const questionTitle = document.createElement("h2");
    questionTitle.className = "card-title";
    questionTitle.textContent = `${qa.id}. ${qa.question}`;
    questionContainer.appendChild(questionTitle);

    // Add the demographic chart for the question
    const img = document.createElement("img");
    img.src = `data/distribution_analysis/patient_${index}/question_${qa.id}.png`;
    img.alt = `Demographic distribution for Question ${qa.id}`;
    img.className = "max-w-full";
    const figure = document.createElement("figure");
    figure.className = "p-4 shadow-md mb-6";
    figure.appendChild(img);
    questionContainer.appendChild(figure);

    // Add the aggregated chart for the question
    const img2 = document.createElement("img");
    img2.src = `data/distribution_analysis/aggregated/question_${qa.id}_aggregated.png`;
    img2.alt = `Aggregated Demographic distribution for Question ${qa.id}`;
    img2.className = "max-w-full";
    const figure2 = document.createElement("figure");
    figure2.className = "p-4 shadow-md mb-6";
    figure2.appendChild(img2);
    questionContainer.appendChild(figure2);
  });
}
