"""
Module lsda_mod


Defined at pwcom.fpp lines 133-161

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_lsda():
    """
    Element lsda ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 144
    
    """
    return libqepy_pw.f90wrap_lsda_mod__get__lsda()

def set_lsda(lsda):
    libqepy_pw.f90wrap_lsda_mod__set__lsda(lsda)

def get_magtot():
    """
    Element magtot ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 146
    
    """
    return libqepy_pw.f90wrap_lsda_mod__get__magtot()

def set_magtot(magtot):
    libqepy_pw.f90wrap_lsda_mod__set__magtot(magtot)

def get_absmag():
    """
    Element absmag ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 148
    
    """
    return libqepy_pw.f90wrap_lsda_mod__get__absmag()

def set_absmag(absmag):
    libqepy_pw.f90wrap_lsda_mod__set__absmag(absmag)

def get_array_starting_magnetization():
    """
    Element starting_magnetization ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 150
    
    """
    global starting_magnetization
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_lsda_mod__array__starting_magnetization(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        starting_magnetization = _arrays[array_handle]
    else:
        starting_magnetization = \
            f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_lsda_mod__array__starting_magnetization)
        _arrays[array_handle] = starting_magnetization
    return starting_magnetization

def set_array_starting_magnetization(starting_magnetization):
    globals()['starting_magnetization'][...] = starting_magnetization

def get_nspin():
    """
    Element nspin ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 152
    
    """
    return libqepy_pw.f90wrap_lsda_mod__get__nspin()

def set_nspin(nspin):
    libqepy_pw.f90wrap_lsda_mod__set__nspin(nspin)

def get_current_spin():
    """
    Element current_spin ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 154
    
    """
    return libqepy_pw.f90wrap_lsda_mod__get__current_spin()

def set_current_spin(current_spin):
    libqepy_pw.f90wrap_lsda_mod__set__current_spin(current_spin)

def get_array_isk():
    """
    Element isk ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 156
    
    """
    global isk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_lsda_mod__array__isk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        isk = _arrays[array_handle]
    else:
        isk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_lsda_mod__array__isk)
        _arrays[array_handle] = isk
    return isk

def set_array_isk(isk):
    globals()['isk'][...] = isk

def get_array_local_charges():
    """
    Element local_charges ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 158
    
    """
    global local_charges
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_lsda_mod__array__local_charges(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        local_charges = _arrays[array_handle]
    else:
        local_charges = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_lsda_mod__array__local_charges)
        _arrays[array_handle] = local_charges
    return local_charges

def set_array_local_charges(local_charges):
    globals()['local_charges'][...] = local_charges

def get_array_local_mag():
    """
    Element local_mag ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 158
    
    """
    global local_mag
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_lsda_mod__array__local_mag(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        local_mag = _arrays[array_handle]
    else:
        local_mag = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_lsda_mod__array__local_mag)
        _arrays[array_handle] = local_mag
    return local_mag

def set_array_local_mag(local_mag):
    globals()['local_mag'][...] = local_mag


_array_initialisers = [get_array_starting_magnetization, get_array_isk, \
    get_array_local_charges, get_array_local_mag]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "lsda_mod".')

for func in _dt_array_initialisers:
    func()
