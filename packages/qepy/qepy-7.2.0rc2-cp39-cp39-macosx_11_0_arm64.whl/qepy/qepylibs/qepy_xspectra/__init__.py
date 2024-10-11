from __future__ import print_function, absolute_import, division
pname = 'libqepy_xspectra'

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
import libqepy_xspectra
import f90wrap.runtime
import logging
import numpy

def nexafsanalysis():
    """
    nexafsanalysis()
    
    
    Defined at molecularnexafs.fpp lines 166-520
    
    
    """
    libqepy_xspectra.f90wrap_nexafsanalysis()

def manip_spectra():
    """
    manip_spectra()
    
    
    Defined at spectra_correction.fpp lines 113-434
    
    
    """
    libqepy_xspectra.f90wrap_manip_spectra()

def x_spectra():
    """
    x_spectra()
    
    
    Defined at xspectra.fpp lines 13-591
    
    
    ------------------------------------------------------------------------------
    ------------------------------------------------------------------------------
    """
    libqepy_xspectra.f90wrap_x_spectra()

def read_input_and_bcast(filerecon, r_paw):
    """
    read_input_and_bcast(filerecon, r_paw)
    
    
    Defined at read_input_and_bcast.fpp lines 5-231
    
    Parameters
    ----------
    filerecon : str array
    r_paw : float array
    
    """
    libqepy_xspectra.f90wrap_read_input_and_bcast(filerecon=filerecon, r_paw=r_paw)


