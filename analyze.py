# analyze.py
# Make KM-Waechter smarter. The 80% rule only warns you once a car is nearly worn. Here we find
# which cars are most likely to break down SOON, from their history, and rank them by risk, so the
# fleet team fixes the risky ones first.
#
# SUMMARY: Total mileage (odometer_km) and age_years do NOT separate the two groups (p ~ 0.98
# and 0.99, Cohen's d ~ 0.00-0.01) -- the "obvious" answer is a dead end. What actually predicts
# a breakdown is neglect and hard use since the last service: km_since_service (d=1.10),
# avg_daily_km (d=0.65), and load_factor (d=0.54).

from __future__ import annotations

import pandas as pd

HISTORY_FILE = "fleet_history.csv"

# Only columns that showed a real, statistically significant gap between the broke_down=1 and
# broke_down=0 groups go into the score. odometer_km and age_years are deliberately excluded --
# see the group comparison printed below for why.
RISK_FEATURES = {
    "km_since_service": 0.48,  # how overdue for a service (strongest signal, d=1.10)
    "avg_daily_km": 0.28,      # how hard/often the car is driven (d=0.65)
    "load_factor": 0.24,       # how heavily loaded the car runs (d=0.54)
}


def compare_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Compare broke_down vs not, column by column, with a t-test and an effect size.

    This is the "follow the data" step: it is what shows total mileage and age are not
    actually predictive, even though they look like the obvious candidates.
    """
    from scipy import stats

    candidate_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
    rows = []
    for col in candidate_cols:
        healthy = df.loc[df["broke_down"] == 0, col]
        broke = df.loc[df["broke_down"] == 1, col]
        _, p_value = stats.ttest_ind(healthy, broke, equal_var=False)
        pooled_std = ((healthy.std() ** 2 + broke.std() ** 2) / 2) ** 0.5
        cohens_d = (broke.mean() - healthy.mean()) / pooled_std
        rows.append(
            {
                "column": col,
                "mean_no_breakdown": round(healthy.mean(), 2),
                "mean_breakdown": round(broke.mean(), 2),
                "p_value": round(p_value, 4),
                "cohens_d": round(cohens_d, 2),
            }
        )
    return pd.DataFrame(rows).set_index("column")


def risk_score(df: pd.DataFrame) -> pd.Series:
    """Return a 0-100 risk score per car from the predictive columns only.

    Each feature is min-max normalized to 0-1, then combined with weights roughly
    proportional to its effect size (see RISK_FEATURES), and scaled to 0-100.
    """
    normalized = pd.DataFrame(index=df.index)
    for feature in RISK_FEATURES:
        lo, hi = df[feature].min(), df[feature].max()
        normalized[feature] = (df[feature] - lo) / (hi - lo)
    weighted = sum(normalized[feature] * weight for feature, weight in RISK_FEATURES.items())
    return (weighted * 100).round(1)


def main() -> None:
    df = pd.read_csv(HISTORY_FILE)

    print("Group comparison: broke_down vs not, column by column")
    print("=" * 70)
    print(compare_groups(df))
    print()
    print("odometer_km and age_years barely differ between the two groups (p > 0.9,")
    print("Cohen's d ~ 0) -- total mileage and age are NOT predictive here. What separates")
    print("the groups is how overdue the car is and how hard it's driven since then.")
    print()

    df["risk_score"] = risk_score(df)
    ranked = df.sort_values("risk_score", ascending=False)

    print("Fleet ranked by breakdown risk (highest first)")
    print("=" * 70)
    print(ranked[["car_id", "risk_score", "km_since_service", "avg_daily_km", "load_factor", "broke_down"]]
          .to_string(index=False))


if __name__ == "__main__":
    main()
