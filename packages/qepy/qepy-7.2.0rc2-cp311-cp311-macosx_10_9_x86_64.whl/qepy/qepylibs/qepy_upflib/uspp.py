"""
Module uspp


Defined at uspp.fpp lines 14-435

"""
from __future__ import print_function, absolute_import, division
import libqepy_upflib
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def aainit(lli):
    """
    aainit(lli)
    
    
    Defined at uspp.fpp lines 118-191
    
    Parameters
    ----------
    lli : int
    
    -----------------------------------------------------------------------
     this routine computes the coefficients of the expansion of the product
     of two real spherical harmonics into real spherical harmonics.
         Y_limi(r) * Y_ljmj(r) = \sum_LM  ap(LM,limi,ljmj)  Y_LM(r)
     On output:
     ap     the expansion coefficients
     lpx    for each input limi,ljmj is the number of LM in the sum
     lpl    for each input limi,ljmj points to the allowed LM
     The indices limi,ljmj and LM assume the order for real spherical
     harmonics given in routine ylmr2
    """
    libqepy_upflib.f90wrap_uspp__aainit(lli=lli)

def allocate_uspp(use_gpu, noncolin, lspinorb, tqr, nhm, nsp, nat, nspin):
    """
    allocate_uspp(use_gpu, noncolin, lspinorb, tqr, nhm, nsp, nat, nspin)
    
    
    Defined at uspp.fpp lines 303-366
    
    Parameters
    ----------
    use_gpu : bool
    noncolin : bool
    lspinorb : bool
    tqr : bool
    nhm : int
    nsp : int
    nat : int
    nspin : int
    
    -----------------------------------------------------------------------
    """
    libqepy_upflib.f90wrap_uspp__allocate_uspp(use_gpu=use_gpu, noncolin=noncolin, \
        lspinorb=lspinorb, tqr=tqr, nhm=nhm, nsp=nsp, nat=nat, nspin=nspin)

def deallocate_uspp():
    """
    deallocate_uspp()
    
    
    Defined at uspp.fpp lines 370-425
    
    
    -----------------------------------------------------------------------
    """
    libqepy_upflib.f90wrap_uspp__deallocate_uspp()

def get_nlx():
    """
    Element nlx ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 43
    
    """
    return libqepy_upflib.f90wrap_uspp__get__nlx()

nlx = get_nlx()

def get_array_lpx():
    """
    Element lpx ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 47
    
    """
    global lpx
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__lpx(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpx = _arrays[array_handle]
    else:
        lpx = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__lpx)
        _arrays[array_handle] = lpx
    return lpx

def set_array_lpx(lpx):
    globals()['lpx'][...] = lpx

def get_array_lpl():
    """
    Element lpl ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 47
    
    """
    global lpl
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__lpl(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpl = _arrays[array_handle]
    else:
        lpl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__lpl)
        _arrays[array_handle] = lpl
    return lpl

def set_array_lpl(lpl):
    globals()['lpl'][...] = lpl

def get_array_ap():
    """
    Element ap ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 48
    
    """
    global ap
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ap(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ap = _arrays[array_handle]
    else:
        ap = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ap)
        _arrays[array_handle] = ap
    return ap

def set_array_ap(ap):
    globals()['ap'][...] = ap

def get_array_lpx_d():
    """
    Element lpx_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 53
    
    """
    global lpx_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__lpx_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpx_d = _arrays[array_handle]
    else:
        lpx_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__lpx_d)
        _arrays[array_handle] = lpx_d
    return lpx_d

def set_array_lpx_d(lpx_d):
    globals()['lpx_d'][...] = lpx_d

def get_array_lpl_d():
    """
    Element lpl_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 53
    
    """
    global lpl_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__lpl_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpl_d = _arrays[array_handle]
    else:
        lpl_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__lpl_d)
        _arrays[array_handle] = lpl_d
    return lpl_d

def set_array_lpl_d(lpl_d):
    globals()['lpl_d'][...] = lpl_d

def get_array_ap_d():
    """
    Element ap_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 54
    
    """
    global ap_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ap_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ap_d = _arrays[array_handle]
    else:
        ap_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ap_d)
        _arrays[array_handle] = ap_d
    return ap_d

def set_array_ap_d(ap_d):
    globals()['ap_d'][...] = ap_d

