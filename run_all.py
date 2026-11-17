import json
import os

from src.simulate_endpoints import simulate, ALL_MEASURES
from src.visualization_suite import generate_all_figures
from src.review_cycle_timing import compare_review_cycle_time


def main():
    df = simulate()
    figure_paths = generate_all_figures(df)
    timing = compare_review_cycle_time(df)

    summary = {"n_subjects": df["USUBJID"].nunique(), "n_measures": len(ALL_MEASURES),
               "n_figures_generated": len(figure_paths), "review_cycle_timing": timing}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
