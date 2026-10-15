# 1. Peta Pembelajaran
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

**Catatan:** Seluruh data contoh pada aplikasi bersifat sintetis, bukan data penelitian nyata.