def get_nkb():
    """
    Element nkb ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 58
    
    """
    return libqepy_upflib.f90wrap_uspp__get__nkb()

def set_nkb(nkb):
    libqepy_upflib.f90wrap_uspp__set__nkb(nkb)

def get_nkbus():
    """
    Element nkbus ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 58
    
    """
    return libqepy_upflib.f90wrap_uspp__get__nkbus()

def set_nkbus(nkbus):
    libqepy_upflib.f90wrap_uspp__set__nkbus(nkbus)

def get_array_indv():
    """
    Element indv ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 65
    
    """
    global indv
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__indv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        indv = _arrays[array_handle]
    else:
        indv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__indv)
        _arrays[array_handle] = indv
    return indv

def set_array_indv(indv):
    globals()['indv'][...] = indv

def get_array_nhtol():
    """
    Element nhtol ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 65
    
    """
    global nhtol
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtol(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtol = _arrays[array_handle]
    else:
        nhtol = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtol)
        _arrays[array_handle] = nhtol
    return nhtol

def set_array_nhtol(nhtol):
    globals()['nhtol'][...] = nhtol

def get_array_nhtolm():
    """
    Element nhtolm ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 65
    
    """
    global nhtolm
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtolm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtolm = _arrays[array_handle]
    else:
        nhtolm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtolm)
        _arrays[array_handle] = nhtolm
    return nhtolm

def set_array_nhtolm(nhtolm):
    globals()['nhtolm'][...] = nhtolm

def get_array_ijtoh():
    """
    Element ijtoh ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 65
    
    """
    global ijtoh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ijtoh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ijtoh = _arrays[array_handle]
    else:
        ijtoh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ijtoh)
        _arrays[array_handle] = ijtoh
    return ijtoh

def set_array_ijtoh(ijtoh):
    globals()['ijtoh'][...] = ijtoh

def get_array_ofsbeta():
    """
    Element ofsbeta ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 65
    
    """
    global ofsbeta
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ofsbeta(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ofsbeta = _arrays[array_handle]
    else:
        ofsbeta = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ofsbeta)
        _arrays[array_handle] = ofsbeta
    return ofsbeta

def set_array_ofsbeta(ofsbeta):
    globals()['ofsbeta'][...] = ofsbeta

def get_array_indv_d():
    """
    Element indv_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 69
    
    """
    global indv_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__indv_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        indv_d = _arrays[array_handle]
    else:
        indv_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__indv_d)
        _arrays[array_handle] = indv_d
    return indv_d

def set_array_indv_d(indv_d):
    globals()['indv_d'][...] = indv_d

def get_array_nhtol_d():
    """
    Element nhtol_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 70
    
    """
    global nhtol_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtol_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtol_d = _arrays[array_handle]
    else:
        nhtol_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtol_d)
        _arrays[array_handle] = nhtol_d
    return nhtol_d

def set_array_nhtol_d(nhtol_d):
    globals()['nhtol_d'][...] = nhtol_d

def get_array_nhtolm_d():
    """
    Element nhtolm_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 71
    
    """
    global nhtolm_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtolm_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtolm_d = _arrays[array_handle]
    else:
        nhtolm_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtolm_d)
        _arrays[array_handle] = nhtolm_d
    return nhtolm_d

def set_array_nhtolm_d(nhtolm_d):
    globals()['nhtolm_d'][...] = nhtolm_d

def get_array_ijtoh_d():
    """
    Element ijtoh_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 72
    
    """
    global ijtoh_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ijtoh_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ijtoh_d = _arrays[array_handle]
    else:
        ijtoh_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ijtoh_d)
        _arrays[array_handle] = ijtoh_d
    return ijtoh_d

def set_array_ijtoh_d(ijtoh_d):
    globals()['ijtoh_d'][...] = ijtoh_d

def get_array_ofsbeta_d():
    """
    Element ofsbeta_d ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 73
    
    """
    global ofsbeta_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ofsbeta_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ofsbeta_d = _arrays[array_handle]
    else:
        ofsbeta_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ofsbeta_d)
        _arrays[array_handle] = ofsbeta_d
    return ofsbeta_d

def set_array_ofsbeta_d(ofsbeta_d):
    globals()['ofsbeta_d'][...] = ofsbeta_d

