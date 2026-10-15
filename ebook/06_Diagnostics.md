# 6. Diagnostik dan Robustness
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
Dokumentasikan revisi data, outlier, dan pemilihan model; hindari p-hacking.