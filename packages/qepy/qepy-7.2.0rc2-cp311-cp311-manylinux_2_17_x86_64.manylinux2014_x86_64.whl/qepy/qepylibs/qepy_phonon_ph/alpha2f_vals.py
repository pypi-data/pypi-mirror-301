"""
Module alpha2f_vals


Defined at alpha2f.fpp lines 18-32

"""
from __future__ import print_function, absolute_import, division
import libqepy_phonon_ph
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nfreq():
    """
    Element nfreq ftype=integer  pytype=int
    
    
    Defined at alpha2f.fpp line 26
    
    """
    return libqepy_phonon_ph.f90wrap_alpha2f_vals__get__nfreq()

def set_nfreq(nfreq):
    libqepy_phonon_ph.f90wrap_alpha2f_vals__set__nfreq(nfreq)

def get_array_omg():
    """
    Element omg ftype=real(dp) pytype=float
    
    
    Defined at alpha2f.fpp line 31
    
    """
    global omg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_alpha2f_vals__array__omg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        omg = _arrays[array_handle]
    else:
        omg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_alpha2f_vals__array__omg)
        _arrays[array_handle] = omg
    return omg

def set_array_omg(omg):
    globals()['omg'][...] = omg

def get_array_lam():
    """
    Element lam ftype=real(dp) pytype=float
    
    
    Defined at alpha2f.fpp line 31
    
    """
    global lam
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_alpha2f_vals__array__lam(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lam = _arrays[array_handle]
    else:
        lam = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_alpha2f_vals__array__lam)
        _arrays[array_handle] = lam
    return lam

def set_array_lam(lam):
    globals()['lam'][...] = lam

def get_array_pol():
    """
    Element pol ftype=real(dp) pytype=float
    
    
    Defined at alpha2f.fpp line 31
    
    """
    global pol
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_alpha2f_vals__array__pol(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        pol = _arrays[array_handle]
    else:
        pol = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_alpha2f_vals__array__pol)
        _arrays[array_handle] = pol
    return pol

def set_array_pol(pol):
    globals()['pol'][...] = pol


_array_initialisers = [get_array_omg, get_array_lam, get_array_pol]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "alpha2f_vals".')

for func in _dt_array_initialisers:
    func()
