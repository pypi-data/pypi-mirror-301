"""
Module klist


Defined at pwcom.fpp lines 13-128

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def init_igk(npwx, ngm, g, gcutw):
    """
    init_igk(npwx, ngm, g, gcutw)
    
    
    Defined at pwcom.fpp lines 81-113
    
    Parameters
    ----------
    npwx : int
    ngm : int
    g : float array
    gcutw : float
    
    --------------------------------------------------------------
     Initialize indices \(\text{igk_k}\) and number of plane waves
     per k-point:
     * \((k_{ik} + G)_i = k_{ik} + G_\text{igk}\);
     * i = 1, \text{ngk}(\text{ik});
     * \text{igk} = \text{igk}_k(i,ik).
    """
    libqepy_pw.f90wrap_klist__init_igk(npwx=npwx, ngm=ngm, g=g, gcutw=gcutw)

def deallocate_igk():
    """
    deallocate_igk()
    
    
    Defined at pwcom.fpp lines 116-125
    
    
    """
    libqepy_pw.f90wrap_klist__deallocate_igk()

def get_smearing():
    """
    Element smearing ftype=character(len=32) pytype=str
    
    
    Defined at pwcom.fpp line 28
    
    """
    return libqepy_pw.f90wrap_klist__get__smearing()

def set_smearing(smearing):
    libqepy_pw.f90wrap_klist__set__smearing(smearing)

def get_array_xk():
    """
    Element xk ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 30
    
    """
    global xk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__xk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        xk = _arrays[array_handle]
    else:
        xk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__xk)
        _arrays[array_handle] = xk
    return xk

def set_array_xk(xk):
    globals()['xk'][...] = xk

def get_array_wk():
    """
    Element wk ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 32
    
    """
    global wk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__wk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wk = _arrays[array_handle]
    else:
        wk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__wk)
        _arrays[array_handle] = wk
    return wk

def set_array_wk(wk):
    globals()['wk'][...] = wk

def get_array_xqq():
    """
    Element xqq ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 34
    
    """
    global xqq
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__xqq(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        xqq = _arrays[array_handle]
    else:
        xqq = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__xqq)
        _arrays[array_handle] = xqq
    return xqq

def set_array_xqq(xqq):
    globals()['xqq'][...] = xqq

def get_degauss():
    """
    Element degauss ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 36
    
    """
    return libqepy_pw.f90wrap_klist__get__degauss()

def set_degauss(degauss):
    libqepy_pw.f90wrap_klist__set__degauss(degauss)

def get_degauss_cond():
    """
    Element degauss_cond ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 38
    
    """
    return libqepy_pw.f90wrap_klist__get__degauss_cond()

def set_degauss_cond(degauss_cond):
    libqepy_pw.f90wrap_klist__set__degauss_cond(degauss_cond)

def get_nelec():
    """
    Element nelec ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 40
    
    """
    return libqepy_pw.f90wrap_klist__get__nelec()

def set_nelec(nelec):
    libqepy_pw.f90wrap_klist__set__nelec(nelec)

def get_nelec_cond():
    """
    Element nelec_cond ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 42
    
    """
    return libqepy_pw.f90wrap_klist__get__nelec_cond()

def set_nelec_cond(nelec_cond):
    libqepy_pw.f90wrap_klist__set__nelec_cond(nelec_cond)

def get_nelup():
    """
    Element nelup ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 44
    
    """
    return libqepy_pw.f90wrap_klist__get__nelup()

def set_nelup(nelup):
    libqepy_pw.f90wrap_klist__set__nelup(nelup)

def get_neldw():
    """
    Element neldw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 46
    
    """
    return libqepy_pw.f90wrap_klist__get__neldw()

def set_neldw(neldw):
    libqepy_pw.f90wrap_klist__set__neldw(neldw)

def get_tot_magnetization():
    """
    Element tot_magnetization ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 48
    
    """
    return libqepy_pw.f90wrap_klist__get__tot_magnetization()

def set_tot_magnetization(tot_magnetization):
    libqepy_pw.f90wrap_klist__set__tot_magnetization(tot_magnetization)

def get_tot_charge():
    """
    Element tot_charge ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 50
    
    """
    return libqepy_pw.f90wrap_klist__get__tot_charge()

def set_tot_charge(tot_charge):
    libqepy_pw.f90wrap_klist__set__tot_charge(tot_charge)

def get_qnorm():
    """
    Element qnorm ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 52
    
    """
    return libqepy_pw.f90wrap_klist__get__qnorm()

def set_qnorm(qnorm):
    libqepy_pw.f90wrap_klist__set__qnorm(qnorm)

def get_array_igk_k():
    """
    Element igk_k ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 54
    
    """
    global igk_k
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__igk_k(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        igk_k = _arrays[array_handle]
    else:
        igk_k = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__igk_k)
        _arrays[array_handle] = igk_k
    return igk_k

def set_array_igk_k(igk_k):
    globals()['igk_k'][...] = igk_k

def get_array_ngk():
    """
    Element ngk ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 56
    
    """
    global ngk
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__ngk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ngk = _arrays[array_handle]
    else:
        ngk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__ngk)
        _arrays[array_handle] = ngk
    return ngk

def set_array_ngk(ngk):
    globals()['ngk'][...] = ngk

def get_array_igk_k_d():
    """
    Element igk_k_d ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 58
    
    """
    global igk_k_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__igk_k_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        igk_k_d = _arrays[array_handle]
    else:
        igk_k_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__igk_k_d)
        _arrays[array_handle] = igk_k_d
    return igk_k_d

def set_array_igk_k_d(igk_k_d):
    globals()['igk_k_d'][...] = igk_k_d

def get_array_ngk_d():
    """
    Element ngk_d ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 60
    
    """
    global ngk_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_klist__array__ngk_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ngk_d = _arrays[array_handle]
    else:
        ngk_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_klist__array__ngk_d)
        _arrays[array_handle] = ngk_d
    return ngk_d

def set_array_ngk_d(ngk_d):
    globals()['ngk_d'][...] = ngk_d

def get_nks():
    """
    Element nks ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 63
    
    """
    return libqepy_pw.f90wrap_klist__get__nks()

def set_nks(nks):
    libqepy_pw.f90wrap_klist__set__nks(nks)

def get_nkstot():
    """
    Element nkstot ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 65
    
    """
    return libqepy_pw.f90wrap_klist__get__nkstot()

def set_nkstot(nkstot):
    libqepy_pw.f90wrap_klist__set__nkstot(nkstot)

def get_ngauss():
    """
    Element ngauss ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 67
    
    """
    return libqepy_pw.f90wrap_klist__get__ngauss()

def set_ngauss(ngauss):
    libqepy_pw.f90wrap_klist__set__ngauss(ngauss)

def get_lgauss():
    """
    Element lgauss ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 69
    
    """
    return libqepy_pw.f90wrap_klist__get__lgauss()

def set_lgauss(lgauss):
    libqepy_pw.f90wrap_klist__set__lgauss(lgauss)

def get_ltetra():
    """
    Element ltetra ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 71
    
    """
    return libqepy_pw.f90wrap_klist__get__ltetra()

def set_ltetra(ltetra):
    libqepy_pw.f90wrap_klist__set__ltetra(ltetra)

def get_lxkcry():
    """
    Element lxkcry ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 73
    
    """
    return libqepy_pw.f90wrap_klist__get__lxkcry()

def set_lxkcry(lxkcry):
    libqepy_pw.f90wrap_klist__set__lxkcry(lxkcry)

def get_two_fermi_energies():
    """
    Element two_fermi_energies ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 75
    
    """
    return libqepy_pw.f90wrap_klist__get__two_fermi_energies()

def set_two_fermi_energies(two_fermi_energies):
    libqepy_pw.f90wrap_klist__set__two_fermi_energies(two_fermi_energies)


_array_initialisers = [get_array_xk, get_array_wk, get_array_xqq, \
    get_array_igk_k, get_array_ngk, get_array_igk_k_d, get_array_ngk_d]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "klist".')

for func in _dt_array_initialisers:
    func()
