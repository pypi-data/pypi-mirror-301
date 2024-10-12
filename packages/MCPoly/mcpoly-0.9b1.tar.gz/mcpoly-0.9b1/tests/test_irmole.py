from MCPoly.irmole import irfig
from MCPoly.irmole import irout
from MCPoly.irmole import relat_peaks
import pytest
import os
import re

@pytest.fixture
def pre_irfig():
    return irfig('1_0.0.hess.ir.dat', loc='./MCPoly/tests/data_irmole/')

def test1_irfig(pre_irfig):
    assert pre_irfig.freq[4] == 314.47
    assert pre_irfig.intensity[5] == -0.0013418445383877042
    assert pre_irfig.I[5] == -0.0013418445383877042
    assert pre_irfig.intensity_R[7] == 0.0012840566467957615
    assert pre_irfig.I_R[7] == 0.0012840566467957615

def test2_irfig(pre_irfig):
    assert len(pre_irfig.peaks) == 12
    assert pre_irfig.peaks[2] == -0.002037461567738319
    assert pre_irfig.peaks_freq[2] == 650.83
    assert pre_irfig.peaks[-1] == -0.01623182936612011
    assert pre_irfig.peaks_freq[-1] == 3121.11

def test3_irfig(pre_irfig):
    num = 0
    try:
        t = pre_irfig.tops_freq
        num = 1
    except:
        pass
    assert num == 0

def test4_irfig(pre_irfig):
    pre_irfig.toprank(3)
    assert pre_irfig.tops == [-0.348795556492405, -0.17936415753672463, -0.08553973141476945]
    assert pre_irfig.tops_R == [0.348795556492405, 0.17936415753672463, 0.08553973141476945]
    assert pre_irfig.tops_freq == [1262.07, 1844.38, 1092.08]
        
@pytest.fixture
def pre_irout():
    return irout('1_0.0', loc='./MCPoly/tests/data_irmole/')

def test1_irout(pre_irout):
    assert pre_irout.freq[10] == 32.48
    assert pre_irout.intensity[10] == 0.82
    assert pre_irout.I[10] == 0.82

def test2_irout(pre_irout):
    num = 0
    try:
        t = pre_irout.tops_freq
        num = 1
    except:
        pass
    assert num == 0

def test3_irout(pre_irout):
    pre_irout.toprank(3)
    assert pre_irout.tops == [1315.15, 374.48, 357.63]
    assert pre_irout.tops_freq == [1264.96, 1837.35, 1220.56]
    
@pytest.fixture
def test_relat_peaks():
    f = irfig('1_0.0.hess.ir.dat', loc='./MCPoly/tests/data_irmole/')
    f.toprank(3)
    f2 = irout('1_0.0', loc='./data_irmole/')
    real_tops, real_tops_freq, js = relat_peaks(f.tops_freq, f2.I, f2.freq, neednum=True)
    assert real_tops == [1315.15, 374.48, 357.63]
    assert real_tops_freq == [1264.96, 1837.35, 1220.56]
    assert js == [77, 102, 71] 