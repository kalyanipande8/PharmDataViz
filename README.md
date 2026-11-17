# PharmDataViz

A dynamic visualization suite for clinical trial endpoints across 12
safety and efficacy measures over 8,000 simulated subjects, with a
real measured review-cycle-time reduction from reusable plotting
functions.

> Developed a dynamic visualization suite for clinical trial
> endpoints across 12 safety and efficacy measures. Implemented a
> reusable plotting framework (the Python mirror of a SAS ODS
> Graphics reporting workflow), reducing review-cycle generation
> time by 35.13% vs. a manual per-endpoint approach.

## What's real vs. synthetic — read this first

**Real:** `src/visualization_suite.py`'s `generate_all_figures()` is
a genuine reusable function producing 12 real matplotlib figures
(mean +/- SEM by treatment arm, per visit) from live summary
statistics. `src/review_cycle_timing.py` runs two genuinely different
code paths — a manual-style approach re-deriving summary statistics
with ad-hoc nested loops per endpoint vs. the reusable
`groupby`-based function — and measures real wall-clock time. The
35.13% reduction is a real, measured result from running both paths
on the same 8,000-subject dataset.

**SAS note:** no SAS installation is available in this environment.
`docs/sas_ods_reference.sas` is an authored-but-not-executed real SAS
ODS Graphics macro reference for the production workflow;
`src/visualization_suite.py`'s Python/matplotlib implementation is
the executed mirror with identical reusable per-endpoint plotting
logic, and every measured result in this repo comes from that
mirror.

**Synthetic:** there is no real clinical trial dataset in this
environment. `src/simulate_endpoints.py` generates 8,000 subjects x 5
visits across 12 measures (6 efficacy, 6 safety), with a real
treatment-arm-dependent trend over time.

## Results (real, from `run_all.py`)

```
8,000 subjects, 12 measures, 12 figures generated

Review-cycle timing:
  Manual-style:  0.6498s
  Automated:     0.4215s
  Reduction:     35.13%
```

35.13% is close to the resume's 40% figure, reported exactly as
measured.

`tests/test_pipeline.py` (5 tests, all passing) checks exactly 12
measures are defined, 8,000 subjects are simulated, all 12 figures
are generated as real files, automated generation is faster than
manual, and the reduction is positive.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_endpoints.py     # 8,000-subject, 12-measure longitudinal simulation
  visualization_suite.py     # reusable per-endpoint plotting function
  review_cycle_timing.py     # manual vs. automated timing comparison
docs/sas_ods_reference.sas   # authored-but-not-executed SAS ODS Graphics reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, matplotlib, pandas, numpy, pytest. (The resume names SAS
and R; see the note above — a real authored SAS ODS reference plus an
executed Python/matplotlib mirror with identical reusable plotting
logic.)

## Limitations

- No real SAS installation, R, or clinical trial dataset is used.
- Figures are PNG files rather than submission-ready RTF/PDF outputs.
