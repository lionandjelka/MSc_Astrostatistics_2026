#!/usr/bin/env python3
"""Prepare common final-project data with IID and shifted blind sets.

Example:
    python prepare_blind_project.py lightcurve_features.parquet OUTDIR \
        --seed 81273 --iid-frac 0.10 --shift-frac 0.10 \
        --shift-column inputs__redshift --shift-quantile 0.80

The shift set is sampled preferentially from the upper tail of shift-column.
Keep *_truth_PRIVATE.parquet files private.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('features')
    ap.add_argument('outdir')
    ap.add_argument('--seed',type=int,required=True)
    ap.add_argument('--iid-frac',type=float,default=.10)
    ap.add_argument('--shift-frac',type=float,default=.10)
    ap.add_argument('--shift-column',default='inputs__redshift')
    ap.add_argument('--shift-quantile',type=float,default=.80)
    args=ap.parse_args()

    df=pd.read_parquet(args.features).reset_index(drop=True)
    targets=['inputs__mass_ratio','inputs__period']
    missing=[c for c in targets if c not in df]
    if missing:
        raise SystemExit(f'Missing targets: {missing}')
    if args.shift_column not in df:
        raise SystemExit(f'Missing shift column: {args.shift_column}')

    rng=np.random.default_rng(args.seed)
    n=len(df)
    n_iid=max(1,int(round(args.iid_frac*n)))
    n_shift=max(1,int(round(args.shift_frac*n)))

    cutoff=df[args.shift_column].quantile(args.shift_quantile)
    shift_pool=np.flatnonzero(df[args.shift_column].to_numpy()>=cutoff)
    if len(shift_pool)<n_shift:
        raise SystemExit('Not enough rows in shifted pool; lower --shift-quantile or --shift-frac.')
    shift_idx=rng.choice(shift_pool,size=n_shift,replace=False)

    remaining=np.setdiff1d(np.arange(n),shift_idx,assume_unique=False)
    iid_idx=rng.choice(remaining,size=n_iid,replace=False)
    train_idx=np.setdiff1d(remaining,iid_idx,assume_unique=False)

    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    input_cols=[c for c in df.columns if c.startswith('inputs__')]
    idcols=['id'] if 'id' in df else []

    def truth_part(x):
        return x[idcols+targets+[args.shift_column]].copy()

    train=df.iloc[train_idx].copy()
    iid=df.iloc[iid_idx].copy()
    shift=df.iloc[shift_idx].copy()

    train_public=train.drop(columns=[c for c in input_cols if c not in targets],errors='ignore')
    iid_features=iid.drop(columns=input_cols,errors='ignore')
    shift_features=shift.drop(columns=input_cols,errors='ignore')

    train_public.to_parquet(out/'final_train.parquet',index=False)
    iid_features.to_parquet(out/'final_blind_iid_features.parquet',index=False)
    shift_features.to_parquet(out/'final_blind_shift_features.parquet',index=False)
    truth_part(iid).to_parquet(out/'final_blind_iid_truth_PRIVATE.parquet',index=False)
    truth_part(shift).to_parquet(out/'final_blind_shift_truth_PRIVATE.parquet',index=False)

    print('rows:',{'train':len(train),'iid':len(iid),'shift':len(shift)})
    print('shift rule:',args.shift_column,'>=',cutoff)
    print('wrote',out)

if __name__=='__main__':
    main()
