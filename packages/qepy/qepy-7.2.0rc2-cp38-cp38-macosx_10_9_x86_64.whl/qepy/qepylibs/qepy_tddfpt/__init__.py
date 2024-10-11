from __future__ import print_function, absolute_import, division
pname = 'libqepy_tddfpt'

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
import libqepy_tddfpt
import f90wrap.runtime
import logging
import numpy
import qepy_tddfpt.lr_dav_variables
import qepy_tddfpt.lr_dav_debug
import qepy_tddfpt.lr_dav_routines

def qepy_lr_dav_main_initial(infile, my_world_comm=None):
    """
    qepy_lr_dav_main_initial(infile[, my_world_comm])
    
    
    Defined at qepy_lr_dav_main.fpp lines 13-156
    
    Parameters
    ----------
    infile : str
    my_world_comm : int
    
    ---------------------------------------------------------------------
     Xiaochuan Ge, SISSA, 2013
    ---------------------------------------------------------------------
     ... overall driver routine for applying davidson algorithm
     ... to the matrix of equations coming from tddft
    ---------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_qepy_lr_dav_main_initial(infile=infile, \
        my_world_comm=my_world_comm)

def qepy_lr_dav_main_finalise():
    """
    qepy_lr_dav_main_finalise()
    
    
    Defined at qepy_lr_dav_main.fpp lines 159-181
    
    
    """
    libqepy_tddfpt.f90wrap_qepy_lr_dav_main_finalise()

def lr_dav_main():
    """
    lr_dav_main()
    
    
    Defined at lr_dav_main.fpp lines 13-145
    
    
    ---------------------------------------------------------------------
     Xiaochuan Ge, SISSA, 2013
    ---------------------------------------------------------------------
     ... overall driver routine for applying davidson algorithm
     ... to the matrix of equations coming from tddft
    ---------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_lr_dav_main()

def lr_eels_main():
    """
    lr_eels_main()
    
    
    Defined at lr_eels_main.fpp lines 13-476
    
    
    ---------------------------------------------------------------------
     This is the main driver of the turboEELS code for Electron Energy Loss \
         Spectroscopy.
     It applys the Lanczos or Sternheimer algorithm to the matrix of
     equations coming from TDDFPT.
     Iurii Timrov(Ecole Polytechnique, SISSA, and EPFL) 2010-2018
     Oscar Baseggio(SISSA) 2020
    """
    libqepy_tddfpt.f90wrap_lr_eels_main()

def lr_magnons_main():
    """
    lr_magnons_main()
    
    
    Defined at lr_magnons_main.fpp lines 13-261
    
    
    ---------------------------------------------------------------------
     This is the main driver of the turboMAGNONS code for spin-fluctation spectra in \
         magnetic system.
     It applys the Lanczos algorithm to the matrix of equations coming from TDDFPT.
     Created by Tommaso Gorni(2018)
     Modified by Oscar Baseggio(2019)
    """
    libqepy_tddfpt.f90wrap_lr_magnons_main()

def lr_main():
    """
    lr_main()
    
    
    Defined at lr_main.fpp lines 13-333
    
    
    ---------------------------------------------------------------------
     This is the main driver of the TDDFPT code
     for Absorption Spectroscopy.
     It applys the Lanczos algorithm to the matrix
     of equations coming from TDDFPT.
     Brent Walker, ICTP, 2004
     Dario Rocca, SISSA, 2006
     Osman Baris Malcioglu, SISSA, 2008
     Simone Binnie, SISSA, 2011
     Xiaochuan Ge, SISSA, 2013
     Iurii Timrov, SISSA, 2015
    """
    libqepy_tddfpt.f90wrap_lr_main()

def lr_calculate_spectrum():
    """
    lr_calculate_spectrum()
    
    
    Defined at turbo_spectrum.fpp lines 13-1982
    
    
    ---------------------------------------------------------------------
     Calculates the spectrum by solving tridiagonal problem for each value
     of the frequency omega
     Modified by Osman Baris Malcioglu(2008)
     Modified by Xiaochuan Ge(2013)
     Modified by Iurii Timrov(2015)
     Modified by Tommaso Gorni(2022)
    """
    libqepy_tddfpt.f90wrap_lr_calculate_spectrum()


lr_dav_variables = qepy_tddfpt.lr_dav_variables
lr_dav_debug = qepy_tddfpt.lr_dav_debug
lr_dav_routines = qepy_tddfpt.lr_dav_routines
