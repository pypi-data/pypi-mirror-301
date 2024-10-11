from __future__ import print_function, absolute_import, division
pname = 'libqepy_gww_head'

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
import libqepy_gww_head
import f90wrap.runtime
import logging
import numpy

def head():
    """
    head()
    
    
    Defined at head.fpp lines 15-151
    
    
    -----------------------------------------------------------------------
     ... This is the main driver of the phonon code.
     ... It reads all the quantities calculated by pwscf, it
     ... checks if some recover file is present and determines
     ... which calculation needs to be done. Finally, it makes
     ... a loop over the q points. At a generic q, if necessary it
     ... recalculates the band structure calling pwscf again.
     ... Then it can calculate the response to an atomic displacement,
     ... the dynamical matrix at that q, and the electron-phonon
     ... interaction at that q. At q=0 it can calculate the linear response
     ... to an electric field perturbation and hence the dielectric
     ... constant, the Born effective charges and the polarizability
     ... at imaginary frequencies.
     ... At q=0, from the second order response to an electric field,
     ... it can calculate also the electro-optic and the raman tensors.
     ... Presently implemented:
     ... dynamical matrix(q/=0)   NC [4], US [4], PAW [3]
     ... dynamical matrix(q=0)    NC [5], US [5], PAW [3]
     ... dielectric constant       NC [5], US [5], PAW [3]
     ... born effective charges    NC [5], US [5], PAW [3]
     ... polarizability(iu)       NC [2], US [2]
     ... elctron-phonon            NC [3], US [3]
     ... electro-optic             NC [1]
     ... raman tensor              NC [1]
     NC = norm conserving pseudopotentials
     US = ultrasoft pseudopotentials
     PAW = projector augmented-wave
     [1] LDA, [2] [1]+GGA, [3] [2]+LSDA/sGGA, [4] [3]+Spin-orbit/nonmagnetic,
     [5] [4]+Spin-orbit/magnetic
    """
    libqepy_gww_head.f90wrap_head()


