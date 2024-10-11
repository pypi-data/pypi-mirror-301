"""
Module qepy_tddft_common


Defined at qepy_tddft_common.fpp lines 13-28

"""
from __future__ import print_function, absolute_import, division
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_tddft_psi():
    """
    Element tddft_psi ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 25
    
    """
    global tddft_psi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_psi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tddft_psi = _arrays[array_handle]
    else:
        tddft_psi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_psi)
        _arrays[array_handle] = tddft_psi
    return tddft_psi

def set_array_tddft_psi(tddft_psi):
    globals()['tddft_psi'][...] = tddft_psi

def get_array_b():
    """
    Element b ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 25
    
    """
    global b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        b = _arrays[array_handle]
    else:
        b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__b)
        _arrays[array_handle] = b
    return b

def set_array_b(b):
    globals()['b'][...] = b

def get_array_tddft_hpsi():
    """
    Element tddft_hpsi ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 26
    
    """
    global tddft_hpsi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_hpsi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tddft_hpsi = _arrays[array_handle]
    else:
        tddft_hpsi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_hpsi)
        _arrays[array_handle] = tddft_hpsi
    return tddft_hpsi

def set_array_tddft_hpsi(tddft_hpsi):
    globals()['tddft_hpsi'][...] = tddft_hpsi

def get_array_tddft_spsi():
    """
    Element tddft_spsi ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 26
    
    """
    global tddft_spsi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_spsi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tddft_spsi = _arrays[array_handle]
    else:
        tddft_spsi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_spsi)
        _arrays[array_handle] = tddft_spsi
    return tddft_spsi

def set_array_tddft_spsi(tddft_spsi):
    globals()['tddft_spsi'][...] = tddft_spsi

def get_array_tddft_ppsi():
    """
    Element tddft_ppsi ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 27
    
    """
    global tddft_ppsi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_ppsi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tddft_ppsi = _arrays[array_handle]
    else:
        tddft_ppsi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__tddft_ppsi)
        _arrays[array_handle] = tddft_ppsi
    return tddft_ppsi

def set_array_tddft_ppsi(tddft_ppsi):
    globals()['tddft_ppsi'][...] = tddft_ppsi

def get_array_charge():
    """
    Element charge ftype=real(dp) pytype=float
    
    
    Defined at qepy_tddft_common.fpp line 28
    
    """
    global charge
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__charge(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        charge = _arrays[array_handle]
    else:
        charge = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__charge)
        _arrays[array_handle] = charge
    return charge

def set_array_charge(charge):
    globals()['charge'][...] = charge

def get_array_dipole():
    """
    Element dipole ftype=real(dp) pytype=float
    
    
    Defined at qepy_tddft_common.fpp line 28
    
    """
    global dipole
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__dipole(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dipole = _arrays[array_handle]
    else:
        dipole = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__dipole)
        _arrays[array_handle] = dipole
    return dipole

def set_array_dipole(dipole):
    globals()['dipole'][...] = dipole

def get_array_quadrupole():
    """
    Element quadrupole ftype=real(dp) pytype=float
    
    
    Defined at qepy_tddft_common.fpp line 28
    
    """
    global quadrupole
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__quadrupole(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        quadrupole = _arrays[array_handle]
    else:
        quadrupole = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__quadrupole)
        _arrays[array_handle] = quadrupole
    return quadrupole

def set_array_quadrupole(quadrupole):
    globals()['quadrupole'][...] = quadrupole

def get_array_circular():
    """
    Element circular ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 29
    
    """
    global circular
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__circular(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        circular = _arrays[array_handle]
    else:
        circular = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__circular)
        _arrays[array_handle] = circular
    return circular

def set_array_circular(circular):
    globals()['circular'][...] = circular

def get_array_circular_local():
    """
    Element circular_local ftype=complex(dp) pytype=complex
    
    
    Defined at qepy_tddft_common.fpp line 29
    
    """
    global circular_local
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_qepy_tddft_common__array__circular_local(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        circular_local = _arrays[array_handle]
    else:
        circular_local = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_qepy_tddft_common__array__circular_local)
        _arrays[array_handle] = circular_local
    return circular_local

def set_array_circular_local(circular_local):
    globals()['circular_local'][...] = circular_local


_array_initialisers = [get_array_tddft_psi, get_array_b, get_array_tddft_hpsi, \
    get_array_tddft_spsi, get_array_tddft_ppsi, get_array_charge, \
    get_array_dipole, get_array_quadrupole, get_array_circular, \
    get_array_circular_local]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qepy_tddft_common".')

for func in _dt_array_initialisers:
    func()
