# 8. Simulasi Monte Carlo
Misal DGP: $$Y_i=1+2X_i+\varepsilon_i.$$
Ulangi eksperimen R kali, simpan $\widehat\beta^{(r)}$. Ukur:
$$Bias=\frac1R\sum_{r=1}^R\widehat\beta^{(r)}-\beta,\quad RMSE=\sqrt{\frac1R\sum_r(\widehat\beta^{(r)}-\beta)^2}.$$
Coverage: $$\frac1R\sum_r\mathbb 1\{\beta\in CI^{(r)}\}.$$
Bandingkan n kecil/besar, heteroskedastisitas dan confounding. **Penting:** heteroskedastisitas sendiri tidak menciptakan bias OLS bila eksogenitas terpenuhi; confounding yang berkorelasi dengan prediktor dapat menyebabkan bias.

## Latihan
Ubah n dari 50 menjadi 500, periksa bias, RMSE, coverage HC3. Aktifkan confounding dan jelaskan mengapa coverage turun. Buat tabel seluruh skenario dengan seed dan jumlah replikasi.