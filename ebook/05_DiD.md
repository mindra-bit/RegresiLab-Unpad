# 5. Difference-in-Differences
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
Koefisien interaksi adalah estimasi efek kebijakan hanya di bawah asumsi identifikasi tersebut, bukan karena p-value signifikan.