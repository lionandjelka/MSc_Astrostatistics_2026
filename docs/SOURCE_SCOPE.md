# Source Scope and Assumptions

## Governing principle

All teaching claims about the binary-SMBH simulation must be supported by the
supplied Parquet data, schema/summary files, or the supplied provider notebook
`reading_datasets.ipynb`.

The course does **not** require additional communication with the simulation
providers.

## Allowed statements

Students and instructors may state that:
- the full with-inputs dataset is documented as containing 1,200,000 simulations;
- the physical inputs and their documented units are those listed in
  `DATA_DICTIONARY.md`;
- `field` is WFD or DDF;
- light-curve timestamps are MJD;
- the stored period is the observed orbital period in years;
- DRW/DHO truth parameters have the units and meanings documented in the
  supplied notebook;
- the blinded data omit physical `inputs` and per-band `info`.

## Statements that must not be invented

Unless directly supported by the supplied material, do not assert:
- a named analytic prior for any physical parameter;
- the magnitude convention (e.g. AB);
- additional physical assumptions behind Eddington fraction;
- independence or dependence of mechanism switches;
- cadence prescriptions beyond what can be measured from the stored time arrays;
- that the simulation parameter distribution represents the real cosmic SMBH
  population.

## Teaching use of unknown metadata

Unknown metadata become part of the statistical lesson:
- describe the empirical simulation distribution;
- distinguish empirical distribution from documented prior;
- quantify what can be learned from observables;
- state unsupported metadata as a limitation;
- avoid external assumptions.

This is scientifically preferable to silently filling gaps.
