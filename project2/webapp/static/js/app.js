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
    const submitBtn = document.getElementById("submitBtn");
    const formStatus = document.getElementById("formStatus");

    formStatus.textContent = "A gerar previsão...";
    submitBtn.disabled = true;

    const data = {};

    const numericFields = [
        "distancia_km", "dias_deslocacao", "n_atores_total", "n_atores_residentes",
        "n_tecnicos", "peso_cenario_kg", "n_figurinos", "receita_esperada",
        "lotacao_espaco", "percentagem_imprevistos", "mes_espetaculo",
    ];
    for (const field of numericFields) {
        const el = form.querySelector(`[name="${field}"]`);
        if (el && el.value !== "") {
            data[field] = Number(el.value);
        } else {
            data[field] = 0;
        }
    }

    const selectFields = [
        "tipo_espetaculo", "tipo_contrato", "local_evento",
        "regiao_geografica", "tipo_local",
    ];
    for (const field of selectFields) {
        const el = form.querySelector(`[name="${field}"]`);
        if (el) data[field] = el.value;
    }

    const checkboxFields = [
        "tem_portagens", "precisa_carrinha", "precisa_autocarro_privado",
        "precisa_alojamento", "catering_pago_pelo_cliente", "alojamento_pago_pelo_cliente",
        "tem_cenario_grande", "tem_costureira", "tem_maquilhagem",
        "tem_sistema_proprio", "marketing_pago_pelo_espaco",
    ];
    for (const field of checkboxFields) {
        const el = form.querySelector(`[name="${field}"]`);
        data[field] = el && el.checked ? 1 : 0;
    }

    data["dia_semana_espetaculo"] = 5;
    data["ano_espetaculo"] = 2025;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Erro na previsão");
        }

        const profitable = result.profitable;
        const probability = result.probability_profit;
        const custo = result.custo_total_estimado;

        window.location.href = `/result?value=${profitable ? "lucro" : "prejuizo"}&probability=${(probability * 100).toFixed(1)}&custo=${custo}`;

    } catch (error) {
        formStatus.textContent = "Erro: " + error.message;
        submitBtn.disabled = false;
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const predictForm = document.getElementById("predictForm");
    if (predictForm) {
        predictForm.addEventListener("submit", submitPrediction);
    }
});