def get_okvan():
    """
    Element okvan ftype=logical pytype=bool
    
    
    Defined at uspp.fpp line 76
    
    """
    return libqepy_upflib.f90wrap_uspp__get__okvan()

def set_okvan(okvan):
    libqepy_upflib.f90wrap_uspp__set__okvan(okvan)

def get_nlcc_any():
    """
    Element nlcc_any ftype=logical pytype=bool
    
    
    Defined at uspp.fpp line 76
    
    """
    return libqepy_upflib.f90wrap_uspp__get__nlcc_any()

def set_nlcc_any(nlcc_any):
    libqepy_upflib.f90wrap_uspp__set__nlcc_any(nlcc_any)

def get_array_vkb():
    """
    Element vkb ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 81
    
    """
    global vkb
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__vkb(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vkb = _arrays[array_handle]
    else:
        vkb = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__vkb)
        _arrays[array_handle] = vkb
    return vkb

def set_array_vkb(vkb):
    globals()['vkb'][...] = vkb

def get_array_becsum():
    """
    Element becsum ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 83
    
    """
    global becsum
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__becsum(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        becsum = _arrays[array_handle]
    else:
        becsum = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__becsum)
        _arrays[array_handle] = becsum
    return becsum

def set_array_becsum(becsum):
    globals()['becsum'][...] = becsum

def get_array_ebecsum():
    """
    Element ebecsum ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 85
    
    """
    global ebecsum
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ebecsum(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ebecsum = _arrays[array_handle]
    else:
        ebecsum = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ebecsum)
        _arrays[array_handle] = ebecsum
    return ebecsum

def set_array_ebecsum(ebecsum):
    globals()['ebecsum'][...] = ebecsum

def get_array_dvan():
    """
    Element dvan ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 91
    
    """
    global dvan
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__dvan(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan = _arrays[array_handle]
    else:
        dvan = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__dvan)
        _arrays[array_handle] = dvan
    return dvan

def set_array_dvan(dvan):
    globals()['dvan'][...] = dvan

def get_array_deeq():
    """
    Element deeq ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 91
    
    """
    global deeq
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__deeq(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        deeq = _arrays[array_handle]
    else:
        deeq = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__deeq)
        _arrays[array_handle] = deeq
    return deeq

def set_array_deeq(deeq):
    globals()['deeq'][...] = deeq

def get_array_qq_nt():
    """
    Element qq_nt ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 91
    
    """
    global qq_nt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__qq_nt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_nt = _arrays[array_handle]
    else:
        qq_nt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__qq_nt)
        _arrays[array_handle] = qq_nt
    return qq_nt

def set_array_qq_nt(qq_nt):
    globals()['qq_nt'][...] = qq_nt

def get_array_qq_at():
    """
    Element qq_at ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 91
    
    """
    global qq_at
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__qq_at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_at = _arrays[array_handle]
    else:
        qq_at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__qq_at)
        _arrays[array_handle] = qq_at
    return qq_at

def set_array_qq_at(qq_at):
    globals()['qq_at'][...] = qq_at

def get_array_nhtoj():
    """
    Element nhtoj ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 91
    
    """
    global nhtoj
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtoj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtoj = _arrays[array_handle]
    else:
        nhtoj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtoj)
        _arrays[array_handle] = nhtoj
    return nhtoj

def set_array_nhtoj(nhtoj):
    globals()['nhtoj'][...] = nhtoj

def get_array_qq_so():
    """
    Element qq_so ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 96
    
    """
    global qq_so
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__qq_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_so = _arrays[array_handle]
    else:
        qq_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__qq_so)
        _arrays[array_handle] = qq_so
    return qq_so

def set_array_qq_so(qq_so):
    globals()['qq_so'][...] = qq_so

def get_array_dvan_so():
    """
    Element dvan_so ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 96
    
    """
    global dvan_so
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__dvan_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan_so = _arrays[array_handle]
    else:
        dvan_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__dvan_so)
        _arrays[array_handle] = dvan_so
    return dvan_so

def set_array_dvan_so(dvan_so):
    globals()['dvan_so'][...] = dvan_so

def get_array_deeq_nc():
    """
    Element deeq_nc ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 96
    
    """
    global deeq_nc
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__deeq_nc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        deeq_nc = _arrays[array_handle]
    else:
        deeq_nc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__deeq_nc)
        _arrays[array_handle] = deeq_nc
    return deeq_nc

