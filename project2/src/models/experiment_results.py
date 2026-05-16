import pandas as pd
from pathlib import Path


def summarize_results(results):
    rows = []

    for exp, res in results.items():
        row = {"experiment": exp}

        for k, v in res.items():
            if k != "y_pred":
                row[k] = v

        rows.append(row)

    df = pd.DataFrame(rows)
    OUTPUT_PATH = Path("outputs/experiments/results.csv")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(df)
    return df
