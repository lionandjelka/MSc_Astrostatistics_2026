#!/usr/bin/env python3
"""Score one final-project submission against a private truth file."""
import argparse, numpy as np, pandas as pd

def coverage(y,lo,hi):
    return np.mean((y>=lo)&(y<=hi))

def score_target(d,name,y):
    pred=d[f'{name}_mean'].to_numpy()
    print(f'\n{name}')
    print('  RMSE    ',np.sqrt(np.mean((pred-y)**2)))
    print('  bias    ',np.mean(pred-y))
    print('  MAE     ',np.mean(np.abs(pred-y)))
    for lev in ['68','95']:
        lo=d[f'{name}_lo{lev}'].to_numpy()
        hi=d[f'{name}_hi{lev}'].to_numpy()
        print(f'  cov{lev}   ',coverage(y,lo,hi))
        print(f'  width{lev} ',np.mean(hi-lo))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('truth')
    ap.add_argument('submission')
    args=ap.parse_args()
    t=pd.read_parquet(args.truth)
    s=pd.read_csv(args.submission)
    if 'id' in t and 'id' in s:
        d=t.merge(s,on='id',validate='one_to_one')
    else:
        if len(t)!=len(s): raise SystemExit('Row count mismatch')
        d=pd.concat([t.reset_index(drop=True),s.reset_index(drop=True)],axis=1)
    score_target(d,'q',d['inputs__mass_ratio'].to_numpy())
    score_target(d,'logP',np.log10(d['inputs__period'].to_numpy()))

if __name__=='__main__':
    main()
