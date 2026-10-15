# RegresiLab Unpad — E-Book & Statistical Learning Studio

**Aplikasi Streamlit nyata** untuk sains data dan ekonometrika, menggunakan data demonstrasi sintetis. Logo Unpad disertakan untuk identitas visual dalam konteks materi pendidikan. Bukan aplikasi web resmi universitas.

## Mulai dalam 3 langkah (laptop/PC)

1. Ekstrak ZIP. Buka Terminal pada folder `RegresiLab_Unpad` (yang berisi `app.py`).
2. Instal lingkungan Python 3.10+:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Jalankan:
   ```bash
   streamlit run app.py
   ```
   Buka `http://localhost:8501` di browser. Hentikan dengan Ctrl+C.

**Mac:** jika `python` tidak tersedia, coba `python3`.

## Jalankan Google Colab
Colab adalah notebook terisolasi, bukan host web permanen. Notebook `colab/Launcher_Streamlit_Colab.ipynb` menyiapkan dependensi dan menggunakan tunneling ngrok yang **membutuhkan akun dan authtoken pengguna**. Tautan publik akan berhenti ketika Colab terputus. **Jangan unggah data sensitif** ke tunnel publik. Untuk penggunaan institusional jangka panjang, deploy ke Streamlit Community Cloud atau layanan cloud yang disetujui kampus.

## Menu
- Beranda: peta kegiatan dan metode
- E-Book: 9 bab teori, model, asumsi, estimator, inferensi dan metodologi penelitian
- Data Studio: impor CSV, ringkasan deskriptif, korelasi, scatter/histogram, unduh dataset
- OLS: cov_type HC3/HC1/nonrobust, estimasi + interval, residual, ekspor
- Panel FE: unit + tahun fixed effects, cluster-robust SE by unit
- IV/2SLS: first stage, partial F, HC0 sandwich pada IV, OLS pembanding
- DiD: TWFE + interaksi perlakuan, tren waktu, cluster SE
- Diagnostik: Breusch–Pagan, Jarque–Bera, Breusch–Godfrey (urutan data relevan), RESET, VIF, Cook’s D
- Machine Learning: Ridge/Lasso/Random Forest, train/test, prediksi dan metrik
- Monte Carlo: simulasi bias, RMSE, dan coverage 95% HC3

## Dataset
Data di `data/` semuanya **sintetis**, dibuat deterministik dengan seed 2026 dan tersedia CSV. Rumus generatif ada di `core.py`. Semua outcome hanya simulasi:
- `pendidikan.csv`: 450 mahasiswa simulasi, fungsi nilai dipengaruhi jam belajar, kehadiran, beban kerja, kemampuan laten, galat heteroskedastik.
- `panel.csv`: 75 unit × 7 tahun, produktivitas, investasi, pendapatan, efek tetap laten.
- `iv.csv`: 650 observasi, regressor endogen dengan confounder laten, instrumen independen.
- `did.csv`: 110 kabupaten × 8 tahun, 55 perlakuan dan 55 kontrol; efek perlakuan sintetis 3 setelah 2021.

**Hindari penggunaan kolom laten sebagai kontrol observabel pada contoh penelitian nyata.** Kolom tersebut tersedia untuk demonstrasi bias.

## Penggunaan file CSV sendiri
Unggah CSV di menu analisis. Variabel outcome dan prediktor wajib numerik. Panel mengharuskan unit/waktu, DiD membutuhkan `treated` dan `post` berupa 0/1. Periksa missing values (aplikasi memakai complete case per model). Aplikasi ini tidak melakukan penanganan missing data otomatis ataupun otomatis mengidentifikasi desain kausal.

## Interpretasi dan keterbatasan penting
- Signifikansi statistik bukan kausalitas. Evaluasi asumsi identifikasi per penelitian.
- OLS HC3 robust terhadap heteroskedastisitas untuk kovarians, tidak membenahi endogeneity.
- Panel/DiD clustered SE memerlukan cukup cluster; staggered DiD dengan heterogenitas butuh estimator khusus.
- IV first-stage F bukan tes eksklusi; untuk weak instrument gunakan tes robust lainnya.
- ML contoh membandingkan hyperparameter tetap pada holdout; untuk studi publikasi gunakan CV/nested CV serta split yang benar untuk panel/time series.
- Plot, diagnostik, dan p-value adalah alat bantu, bukan justifikasi otomatis spesifikasi model.

## Pengujian
```
python -m pip install pytest
python -m pytest -q tests/
```
Core computational tests: OLS, panel, IV, DiD, ML, Monte Carlo. Uji manual seluruh GUI di runtime Streamlit masih direkomendasikan sebelum penggunaan di kelas.

## Referensi
- Wooldridge (2010), *Econometric Analysis of Cross Section and Panel Data*.
- Angrist & Pischke (2009), *Mostly Harmless Econometrics*.
- Cunningham (2021), *Causal Inference: The Mixtape*.
- Chernozhukov et al. (2018), Double/Debiased Machine Learning.
- Callaway & Sant’Anna (2021), Difference-in-Differences with Multiple Time Periods.
- https://docs.streamlit.io/ • https://www.statsmodels.org/ • https://scikit-learn.org/

## Lisensi kode
Kode pembelajaran contoh diberikan untuk penggunaan dan pengembangan pendidikan; hak identitas visual logo mengikuti ketentuan institusi. Tidak ada jaminan bahwa asumsi model berlaku pada data pengguna.
