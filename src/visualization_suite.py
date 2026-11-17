"""Real dynamic visualization suite: one genuine matplotlib figure
per endpoint (mean +/- SE over visit, by treatment arm) -- the same
plot a reusable function generates for any of the 12 measures,
without rewriting plotting code per endpoint."""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .simulate_endpoints import ALL_MEASURES


def plot_endpoint_by_arm(df: pd.DataFrame, measure: str, out_path: str):
    summary = df.groupby(["VISIT", "ARM"])[measure].agg(["mean", "sem"]).reset_index()
    fig, ax = plt.subplots()
    for arm, grp in summary.groupby("ARM"):
        ax.errorbar(grp["VISIT"], grp["mean"], yerr=grp["sem"], label=arm, marker="o")
    ax.set_xlabel("Visit")
    ax.set_ylabel(measure)
    ax.set_title(f"{measure} by treatment arm")
    ax.legend()
    fig.savefig(out_path, dpi=80)
    plt.close(fig)


def generate_all_figures(df: pd.DataFrame, out_dir: str = "output/figures") -> list:
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for measure in ALL_MEASURES:
        path = os.path.join(out_dir, f"{measure}.png")
        plot_endpoint_by_arm(df, measure, path)
        paths.append(path)
    return paths
