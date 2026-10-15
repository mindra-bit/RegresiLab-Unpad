"""Computational core: regression teaching demonstrator. Synthetic datasets only."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, acorr_breusch_godfrey, linear_reset
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from scipy.stats import jarque_bera
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def generate_cross(n=450, seed=2026):
    rng=np.random.default_rng(seed)
    x1=rng.normal(6,1.8,n)
    x2=rng.normal(10,2.4,n)
    x3=rng.normal(0,1,n)
    ability=rng.normal(0,1,n)
    hetero=2+0.32*np.maximum(x2,0)
    y=25+3.2*x1+1.8*x2-2.0*x3+1.7*ability+rng.normal(0,hetero,n)
    return pd.DataFrame({'nilai':y,'jam_belajar':x1,'kehadiran':x2,'beban_kerja':x3,'kemampuan_tak_teramati':ability,'sigma_error':hetero})


def generate_panel(n=75,t=7,seed=2026):
    rng=np.random.default_rng(seed); a=rng.normal(0,2,n); years=np.arange(2019,2019+t); rec=[]
    for i in range(n):
        for j,yr in enumerate(years):
            policy=0.5*a[i]+rng.normal(0,1.2)
            income=10+0.8*j+0.5*a[i]+rng.normal(0,1)
            outcome=35+1.6*policy+2.2*income+a[i]+0.65*j+rng.normal(0,1.7)
            rec.append((f'R{i+1:03}',yr,outcome,policy,income,a[i]))
    return pd.DataFrame(rec,columns=['wilayah','tahun','produktivitas','investasi','pendapatan','efek_individu_laten'])


def generate_iv(n=650,seed=2026):
    rng=np.random.default_rng(seed); z=rng.normal(size=n); u=rng.normal(size=n)
    x=0.8*z+0.9*u+rng.normal(size=n)
    y=4+2.5*x+1.5*u+rng.normal(size=n)
    return pd.DataFrame({'outcome':y,'treatment_endogen':x,'instrumen':z,'confounder_laten':u})


def generate_did(n=110,t=8,seed=2026):
    rng=np.random.default_rng(seed); rows=[]
    for i in range(n):
        tr=int(i<n//2); intercept=rng.normal(0,1.6)
        for year in range(2017,2017+t):
            post=int(year>=2021); outcome=18+0.8*(year-2017)+intercept+1.1*tr+3.0*tr*post+rng.normal(0,1.25)
            rows.append((f'K{i+1:03}',year,tr,post,outcome))
    return pd.DataFrame(rows,columns=['kabupaten','tahun','treated','post','kemiskinan_indeks'])


def fit_ols(df,y,x,cov='HC3'):
    work=df[[y]+x].dropna().copy(); X=sm.add_constant(work[x].astype(float),has_constant='add')
    if len(work)<=X.shape[1]+2: raise ValueError('Observasi terlalu sedikit untuk estimasi.')
    if np.linalg.matrix_rank(X)<X.shape[1]: raise ValueError('Matriks desain tidak full-rank: hapus prediktor yang kolinear.')
    model=sm.OLS(work[y].astype(float),X).fit(cov_type=cov)
    return model,work,X


def coefficient_table(model):
    ci=model.conf_int(); return pd.DataFrame({'koefisien':model.params,'std_error':model.bse,'statistik':model.tvalues,'p_value':model.pvalues,'CI_2.5%':ci.iloc[:,0],'CI_97.5%':ci.iloc[:,1]})


def diagnostics(model,X):
    out={}; resid=np.asarray(model.resid); n=len(resid)
    if n>=8:
        try: out['Jarque-Bera p']=float(jarque_bera(resid).pvalue)
        except Exception: pass
    try: out['Breusch-Pagan p']=float(het_breuschpagan(resid,X)[1])
    except Exception: pass
    try: out['Breusch-Godfrey p (lag 1)']=float(acorr_breusch_godfrey(model,nlags=1)[1])
    except Exception: pass
    try: out['RESET p (pangkat 2)']=float(linear_reset(model,power=2,use_f=True).pvalue)
    except Exception: pass
    try:
        influence=OLSInfluence(model)
        out['Cook’s D maksimum']=float(np.nanmax(influence.cooks_distance[0]))
    except Exception: pass
    out['Condition number']=float(np.linalg.cond(X))
    vals=[]
    for i,c in enumerate(X.columns):
        if c!='const':
            try: vals.append({'variabel':c,'VIF':float(variance_inflation_factor(X.values,i))})
            except Exception: pass
    return pd.DataFrame({'indikator':list(out),'nilai':list(out.values())}),pd.DataFrame(vals)


def fit_panel_twfe(df,y,x,entity='wilayah',time='tahun',cluster=True):
    d=df[[entity,time,y]+x].dropna().copy()
    if d[entity].nunique()<3 or d[time].nunique()<2: raise ValueError('Panel membutuhkan >=3 unit dan >=2 periode.')
    for c in [y]+x:d[c]=pd.to_numeric(d[c])
    D=pd.get_dummies(d[[entity,time]].astype(str),drop_first=True,dtype=float)
    # Explicit FE dummies: works for balanced/unbalanced panels. No between effect recovered.
    X=sm.add_constant(pd.concat([d[x].reset_index(drop=True),D.reset_index(drop=True)],axis=1),has_constant='add')
    Y=d[y].reset_index(drop=True)
    if np.linalg.matrix_rank(X)<X.shape[1]:raise ValueError('Prediktor terserap oleh fixed effects / kolinear.')
    if len(d)<=X.shape[1]+1:raise ValueError('Terlalu sedikit observasi dibanding parameter fixed effects.')
    kw={'cov_type':'cluster','cov_kwds':{'groups':d[entity].to_numpy()}} if cluster else {'cov_type':'HC3'}
    m=sm.OLS(Y,X).fit(**kw)
    return m,d


def fit_iv(df,y,x,z,controls=None):
    controls=controls or []
    d=df[[y,x,z]+controls].dropna().astype(float)
    if len(d)<15:raise ValueError('Minimal 15 observasi untuk demonstrasi IV.')
    C=sm.add_constant(d[controls],has_constant='add') if controls else pd.DataFrame({'const':np.ones(len(d))},index=d.index)
    Z=pd.concat([C,d[[z]]],axis=1); X=pd.concat([C,d[[x]]],axis=1)
    if np.linalg.matrix_rank(Z)<Z.shape[1] or np.linalg.matrix_rank(X)<X.shape[1]:raise ValueError('Kolinearitas pada instrumen/prediktor.')
    first=sm.OLS(d[x],Z).fit()
    # For one endogenous regressor and one excluded instrument, partial first-stage F.
    hyp=f'{z} = 0'; fstat=float(first.f_test(hyp).fvalue)
    Zm=Z.to_numpy(); Xm=X.to_numpy(); ym=d[y].to_numpy()
    PZX=Zm @ np.linalg.solve(Zm.T@Zm,Zm.T@Xm)
    A=PZX.T@Xm
    if np.linalg.cond(A)>1e12:raise ValueError('Instrumen terlalu lemah atau matriks hampir singular.')
    beta=np.linalg.solve(A,PZX.T@ym)
    resid=ym-Xm@beta
    # HC0 sandwich for 2SLS: (X'PzX)^-1 X'Pz diag(u^2) PzX (X'PzX)^-1.
    bread=np.linalg.inv(A); meat=PZX.T @ ((resid**2)[:,None]*PZX)
    se=np.sqrt(np.diag(bread@meat@bread)); tab=pd.DataFrame({'koefisien':beta,'SE_HC0':se,'z':beta/se},index=X.columns)
    return tab,first,fstat


def fit_did(df,y='kemiskinan_indeks',unit='kabupaten',time='tahun',treated='treated',post='post'):
    d=df[[y,unit,time,treated,post]].dropna().copy()
    if not (set(d[treated].unique())=={0,1} and set(d[post].unique())=={0,1}):raise ValueError('Treated dan post harus berupa 0 dan 1.')
    d['did']=d[treated]*d[post]
    D=pd.get_dummies(d[[unit,time]].astype(str),drop_first=True,dtype=float)
    X=sm.add_constant(pd.concat([d[['did']].reset_index(drop=True),D.reset_index(drop=True)],axis=1))
    if np.linalg.matrix_rank(X)<X.shape[1]:raise ValueError('Desain DiD tidak full-rank.')
    m=sm.OLS(d[y].to_numpy(),X).fit(cov_type='cluster',cov_kwds={'groups':d[unit].to_numpy()})
    trends=d.groupby([time,treated],as_index=False)[y].mean()
    return m,trends


def fit_ml(df,y,x,test_size=.25,seed=2026):
    d=df[[y]+x].dropna(); X=d[x].to_numpy(); Y=d[y].to_numpy()
    if len(d)<40:raise ValueError('Minimal 40 observasi untuk evaluasi train/test.')
    xtr,xte,ytr,yte=train_test_split(X,Y,test_size=test_size,random_state=seed)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    models={'Ridge':make_pipeline(StandardScaler(),Ridge(alpha=10.0)), 'Lasso':make_pipeline(StandardScaler(),Lasso(alpha=0.1,max_iter=15000)), 'Random Forest':RandomForestRegressor(n_estimators=150,min_samples_leaf=3,random_state=seed,n_jobs=1)}
    rows=[]; predictions={}
    for name,m in models.items():
        m.fit(xtr,ytr); pred=m.predict(xte)
        rows.append({'model':name,'RMSE_test':np.sqrt(mean_squared_error(yte,pred)),'MAE_test':mean_absolute_error(yte,pred),'R2_test':r2_score(yte,pred)})
        predictions[name]=pd.DataFrame({'aktual':yte,'prediksi':pred})
    return pd.DataFrame(rows).sort_values('RMSE_test'),predictions


def monte_carlo(n=100,reps=500,seed=2026,hetero=False,confounded=False):
    rng=np.random.default_rng(seed); out=[]; truth=2.0
    for _ in range(reps):
        x=rng.normal(size=n); u=rng.normal(size=n)
        err=rng.normal(size=n)*(1+0.9*np.abs(x) if hetero else 1)
        y=1+truth*x+err+(1.4*u if confounded else 0)
        xx=x+(.75*u if confounded else 0)
        m=sm.OLS(y,sm.add_constant(xx)).fit(cov_type='HC3')
        ci=np.asarray(m.conf_int())[1]
        out.append((float(m.params[1]),float(m.bse[1]),float(ci[0]<=truth<=ci[1])))
    r=pd.DataFrame(out,columns=['beta_hat','SE_HC3','covered'])
    return r,{'beta_sebenarnya':truth,'bias':r.beta_hat.mean()-truth,'RMSE':np.sqrt(np.mean((r.beta_hat-truth)**2)),'coverage_95%':r.covered.mean()}
