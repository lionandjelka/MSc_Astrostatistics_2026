# Publish as a GitHub repository

The recommended structure keeps the original Crete material unchanged and adds `MSc_Astrostatistics_2026/` at repository root.

```bash
git clone https://github.com/lionandjelka/2025_summer_school.git
cd 2025_summer_school
git checkout -b msc-astrostatistics-2026
# copy MSc_Astrostatistics_2026/ into this directory
git add MSc_Astrostatistics_2026 .gitignore
git commit -m "Add 11-week MSc Astrostatistics course"
git push -u origin msc-astrostatistics-2026
```

Then open a pull request into `main`.  Do not commit the full SMBH Parquet file or private blind-test truth.
