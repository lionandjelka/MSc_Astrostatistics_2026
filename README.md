# MSc Astrostatistics 2026

## Astrostatistics for the Survey Era: Probabilistic Inference, Time Series and AI

**Duration:** 11 weeks  
**Weekly contact:** 3 h lecture + 4 h hands-on  
**Total contact:** 77 hours

This is the student-facing course layer built around the **2025 Summer School for AstroStatistics in Crete** learning notebooks and a simulated binary-supermassive-black-hole dataset.

### Course principle

> **Physics → Population → Observation → Selection → Data → Inference → Physics**

The same binary-SMBH simulation is revisited throughout the semester so that statistical methods form one cumulative scientific investigation rather than disconnected exercises.

**Expanded edition:** each week now includes a substantive 3-hour lecture notebook and a paced 4-hour hands-on notebook. Six common homeworks and one common blind final project are student-facing and solution-free.

## Start here

1. Create the original Crete environment from the repository root: `conda env create -f environment.yml`.
2. Activate it: `conda activate astrostat25`.
3. Add the course data dependencies: `pip install -r MSc_Astrostatistics_2026/course_requirements.txt`.
4. Open `STUDENT_START_HERE.md`.
5. Do **not** add the 500+ GB simulation file to Git.

## Weekly course map

| Week | Topic | 3 h lecture | 4 h hands-on | Crete learning material |
|---:|---|---|---|---|
| 1 | Statistical Thinking, Probability and the Generative View | [Lecture](lectures/W01_LECTURE_Statistical_Thinking_Probability_and_the_Generative_View.ipynb) | [Hands-on](labs/W01_LAB.ipynb) | `01_Intro/Intro.ipynb` |
| 2 | Hypothesis Testing, Resampling and Multiple Discovery | [Lecture](lectures/W02_LECTURE_Hypothesis_Testing_Resampling_and_Multiple_Discovery.ipynb) | [Hands-on](labs/W02_LAB.ipynb) | `02_Hypothesis_Testing/Hypothesis.ipynb` |
| 3 | Optimisation, Likelihood and Maximum-Likelihood Estimation | [Lecture](lectures/W03_LECTURE_Optimisation_Likelihood_and_Maximum-Likelihood_Estimation.ipynb) | [Hands-on](labs/W03_LAB.ipynb) | `03_Optimization/Optimization.ipynb`, `04_MLE/MLE.ipynb` |
| 4 | Bayesian Inference, Priors and Posterior Prediction | [Lecture](lectures/W04_LECTURE_Bayesian_Inference_Priors_and_Posterior_Prediction.ipynb) | [Hands-on](labs/W04_LAB.ipynb) | `06_Bayesian/Bayesian_1.ipynb`, `06_Bayesian/Bayesian_2_Bayesball.ipynb`, `06_Bayesian/Bayesian_3.ipynb` |
| 5 | MCMC, Degeneracy and Hierarchical Population Inference | [Lecture](lectures/W05_LECTURE_MCMC_Degeneracy_and_Hierarchical_Population_Inference.ipynb) | [Hands-on](labs/W05_LAB.ipynb) | `07_MCMC/MCMC.ipynb` |
| 6 | Selection Effects, Completeness and Survey Population Inference | [Lecture](lectures/W06_LECTURE_Selection_Effects_Completeness_and_Survey_Population_Inferen.ipynb) | [Hands-on](labs/W06_LAB.ipynb) | `06_Bayesian/Bayesian_3.ipynb`, `07_MCMC/MCMC.ipynb` |
| 7 | Irregular Time Series, Periodicity, Red Noise and Gaussian Processes | [Lecture](lectures/W07_LECTURE_Irregular_Time_Series_Periodicity_Red_Noise_and_Gaussian_Pro.ipynb) | [Hands-on](labs/W07_LAB.ipynb) | `08_Gaussian_Processes/Gaussian_Processes.ipynb` |
| 8 | Machine Learning for Astronomical Inference | [Lecture](lectures/W08_LECTURE_Machine_Learning_for_Astronomical_Inference.ipynb) | [Hands-on](labs/W08_LAB.ipynb) | `05_ML/01-ML_Intro_and_Clustering.ipynb`, `05_ML/02-ML_Classification.ipynb` |
| 9 | Trustworthy ML: Leakage, Calibration, Coverage and Domain Shift | [Lecture](lectures/W09_LECTURE_Trustworthy_ML_Leakage_Calibration_Coverage_and_Domain_Shift.ipynb) | [Hands-on](labs/W09_LAB.ipynb) | `10_ML_Practices/ML_Practices.ipynb` |
| 10 | Deep Probabilistic Models and Simulation-Based Inference | [Lecture](lectures/W10_LECTURE_Deep_Probabilistic_Models_and_Simulation-Based_Inference.ipynb) | [Hands-on](labs/W10_LAB.ipynb) | `11_DL/01_DL_Intro.ipynb`, `11_DL/02_DL_Regression.ipynb`, `14_SBI/SBI_short.ipynb`, `14_SBI/SBI_full.ipynb` |
| 11 | Active Follow-up, Bayesian Optimisation, Scaling and Scientific Synthesis | [Lecture](lectures/W11_LECTURE_Active_Follow-up_Bayesian_Optimisation_Scaling_and_Scientifi.ipynb) | [Hands-on](labs/W11_LAB.ipynb) | `09_Bayesian_Optimization/Bayesian_Optimization.ipynb`, `13_GPU_parallelization/GPU_parallelization_answerkey.ipynb`, `14_SBI/SBI_exercise.ipynb` |

## Assessment suggestion

- Weekly lab checkpoints: **20%**
- Six homeworks: **30%** (5% each)
- Final blind project: **40%**
- Final presentation / scientific defence: **10%**

## Data

A small scalar teaching sample and schema/storage reports are included under `data/teaching/`.  The large `tenpct_dataset_withinputs.parquet` stays outside Git and is configured through the `SMBH_PARQUET` environment variable or `data/private/`.

## Important provenance

The original Crete notebooks are retained unchanged and remain governed by the repository's GNU GPLv3 licence and original authorship/credits.  New assessed tasks in this course use the binary-SMBH simulations and are not copies of Crete answer-key exercises.


## Provider dataset notebook

The simulation providers supplied a dataset-reading notebook that now anchors
the course metadata. It confirms the physical units, the 1.2-million-simulation
scale of the full with-inputs dataset, and that their blinded dataset removes
both physical `inputs` and per-band stochastic-process `info`.

See:
- `docs/DATA_DICTIONARY.md`
- `docs/PROVIDER_NOTEBOOK_REVIEW.md`
- `docs/DATA_ARCHITECTURE.md`


## Source-scope rule

The binary-SMBH component is taught strictly from the supplied dataset and
provider notebook. No additional provider clarification is assumed. Metadata
not stated in those materials are treated as unknown and reported as limitations;
see `docs/SOURCE_SCOPE.md`.


## Fully developed lectures

The eleven notebooks in `lectures/` are full three-hour teaching spines, not
topic outlines. They combine the relevant Crete learning material with detailed
derivations, probability/statistical reasoning, worked astronomical examples,
binary-SMBH applications, code demonstrations, diagnostics, board problems and
discussion checkpoints.

See `FULLY_DEVELOPED_LECTURE_QA.md` for the final lecture-depth audit.


## Equation rendering on GitHub

All course notebooks use GitHub-compatible Markdown math delimiters:

- inline mathematics: `$...$`
- displayed mathematics: `$$...$$`

This is intentionally preferred over `\(...\)` and `\[...\]` so equations
render reliably in GitHub notebook previews as well as Jupyter.
