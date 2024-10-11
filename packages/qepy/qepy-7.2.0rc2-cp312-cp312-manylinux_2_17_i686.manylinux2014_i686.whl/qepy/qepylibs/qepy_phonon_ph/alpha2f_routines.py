"""
Module alpha2f_routines


Defined at alpha2f.fpp lines 36-369

"""
from __future__ import print_function, absolute_import, division
import libqepy_phonon_ph
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def read_polarization():
    """
    read_polarization()
    
    
    Defined at alpha2f.fpp lines 45-141
    
    
    -----------------------------------------------------------------------
     This routine read the polarization vectors
     from [prefix].dyn* & lambda*.dat
    """
    libqepy_phonon_ph.f90wrap_alpha2f_routines__read_polarization()

def read_lam():
    """
    read_lam()
    
    
    Defined at alpha2f.fpp lines 145-202
    
    
    ------------------------------------------------------------------
     This routine reads \(\text{lambda}_\text{q nu}\) & \(\text{omega}_\text{q nu}\)
     from lambda*.dat
    """
    libqepy_phonon_ph.f90wrap_alpha2f_routines__read_lam()

def compute_a2f():
    """
    compute_a2f()
    
    
    Defined at alpha2f.fpp lines 206-297
    
    
    -----------------------------------------------------------------
     This routine writes a2F and phonon DOS to file(a2F.dat).
    """
    libqepy_phonon_ph.f90wrap_alpha2f_routines__compute_a2f()

def compute_lambda():
    """
    compute_lambda()
    
    
    Defined at alpha2f.fpp lines 301-367
    
    
    ---------------------------------------------------------------
     This routine computes \(\text{omega_{ln}}\) & \(\text{lambda}\).
    """
    libqepy_phonon_ph.f90wrap_alpha2f_routines__compute_lambda()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "alpha2f_routines".')

for func in _dt_array_initialisers:
    func()
