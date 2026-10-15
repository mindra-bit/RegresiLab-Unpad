# 3. Data Panel dan Fixed Effects
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
Koefisien adalah asosiasi perubahan *within unit*, kondisional pada FE unit, FE waktu, dan kovariat yang tercakup.