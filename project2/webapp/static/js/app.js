const NUMERIC_FIELDS = [
    "distancia_km", "dias_deslocacao", "n_atores_total", "n_atores_residentes",
    "n_tecnicos", "peso_cenario_kg", "n_figurinos", "receita_esperada",
    "lotacao_espaco", "percentagem_imprevistos", "mes_espetaculo",
];

const SELECT_FIELDS = [
    "tipo_espetaculo", "tipo_contrato", "local_evento",
    "regiao_geografica", "tipo_local",
];

const CHECKBOX_FIELDS = [
    "tem_portagens", "precisa_carrinha", "precisa_autocarro_privado",
    "precisa_alojamento", "catering_pago_pelo_cliente", "alojamento_pago_pelo_cliente",
    "tem_cenario_grande", "tem_costureira", "tem_maquilhagem",
    "tem_sistema_proprio", "marketing_pago_pelo_espaco",
];

const REGION_BY_LOCATION = {
    "Braga": "Norte",
    "Bragança": "Norte",
    "Porto": "Norte",
    "Viana do Castelo": "Norte",
    "Vila Real": "Norte",
    "Aveiro": "Centro",
    "Castelo Branco": "Centro",
    "Coimbra": "Centro",
    "Guarda": "Centro",
    "Leiria": "Centro",
    "Santarém": "Centro",
    "Viseu": "Centro",
    "Lisboa": "Lisboa",
    "Setúbal": "Lisboa",
    "Évora": "Alentejo",
    "Faro": "Algarve",
};

function formatEuro(value) {
    return new Intl.NumberFormat("pt-PT", {
        style: "currency",
        currency: "EUR",
        maximumFractionDigits: 0,
    }).format(value);
}

function readNumber(form, field) {
    const el = form.querySelector(`[name="${field}"]`);
    if (!el) {
        return 0;
    }

    const value = el.value === "" ? Number(el.min || 0) : Number(el.value);
    const minAttr = el.getAttribute("min");
    const maxAttr = el.getAttribute("max");
    const min = minAttr === null || minAttr === "" ? -Infinity : Number(minAttr);
    const max = maxAttr === null || maxAttr === "" ? Infinity : Number(maxAttr);

    if (!Number.isFinite(value)) {
        throw new Error(`${el.labels[0].textContent} tem de ser um número válido.`);
    }

    if (value < min || value > max) {
        throw new Error(`${el.labels[0].textContent} deve estar entre ${min} e ${max}.`);
    }

    return value;
}

function collectFormData(form) {
    const data = {};

    for (const field of NUMERIC_FIELDS) {
        data[field] = readNumber(form, field);
    }

    for (const field of SELECT_FIELDS) {
        const el = form.querySelector(`[name="${field}"]`);
        if (el) {
            data[field] = el.value;
        }
    }

    for (const field of CHECKBOX_FIELDS) {
        const el = form.querySelector(`[name="${field}"]`);
        data[field] = el && el.checked ? 1 : 0;
    }

    if (data.n_atores_residentes > data.n_atores_total) {
        throw new Error("O número de atores residentes não pode exceder o total de atores.");
    }

    data.dia_semana_espetaculo = 5;
    data.ano_espetaculo = 2025;
    data.regiao_geografica = REGION_BY_LOCATION[data.local_evento] || data.regiao_geografica || "Norte";

    return data;
}

function syncRegionFromLocation() {
    const form = document.getElementById("predictForm");
    if (!form) {
        return;
    }

    const locationEl = form.querySelector('[name="local_evento"]');
    const regionEl = form.querySelector('[name="regiao_geografica"]');
    if (!locationEl || !regionEl) {
        return;
    }

    regionEl.value = REGION_BY_LOCATION[locationEl.value] || "Norte";
}

function estimateCosts(data) {
    const distancia = data.distancia_km;
    const totalAtores = data.n_atores_total;
    const atoresResidentes = data.n_atores_residentes;
    const tecnicos = data.n_tecnicos;
    const totalEquipa = totalAtores + tecnicos;
    const dias = data.dias_deslocacao;

    const custoCombustivel = distancia * 0.15;
    const custoPortagens = data.tem_portagens ? distancia * 0.08 : 0;
    const custoCarrinha = data.precisa_carrinha ? 80 : 0;
    const custoTransporte = custoCombustivel + custoPortagens + custoCarrinha;

    const atoresExternos = Math.max(0, totalAtores - atoresResidentes);
    const custoCachets = atoresExternos * 150;

    const custoCenario =
        data.peso_cenario_kg * 2 +
        (data.tem_cenario_grande ? 200 : 0) +
        (data.tem_cenario_grande ? 100 : 0) +
        50;

    const custoFigurinos =
        data.n_figurinos * 30 +
        (data.tem_costureira ? 100 : 0) +
        (data.tem_maquilhagem ? 50 : 0);

    const custoCatering = data.catering_pago_pelo_cliente ? 0 : totalEquipa * 15 * Math.max(1, dias);
    const custoAlojamento =
        !data.precisa_alojamento || data.alojamento_pago_pelo_cliente
            ? 0
            : totalEquipa * 50 * Math.max(0, dias - 1);

    const custoTecnica =
        (data.tem_sistema_proprio ? 0 : 150) +
        (data.tem_sistema_proprio ? 0 : 100) +
        80 +
        80 +
        tecnicos * 60;

    const custoLicencas = 50;
    const custoMarketing = data.marketing_pago_pelo_espaco ? 0 : 100;

    const subtotal =
        custoTransporte +
        custoCachets +
        custoCenario +
        custoFigurinos +
        custoCatering +
        custoAlojamento +
        custoTecnica +
        custoLicencas +
        custoMarketing;

    const custoTotal = subtotal * (1 + data.percentagem_imprevistos / 100);
    return {
        custoTotal,
        margem: data.receita_esperada - custoTotal,
    };
}

function updateEstimate() {
    const form = document.getElementById("predictForm");
    const costEl = document.getElementById("estimatedCost");
    const marginEl = document.getElementById("estimatedMargin");
    const formStatus = document.getElementById("formStatus");

    if (!form || !costEl || !marginEl) {
        return;
    }

    try {
        const data = collectFormData(form);
        const estimate = estimateCosts(data);
        costEl.textContent = formatEuro(estimate.custoTotal);
        marginEl.textContent = formatEuro(estimate.margem);
        marginEl.classList.toggle("is-negative", estimate.margem < 0);
        marginEl.classList.toggle("is-positive", estimate.margem >= 0);
        if (formStatus) {
            formStatus.textContent = "";
        }
    } catch (error) {
        costEl.textContent = "--";
        marginEl.textContent = "--";
        marginEl.classList.remove("is-negative", "is-positive");
        if (formStatus) {
            formStatus.textContent = error.message;
        }
    }
}

async function submitPrediction(event) {
    event.preventDefault();

    const form = event.currentTarget;
    const submitBtn = document.getElementById("submitBtn");
    const formStatus = document.getElementById("formStatus");

    let data;
    try {
        data = collectFormData(form);
    } catch (error) {
        formStatus.textContent = error.message;
        return;
    }

    formStatus.textContent = "A gerar previsão...";
    submitBtn.disabled = true;

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
        predictForm.addEventListener("input", updateEstimate);
        predictForm.addEventListener("change", () => {
            syncRegionFromLocation();
            updateEstimate();
        });
        syncRegionFromLocation();
        updateEstimate();
    }
});
