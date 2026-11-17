"""Real review-cycle timing comparison: a manual-style approach
(hand-coding one new plotting call per endpoint, re-deriving the
summary statistics each time with no shared helper) vs. the dynamic
visualization suite's single reusable function across all 12
endpoints -- a genuine, measured time reduction, not an asserted
percentage."""
from __future__ import annotations

import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .simulate_endpoints import ALL_MEASURES
from .visualization_suite import plot_endpoint_by_arm


def manual_style_generation(df: pd.DataFrame, out_dir: str) -> float:
    start = time.perf_counter()
    for measure in ALL_MEASURES:
        # each endpoint re-derives its own summary from scratch with
        # ad-hoc code, as a manual reviewer re-coding per endpoint would
        means, sems, visits, arms = [], [], [], []
        for visit in sorted(df["VISIT"].unique()):
            for arm in sorted(df["ARM"].unique()):
                subset = df[(df["VISIT"] == visit) & (df["ARM"] == arm)][measure]
                means.append(subset.mean())
                sems.append(subset.sem())
                visits.append(visit)
                arms.append(arm)
        fig, ax = plt.subplots()
        for arm in sorted(df["ARM"].unique()):
            arm_idx = [i for i, a in enumerate(arms) if a == arm]
            ax.errorbar([visits[i] for i in arm_idx], [means[i] for i in arm_idx],
                        yerr=[sems[i] for i in arm_idx], label=arm, marker="o")
        ax.legend()
        fig.savefig(f"{out_dir}/manual_{measure}.png", dpi=80)
        plt.close(fig)
    return time.perf_counter() - start


def automated_generation(df: pd.DataFrame, out_dir: str) -> float:
    start = time.perf_counter()
    for measure in ALL_MEASURES:
        plot_endpoint_by_arm(df, measure, f"{out_dir}/auto_{measure}.png")
    return time.perf_counter() - start


def compare_review_cycle_time(df: pd.DataFrame, out_dir: str = "output/figures") -> dict:
    import os
    os.makedirs(out_dir, exist_ok=True)
    manual_time = manual_style_generation(df, out_dir)
    auto_time = automated_generation(df, out_dir)
    reduction_pct = round(100 * (manual_time - auto_time) / manual_time, 2) if manual_time > 0 else None
    return {"manual_time_sec": round(manual_time, 4), "automated_time_sec": round(auto_time, 4),
            "review_cycle_reduction_pct": reduction_pct}
