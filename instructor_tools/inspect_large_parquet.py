#!/usr/bin/env python3
"""
Explore a large Parquet file safely without loading the whole dataset.

Default file:
    tenpct_dataset_withinputs.parquet

Usage:
    python explore_smbh_parquet.py

or:
    python explore_smbh_parquet.py /path/to/tenpct_dataset_withinputs.parquet

Optional:
    python explore_smbh_parquet.py tenpct_dataset_withinputs.parquet --sample-rows 5000
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def human_bytes(n):
    if n is None:
        return "?"
    n = float(n)
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    for unit in units:
        if n < 1024 or unit == units[-1]:
            return f"{n:.2f} {unit}"
        n /= 1024


def is_simple_scalar(dtype: pa.DataType) -> bool:
    """Columns that are normally safe and compact for first-pass statistics."""
    return (
        pa.types.is_boolean(dtype)
        or pa.types.is_integer(dtype)
        or pa.types.is_floating(dtype)
        or pa.types.is_decimal(dtype)
        or pa.types.is_string(dtype)
        or pa.types.is_large_string(dtype)
        or pa.types.is_timestamp(dtype)
        or pa.types.is_date(dtype)
        or pa.types.is_time(dtype)
        or pa.types.is_duration(dtype)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="?",
        default="tenpct_dataset_withinputs.parquet",
        help="Parquet file to inspect",
    )
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=10000,
        help="Maximum number of rows in the exploratory sample",
    )
    parser.add_argument(
        "--max-row-groups",
        type=int,
        default=5,
        help="Maximum row groups to read for the sample",
    )
    parser.add_argument(
        "--corr-max-columns",
        type=int,
        default=30,
        help="Maximum numeric columns used for correlation matrix",
    )
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    print("=" * 80)
    print("PARQUET FILE")
    print("=" * 80)
    print("Path:", path)
    print("File size:", human_bytes(path.stat().st_size))

    # -------------------------------------------------------------------------
    # 1. METADATA ONLY
    # -------------------------------------------------------------------------
    pf = pq.ParquetFile(path)
    md = pf.metadata
    schema = pf.schema_arrow

    print("\n" + "=" * 80)
    print("GLOBAL METADATA")
    print("=" * 80)
    print(f"Rows       : {md.num_rows:,}")
    print(f"Columns    : {md.num_columns:,}")
    print(f"Row groups : {md.num_row_groups:,}")

    # -------------------------------------------------------------------------
    # 2. SCHEMA
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SCHEMA")
    print("=" * 80)

    schema_rows = []
    scalar_cols = []
    heavy_cols = []

    for i, field in enumerate(schema):
        simple = is_simple_scalar(field.type)

        if simple:
            scalar_cols.append(field.name)
        else:
            heavy_cols.append(field.name)

        schema_rows.append(
            {
                "index": i,
                "column": field.name,
                "arrow_type": str(field.type),
                "category": "scalar" if simple else "nested/heavy",
            }
        )

    schema_df = pd.DataFrame(schema_rows)

    with pd.option_context(
        "display.max_rows", 500,
        "display.max_columns", None,
        "display.width", 200,
        "display.max_colwidth", 80,
    ):
        print(schema_df.to_string(index=False))

    print("\nScalar columns:")
    print(scalar_cols)

    print("\nNested / potentially heavy columns:")
    print(heavy_cols)

    # -------------------------------------------------------------------------
    # 3. APPROXIMATE STORAGE BY COLUMN
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PARQUET STORAGE BY COLUMN")
    print("=" * 80)

    storage = {}

    for rg_i in range(md.num_row_groups):
        rg = md.row_group(rg_i)

        for c_i in range(rg.num_columns):
            col = rg.column(c_i)
            name = col.path_in_schema

            if name not in storage:
                storage[name] = {
                    "compressed_bytes": 0,
                    "uncompressed_bytes": 0,
                }

            storage[name]["compressed_bytes"] += col.total_compressed_size
            storage[name]["uncompressed_bytes"] += col.total_uncompressed_size

    storage_rows = []

    for name, vals in storage.items():
        storage_rows.append(
            {
                "column": name,
                "compressed_GiB": vals["compressed_bytes"] / 1024**3,
                "uncompressed_GiB": vals["uncompressed_bytes"] / 1024**3,
            }
        )

    storage_df = (
        pd.DataFrame(storage_rows)
        .sort_values("compressed_GiB", ascending=False)
        .reset_index(drop=True)
    )

    with pd.option_context(
        "display.max_rows", 200,
        "display.width", 160,
    ):
        print(storage_df.to_string(index=False))

    print("\nTop 20 largest stored columns:")
    print(storage_df.head(20).to_string(index=False))

    # -------------------------------------------------------------------------
    # 4. READ ONLY A SMALL SAMPLE OF SCALAR COLUMNS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SMALL EXPLORATORY SAMPLE")
    print("=" * 80)

    if not scalar_cols:
        print("No primitive scalar columns found.")
        return

    batches = []
    rows_loaded = 0

    n_rg = min(md.num_row_groups, args.max_row_groups)

    for rg_i in range(n_rg):
        table = pf.read_row_group(rg_i, columns=scalar_cols)
        part = table.to_pandas()

        remaining = args.sample_rows - rows_loaded

        if remaining <= 0:
            break

        if len(part) > remaining:
            part = part.iloc[:remaining]

        batches.append(part)
        rows_loaded += len(part)

        if rows_loaded >= args.sample_rows:
            break

    sample = pd.concat(batches, ignore_index=True)

    print(f"Sample rows loaded: {len(sample):,}")
    print(f"Sample columns    : {sample.shape[1]:,}")

    print("\nFirst rows:")
    with pd.option_context(
        "display.max_columns", 100,
        "display.width", 220,
    ):
        print(sample.head().to_string())

    # -------------------------------------------------------------------------
    # 5. DTYPES + MISSINGNESS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("DTYPES AND MISSING VALUES")
    print("=" * 80)

    info = pd.DataFrame(
        {
            "dtype": sample.dtypes.astype(str),
            "missing_n": sample.isna().sum(),
            "missing_frac": sample.isna().mean(),
            "n_unique_sample": sample.nunique(dropna=True),
        }
    )

    info["missing_pct"] = 100 * info["missing_frac"]

    print(
        info
        .sort_values(["missing_frac", "n_unique_sample"], ascending=[False, False])
        .drop(columns="missing_frac")
        .to_string()
    )

    # -------------------------------------------------------------------------
    # 6. NUMERIC SUMMARY
    # -------------------------------------------------------------------------
    numeric = sample.select_dtypes(include=np.number)

    print("\n" + "=" * 80)
    print("NUMERIC SUMMARY")
    print("=" * 80)

    if numeric.shape[1] > 0:
        summary = numeric.describe(
            percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
        ).T

        # add useful robust quantities
        summary["missing_frac"] = numeric.isna().mean()

        q25 = numeric.quantile(0.25)
        q75 = numeric.quantile(0.75)
        summary["IQR"] = q75 - q25

        print(summary.to_string())
    else:
        print("No numeric scalar columns in sample.")

    # -------------------------------------------------------------------------
    # 7. FIND POSSIBLE INPUT / LATENT / TARGET COLUMNS BY NAME
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("COLUMN-NAME HINTS")
    print("=" * 80)

    keywords = [
        "input", "mass", "m1", "m2", "mass1", "mass2",
        "q", "ratio", "period", "sep", "separation",
        "ecc", "eccentricity", "redshift", "z",
        "lum", "luminosity", "incl", "inclination",
        "spin", "mdot", "accretion", "velocity",
        "angle", "phase", "time", "flux", "mag"
    ]

    hits = []

    for c in schema.names:
        low = c.lower()

        matched = [
            k for k in keywords
            if k in low
        ]

        if matched:
            hits.append(
                {
                    "column": c,
                    "matched_keywords": ", ".join(matched),
                    "type": str(schema.field(c).type),
                }
            )

    if hits:
        hints = pd.DataFrame(hits)
        print(hints.to_string(index=False))
    else:
        print("No obvious parameter names identified automatically.")

    # -------------------------------------------------------------------------
    # 8. CORRELATION MATRIX ON A LIMITED NUMBER OF NUMERIC COLUMNS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CORRELATION SCREEN")
    print("=" * 80)

    if numeric.shape[1] >= 2:
        # Avoid identifier-like columns where practically every row is unique
        candidate_cols = []

        for c in numeric.columns:
            nunique = numeric[c].nunique(dropna=True)

            if nunique > 1 and nunique < 0.99 * len(numeric):
                candidate_cols.append(c)

        candidate_cols = candidate_cols[: args.corr_max_columns]

        if len(candidate_cols) >= 2:
            corr = numeric[candidate_cols].corr(method="spearman")

            pairs = []

            for i, c1 in enumerate(corr.columns):
                for j in range(i + 1, len(corr.columns)):
                    c2 = corr.columns[j]
                    r = corr.loc[c1, c2]

                    if pd.notna(r):
                        pairs.append(
                            {
                                "column_1": c1,
                                "column_2": c2,
                                "spearman_rho": r,
                                "abs_rho": abs(r),
                            }
                        )

            pair_df = (
                pd.DataFrame(pairs)
                .sort_values("abs_rho", ascending=False)
                .drop(columns="abs_rho")
            )

            print("Strongest correlations in sample:")
            print(pair_df.head(30).to_string(index=False))
        else:
            print("Not enough suitable numeric columns for correlations.")
    else:
        print("Not enough numeric columns.")

    # -------------------------------------------------------------------------
    # 9. SAVE SMALL REPORT TABLES
    # -------------------------------------------------------------------------
    report_dir = path.parent / "parquet_exploration_report"
    report_dir.mkdir(exist_ok=True)

    schema_df.to_csv(report_dir / "schema.csv", index=False)
    storage_df.to_csv(report_dir / "column_storage.csv", index=False)
    info.to_csv(report_dir / "sample_column_info.csv")

    if numeric.shape[1] > 0:
        summary.to_csv(report_dir / "numeric_summary.csv")

    # Small scalar sample only
    sample.to_parquet(
        report_dir / "scalar_sample.parquet",
        index=False,
    )

    print("\n" + "=" * 80)
    print("REPORT WRITTEN")
    print("=" * 80)
    print(report_dir)
    print("Files:")
    for f in sorted(report_dir.iterdir()):
        print(" ", f.name)

    print("\nNEXT STEP:")
    print(
        "Send/share schema.csv and column_storage.csv first. "
        "They are enough to identify which columns should be used for "
        "population statistics, ML, and SBI without moving the large dataset."
    )


if __name__ == "__main__":
    main()
