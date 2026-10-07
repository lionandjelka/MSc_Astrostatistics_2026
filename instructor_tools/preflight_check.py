#!/usr/bin/env python3
"""Static/preflight checks for the MSc Astrostatistics course repository."""
from pathlib import Path
import importlib.util, json, sys, re

try:
    import nbformat
except ImportError:
    nbformat=None

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent

REQUIRED_PACKAGES=['numpy','pandas','scipy','matplotlib','sklearn','pyarrow']
REQUIRED_FILES=[
    ROOT/'data/teaching/scalar_sample.parquet',
    ROOT/'src/course_utils.py',
    REPO/'01_Intro/Intro.ipynb',
    REPO/'08_Gaussian_Processes/Gaussian_Processes.ipynb',
    REPO/'14_SBI/SBI_short.ipynb',
]

def main():
    ok=True
    print('Course root:',ROOT)
    print('\nPackages:')
    for pkg in REQUIRED_PACKAGES:
        found=importlib.util.find_spec(pkg) is not None
        print(f'  {pkg:12s}', 'OK' if found else 'MISSING')
        ok &= found
    print('\nRequired files:')
    for p in REQUIRED_FILES:
        found=p.exists()
        print(' ', 'OK' if found else 'MISSING', p)
        ok &= found
    if nbformat:
        print('\nNotebooks:')
        n=0
        for p in ROOT.rglob('*.ipynb'):
            try:
                nb=nbformat.read(p,as_version=4); nbformat.validate(nb); n+=1
            except Exception as e:
                ok=False; print('  INVALID',p.relative_to(ROOT),e)
        print('  valid:',n)
    else:
        print('\nnbformat not installed; notebook JSON validation skipped.')
    # duplicate homework numbers
    hws=list((ROOT/'homeworks').glob('HW*.ipynb'))
    nums={}
    for p in hws:
        m=re.match(r'HW(\d+)',p.name)
        if m: nums.setdefault(m.group(1),[]).append(p.name)
    for n,names in nums.items():
        if len(names)>1:
            ok=False; print('DUPLICATE HOMEWORK',n,names)
    print('\nPRE-FLIGHT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
