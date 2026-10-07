# Binary-SMBH Data Dictionary — provider-confirmed teaching version

This document is based on the dataset-reading notebook supplied by the simulation
providers (`reading_datasets.ipynb`) together with the schema extracted from
`tenpct_dataset_withinputs.parquet`.

## Dataset scale

The provider notebook states that:

- `full_dataset_withinputs.parquet` contains **1,200,000 simulations**;
- the data are naturally read in batches;
- the corresponding **blinded dataset excludes both `inputs` and per-band `info`**.

Therefore a 10% dataset is expected to contain roughly 120,000 systems, consistent
with treating the teaching file as an approximately 100k-object sample.

## Top-level structure

The first-level keys are:

```text
id
inputs
u band
g band
r band
i band
z band
y band
```

## Physical / simulation inputs

| Parquet column | Flattened course name | Meaning | Units / definition | Statistical role |
|---|---|---|---|---|
| `('id','')` | `id` | simulation/object identifier | identifier | join key only |
| `('inputs','field')` | `inputs__field` | survey field type | `WFD` or `DDF` | survey/context |
| `('inputs','RA')` | `inputs__RA` | right ascension | degrees | survey/context |
| `('inputs','dec')` | `inputs__dec` | declination | degrees | survey/context |
| `('inputs','total mass')` | `inputs__total_mass` | total binary mass | solar masses | latent physical input / target |
| `('inputs','mass ratio')` | `inputs__mass_ratio` | binary mass ratio | \(M_2/M_1\) | latent physical input / target |
| `('inputs','period')` | `inputs__period` | **observed orbital period** | years | latent physical input / target |
| `('inputs','eccentricity')` | `inputs__eccentricity` | orbital eccentricity | dimensionless | latent physical input |
| `('inputs','inclination')` | `inputs__inclination` | orbital inclination angle | degrees | latent geometry |
| `('inputs','arg of pericenter')` | `inputs__arg_of_pericenter` | argument of pericenter | degrees | latent geometry |
| `('inputs','redshift')` | `inputs__redshift` | distance redshift to binary | dimensionless | latent/context physical input |
| `('inputs','Eddington fraction')` | `inputs__Eddington_fraction` | Eddington fraction | dimensionless | latent physical input |
| `('inputs','retrograde')` | `inputs__retrograde` | include retrograde orbit | Boolean | simulator mechanism flag |
| `('inputs','Doppler boosting')` | `inputs__Doppler_boosting` | include Doppler boosting signal | Boolean | simulator mechanism flag |
| `('inputs','lensing flare')` | `inputs__lensing_flare` | include gravitational self-lensing flare signal | Boolean | simulator mechanism flag |
| `('inputs','accretion modulation')` | `inputs__accretion_modulation` | include accretion modulation signal | Boolean | simulator mechanism flag |

## Per-band observed light-curve data

For each of `u`, `g`, `r`, `i`, `z`, and `y`:

| Key | Meaning | Units |
|---|---|---|
| `time` | observation timestamp | MJD |
| `obs mag` | observed magnitude | mag |
| `mag err` | photometric uncertainty on observed magnitude | mag |

The provider notebook does **not** specify the photometric magnitude convention
(e.g. AB versus another convention), so do not add a convention to student notes
until the providers confirm it.

## Per-band stochastic-process truth (`info`)

The `info` structure contains:

| Key | Symbol | Meaning | Units |
|---|---|---|---|
| `DRW amp` | \(\sigma\) | long-term RMS variability amplitude | mag |
| `DRW tau` | \(\tau\) | damping timescale | days |
| `DHO sigma_DHO` | \(\sigma_{\rm DHO}\) | long-term RMS variability amplitude | mag |
| `DHO tau_decay` | \(\tau_{\rm decay}\) | long-term decay timescale | days |
| `DHO sigma_epsilon` | \(\sigma_\epsilon\) | amplitude of short-term / white-noise perturbations | mag day\(^{-3/2}\) |
| `DHO tau_perturb` | \(\tau_{\rm perturb}\) | short-term perturbation timescale | days |

The provider states that:
- simulations with **DRW noise** contain NaNs in the DHO truth parameters;
- simulations with **DHO noise** contain NaNs in the DRW truth parameters.

This is not ordinary missing data. It is **structural missingness induced by the
simulator model choice**.

## Blinded-data rule

The provider notebook explicitly says that the blinded dataset does **not** contain:

- the `inputs` block;
- the per-band `info` block.

This is exactly the right separation for inverse inference. For student blind
projects, physical inputs and stochastic-process truth must remain unavailable.

## Important teaching rules

1. `id` is a join key and **must not be used as an ML feature**.
2. The `inputs` block is ground truth. A target cannot simultaneously be used as a predictor.
3. Per-band `info` is simulator truth. It may be revealed **after** fitting for validation, never supplied as a predictor when estimating DRW/DHO quantities.
4. Period is already the **observed orbital period in years**. Light-curve timestamps are in **MJD (days)**. Convert deliberately when comparing them.
5. Angular variables require angular/circular treatment where appropriate.
6. NaNs in DRW/DHO truth are structural and identify which stochastic model generated the simulation; do not impute them as ordinary missing values.

## Metadata not specified in the supplied materials

The course does **not** assume information that is absent from the supplied
dataset and provider notebook. The following points are therefore treated as
unknown:

1. exact sampling/prior distributions used for each continuous physical input;
2. the precise magnitude convention beyond the documented unit `mag`;
3. any additional physical prescription behind the Eddington-fraction variable;
4. dependence structure among the mechanism switches beyond what is visible
   empirically in the data;
5. any cadence/field details beyond the documented `WFD` / `DDF` labels and the
   actual time arrays stored in each light curve.

### Course rule

Students must infer or describe only what is supported by the supplied data.

For example:
- they may **empirically describe** the simulated distribution of mass ratio;
- they may **not claim** that this is the intended astrophysical prior unless the
  supplied material explicitly states that;
- they may compare WFD and DDF light-curve cadences from the stored time arrays;
- they may not invent additional survey assumptions not present in the files.

Unknown metadata should be reported as a limitation, not filled in from external
sources or assumptions.
