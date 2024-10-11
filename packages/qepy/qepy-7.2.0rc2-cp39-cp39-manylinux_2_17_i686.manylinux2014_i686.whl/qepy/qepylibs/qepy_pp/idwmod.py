"""
Module idwmod


Defined at idwmod.fpp lines 17-147

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def idw(iwhat):
    """
    idw(iwhat)
    
    
    Defined at idwmod.fpp lines 35-145
    
    Parameters
    ----------
    iwhat : int
    
    """
    libqepy_pp.f90wrap_idwmod__idw(iwhat=iwhat)

def get_p_metric():
    """
    Element p_metric ftype=integer  pytype=int
    
    
    Defined at idwmod.fpp line 29
    
    """
    return libqepy_pp.f90wrap_idwmod__get__p_metric()

def set_p_metric(p_metric):
    libqepy_pp.f90wrap_idwmod__set__p_metric(p_metric)

def get_scale_sphere():
    """
    Element scale_sphere ftype=real(dp) pytype=float
    
    
    Defined at idwmod.fpp line 31
    
    """
    return libqepy_pp.f90wrap_idwmod__get__scale_sphere()

def set_scale_sphere(scale_sphere):
    libqepy_pp.f90wrap_idwmod__set__scale_sphere(scale_sphere)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "idwmod".')

for func in _dt_array_initialisers:
    func()
