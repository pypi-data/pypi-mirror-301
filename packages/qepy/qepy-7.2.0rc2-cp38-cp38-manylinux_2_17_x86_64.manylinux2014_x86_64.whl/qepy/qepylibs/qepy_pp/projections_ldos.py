"""
Module projections_ldos


Defined at projwfc_box.fpp lines 14-16

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_proj():
    """
    Element proj ftype=real(dp) pytype=float
    
    
    Defined at projwfc_box.fpp line 16
    
    """
    global proj
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_projections_ldos__array__proj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        proj = _arrays[array_handle]
    else:
        proj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_projections_ldos__array__proj)
        _arrays[array_handle] = proj
    return proj

def set_array_proj(proj):
    globals()['proj'][...] = proj


_array_initialisers = [get_array_proj]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "projections_ldos".')

for func in _dt_array_initialisers:
    func()
