"""
Module uspp_param


Defined at uspp_param.fpp lines 12-74

"""
from __future__ import print_function, absolute_import, division
import libqepy_upflib
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def init_uspp_dims():
    """
    init_uspp_dims()
    
    
    Defined at uspp_param.fpp lines 38-73
    
    
    """
    libqepy_upflib.f90wrap_uspp_param__init_uspp_dims()

def get_nsp():
    """
    Element nsp ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 20
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__nsp()

def set_nsp(nsp):
    libqepy_upflib.f90wrap_uspp_param__set__nsp(nsp)

def get_array_nh():
    """
    Element nh ftype=integer pytype=int
    
    
    Defined at uspp_param.fpp line 23
    
    """
    global nh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp_param__array__nh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nh = _arrays[array_handle]
    else:
        nh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp_param__array__nh)
        _arrays[array_handle] = nh
    return nh

def set_array_nh(nh):
    globals()['nh'][...] = nh

def get_nhm():
    """
    Element nhm ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 25
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__nhm()

def set_nhm(nhm):
    libqepy_upflib.f90wrap_uspp_param__set__nhm(nhm)

def get_nbetam():
    """
    Element nbetam ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 27
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__nbetam()

def set_nbetam(nbetam):
    libqepy_upflib.f90wrap_uspp_param__set__nbetam(nbetam)

def get_nwfcm():
    """
    Element nwfcm ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 29
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__nwfcm()

def set_nwfcm(nwfcm):
    libqepy_upflib.f90wrap_uspp_param__set__nwfcm(nwfcm)

def get_lmaxkb():
    """
    Element lmaxkb ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 31
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__lmaxkb()

def set_lmaxkb(lmaxkb):
    libqepy_upflib.f90wrap_uspp_param__set__lmaxkb(lmaxkb)

def get_lmaxq():
    """
    Element lmaxq ftype=integer  pytype=int
    
    
    Defined at uspp_param.fpp line 33
    
    """
    return libqepy_upflib.f90wrap_uspp_param__get__lmaxq()

def set_lmaxq(lmaxq):
    libqepy_upflib.f90wrap_uspp_param__set__lmaxq(lmaxq)


_array_initialisers = [get_array_nh]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "uspp_param".')

for func in _dt_array_initialisers:
    func()
