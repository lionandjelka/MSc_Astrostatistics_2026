# Instructor Guide

## Contact structure

Each week contains a **3-hour lecture notebook** and a **4-hour student lab**.
The lecture notebook is the primary teaching spine; the original Crete notebook(s)
are pre-class/in-class Learning Notebooks.

## Provider metadata now confirmed

The supplied dataset-reading notebook confirms:

- `field` = WFD or DDF;
- RA/Dec and orbital angles in degrees;
- total mass in solar masses;
- mass ratio \(M_2/M_1\);
- **observed orbital period in years**;
- light-curve timestamps in MJD;
- observed magnitude and uncertainty in mag;
- DRW/DHO truth definitions and units;
- full with-inputs file contains 1,200,000 simulations;
- blinded data exclude both `inputs` and `info`.

See `docs/DATA_DICTIONARY.md` and `docs/PROVIDER_NOTEBOOK_REVIEW.md`.

## Before semester launch

1. Keep the >500 GB parent dataset outside Git.
2. Pilot the proposed final-project targets using
   `instructor_tools/extract_lightcurve_features.py`. In particular, verify
   empirically whether mass ratio `q` is identifiable from the supplied observable
   features.
3. Prepare a common curated Week-7 light-curve subset from the supplied data.
4. Produce the common final-project split with a **secret seed**, unless the
   supplied blinded dataset is used directly.
5. Keep all truth tables outside student access.

No external clarification from the simulation providers is required for the
course. If metadata are not stated in the supplied dataset/notebook, treat them
as unknown and make that limitation explicit.

## Large-data rule

Do **not** read the entire with-inputs dataset into a list of pandas DataFrames
and concatenate it merely because reads occur in batches. That still materialises
the full dataset in RAM.

Use:
- Parquet column projection;
- true batch-by-batch processing;
- row-group filtering / curated subsets;
- compact derived feature tables.

## Lecture pacing

The notebooks contain 3-hour pacing. Do not read every Markdown paragraph
verbatim. Use derivations and code as anchors, with portions of the Crete
notebooks assigned before class.

## Lab pacing

Labs progress from reproduction → guided work → independent extension →
deliberate failure → interpretation. Student versions contain no solutions.

## Week 7

Emphasise the unit distinction:

- observed binary period: **years**;
- light-curve timestamps: **MJD (days)**;
- DRW/DHO timescales: **days**.

Students should perform explicit unit conversion before comparisons.

## Final project

Use both an IID blind set and a deliberately shifted blind set when possible.
Numerical performance is only one rubric component; calibration, coverage,
failure analysis and simulation-to-real reasoning are required.

The provider's own blinded-data convention is appropriate: `inputs` and
per-band `info` are absent.

## Suggested final presentation

8 minutes presentation + 4 minutes questions. Require one generative/pipeline
diagram, one performance figure, one calibration figure, one domain-shift result
and one failure case.
