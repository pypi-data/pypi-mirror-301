import os
import re
import sys
from .view3dchoose import view3dchoose
from .orca import orca
import py3Dmol
import shutil
from ipywidgets import interact
import ipywidgets as iw
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdDetermineBonds

def cleanup_qm9_xyz(fname):
    ind = open(fname).readlines()
    nAts = int(ind[0])
    # There are two smiles in the data: the one from GDB and the one assigned from the
    # 3D coordinates in the QM9 paper using OpenBabel (I think).
    gdb_smi, relax_smi = ind[-2].split()[:2]
    ind[1] = '\n'
    ind = ind[:nAts+2]
    for i in range(2, nAts+2):
        l = ind[i]
        l = l.split('\t')
        l.pop(-1)
        ind[i] = '\t'.join(l)+'\n'
    ind = ''.join(ind)
    return ind, gdb_smi, relax_smi

def draw_with_spheres(mol, width, height):
    v = py3Dmol.view(width=width, height=height)
    IPythonConsole.addMolToView(mol, v)
    v.zoomTo()
    v.setStyle({'sphere':{'radius':0.4}, 'stick':{'radius':0.1}});
    v.show()
    return v

def multicreatemol(filename, turn, width, height):
    try:
        ind = open('{0}.xyz'.format(filename), 'r+')
    except:
        raise FileNotFoundError('Perhaps your _trj.xyz file has some errors. '
                            + 'Please check the location of '
                            + 'your XYZ file and then modify your file.')
    mains = ind.readlines()
    num = eval(mains[0][:-1])
    term = len(mains)/(num+2)
    main = ''
    partmain = mains[turn*(num+2):(turn+1)*(num+2)]
    for i, line in enumerate(partmain):
        if i == 1:
            main = main + '\n'
        else:
            main = main + partmain[i]
    #print(main)
    raw_mol = Chem.MolFromXYZBlock(main)
    conn_mol = Chem.Mol(raw_mol)
    rdDetermineBonds.DetermineConnectivity(conn_mol)
    v = draw_with_spheres(conn_mol, width, height)
    return v

def freqshow(file, freqnum, loc='./', width=400, height=550):
    """
    A method to see the trajectory of the vibration, powered by py3Dmol and rdkit. Not original.
    TIPS: Make sure your multi .xyz file is in the document, or there will be NoFileFoundError!!!
    
    freqshow(file, freqnum, loc='./', width=400, height=500)
    file: File Name.
    loc: File Location. The default is your current location.
    num: The step of your convergence.
    width, height: The size of your 3D geometry molecule strcuture. Default: 300x300.
    """
    file = file + '.hess.v{0:0>3}'.format(freqnum)
    def turn(num):
        path = os.getcwd()
        os.chdir(loc)
        multicreatemol(file, 20, width, height)
        os.chdir(path)
    interact(turn, num=iw.IntSlider(min=0, max=19, step=1, value=0))