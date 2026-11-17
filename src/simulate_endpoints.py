"""Simulate longitudinal data for 12 real clinical trial endpoints
(6 efficacy, 6 safety) across 300 subjects over 5 visits -- the real
input a visualization suite renders."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_SUBJECTS = 8000
N_VISITS = 5
SEED = 1033

EFFICACY_MEASURES = ["symptom_score", "function_score", "qol_score", "pain_score", "mobility_score", "fatigue_score"]
SAFETY_MEASURES = ["alt_level", "ast_level", "creatinine", "heart_rate", "systolic_bp", "wbc_count"]
ALL_MEASURES = EFFICACY_MEASURES + SAFETY_MEASURES


def simulate(n_subjects: int = N_SUBJECTS, n_visits: int = N_VISITS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    records = []
    for subj in range(n_subjects):
        arm = rng.choice(["Active", "Placebo"])
        baseline = {m: rng.normal(50, 10) for m in ALL_MEASURES}
        for visit in range(n_visits):
            trend = -2 * visit if arm == "Active" else -0.5 * visit
            row = {"USUBJID": f"S-{subj:04d}", "ARM": arm, "VISIT": visit}
            for m in ALL_MEASURES:
                row[m] = round(baseline[m] + trend + rng.normal(0, 3), 2)
            records.append(row)
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
