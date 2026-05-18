FEATURE_GROUPS = {
    "binary_operational": [
        "tem_portagens",
        "precisa_carrinha",
        "precisa_autocarro_privado",
        "tem_cenario_grande",
        "tem_costureira",
        "tem_maquilhagem",
        "catering_pago_pelo_cliente",
        "alojamento_pago_pelo_cliente",
        "precisa_alojamento",
        "tem_sistema_proprio",
        "marketing_pago_pelo_espaco",
        "n_carros_extra",
    ],
    "aggregated_costs": [
        "custo_total_transporte_eur",
        "custo_total_cenario_eur",
        "custo_total_figurinos_eur",
        "custo_total_tecnica_eur",
        "custo_total_alimentacao_alojamento_eur",
        "custo_total_eur",
        "custo_imprevistos_eur",
        "lucro_estimado_eur",
    ],
    "geo_time": [
        "mes_espetaculo",
        "dia_semana_espetaculo",
        "ano_espetaculo",
        "local_evento_",
        "regiao_geografica_",
    ],
}

STRUCTURAL_FEATURES = [
    "distancia_km",
    "n_atores_total",
    "n_atores_residentes",
    "n_atores_externos",
    "n_tecnicos",
    "total_pessoas_equipa",
    "peso_cenario_kg",
    "n_figurinos",
    "dias_deslocacao",
    "lotacao_espaco",
    "receita_esperada",
    "percentagem_imprevistos",
    "tipo_espetaculo_",
    "tipo_contrato_",
    "tipo_local_",
]

EXPERIMENTS = {
    "baseline": {
        "description": "All cleaned and engineered features.",
        "drop": [],
        "keep": None,
    },
    "no_binary": {
        "description": "Remove binary operational decision variables.",
        "drop": FEATURE_GROUPS["binary_operational"],
        "keep": None,
    },
    "no_aggregated_costs": {
        "description": "Remove aggregated cost and estimated margin features.",
        "drop": FEATURE_GROUPS["aggregated_costs"],
        "keep": None,
    },
    "no_geo_time": {
        "description": "Remove geographic and temporal features.",
        "drop": FEATURE_GROUPS["geo_time"],
        "keep": None,
    },
    "structural_only": {
        "description": "Keep only early planning and structural variables.",
        "drop": [],
        "keep": STRUCTURAL_FEATURES,
    },
}
