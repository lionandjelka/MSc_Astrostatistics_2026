from __future__ import annotations
from pathlib import Path
import os, ast, re
import numpy as np
import pandas as pd

COURSE_ROOT = Path(__file__).resolve().parents[1]
TEACHING_DATA = COURSE_ROOT / "data" / "teaching"
DEFAULT_SCALAR = TEACHING_DATA / "scalar_sample.parquet"


def _clean_piece(x):
    x = str(x).strip()
    x = re.sub(r"[^0-9A-Za-z]+", "_", x).strip("_")
    return x


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten Pandas MultiIndex / tuple-like Parquet columns to stable names."""
    out = df.copy()
    names=[]
    for c in out.columns:
        if isinstance(c, tuple):
            parts=[p for p in c if str(p).strip()]
        else:
            parts=None
            if isinstance(c,str) and c.startswith("(") and c.endswith(")"):
                try:
                    v=ast.literal_eval(c)
                    if isinstance(v,tuple): parts=[p for p in v if str(p).strip()]
                except Exception:
                    pass
            if parts is None: parts=[c]
        names.append("__".join(_clean_piece(p) for p in parts))
    out.columns=names
    return out


def load_scalar_sample(path=None):
    path = Path(path) if path else DEFAULT_SCALAR
    df = pd.read_parquet(path)
    return flatten_columns(df)


def full_parquet_path(path=None):
    if path:
        return Path(path).expanduser()
    env=os.getenv("SMBH_PARQUET")
    if env:
        return Path(env).expanduser()
    return COURSE_ROOT / "data" / "private" / "tenpct_dataset_withinputs.parquet"


def expected_input_columns():
    return [
        'inputs__RA','inputs__dec','inputs__total_mass','inputs__mass_ratio',
        'inputs__period','inputs__eccentricity','inputs__inclination',
        'inputs__arg_of_pericenter','inputs__redshift','inputs__Eddington_fraction',
        'inputs__retrograde','inputs__Doppler_boosting','inputs__lensing_flare',
        'inputs__accretion_modulation'
    ]


def robust_mad(x):
    x=np.asarray(x,float)
    med=np.nanmedian(x)
    return np.nanmedian(np.abs(x-med))
