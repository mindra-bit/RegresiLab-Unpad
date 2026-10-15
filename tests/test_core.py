import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from core import *

def test_ols():
 d=generate_cross();m,w,X=fit_ols(d,'nilai',['jam_belajar','kehadiran','beban_kerja']);assert m.rsquared>.45
 assert len(coefficient_table(m))==4
 diag,vif=diagnostics(m,X);assert len(diag)>2

def test_panel():
 d=generate_panel();m,w=fit_panel_twfe(d,'produktivitas',['investasi','pendapatan']); assert abs(m.params['investasi']-1.6)<.4

def test_iv():
 d=generate_iv();tab,first,f=fit_iv(d,'outcome','treatment_endogen','instrumen');assert f>10
 assert abs(tab.loc['treatment_endogen','koefisien']-2.5)<.35

def test_did():
 d=generate_did();m,t=fit_did(d);assert abs(m.params['did']-3)<.45

def test_ml():
 d=generate_cross();r,p=fit_ml(d,'nilai',['jam_belajar','kehadiran','beban_kerja']); assert len(r)==3

def test_montecarlo():
 a,s=monte_carlo(80,100,2026);assert abs(s['bias'])<.15
