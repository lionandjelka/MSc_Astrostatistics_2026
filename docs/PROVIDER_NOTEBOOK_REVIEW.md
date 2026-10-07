# Review of the Provider Dataset-Reading Notebook

The provider notebook is extremely useful and resolves the principal metadata
questions for the course. It also provides clear examples for selecting physical
inputs and extracting individual multiband light curves.

## Confirmed facts used by the course

- Full with-inputs dataset: **1,200,000 simulations**.
- Field values: `WFD` or `DDF`.
- Total binary mass: solar masses.
- Mass ratio: $M_2/M_1$.
- Period: **observed orbital period [yr]**.
- RA/Dec, inclination, argument of pericenter: degrees.
- Light-curve time: MJD.
- Observed magnitude / error: mag.
- DRW/DHO truth definitions and units are given in `DATA_DICTIONARY.md`.
- Blinded data exclude the `inputs` and `info` structures.

## Important memory distinction

The notebook shows two batching patterns.

### Pattern A — batching but then concatenating every batch

```python
df_list = []
for batch in parquet_file.iter_batches(batch_size=5000):
    df_list.append(batch.to_pandas())
df = pd.concat(df_list, ignore_index=True)
```

This reduces the size of each read operation, but it **does not avoid allocating
memory for the complete dataset**, because all batches are retained and finally
concatenated.

For the >500 GB parent dataset, do not use this as the default course workflow.

### Pattern B — process each batch and discard it

```python
for batch in parquet_file.iter_batches(batch_size=5000):
    df_batch = batch.to_pandas()
    # compute/update compact summaries here
```

This is the preferred approach when the full dataset is too large for RAM.

Even better, use **column projection** so the large nested light-curve arrays are
not read when only scalar inputs are required.

## Small robustness fix

The provider example that counts u-band observations uses:

```python
for j in range(batchsize):
    ...
```

For general code, the last Parquet batch may contain fewer than `batchsize` rows.
Use:

```python
for j in range(len(df_batch)):
    ...
```

or vectorised/list-comprehension logic over the actual batch length.

## Recommended safe scalar access

```python
import pyarrow.parquet as pq

pf = pq.ParquetFile("tenpct_dataset_withinputs.parquet")

columns = [
    "('inputs', 'total mass')",
    "('inputs', 'mass ratio')",
    "('inputs', 'period')",
    "('inputs', 'eccentricity')",
    "('inputs', 'redshift')",
]

for batch in pf.iter_batches(batch_size=5000, columns=columns):
    df_batch = batch.to_pandas()
    # analyse or accumulate only compact summaries
```

Depending on the exact PyArrow representation of the multi-level/nested schema,
column names may need to be taken directly from the schema. The course helper
scripts inspect the schema first rather than hard-coding assumptions.

## Recommended safe light-curve access

For time-domain classes, do not scan every object's six-band arrays. Prepare a
curated subset of systems and extract only those rows / row groups required for
the practical.

## Pedagogical implication

The provider's blinded-data design is excellent for the final course challenge:
students can learn from with-inputs simulations and then receive a physically
appropriate blind table in which neither latent physical truth nor DRW/DHO
truth is exposed.


## Scope rule for this course

This course is intentionally restricted to the supplied dataset and notebook.
Where the provider notebook is silent, the course will not introduce an
unstated convention or request additional information.

In particular, the course will work directly with:
- empirical distributions present in the simulation sample;
- WFD/DDF labels as stored;
- actual MJD cadence arrays;
- documented physical input definitions and units;
- documented DRW/DHO truth parameters;
- the supplied with-inputs versus blinded-data distinction.

Anything beyond those items is outside the documented scope.
