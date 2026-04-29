function updateMeter(inputId, outputId) {
    const input = document.getElementById(inputId);
    const output = document.getElementById(outputId);

    if (!input || !output) {
        return;
    }

    const syncValue = () => {
        output.textContent = input.value;
    };

    input.addEventListener("input", syncValue);
    syncValue();
}

async function submitPrediction(event) {
    event.preventDefault();

    const form = event.currentTarget;
    const genre = document.getElementById("genre");
    const budget = document.getElementById("budget");
    const submitBtn = document.getElementById("submitBtn");
    const formStatus = document.getElementById("formStatus");

    if (!genre || !budget || !submitBtn || !formStatus) {
        return;
    }

    formStatus.textContent = "Generating recommendation...";
    submitBtn.disabled = true;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                genre: genre.value,
                budget: budget.value
            })
        });

        if (!response.ok) {
            throw new Error("Predict request failed");
        }

        const data = await response.json();
        const recommendation = data.recommendation || "Unknown recommendation";

        window.location.href = `/result?value=${encodeURIComponent(recommendation)}`;
    } catch (error) {
        formStatus.textContent = "Could not generate recommendation. Please try again.";
        submitBtn.disabled = false;
    }
}

window.addEventListener("DOMContentLoaded", () => {
    updateMeter("genre", "genreValue");
    updateMeter("budget", "budgetValue");

    const predictForm = document.getElementById("predictForm");
    if (predictForm) {
        predictForm.addEventListener("submit", submitPrediction);
    }
});
