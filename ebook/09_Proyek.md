# 9. Praktikum dan Penilaian
## Model v1: Estimasi Utama (10%)
- Rumusan pertanyaan, estimand, dan diagram sebab-akibat (20%).
- Spesifikasi dan argumentasi asumsi (25%).
- Hasil estimasi dan interpretasi ketidakpastian (30%).
- Reproduksibilitas kode/data dan transparansi (25%).

## Milestone B: Validation Plan (10%)
- Diagnostik sesuai desain data (25%).
- Justifikasi pilihan SE, kelompok cluster, dan asumsi (25%).
- Robustness, placebo/pretrend/weak-IV checks sesuai model (30%).
- Rencana validasi prediktif jika relevan (20%).

## Skenario proyek
**Pendidikan:** pengaruh jam belajar terhadap nilai (latihan OLS, bukan klaim kausal otomatis).
**Panel wilayah:** hubungan investasi dan produktivitas dengan FE wilayah-tahun.
**IV:** instrumen sintetis pada variabel endogen; bandingkan OLS dan 2SLS.
**DiD:** estimasi kebijakan sintetis 2021; visualisasi pretrends.
**ML:** bandingkan Ridge/Lasso/Forest pada sampel holdout.

## Referensi utama
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data*, 2nd ed. MIT Press.
- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University Press.
- Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*, 2nd ed. Springer.
- Chernozhukov et al. (2018). Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1–C68.
- Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-Differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230.
- Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2), 175–199.

### Dokumentasi teknis
https://docs.streamlit.io/ • https://www.statsmodels.org/ • https://scikit-learn.org/