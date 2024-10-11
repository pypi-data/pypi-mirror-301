"""
Module basis


Defined at atomic_wfc_mod.fpp lines 14-33

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_natomwfc():
    """
    Element natomwfc ftype=integer  pytype=int
    
    
    Defined at atomic_wfc_mod.fpp line 22
    
    """
    return libqepy_pw.f90wrap_basis__get__natomwfc()

def set_natomwfc(natomwfc):
    libqepy_pw.f90wrap_basis__set__natomwfc(natomwfc)

def get_array_wfcatom():
    """
    Element wfcatom ftype=complex(dp) pytype=complex
    
    
    Defined at atomic_wfc_mod.fpp line 24
    
    """
    global wfcatom
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_basis__array__wfcatom(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wfcatom = _arrays[array_handle]
    else:
        wfcatom = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_basis__array__wfcatom)
        _arrays[array_handle] = wfcatom
    return wfcatom

def set_array_wfcatom(wfcatom):
    globals()['wfcatom'][...] = wfcatom

def get_array_swfcatom():
    """
    Element swfcatom ftype=complex(dp) pytype=complex
    
    
    Defined at atomic_wfc_mod.fpp line 26
    
    """
    global swfcatom
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_basis__array__swfcatom(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        swfcatom = _arrays[array_handle]
    else:
        swfcatom = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_basis__array__swfcatom)
        _arrays[array_handle] = swfcatom
    return swfcatom

def set_array_swfcatom(swfcatom):
    globals()['swfcatom'][...] = swfcatom

def get_starting_wfc():
    """
    Element starting_wfc ftype=character(len=30) pytype=str
    
    
    Defined at atomic_wfc_mod.fpp line 28
    
    """
    return libqepy_pw.f90wrap_basis__get__starting_wfc()

def set_starting_wfc(starting_wfc):
    libqepy_pw.f90wrap_basis__set__starting_wfc(starting_wfc)

def get_starting_pot():
    """
    Element starting_pot ftype=character(len=30) pytype=str
    
    
    Defined at atomic_wfc_mod.fpp line 30
    
    """
    return libqepy_pw.f90wrap_basis__get__starting_pot()

def set_starting_pot(starting_pot):
    libqepy_pw.f90wrap_basis__set__starting_pot(starting_pot)

def get_startingconfig():
    """
    Element startingconfig ftype=character(len=30) pytype=str
    
    
    Defined at atomic_wfc_mod.fpp line 32
    
    """
    return libqepy_pw.f90wrap_basis__get__startingconfig()

def set_startingconfig(startingconfig):
    libqepy_pw.f90wrap_basis__set__startingconfig(startingconfig)


_array_initialisers = [get_array_wfcatom, get_array_swfcatom]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "basis".')

for func in _dt_array_initialisers:
    func()
