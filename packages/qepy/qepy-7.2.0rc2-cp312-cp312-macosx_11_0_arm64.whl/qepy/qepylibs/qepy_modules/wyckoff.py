"""
Module wyckoff


Defined at wyckoff.fpp lines 5-268

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def clean_spacegroup():
    """
    clean_spacegroup()
    
    
    Defined at wyckoff.fpp lines 79-84
    
    
    """
    libqepy_modules.f90wrap_wyckoff__clean_spacegroup()

def get_nattot():
    """
    Element nattot ftype=integer  pytype=int
    
    
    Defined at wyckoff.fpp line 9
    
    """
    return libqepy_modules.f90wrap_wyckoff__get__nattot()

def set_nattot(nattot):
    libqepy_modules.f90wrap_wyckoff__set__nattot(nattot)

def get_array_tautot():
    """
    Element tautot ftype=real(dp) pytype=float
    
    
    Defined at wyckoff.fpp line 10
    
    """
    global tautot
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_wyckoff__array__tautot(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tautot = _arrays[array_handle]
    else:
        tautot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_wyckoff__array__tautot)
        _arrays[array_handle] = tautot
    return tautot

def set_array_tautot(tautot):
    globals()['tautot'][...] = tautot

def get_array_extfortot():
    """
    Element extfortot ftype=real(dp) pytype=float
    
    
    Defined at wyckoff.fpp line 10
    
    """
    global extfortot
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_wyckoff__array__extfortot(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        extfortot = _arrays[array_handle]
    else:
        extfortot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_wyckoff__array__extfortot)
        _arrays[array_handle] = extfortot
    return extfortot

def set_array_extfortot(extfortot):
    globals()['extfortot'][...] = extfortot

def get_array_ityptot():
    """
    Element ityptot ftype=integer pytype=int
    
    
    Defined at wyckoff.fpp line 11
    
    """
    global ityptot
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_wyckoff__array__ityptot(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ityptot = _arrays[array_handle]
    else:
        ityptot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_wyckoff__array__ityptot)
        _arrays[array_handle] = ityptot
    return ityptot

def set_array_ityptot(ityptot):
    globals()['ityptot'][...] = ityptot

def get_array_if_postot():
    """
    Element if_postot ftype=integer pytype=int
    
    
    Defined at wyckoff.fpp line 11
    
    """
    global if_postot
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_wyckoff__array__if_postot(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        if_postot = _arrays[array_handle]
    else:
        if_postot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_wyckoff__array__if_postot)
        _arrays[array_handle] = if_postot
    return if_postot

def set_array_if_postot(if_postot):
    globals()['if_postot'][...] = if_postot


_array_initialisers = [get_array_tautot, get_array_extfortot, get_array_ityptot, \
    get_array_if_postot]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "wyckoff".')

for func in _dt_array_initialisers:
    func()
