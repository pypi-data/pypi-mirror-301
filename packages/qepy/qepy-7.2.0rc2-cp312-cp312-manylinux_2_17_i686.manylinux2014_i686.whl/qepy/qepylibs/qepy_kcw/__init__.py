from __future__ import print_function, absolute_import, division
pname = 'libqepy_kcw'

# control the output
import sys
from importlib import import_module
from qepy.core import Logger, env
class QEpyLib :
    def __init__(self, **kwargs):
        qepylib = import_module(pname)
        sys.modules[pname] = self
        self.qepylib = qepylib

    def __getattr__(self, attr):
        attr_value = getattr(self.qepylib, attr)
        if '__array__' not in attr :
            attr_value = Logger.stdout2file(attr_value, fileobj=env['STDOUT'])
        return attr_value
qepylib = QEpyLib()
import libqepy_kcw
import f90wrap.runtime
import logging
import numpy

def kcw():
    """
    kcw()
    
    
    Defined at kcw.fpp lines 14-89
    
    
    -----------------------------------------------------------------
     This is the main driver of the kcw.x code, an implementation of koopmans
     functionals based on DFPT and Wannier functions. The code reads the output
     of PWSCF and Wannier90 and performe a Koopmans calculation in a perturbative
     way. It performe several task depending on the vaule of the variable \
         "calculation".
     1) calculation=wann2kcw: interface between PWSCF and W90, and KCW.
     2) calculation=screen: calculates the screening coefficients as described in
        N. Colonna et al. J. Chem. Theory Comput. 14, 2549(2018)
        N. Colonna et al. J. Chem. Theory Comput. 18, 5435(2022)
     3) calculation=ham: compute, interpolate and diagonalize the KC hamiltonian
      Code written by Nicola Colonna(EPFL April 2019)
    """
    libqepy_kcw.f90wrap_kcw()


