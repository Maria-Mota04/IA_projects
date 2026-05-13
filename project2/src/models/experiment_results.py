import pandas as pd

def summarize_results(results):
    rows = []

    for exp, res in results.items():
        row = {"experiment": exp}

        for k, v in res.items():
            if k != "y_pred":
                row[k] = v

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv("outputs/experiments/results.csv", index=False)

    print(df)
    return df