def set_array_deeq_nc(deeq_nc):
    globals()['deeq_nc'][...] = deeq_nc

def get_array_becsum_d():
    """
    Element becsum_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 100
    
    """
    global becsum_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__becsum_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        becsum_d = _arrays[array_handle]
    else:
        becsum_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__becsum_d)
        _arrays[array_handle] = becsum_d
    return becsum_d

def set_array_becsum_d(becsum_d):
    globals()['becsum_d'][...] = becsum_d

def get_array_ebecsum_d():
    """
    Element ebecsum_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 101
    
    """
    global ebecsum_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__ebecsum_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ebecsum_d = _arrays[array_handle]
    else:
        ebecsum_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__ebecsum_d)
        _arrays[array_handle] = ebecsum_d
    return ebecsum_d

def set_array_ebecsum_d(ebecsum_d):
    globals()['ebecsum_d'][...] = ebecsum_d

def get_array_dvan_d():
    """
    Element dvan_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 102
    
    """
    global dvan_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__dvan_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan_d = _arrays[array_handle]
    else:
        dvan_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__dvan_d)
        _arrays[array_handle] = dvan_d
    return dvan_d

def set_array_dvan_d(dvan_d):
    globals()['dvan_d'][...] = dvan_d

def get_array_qq_nt_d():
    """
    Element qq_nt_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 103
    
    """
    global qq_nt_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__qq_nt_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_nt_d = _arrays[array_handle]
    else:
        qq_nt_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__qq_nt_d)
        _arrays[array_handle] = qq_nt_d
    return qq_nt_d

def set_array_qq_nt_d(qq_nt_d):
    globals()['qq_nt_d'][...] = qq_nt_d

def get_array_nhtoj_d():
    """
    Element nhtoj_d ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 104
    
    """
    global nhtoj_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__nhtoj_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtoj_d = _arrays[array_handle]
    else:
        nhtoj_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__nhtoj_d)
        _arrays[array_handle] = nhtoj_d
    return nhtoj_d

def set_array_nhtoj_d(nhtoj_d):
    globals()['nhtoj_d'][...] = nhtoj_d

def get_array_dvan_so_d():
    """
    Element dvan_so_d ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 105
    
    """
    global dvan_so_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__dvan_so_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan_so_d = _arrays[array_handle]
    else:
        dvan_so_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__dvan_so_d)
        _arrays[array_handle] = dvan_so_d
    return dvan_so_d

def set_array_dvan_so_d(dvan_so_d):
    globals()['dvan_so_d'][...] = dvan_so_d

def get_array_beta():
    """
    Element beta ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 111
    
    """
    global beta
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__beta(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        beta = _arrays[array_handle]
    else:
        beta = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__beta)
        _arrays[array_handle] = beta
    return beta

def set_array_beta(beta):
    globals()['beta'][...] = beta

def get_array_dbeta():
    """
    Element dbeta ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 113
    
    """
    global dbeta
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_upflib.f90wrap_uspp__array__dbeta(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dbeta = _arrays[array_handle]
    else:
        dbeta = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_upflib.f90wrap_uspp__array__dbeta)
        _arrays[array_handle] = dbeta
    return dbeta

def set_array_dbeta(dbeta):
    globals()['dbeta'][...] = dbeta


_array_initialisers = [get_array_lpx, get_array_lpl, get_array_ap, \
    get_array_lpx_d, get_array_lpl_d, get_array_ap_d, get_array_indv, \
    get_array_nhtol, get_array_nhtolm, get_array_ijtoh, get_array_ofsbeta, \
    get_array_indv_d, get_array_nhtol_d, get_array_nhtolm_d, get_array_ijtoh_d, \
    get_array_ofsbeta_d, get_array_vkb, get_array_becsum, get_array_ebecsum, \
    get_array_dvan, get_array_deeq, get_array_qq_nt, get_array_qq_at, \
    get_array_nhtoj, get_array_qq_so, get_array_dvan_so, get_array_deeq_nc, \
    get_array_becsum_d, get_array_ebecsum_d, get_array_dvan_d, \
    get_array_qq_nt_d, get_array_nhtoj_d, get_array_dvan_so_d, get_array_beta, \
    get_array_dbeta]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "uspp".')

for func in _dt_array_initialisers:
    func()
