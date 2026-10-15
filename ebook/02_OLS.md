# 2. OLS: Model, Estimasi, Inferensi
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
Koefisien $$\beta_j$$ menyatakan perubahan **rerata kondisional** Y untuk perubahan satu unit X_j ketika variabel lain konstan; bukan otomatis efek kausal. R² tidak menentukan validitas identifikasi.