"""RegresiLab Unpad: ebook + executable econometrics lab."""
from pathlib import Path
import io, json, zipfile
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core import (generate_cross,generate_panel,generate_iv,generate_did,fit_ols,
    fit_panel_twfe,fit_iv,fit_did,fit_ml,monte_carlo,coefficient_table,diagnostics)

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='RegresiLab | Universitas Padjadjaran',page_icon='🎓',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.block-container {max-width:1450px;padding-top:1.35rem;padding-bottom:3rem}
[data-testid="stSidebar"] {background:#12223b}
[data-testid="stSidebar"] * {color:#f7f9ff!important}
[data-testid="stSidebar"] div[data-baseweb="select"] * {color:#15243b!important}
h1,h2,h3{color:#132743!important;letter-spacing:-.028em}
.metric-card{border:1px solid #dce6f2;background:#fff;border-radius:15px;padding:20px}
.hero{background:linear-gradient(115deg,#14263e,#204568);color:white;border-radius:22px;padding:30px 35px;margin-bottom:22px;border-bottom:5px solid #f3be2d}
.hero h1{color:white!important;font-size:2.25rem;margin-bottom:8px}
.hero p{color:#dbe8f8;font-size:1.05rem}
.small-note{font-size:.92rem;color:#66788d}
</style>''',unsafe_allow_html=True)

DATASETS={'Pendidikan (cross-section)':'pendidikan.csv','Panel wilayah':'panel.csv','Instrumen (IV)':'iv.csv','Evaluasi kebijakan (DiD)':'did.csv'}
def load_data(key):return pd.read_csv(ROOT/'data'/DATASETS[key])
def render_table(df):st.dataframe(df,use_container_width=True,hide_index=False)
def export_data(df,name): st.download_button('⬇️ Unduh CSV',df.to_csv(index=False).encode('utf-8-sig'),file_name=name,mime='text/csv')
def chart(fig):fig.update_layout(template='plotly_white',margin=dict(l=10,r=10,t=40,b=20),height=430);st.plotly_chart(fig,use_container_width=True)
def dataselect(default='Pendidikan (cross-section)',allow_upload=True):
    choices=list(DATASETS)+(['Unggah CSV pengguna'] if allow_upload else [])
    pick=st.selectbox('Sumber dataset',choices,index=choices.index(default),key='source_'+st.session_state.get('section',''))
    if pick=='Unggah CSV pengguna':
        file=st.file_uploader('Unggah .csv (maks. 50 MB)',type='csv',key='upload_'+st.session_state.get('section',''))
        if file is None:st.info('Unggah CSV untuk melanjutkan.');st.stop()
        df=pd.read_csv(file)
    else:df=load_data(pick)
    return df,pick

def menu_dashboard():
    st.markdown('''<div class="hero"><h1>RegresiLab • Sains Data & Ekonometrika</h1><p>Belajar konsep, eksplorasi data, estimasi model, inferensi, diagnostik, simulasi, dan evaluasi prediksi — dalam satu ruang kerja akademik.</p></div>''',unsafe_allow_html=True)
    c=st.columns(4)
    for col,label,value in zip(c,['Bab e-book','Dataset sintetis','Laboratorium analitik','Bahasa komputasi'],['9','4','7','Python']): col.metric(label,value)
    st.subheader('🧭 Alur pembelajaran')
    st.markdown('**1. Pelajari teori** → **2. Pilih data** → **3. Estimasi & interpretasi** → **4. Diagnostik & validasi** → **5. Unduh hasil**')
    t1,t2=st.tabs(['Peta metode','Tentang dataset'])
    with t1:
        st.dataframe(pd.DataFrame([
            ['OLS','Asosiasi kondisional','Eksogenitas untuk penafsiran struktural'],['Two-way FE','Perubahan within-unit','Eksogenitas ketat / faktor time-varying'],['IV/2SLS','Efek dari variasi instrumen','Relevansi, eksklusi, independensi'],['DiD','Efek kebijakan relatif kontrol','Parallel trends dan no anticipation'],['ML','Prediksi observasi baru','Validasi out-of-sample dan cegah leakage']],columns=['Metode','Target','Asumsi utama']),hide_index=True,use_container_width=True)
    with t2:
        st.write('Seluruh data adalah **sintetis** dan memuat mekanisme pembangkitan yang dapat dilacak dalam `core.py`. Dataset tidak boleh diklaim sebagai temuan empiris Unpad.')
        for title in DATASETS:st.write(f'• **{title}**: {len(load_data(title)):,} baris')
    if (ROOT/'assets/logo_unpad.png').exists():st.caption('Materi edukasi dengan identitas visual Universitas Padjadjaran. Bukan layanan resmi institusi.')


def menu_ebook():
    st.title('📚 E-Book Interaktif')
    files=sorted((ROOT/'ebook').glob('*.md'))
    chosen=st.selectbox('Pilih bab',files,format_func=lambda p:p.stem.replace('_',' '))
    text=chosen.read_text(encoding='utf-8')
    st.markdown(text)
    st.download_button('⬇️ Simpan bab Markdown',text,file_name=chosen.name)
    with st.expander('Kumpulan bab & penugasan'):st.write('9 bab: peta pembelajaran, OLS, panel, IV, DiD, diagnostik, ML, Monte Carlo, dan proyek penelitian.')


def menu_data():
    st.title('🗂️ Data Studio')
    d,pick=dataselect();a,b,c=st.columns(3);a.metric('Observasi',len(d));b.metric('Variabel',len(d.columns));c.metric('Missing values',int(d.isna().sum().sum()))
    st.subheader('Pratinjau data');render_table(d.head(100));export_data(d,'data_regresilab.csv')
    t1,t2,t3=st.tabs(['Ringkasan','Visualisasi','Kamus data'])
    with t1:
        st.write('Deskriptif numerik');render_table(d.describe().T)
        st.write('Proporsi missing per variabel');render_table((d.isna().mean()*100).to_frame('persen_missing'))
        num=d.select_dtypes('number');
        if num.shape[1]>=2:chart(px.imshow(num.corr(),text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,title='Korelasi Pearson (tidak berarti kausalitas)'))
    with t2:
        num=list(d.select_dtypes('number').columns)
        if len(num)>1:
            x=st.selectbox('Sumbu X',num,index=0);y=st.selectbox('Sumbu Y',num,index=1)
            chart(px.scatter(d,x=x,y=y,opacity=.55,title='Eksplorasi hubungan bivariabel'))
            chart(px.histogram(d,x=y,nbins=35,title=f'Distribusi {y}'))
    with t3:
        render_table(pd.DataFrame({'variabel':d.columns,'tipe':[str(x) for x in d.dtypes],'missing':d.isna().sum().values}))
        st.caption('Kolom dengan akhiran `_laten`, `kemampuan_tak_teramati`, atau `sigma_error` hanya tersedia pada data sintetik untuk pengajaran; jangan digunakan sebagai kovariat observabel realistis.')


def menu_ols():
    st.title('📈 Laboratorium OLS')
    d,_=dataselect();numeric=list(d.select_dtypes('number').columns)
    y=st.selectbox('Outcome (Y)',numeric,index=0)
    defaults=[x for x in ['jam_belajar','kehadiran','beban_kerja'] if x in numeric and x!=y]
    x=st.multiselect('Regresor', [c for c in numeric if c!=y],default=defaults)
    cov=st.selectbox('Jenis standard errors',['HC3','nonrobust','HC1'],index=0)
    if not x:st.warning('Pilih minimal satu regresor.');return
    try: m,d_used,X=fit_ols(d,y,x,cov)
    except Exception as e:st.error(str(e));return
    c1,c2,c3=st.columns(3);c1.metric('n',m.nobs);c2.metric('R²',f'{m.rsquared:.3f}');c3.metric('Adjusted R²',f'{m.rsquared_adj:.3f}')
    st.subheader('Estimasi dan inferensi');render_table(coefficient_table(m));st.caption('p-values dari kovarians yang dipilih; untuk HC3 bersifat asimtotik.')
    t1,t2,t3=st.tabs(['Fitted & residual','Ringkasan lengkap','Ekspor'])
    with t1:
        diagnostics_data=pd.DataFrame({'fitted':m.fittedvalues,'residual':m.resid,'observed':d_used[y].values})
        a,b=st.columns(2)
        with a:chart(px.scatter(diagnostics_data,x='fitted',y='observed',title='Observed vs fitted'))
        with b:chart(px.scatter(diagnostics_data,x='fitted',y='residual',title='Residual vs fitted'))
    with t2:st.code(m.summary().as_text(),language='text')
    with t3:
        st.download_button('⬇️ Koefisien CSV',coefficient_table(m).to_csv().encode('utf-8'),file_name='koefisien_ols.csv',mime='text/csv')
        st.download_button('⬇️ Prediksi/residual CSV',pd.DataFrame({'observed':d_used[y].values,'fitted':np.asarray(m.fittedvalues),'residual':np.asarray(m.resid)}).to_csv(index=False).encode(),file_name='prediksi_residual.csv')
    st.session_state['ols_model']=m;st.session_state['ols_X']=X


def menu_panel():
    st.title('🏙️ Panel Data: Two-way Fixed Effects')
    d,_=dataselect('Panel wilayah');unit=st.selectbox('Kolom unit',list(d.columns),index=list(d.columns).index('wilayah') if 'wilayah' in d else 0)
    time=st.selectbox('Kolom waktu',list(d.columns),index=list(d.columns).index('tahun') if 'tahun' in d else 1)
    num=[x for x in d.select_dtypes('number') if x!=time]
    y=st.selectbox('Outcome',num,index=num.index('produktivitas') if 'produktivitas' in num else 0)
    x=st.multiselect('Regresor', [v for v in num if v!=y],default=[v for v in ['investasi','pendapatan'] if v in num])
    if not x:st.info('Pilih regresor.');return
    try:m,w=fit_panel_twfe(d,y,x,unit,time)
    except Exception as e:st.error(str(e));return
    st.caption('Dummy unit dan dummy tahun, dengan cluster-robust covariance menurut unit. Koefisien FE yang terserap tidak ditampilkan.')
    st.metric('Unit panel',w[unit].nunique());render_table(coefficient_table(m).loc[['const']+x])
    chart(px.line(w.groupby(time,as_index=False)[y].mean(),x=time,y=y,markers=True,title='Rerata outcome menurut waktu'))
    st.download_button('⬇️ Estimasi panel CSV',coefficient_table(m).loc[x].to_csv().encode(),file_name='panel_fe.csv')


def menu_iv():
    st.title('🔬 Instrumental Variables (2SLS)')
    d,_=dataselect('Instrumen (IV)');num=list(d.select_dtypes('number'))
    y=st.selectbox('Outcome',num,index=num.index('outcome') if 'outcome' in num else 0)
    x=st.selectbox('Prediktor endogen',[k for k in num if k!=y],index=0)
    z=st.selectbox('Instrumen',[k for k in num if k not in (y,x)],index=0)
    controls=st.multiselect('Kontrol eksogen (opsional)',[k for k in num if k not in (y,x,z)])
    try:
        tab,first,fstat=fit_iv(d,y,x,z,controls)
        ols,_,_=fit_ols(d,y,[x]+controls,'HC3')
    except Exception as e:st.error(str(e));return
    st.metric('First-stage partial F (satu instrumen)',f'{fstat:.2f}')
    a,b=st.columns(2)
    with a:st.subheader('2SLS / IV');render_table(tab)
    with b:st.subheader('OLS pembanding (HC3)');render_table(coefficient_table(ols).loc[[x]])
    st.subheader('First stage');render_table(coefficient_table(first))
    st.warning('Validitas eksklusi instrumen tidak dapat diuji hanya dengan F first-stage. F juga tidak menggantikan uji inferensi weak-IV robust. SE 2SLS menggunakan HC0 sandwich sebagai demonstrasi.')
    st.download_button('⬇️ Koefisien 2SLS',tab.to_csv().encode(),file_name='iv_2sls.csv')


def menu_did():
    st.title('⚖️ Difference-in-Differences')
    d,_=dataselect('Evaluasi kebijakan (DiD)');cols=list(d.columns)
    unit=st.selectbox('Unit',cols,index=cols.index('kabupaten') if 'kabupaten' in cols else 0)
    time=st.selectbox('Waktu',cols,index=cols.index('tahun') if 'tahun' in cols else 1)
    tr=st.selectbox('Treatment group (0/1)',cols,index=cols.index('treated') if 'treated' in cols else 2)
    post=st.selectbox('Post-policy (0/1)',cols,index=cols.index('post') if 'post' in cols else 3)
    ys=[c for c in d.select_dtypes('number') if c not in (time,tr,post)]
    y=st.selectbox('Outcome',ys,index=0)
    try:m,trends=fit_did(d,y,unit,time,tr,post)
    except Exception as e:st.error(str(e));return
    st.metric('Efek DiD (TWFE)',f'{m.params["did"]:.3f}');render_table(coefficient_table(m).loc[['did']]);chart(px.line(trends,x=time,y=y,color=tr,markers=True,title='Tren rata-rata sebelum dan sesudah kebijakan'))
    st.warning('Asumsi parallel trends bersifat counterfactual; kesamaan grafik pra-kebijakan tidak membuktikan asumsi. Desain ini untuk treatment timing seragam.')
    st.download_button('⬇️ Efek DiD',coefficient_table(m).loc[['did']].to_csv().encode(),file_name='did.csv')


def menu_diag():
    st.title('🩺 Diagnostik Regresi & Robustness')
    d,_=dataselect();nums=list(d.select_dtypes('number'));y=st.selectbox('Outcome',nums,index=0)
    x=st.multiselect('Prediktor',[c for c in nums if c!=y],default=[v for v in ['jam_belajar','kehadiran','beban_kerja'] if v in nums])
    if not x:st.warning('Pilih regresor.');return
    try:
        m,w,X=fit_ols(d,y,x,'HC3');tab,vif=diagnostics(m,X)
    except Exception as e:st.error(str(e));return
    a,b=st.columns(2)
    with a:st.subheader('Uji diagnostik');render_table(tab)
    with b:st.subheader('VIF');render_table(vif)
    chart(px.scatter(x=np.asarray(m.fittedvalues),y=np.asarray(m.resid),labels={'x':'Fitted','y':'Residual'},title='Residual vs fitted'))
    st.info('Uji autokorelasi pada data cross-section tidak memiliki interpretasi temporal tanpa urutan observasi bermakna. p-value diagnostik bukan ukuran besar pelanggaran. Pemetaan diagnosis → tindakan harus didasarkan pada desain penelitian.')
    st.download_button('⬇️ Hasil diagnostik',tab.to_csv(index=False).encode(),file_name='diagnostik.csv')


def menu_ml():
    st.title('🤖 Machine Learning: Prediksi & Regularisasi')
    d,_=dataselect();nums=list(d.select_dtypes('number'));y=st.selectbox('Target',nums,index=0)
    x=st.multiselect('Fitur numerik',[v for v in nums if v!=y],default=[v for v in ['jam_belajar','kehadiran','beban_kerja'] if v in nums])
    frac=st.slider('Proporsi data uji',.15,.45,.25,.05)
    if not x:st.warning('Pilih minimal satu fitur.');return
    try:results,preds=fit_ml(d,y,x,frac)
    except Exception as e:st.error(str(e));return
    render_table(results)
    chart(px.bar(results,x='model',y='RMSE_test',title='RMSE test (lebih kecil lebih baik)'))
    name=st.selectbox('Plot model',list(preds))
    chart(px.scatter(preds[name],x='aktual',y='prediksi',title=f'Prediksi vs aktual: {name}'))
    st.warning('Ini hanya train/test holdout sederhana dan hyperparameter contoh; untuk evaluasi final gunakan nested CV atau set validasi tuning terpisah. Jangan menyamakan feature importance dengan dampak kausal.')
    st.download_button('⬇️ Metrik',results.to_csv(index=False).encode(),file_name='metric_ml.csv')


def menu_sim():
    st.title('🎛️ Monte Carlo Studio')
    n=st.slider('Ukuran sampel per replikasi',30,600,120,10)
    reps=st.slider('Jumlah replikasi',100,1200,300,100)
    hetero=st.checkbox('Heteroskedastisitas',value=False)
    confounded=st.checkbox('Confounding pada regressor yang teramati',value=False)
    seed=st.number_input('Random seed',min_value=1,max_value=999999,value=2026)
    if st.button('▶️ Jalankan Monte Carlo',type='primary'):
        with st.spinner('Menghitung distribusi sampling...'):r,summary=monte_carlo(n,reps,int(seed),hetero,confounded)
        st.session_state['mc_results']=r;st.session_state['mc_summary']=summary
    if 'mc_results' in st.session_state:
        r=st.session_state['mc_results'];summary=st.session_state['mc_summary']
        a,b,c=st.columns(3);a.metric('Bias',f'{summary["bias"]:.3f}');b.metric('RMSE',f'{summary["RMSE"]:.3f}');c.metric('Coverage 95%',f'{summary["coverage_95%"]:.1%}')
        chart(px.histogram(r,x='beta_hat',nbins=40,title='Distribusi estimator OLS (true beta = 2)'))
        st.caption('HC3 digunakan untuk interval; dengan confounding, asumsi eksogenitas tidak terpenuhi.')
        st.download_button('⬇️ Hasil replikasi',r.to_csv(index=False).encode(),file_name='montecarlo.csv')

PAGES={'🏠 Beranda':menu_dashboard,'📚 E-Book':menu_ebook,'🗂️ Data Studio':menu_data,'📈 OLS':menu_ols,'🏙️ Panel FE':menu_panel,'🔬 IV / 2SLS':menu_iv,'⚖️ DiD':menu_did,'🩺 Diagnostik':menu_diag,'🤖 Machine Learning':menu_ml,'🎛️ Monte Carlo':menu_sim}
with st.sidebar:
    if (ROOT/'assets/logo_unpad.png').exists():st.image(str(ROOT/'assets/logo_unpad.png'),width=82)
    st.markdown('### REGRESILAB')
    st.caption('FMIPA • Universitas Padjadjaran')
    page=st.radio('Menu pembelajaran',list(PAGES))
    st.markdown('---')
    st.caption('v1.0 • Data demonstrasi sintetis • Open-source stack')
    st.markdown('**Panduan:** pilih menu → dataset → parameter → unduh hasil')
st.session_state['section']=page
PAGES[page]()
st.divider()
st.caption('RegresiLab Unpad • Materi edukasi, bukan perangkat identifikasi kausal otomatis. Periksa asumsi desain dan validasi hasil sebelum publikasi.')
