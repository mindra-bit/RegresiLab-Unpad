from pathlib import Path
p=Path(__file__).parent/'ebook';p.mkdir(exist_ok=True)
chapters={
'01_Peta_Pembelajaran':('Peta Pembelajaran dan Kerangka Sains Data',r'''# 1. Peta Pembelajaran
**Tujuan:** membedakan deskripsi, prediksi, asosiasi, dan estimasi efek kausal. Pertanyaan penelitian menentukan metode; akurasi prediksi bukan bukti kausalitas.

## Alur kerja
1. Definisikan unit analisis, populasi, periode, outcome, variabel perlakuan, dan estimand.
2. Susun data dictionary, eksplorasi missingness, outlier, struktur panel, serta sumber bias.
3. Tentukan spesifikasi dan asumsi identifikasi sebelum melihat hasil utama.
4. Estimasi model dengan standard error yang sesuai desain data.
5. Lakukan diagnostik, validasi, sensitivitas, dan komunikasi ketidakpastian.

## Matriks metode
| Pertanyaan | Metode | Syarat penting |
|---|---|---|
| Hubungan kondisional | OLS | Eksogenitas kondisional untuk interpretasi struktural |
| Efek variabel dalam unit dari waktu ke waktu | Fixed effects | Eksogenitas ketat / asumsi desain relevan |
| Efek pengobatan dengan instrumen | IV/2SLS | Relevansi, eksklusi, independensi |
| Efek kebijakan | DiD | Parallel trends untuk counterfactual |
| Prediksi | Ridge/Lasso/Forest | Evaluasi out-of-sample tanpa kebocoran data |

**Catatan:** Seluruh data contoh pada aplikasi bersifat sintetis, bukan data penelitian nyata.'''),
'02_OLS':('OLS: Model, Estimasi dan Inferensi',r'''# 2. OLS: Model, Estimasi, Inferensi
## Model populasi
$$Y_i=\beta_0+\sum_{j=1}^{p}\beta_j X_{ij}+\varepsilon_i,\qquad E(\varepsilon_i\mid\mathbf X_i)=0.$$
Persamaan matriks: $$\mathbf y=\mathbf X\boldsymbol\beta+\boldsymbol\varepsilon.$$
## Estimasi
Minimalkan $$S(\boldsymbol\beta)=(\mathbf y-\mathbf X\boldsymbol\beta)^\top(\mathbf y-\mathbf X\boldsymbol\beta).$$
Gradien $$-2\mathbf X^\top(\mathbf y-\mathbf X\boldsymbol\beta)=\mathbf 0$$ sehingga, jika $$\operatorname{rank}(\mathbf X)=p+1,$$
$$\widehat{\boldsymbol\beta}_{OLS}=(\mathbf X^\top\mathbf X)^{-1}\mathbf X^\top\mathbf y.$$
## Asumsi dan konsekuensi
- Sampling independen atau struktur dependensi dimodelkan; tidak ada kolinearitas sempurna.
- Eksogenitas kondisional menghasilkan ketakbiasan OLS di bawah asumsi sampling lazim.
- Homoskedastisitas dan tidak ada autokorelasi memberi formula varians klasik dan efisiensi Gauss–Markov, bukan syarat ketakbiasan.
- Normalitas galat diperlukan untuk inferensi t/F eksak pada sampel kecil, bukan untuk mendefinisikan estimator.

## Inferensi
$$\operatorname{Var}(\widehat\beta\mid X)=\sigma^2(X^\top X)^{-1},\qquad \widehat\sigma^2=\frac{SSE}{n-p-1}.$$
Uji koefisien: $$t_j=\frac{\widehat\beta_j-\beta_{j,0}}{\widehat{se}(\widehat\beta_j)}.$$
CI klasik: $$\widehat\beta_j\pm t_{n-p-1,1-\alpha/2}\widehat{se}(\widehat\beta_j).$$
Gunakan HC3 untuk inferensi robust terhadap heteroskedastisitas pada regresi cross-sectional, dengan pendekatan asimtotik.

## Interpretasi
Koefisien $$\beta_j$$ menyatakan perubahan **rerata kondisional** Y untuk perubahan satu unit X_j ketika variabel lain konstan; bukan otomatis efek kausal. R² tidak menentukan validitas identifikasi.'''),
'03_Panel':('Pooled OLS dan Fixed Effects Panel',r'''# 3. Data Panel dan Fixed Effects
## Formulasi
$$Y_{it}=\alpha_i+\lambda_t+\mathbf X_{it}^\top\beta+\varepsilon_{it}.$$
Indeks $i$ unit dan $t$ periode; $\alpha_i$ heterogenitas tetap tidak teramati, $\lambda_t$ guncangan umum.

## Within transformation satu arah
$$\widetilde Y_{it}=Y_{it}-\bar Y_i,\quad \widetilde X_{it}=X_{it}-\bar X_i.$$
Estimator satu-arah: $$\widehat\beta_{FE}=(\widetilde X^\top\widetilde X)^{-1}\widetilde X^\top\widetilde Y.$$
Untuk two-way FE dapat memakai dummy unit dan waktu; aplikasi menggunakan metode ini.

## Asumsi
- Variasi dalam unit mencukupi; regresor konstan sepanjang waktu terserap FE unit.
- Kondisi eksogenitas ketat untuk FE linear klasik: $E(\varepsilon_{it}\mid X_{i1},\ldots,X_{iT},\alpha_i)=0$.
- Shock bersama dan tren dapat menimbulkan confounding bila tidak dimodelkan.
- Korelasi serial dalam unit -> cluster standard errors di unit; memerlukan jumlah cluster memadai untuk pendekatan asimtotik.

## FE vs Random Effects
RE membutuhkan orthogonalitas antara komponen efek unit dan regresor; bila kondisi itu tidak berlaku FE lebih aman untuk asosiasi within. Hausman test bukan pengganti argumen substantif. FE tidak otomatis mengatasi time-varying confounders.

## Interpretasi
Koefisien adalah asosiasi perubahan *within unit*, kondisional pada FE unit, FE waktu, dan kovariat yang tercakup.'''),
'04_IV':('Endogeneity dan Instrumental Variables / 2SLS',r'''# 4. Endogeneity, IV, dan 2SLS
## Masalah
$$Y=\beta_0+\beta_1 X+u,\qquad \operatorname{Cov}(X,u)\ne 0.$$
Sumber endogenitas: omitted variables, simultanitas, measurement error.

## Validitas instrumen Z
1. Relevansi: $\operatorname{Cov}(Z,X\mid W)\ne0$.
2. Eksklusi: Z mempengaruhi Y hanya melalui X, kondisional pada kontrol W.
3. Independensi terhadap gangguan tak teramati dan asumsi desain yang memadai.

## Two-stage least squares
Tahap 1: $$X_i=\pi_0+\pi_1 Z_i+W_i^\top\gamma+v_i.$$
Tahap 2: $$Y_i=\beta_0+\beta_1\widehat X_i+W_i^\top\delta+u_i.$$
Formula umum: $$\widehat\beta_{2SLS}=(X^\top P_Z X)^{-1}X^\top P_Z y,\quad P_Z=Z(Z^\top Z)^{-1}Z^\top.$$
**Penting:** Tidak boleh mengambil SE OLS biasa dari regresi tahap 2 sebagai inferensi 2SLS; gunakan kovarians 2SLS yang tepat. Modul aplikasi menyediakan kovarians sandwich HC0 untuk demonstrasi satu endogen + satu instrumen.

## Identifikasi dan weak instruments
Untuk satu instrumen terbuang dan satu regresor endogen, uji parsial tahap pertama F dapat menjadi indikator relevansi, tetapi aturan F>10 bukan sertifikat universal instrumen kuat. Pada banyak instrumen / heteroskedastisitas, pertimbangkan Kleibergen–Paap, Anderson–Rubin dan metode weak-IV robust.

## LATE
Dalam kerangka instrumen biner, asumsi exclusion, monotonicity, dan lainnya dapat mengidentifikasi *local average treatment effect* pada compliers, bukan otomatis ATE populasi. P-value first stage tidak memvalidasi exclusion.'''),
'05_DiD':('Difference-in-Differences dan Evaluasi Kebijakan',r'''# 5. Difference-in-Differences
## Definisi estimand
Untuk dua kelompok dan dua periode:
$$\widehat\tau_{DiD}=(\bar Y_{T,post}-\bar Y_{T,pre})-(\bar Y_{C,post}-\bar Y_{C,pre}).$$
Model regresi: $$Y_{it}=\alpha_i+\lambda_t+\tau(D_i\times Post_t)+u_{it}.$$
## Identifikasi
*Parallel trends* berarti kelompok yang diberi perlakuan akan memiliki perubahan outcome rata-rata yang sama dengan pembanding **seandainya tidak ada perlakuan**. Ini tidak dapat diuji langsung setelah perlakuan. Pemeriksaan pre-trends, studi konteks, dan placebo hanya memberi dukungan tidak konklusif.

## Ancaman
- Antisipasi perlakuan, spillover, confounder yang berubah dari waktu ke waktu.
- Perubahan komposisi sampel, selective treatment timing.
- Pada staggered adoption dan efek heterogen, TWFE konvensional bisa memberi bobot negatif; gunakan estimator cohort-time yang sesuai.

## Diagnostik
Visualisasikan rata-rata outcome antar kelompok sebelum dan sesudah implementasi. Gunakan standard errors cluster pada unit penetapan kebijakan jika relevan. Untuk sedikit cluster, inferensi cluster standar bisa bias. Evaluasi robustnes pada jendela waktu, kontrol, dan kelompok pembanding.

## Interpretasi
Koefisien interaksi adalah estimasi efek kebijakan hanya di bawah asumsi identifikasi tersebut, bukan karena p-value signifikan.'''),
'06_Diagnostics':('Diagnostik, Ketahanan, dan Kualitas Inferensi',r'''# 6. Diagnostik dan Robustness
## Heteroskedastisitas
$$\operatorname{Var}(u_i\mid X_i)=\sigma_i^2.$$ Breusch–Pagan menguji pola tertentu; p kecil memberi indikasi ketidakhomogenan varians, bukan bukti pelanggaran eksogenitas. HC3 memperbaiki estimasi varians koefisien, tidak menghilangkan bias omitted variable.

## Multikolinearitas
$$VIF_j=\frac{1}{1-R_j^2}.$$ Nilai tinggi dapat memperbesar ketidakpastian; ambang VIF=5 atau 10 adalah heuristik, bukan aturan universal. Kolinearitas sempurna membuat model tak teridentifikasi.

## Residual dan spesifikasi
- Jarque–Bera: normalitas residual; sensitif pada n besar.
- Breusch–Godfrey: korelasi serial jika observasi punya urutan bermakna; **jangan** menafsirkan uji BG pada cross-section acak sebagai bukti dependensi temporal.
- Ramsey RESET: kemungkinan salah spesifikasi fungsional; tidak membuktikan kausalitas.
- Cook’s D dan leverage: tinjau observasi berpengaruh, jangan hapus otomatis.
- Residual vs fitted, QQ plot, heteroskedastisitas, nonlinieritas, dan distribusi errors.

## Robustness plan
Sebelum fitting: tentukan kovariat inti, alternatif, outlier rule, cluster level, negative controls, placebo, interval waktu, dan subgrup. Laporkan semua hasil utama secara transparan, termasuk yang tidak signifikan.

## Etika
Dokumentasikan revisi data, outlier, dan pemilihan model; hindari p-hacking.'''),
'07_ML':('Machine Learning, Validasi dan Heterogenitas',r'''# 7. Machine Learning untuk Ekonometrika
## Objektif prediktif
Bagi data menjadi train/test sebelum fitting preprocessing. Untuk data panel, kelompokkan split berdasarkan unit bila targetnya generalisasi ke unit baru; untuk forecasting gunakan split berbasis waktu.

## Regularisasi
Ridge: $$\widehat\beta=\arg\min_\beta\{\sum_i(y_i-x_i^\top\beta)^2+\lambda\|\beta\|_2^2\}.$$
Lasso: $$\widehat\beta=\arg\min_\beta\{\sum_i(y_i-x_i^\top\beta)^2+\lambda\|\beta\|_1\}.$$
Skalakan fitur hanya dengan pelatihan (pipeline). Ridge mengecilkan koefisien; Lasso bisa membuat koefisien nol. Random Forest menangkap interaksi/nonlinieritas tetapi tidak memberi efek kausal tanpa desain identifikasi.

## Evaluasi
$$RMSE=\sqrt{\frac1m\sum_{i=1}^m(y_i-\widehat y_i)^2},\quad MAE=\frac1m\sum_i|y_i-\widehat y_i|.$$
Gunakan cross-validation untuk tuning dan test holdout terpisah untuk estimasi kinerja akhir. Ketidaksetaraan distribusi train/test dan temporal drift perlu diperiksa.

## ML dan kausal
**Double Machine Learning:** nuisance functions dipelajari dengan cross-fitting agar bias regularisasi pada parameter target berkurang di bawah asumsi orthogonal score dan identifikasi. **Causal forest:** heterogeneity of treatment effects memerlukan unconfoundedness/overlap atau desain kausal relevan; feature importance ≠ effect heterogeneity.

## Kapan menggunakan apa?
OLS/FE/IV/DiD untuk pertanyaan identifikasi dan inferensi dengan desain tepat; Ridge/Lasso/Forest untuk prediksi; metode causal ML bila estimand dan asumsi kausal telah ditentukan.'''),
'08_Monte_Carlo':('Simulasi Monte Carlo: Bias, RMSE, Coverage',r'''# 8. Simulasi Monte Carlo
Misal DGP: $$Y_i=1+2X_i+\varepsilon_i.$$
Ulangi eksperimen R kali, simpan $\widehat\beta^{(r)}$. Ukur:
$$Bias=\frac1R\sum_{r=1}^R\widehat\beta^{(r)}-\beta,\quad RMSE=\sqrt{\frac1R\sum_r(\widehat\beta^{(r)}-\beta)^2}.$$
Coverage: $$\frac1R\sum_r\mathbb 1\{\beta\in CI^{(r)}\}.$$
Bandingkan n kecil/besar, heteroskedastisitas dan confounding. **Penting:** heteroskedastisitas sendiri tidak menciptakan bias OLS bila eksogenitas terpenuhi; confounding yang berkorelasi dengan prediktor dapat menyebabkan bias.

## Latihan
Ubah n dari 50 menjadi 500, periksa bias, RMSE, coverage HC3. Aktifkan confounding dan jelaskan mengapa coverage turun. Buat tabel seluruh skenario dengan seed dan jumlah replikasi.'''),
'09_Proyek':('Rancangan Proyek, Rubrik, dan Referensi',r'''# 9. Praktikum dan Penilaian
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
https://docs.streamlit.io/ • https://www.statsmodels.org/ • https://scikit-learn.org/''')
}
for name,(title,body) in chapters.items():
 (p/(name+'.md')).write_text(body,encoding='utf-8')
print(len(chapters),'chapters created')
