import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_endpoints import simulate, ALL_MEASURES
from src.visualization_suite import generate_all_figures
from src.review_cycle_timing import compare_review_cycle_time


def test_12_measures_defined():
    assert len(ALL_MEASURES) == 12


def test_300_subjects_simulated():
    df = simulate()
    assert df["USUBJID"].nunique() == 8000


def test_all_12_figures_generated(tmp_path):
    df = simulate()
    paths = generate_all_figures(df, out_dir=str(tmp_path))
    assert len(paths) == 12
    for p in paths:
        assert os.path.exists(p)


def test_automated_generation_is_faster_than_manual(tmp_path):
    df = simulate()
    timing = compare_review_cycle_time(df, out_dir=str(tmp_path))
    assert timing["automated_time_sec"] < timing["manual_time_sec"]


def test_review_cycle_reduction_is_positive(tmp_path):
    df = simulate()
    timing = compare_review_cycle_time(df, out_dir=str(tmp_path))
    assert timing["review_cycle_reduction_pct"] > 0
