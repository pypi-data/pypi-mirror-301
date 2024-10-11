"""
Module grid_module


Defined at epsilon.fpp lines 13-127

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def grid_build(nw_, wmax_, wmin_, metalcalc=None):
    """
    grid_build(nw_, wmax_, wmin_[, metalcalc])
    
    
    Defined at epsilon.fpp lines 32-110
    
    Parameters
    ----------
    nw_ : int
    wmax_ : float
    wmin_ : float
    metalcalc : bool
    
    -------------------------------------------
    """
    libqepy_pp.f90wrap_grid_module__grid_build(nw_=nw_, wmax_=wmax_, wmin_=wmin_, \
        metalcalc=metalcalc)

def grid_destroy():
    """
    grid_destroy()
    
    
    Defined at epsilon.fpp lines 115-126
    
    
    ----------------------------------
    """
    libqepy_pp.f90wrap_grid_module__grid_destroy()

def get_nw():
    """
    Element nw ftype=integer                 pytype=int
    
    
    Defined at epsilon.fpp line 21
    
    """
    return libqepy_pp.f90wrap_grid_module__get__nw()

def set_nw(nw):
    libqepy_pp.f90wrap_grid_module__set__nw(nw)

def get_wmax():
    """
    Element wmax ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 22
    
    """
    return libqepy_pp.f90wrap_grid_module__get__wmax()

def set_wmax(wmax):
    libqepy_pp.f90wrap_grid_module__set__wmax(wmax)

def get_wmin():
    """
    Element wmin ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 22
    
    """
    return libqepy_pp.f90wrap_grid_module__get__wmin()

def set_wmin(wmin):
    libqepy_pp.f90wrap_grid_module__set__wmin(wmin)

def get_alpha():
    """
    Element alpha ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 23
    
    """
    return libqepy_pp.f90wrap_grid_module__get__alpha()

def set_alpha(alpha):
    libqepy_pp.f90wrap_grid_module__set__alpha(alpha)

def get_full_occ():
    """
    Element full_occ ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 23
    
    """
    return libqepy_pp.f90wrap_grid_module__get__full_occ()

def set_full_occ(full_occ):
    libqepy_pp.f90wrap_grid_module__set__full_occ(full_occ)

def get_array_focc():
    """
    Element focc ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 24
    
    """
    global focc
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_grid_module__array__focc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        focc = _arrays[array_handle]
    else:
        focc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_grid_module__array__focc)
        _arrays[array_handle] = focc
    return focc

def set_array_focc(focc):
    globals()['focc'][...] = focc

def get_array_wgrid():
    """
    Element wgrid ftype=real(dp) pytype=float
    
    
    Defined at epsilon.fpp line 24
    
    """
    global wgrid
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_grid_module__array__wgrid(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wgrid = _arrays[array_handle]
    else:
        wgrid = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_grid_module__array__wgrid)
        _arrays[array_handle] = wgrid
    return wgrid

def set_array_wgrid(wgrid):
    globals()['wgrid'][...] = wgrid


_array_initialisers = [get_array_focc, get_array_wgrid]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "grid_module".')

for func in _dt_array_initialisers:
    func()
