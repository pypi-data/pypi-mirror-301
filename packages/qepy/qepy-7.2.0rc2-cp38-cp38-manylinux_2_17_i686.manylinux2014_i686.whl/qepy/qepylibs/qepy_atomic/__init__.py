from __future__ import print_function, absolute_import, division
pname = 'libqepy_atomic'

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
import libqepy_atomic
import f90wrap.runtime
import logging
import numpy

def ld1():
    """
    ld1()
    
    
    Defined at ld1.fpp lines 13-80
    
    
    ---------------------------------------------------------------
         atomic self-consistent local-density program
         atomic rydberg units are used : e^2=2, m=1/2, hbar=1
         psi(r) = rR(r), where R(r) is the radial part of the wfct
         rho(r) = psi(r)^2 => rho(r) = (true charge density)*(4\pi r^2)
                           The same applies to the core charge
    ---------------------------------------------------------------
    """
    libqepy_atomic.f90wrap_ld1()


