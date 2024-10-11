"""
Module cellmd


Defined at pwcom.fpp lines 424-451

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_at_old():
    """
    Element at_old ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 432
    
    """
    global at_old
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_cellmd__array__at_old(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at_old = _arrays[array_handle]
    else:
        at_old = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_cellmd__array__at_old)
        _arrays[array_handle] = at_old
    return at_old

def set_array_at_old(at_old):
    globals()['at_old'][...] = at_old

def get_omega_old():
    """
    Element omega_old ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 434
    
    """
    return libqepy_pw.f90wrap_cellmd__get__omega_old()

def set_omega_old(omega_old):
    libqepy_pw.f90wrap_cellmd__set__omega_old(omega_old)

def get_cell_factor():
    """
    Element cell_factor ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 436
    
    """
    return libqepy_pw.f90wrap_cellmd__get__cell_factor()

def set_cell_factor(cell_factor):
    libqepy_pw.f90wrap_cellmd__set__cell_factor(cell_factor)

def get_nzero():
    """
    Element nzero ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 439
    
    """
    return libqepy_pw.f90wrap_cellmd__get__nzero()

def set_nzero(nzero):
    libqepy_pw.f90wrap_cellmd__set__nzero(nzero)

def get_ntimes():
    """
    Element ntimes ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 441
    
    """
    return libqepy_pw.f90wrap_cellmd__get__ntimes()

def set_ntimes(ntimes):
    libqepy_pw.f90wrap_cellmd__set__ntimes(ntimes)

def get_ntcheck():
    """
    Element ntcheck ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 443
    
    """
    return libqepy_pw.f90wrap_cellmd__get__ntcheck()

def set_ntcheck(ntcheck):
    libqepy_pw.f90wrap_cellmd__set__ntcheck(ntcheck)

def get_lmovecell():
    """
    Element lmovecell ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 445
    
    """
    return libqepy_pw.f90wrap_cellmd__get__lmovecell()

def set_lmovecell(lmovecell):
    libqepy_pw.f90wrap_cellmd__set__lmovecell(lmovecell)

def get_calc():
    """
    Element calc ftype=character(len=2) pytype=str
    
    
    Defined at pwcom.fpp line 448
    
    """
    return libqepy_pw.f90wrap_cellmd__get__calc()

def set_calc(calc):
    libqepy_pw.f90wrap_cellmd__set__calc(calc)


_array_initialisers = [get_array_at_old]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "cellmd".')

for func in _dt_array_initialisers:
    func()
