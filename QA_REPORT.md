# Final Course QA Report

- Valid notebooks: **29**
- Notebook validation errors: **0**
- Python source/code-cell syntax: checked separately before packaging.
- Duplicate Homework 2: **removed**.
- Week 8 variable-reuse bug: **fixed**.
- Final-project filenames/documentation: **synchronised**.

## Lecture notebook depth

| Notebook | Cells | Markdown words | Code cells |
|---|---:|---:|---:|
| `lectures/W01_LECTURE_Statistical_Thinking_Probability_and_the_Generative_View.ipynb` | 18 | 1543 | 3 |
| `lectures/W02_LECTURE_Hypothesis_Testing_Resampling_and_Multiple_Discovery.ipynb` | 18 | 1226 | 3 |
| `lectures/W03_LECTURE_Optimisation_Likelihood_and_Maximum-Likelihood_Estimation.ipynb` | 18 | 1066 | 3 |
| `lectures/W04_LECTURE_Bayesian_Inference_Priors_and_Posterior_Prediction.ipynb` | 18 | 1014 | 3 |
| `lectures/W05_LECTURE_MCMC_Degeneracy_and_Hierarchical_Population_Inference.ipynb` | 18 | 973 | 3 |
| `lectures/W06_LECTURE_Selection_Effects_Completeness_and_Survey_Population_Inferen.ipynb` | 18 | 1054 | 3 |
| `lectures/W07_LECTURE_Irregular_Time_Series_Periodicity_Red_Noise_and_Gaussian_Pro.ipynb` | 19 | 1082 | 3 |
| `lectures/W08_LECTURE_Machine_Learning_for_Astronomical_Inference.ipynb` | 19 | 1053 | 3 |
| `lectures/W09_LECTURE_Trustworthy_ML_Leakage_Calibration_Coverage_and_Domain_Shift.ipynb` | 19 | 1029 | 3 |
| `lectures/W10_LECTURE_Deep_Probabilistic_Models_and_Simulation-Based_Inference.ipynb` | 20 | 1116 | 3 |
| `lectures/W11_LECTURE_Active_Follow-up_Bayesian_Optimisation_Scaling_and_Scientifi.ipynb` | 20 | 1110 | 3 |

## Lab notebook depth

| Notebook | Cells | Markdown words | Code cells |
|---|---:|---:|---:|
| `labs/W01_LAB.ipynb` | 15 | 563 | 6 |
| `labs/W02_LAB.ipynb` | 15 | 561 | 6 |
| `labs/W03_LAB.ipynb` | 15 | 536 | 6 |
| `labs/W04_LAB.ipynb` | 15 | 531 | 6 |
| `labs/W05_LAB.ipynb` | 15 | 542 | 6 |
| `labs/W06_LAB.ipynb` | 15 | 528 | 6 |
| `labs/W07_LAB.ipynb` | 15 | 549 | 6 |
| `labs/W08_LAB.ipynb` | 15 | 537 | 6 |
| `labs/W09_LAB.ipynb` | 15 | 521 | 6 |
| `labs/W10_LAB.ipynb` | 15 | 527 | 6 |
| `labs/W11_LAB.ipynb` | 15 | 543 | 6 |

## Homeworks

| Notebook | Cells | Markdown words | Code cells |
|---|---:|---:|---:|
| `homeworks/HW01_Population_Description_and_Statistical_Evidence.ipynb` | 16 | 469 | 7 |
| `homeworks/HW02_Likelihood_Bayesian_Inference_and_MCMC.ipynb` | 18 | 453 | 8 |
| `homeworks/HW03_Selection_Changes_the_Inferred_Universe.ipynb` | 18 | 437 | 8 |
| `homeworks/HW04_Time-Domain_Inference_under_Irregular_Sampling.ipynb` | 16 | 401 | 7 |
| `homeworks/HW05_Trustworthy_Machine_Learning_under_Domain_Shift.ipynb` | 18 | 436 | 8 |
| `homeworks/HW06_Mini_SBI_From_Simulator_to_Calibrated_Posterior.ipynb` | 18 | 459 | 8 |

## Runtime note

The audit environment used to package this repository did not contain `pyarrow`, so Parquet-dependent notebook cells could not be executed end-to-end there. `pyarrow` is explicitly included in `course_requirements.txt`; run `python instructor_tools/preflight_check.py` after creating the course environment.

## Remaining scientific actions before student release

1. Confirm units and simulator definitions in `docs/DATA_DICTIONARY.md`.
2. Pilot identifiability of final-project targets, especially mass ratio `q`.
3. Prepare the common Week-7 light-curve subset.
4. Generate final-project IID and shifted blind sets with a private seed.
5. Add local deadlines, academic-integrity wording and grade-conversion rules.


## Provider-reading-notebook audit

The course was re-audited against the simulation providers' dataset-reading
notebook.

Confirmed and incorporated:
- full with-inputs dataset size: 1,200,000 simulations;
- `field` values WFD/DDF;
- RA/Dec and orbital angles in degrees;
- total mass in solar masses;
- mass ratio $M_2/M_1$;
- period is the **observed orbital period in years**;
- light-curve time is MJD;
- DRW/DHO truth definitions and units;
- provider blind data omit `inputs` and `info`.

Course-side data access remains intentionally more conservative than the
provider example: batches are processed/discarded or columns are projected,
rather than accumulating all batches and concatenating the full dataset in RAM.

Metadata not specified in the supplied material are intentionally left
unknown and are **not required** for course release. They include the exact
simulation priors, precise magnitude convention, additional Eddington-fraction
prescription, dependence among physical switches, and cadence details beyond
the actual stored time arrays / WFD-DDF labels. These must be stated as
limitations rather than inferred or invented.
