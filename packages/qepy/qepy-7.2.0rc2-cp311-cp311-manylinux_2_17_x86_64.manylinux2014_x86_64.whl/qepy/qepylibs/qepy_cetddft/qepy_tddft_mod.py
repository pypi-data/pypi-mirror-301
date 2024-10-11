"""
Module qepy_tddft_mod


Defined at qepy_tddft_mod.fpp lines 5-32

"""
from __future__ import print_function, absolute_import, division
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qepy_cetddft_wfc2rho(iunit=None):
    """
    qepy_cetddft_wfc2rho([iunit])
    
    
    Defined at qepy_tddft_mod.fpp lines 12-32
    
    Parameters
    ----------
    iunit : int
    
    """
    libqepy_cetddft.f90wrap_qepy_tddft_mod__qepy_cetddft_wfc2rho(iunit=iunit)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qepy_tddft_mod".')

for func in _dt_array_initialisers:
    func()
