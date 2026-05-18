# Experiment Conclusions

This folder contains the trained models for each feature-ablation experiment.
Each experiment trains all registered classifiers, saves every fitted model, and highlights the model with the best F1-score.

## Overall Best Model

- Experiment: `no_binary`
- Model: `Random Forest`
- Accuracy: `0.9700`
- Precision: `0.9701`
- Recall: `0.9700`
- F1-score: `0.9700`
- ROC AUC: `0.9840`

## Results by Experiment

| Experiment | Best model | Features | Accuracy | Precision | Recall | F1 | ROC AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| no_binary | Random Forest | 78 | 0.9700 | 0.9701 | 0.9700 | 0.9700 | 0.9840 |
| no_geo_time | Random Forest | 69 | 0.9700 | 0.9701 | 0.9700 | 0.9700 | 0.9903 |
| no_aggregated_costs | AdaBoost | 82 | 0.9600 | 0.9600 | 0.9600 | 0.9600 | 0.9677 |
| structural_only | Gradient Boosting | 26 | 0.9600 | 0.9600 | 0.9600 | 0.9600 | 0.9749 |
| baseline | AdaBoost | 90 | 0.9600 | 0.9606 | 0.9600 | 0.9599 | 0.9879 |

## Interpretation

- The baseline uses all cleaned and engineered features and is the main reference.
- The `no_binary` experiment measures the impact of operational yes/no decisions.
- The `no_aggregated_costs` experiment removes total-cost and estimated-margin variables, checking how much the model depends on financial aggregates.
- The `no_geo_time` experiment checks whether location and time variables are important.
- The `structural_only` experiment tests whether early planning variables are enough for useful predictions.

## Main Conclusions

- Removing binary operational variables did not reduce performance. This suggests that the monetary and structural variables already capture most of the information carried by yes/no operational flags.
- Removing geographic and temporal variables also preserved performance, indicating that the model is not strongly dependent on region or date patterns in this dataset.
- Removing aggregated costs and estimated margin kept performance high, but slightly below the best experiments. These financial aggregates are useful, but the model can still infer profitability from lower-level cost and revenue information.
- The structural-only setup achieved strong results with far fewer features, showing that early planning variables can already support useful predictions.
- Since several experiments have very similar F1-scores, the simpler experiments should be considered if interpretability and robustness are more important than a marginal metric gain.

A strong drop in F1 after removing a group would indicate that the removed feature group carries important predictive information. In this run, no feature group caused a severe drop, which is a positive robustness sign.