"""
Module force_mod


Defined at pwcom.fpp lines 372-398

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_force():
    """
    Element force ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 380
    
    """
    global force
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__force(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        force = _arrays[array_handle]
    else:
        force = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__force)
        _arrays[array_handle] = force
    return force

def set_array_force(force):
    globals()['force'][...] = force

def get_sumfor():
    """
    Element sumfor ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 382
    
    """
    return libqepy_pw.f90wrap_force_mod__get__sumfor()

def set_sumfor(sumfor):
    libqepy_pw.f90wrap_force_mod__set__sumfor(sumfor)

def get_array_sigma():
    """
    Element sigma ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 384
    
    """
    global sigma
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__sigma(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sigma = _arrays[array_handle]
    else:
        sigma = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__sigma)
        _arrays[array_handle] = sigma
    return sigma

def set_array_sigma(sigma):
    globals()['sigma'][...] = sigma

def get_array_eigenval():
    """
    Element eigenval ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 386
    
    """
    global eigenval
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__eigenval(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigenval = _arrays[array_handle]
    else:
        eigenval = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__eigenval)
        _arrays[array_handle] = eigenval
    return eigenval

def set_array_eigenval(eigenval):
    globals()['eigenval'][...] = eigenval

def get_array_eigenvect():
    """
    Element eigenvect ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 388
    
    """
    global eigenvect
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__eigenvect(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigenvect = _arrays[array_handle]
    else:
        eigenvect = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__eigenvect)
        _arrays[array_handle] = eigenvect
    return eigenvect

def set_array_eigenvect(eigenvect):
    globals()['eigenvect'][...] = eigenvect

def get_array_overlap_inv():
    """
    Element overlap_inv ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 390
    
    """
    global overlap_inv
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__overlap_inv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        overlap_inv = _arrays[array_handle]
    else:
        overlap_inv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__overlap_inv)
        _arrays[array_handle] = overlap_inv
    return overlap_inv

def set_array_overlap_inv(overlap_inv):
    globals()['overlap_inv'][...] = overlap_inv

def get_array_doverlap_inv():
    """
    Element doverlap_inv ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 392
    
    """
    global doverlap_inv
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__doverlap_inv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        doverlap_inv = _arrays[array_handle]
    else:
        doverlap_inv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__doverlap_inv)
        _arrays[array_handle] = doverlap_inv
    return doverlap_inv

def set_array_doverlap_inv(doverlap_inv):
    globals()['doverlap_inv'][...] = doverlap_inv

def get_array_at_dy():
    """
    Element at_dy ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 394
    
    """
    global at_dy
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__at_dy(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at_dy = _arrays[array_handle]
    else:
        at_dy = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__at_dy)
        _arrays[array_handle] = at_dy
    return at_dy

def set_array_at_dy(at_dy):
    globals()['at_dy'][...] = at_dy

def get_array_at_dj():
    """
    Element at_dj ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 394
    
    """
    global at_dj
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__at_dj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at_dj = _arrays[array_handle]
    else:
        at_dj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__at_dj)
        _arrays[array_handle] = at_dj
    return at_dj

def set_array_at_dj(at_dj):
    globals()['at_dj'][...] = at_dj

def get_array_us_dy():
    """
    Element us_dy ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 396
    
    """
    global us_dy
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__us_dy(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        us_dy = _arrays[array_handle]
    else:
        us_dy = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__us_dy)
        _arrays[array_handle] = us_dy
    return us_dy

def set_array_us_dy(us_dy):
    globals()['us_dy'][...] = us_dy

def get_array_us_dj():
    """
    Element us_dj ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 396
    
    """
    global us_dj
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_force_mod__array__us_dj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        us_dj = _arrays[array_handle]
    else:
        us_dj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_force_mod__array__us_dj)
        _arrays[array_handle] = us_dj
    return us_dj

def set_array_us_dj(us_dj):
    globals()['us_dj'][...] = us_dj


_array_initialisers = [get_array_force, get_array_sigma, get_array_eigenval, \
    get_array_eigenvect, get_array_overlap_inv, get_array_doverlap_inv, \
    get_array_at_dy, get_array_at_dj, get_array_us_dy, get_array_us_dj]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "force_mod".')

for func in _dt_array_initialisers:
    func()
