# Data Architecture

## Provider-confirmed scale

The provider reading notebook states that `full_dataset_withinputs.parquet`
contains **1,200,000 simulations**. The 10% dataset is therefore expected to
contain roughly 120,000 systems.

The full parent store is not committed to Git.

## Tier 1 — full simulation store

Contains:

- physical `inputs`;
- nested `u,g,r,i,z,y` light curves (`time`, `obs mag`, `mag err`);
- per-band DRW/DHO `info` truth.

The provider's blinded dataset excludes `inputs` and `info`.

## Tier 2 — scalar teaching catalogue

`data/teaching/scalar_sample.parquet` (10,000 rows) supports Weeks 1–6 and
methodological demonstrations.

For larger population exercises, the instructor may create a compact scalar
catalogue retaining all ~120k rows of the 10% file while projecting away the
heavy light-curve arrays.

## Tier 3 — curated raw light curves

Prepare a common Week-7 subset containing a manageable number of full
\(ugrizy\) light curves. Timestamps are MJD; the physical input period is the
**observed orbital period in years**.

Per-band `info` should remain private until students finish inference and are
ready to validate against truth.

## Tier 4 — compact observable feature table

Create with `instructor_tools/extract_lightcurve_features.py`. Suitable for
ML/SBI and the final project.

If created from a with-inputs file, the instructor's preparation table may
temporarily retain truths. Student feature files must not contain `inputs`,
`info`, or hidden proxies created directly from them.

## Tier 5 — common blind final-project split

Create with `instructor_tools/prepare_blind_project.py`, or use a provider-supplied
blinded dataset if it supports the chosen project targets and split design.

The local project tool produces:

- `final_train.parquet`
- `final_blind_iid_features.parquet`
- `final_blind_shift_features.parquet`
- `final_blind_iid_truth_PRIVATE.parquet`
- `final_blind_shift_truth_PRIVATE.parquet`

Keep both truth files outside student access.

The shifted blind set is a stress test and is not a substitute for validating
the simulation family against real survey data.
