"""
Module ifconstants


Defined at matdyn.fpp lines 12-32

"""
from __future__ import print_function, absolute_import, division
import libqepy_phonon_ph
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_frc():
    """
    Element frc ftype=real(dp) pytype=float
    
    
    Defined at matdyn.fpp line 18
    
    """
    global frc
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__frc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        frc = _arrays[array_handle]
    else:
        frc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__frc)
        _arrays[array_handle] = frc
    return frc

def set_array_frc(frc):
    globals()['frc'][...] = frc

def get_array_frc_lr():
    """
    Element frc_lr ftype=real(dp) pytype=float
    
    
    Defined at matdyn.fpp line 20
    
    """
    global frc_lr
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__frc_lr(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        frc_lr = _arrays[array_handle]
    else:
        frc_lr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__frc_lr)
        _arrays[array_handle] = frc_lr
    return frc_lr

def set_array_frc_lr(frc_lr):
    globals()['frc_lr'][...] = frc_lr

def get_array_tau_blk():
    """
    Element tau_blk ftype=real(dp) pytype=float
    
    
    Defined at matdyn.fpp line 22
    
    """
    global tau_blk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__tau_blk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tau_blk = _arrays[array_handle]
    else:
        tau_blk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__tau_blk)
        _arrays[array_handle] = tau_blk
    return tau_blk

def set_array_tau_blk(tau_blk):
    globals()['tau_blk'][...] = tau_blk

def get_array_zeu():
    """
    Element zeu ftype=real(dp) pytype=float
    
    
    Defined at matdyn.fpp line 24
    
    """
    global zeu
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__zeu(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        zeu = _arrays[array_handle]
    else:
        zeu = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__zeu)
        _arrays[array_handle] = zeu
    return zeu

def set_array_zeu(zeu):
    globals()['zeu'][...] = zeu

def get_array_m_loc():
    """
    Element m_loc ftype=real(dp) pytype=float
    
    
    Defined at matdyn.fpp line 26
    
    """
    global m_loc
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__m_loc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m_loc = _arrays[array_handle]
    else:
        m_loc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__m_loc)
        _arrays[array_handle] = m_loc
    return m_loc

def set_array_m_loc(m_loc):
    globals()['m_loc'][...] = m_loc

def get_array_ityp_blk():
    """
    Element ityp_blk ftype=integer pytype=int
    
    
    Defined at matdyn.fpp line 28
    
    """
    global ityp_blk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__ityp_blk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ityp_blk = _arrays[array_handle]
    else:
        ityp_blk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__ityp_blk)
        _arrays[array_handle] = ityp_blk
    return ityp_blk

def set_array_ityp_blk(ityp_blk):
    globals()['ityp_blk'][...] = ityp_blk

def get_array_atm():
    """
    Element atm ftype=character(len=3) pytype=str
    
    
    Defined at matdyn.fpp line 31
    
    """
    global atm
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_phonon_ph.f90wrap_ifconstants__array__atm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        atm = _arrays[array_handle]
    else:
        atm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_phonon_ph.f90wrap_ifconstants__array__atm)
        _arrays[array_handle] = atm
    return atm

def set_array_atm(atm):
    globals()['atm'][...] = atm


_array_initialisers = [get_array_frc, get_array_frc_lr, get_array_tau_blk, \
    get_array_zeu, get_array_m_loc, get_array_ityp_blk, get_array_atm]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "ifconstants".')

for func in _dt_array_initialisers:
    func()
