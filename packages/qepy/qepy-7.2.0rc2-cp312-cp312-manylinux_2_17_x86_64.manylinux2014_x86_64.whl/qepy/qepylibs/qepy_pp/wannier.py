"""
Module wannier


Defined at pw2wannier90.fpp lines 29-96

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nnb():
    """
    Element nnb ftype=integer               pytype=int
    
    
    Defined at pw2wannier90.fpp line 32
    
    """
    return libqepy_pp.f90wrap_wannier__get__nnb()

def set_nnb(nnb):
    libqepy_pp.f90wrap_wannier__set__nnb(nnb)

def get_array_kpb():
    """
    Element kpb ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 33
    
    """
    global kpb
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__kpb(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        kpb = _arrays[array_handle]
    else:
        kpb = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__kpb)
        _arrays[array_handle] = kpb
    return kpb

def set_array_kpb(kpb):
    globals()['kpb'][...] = kpb

def get_array_g_kpb():
    """
    Element g_kpb ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 34
    
    """
    global g_kpb
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__g_kpb(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        g_kpb = _arrays[array_handle]
    else:
        g_kpb = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__g_kpb)
        _arrays[array_handle] = g_kpb
    return g_kpb

def set_array_g_kpb(g_kpb):
    globals()['g_kpb'][...] = g_kpb

def get_array_ig_():
    """
    Element ig_ ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 35
    
    """
    global ig_
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__ig_(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ig_ = _arrays[array_handle]
    else:
        ig_ = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__ig_)
        _arrays[array_handle] = ig_
    return ig_

def set_array_ig_(ig_):
    globals()['ig_'][...] = ig_

def get_array_lw():
    """
    Element lw ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 36
    
    """
    global lw
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__lw(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lw = _arrays[array_handle]
    else:
        lw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__lw)
        _arrays[array_handle] = lw
    return lw

def set_array_lw(lw):
    globals()['lw'][...] = lw

def get_array_mw():
    """
    Element mw ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 36
    
    """
    global mw
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__mw(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mw = _arrays[array_handle]
    else:
        mw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__mw)
        _arrays[array_handle] = mw
    return mw

def set_array_mw(mw):
    globals()['mw'][...] = mw

def get_array_num_sph():
    """
    Element num_sph ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 37
    
    """
    global num_sph
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__num_sph(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        num_sph = _arrays[array_handle]
    else:
        num_sph = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__num_sph)
        _arrays[array_handle] = num_sph
    return num_sph

def set_array_num_sph(num_sph):
    globals()['num_sph'][...] = num_sph

def get_array_excluded_band():
    """
    Element excluded_band ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 38
    
    """
    global excluded_band
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__excluded_band(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        excluded_band = _arrays[array_handle]
    else:
        excluded_band = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__excluded_band)
        _arrays[array_handle] = excluded_band
    return excluded_band

def set_array_excluded_band(excluded_band):
    globals()['excluded_band'][...] = excluded_band

def get_iun_nnkp():
    """
    Element iun_nnkp ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_nnkp()

def set_iun_nnkp(iun_nnkp):
    libqepy_pp.f90wrap_wannier__set__iun_nnkp(iun_nnkp)

def get_iun_mmn():
    """
    Element iun_mmn ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_mmn()

def set_iun_mmn(iun_mmn):
    libqepy_pp.f90wrap_wannier__set__iun_mmn(iun_mmn)

def get_iun_amn():
    """
    Element iun_amn ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_amn()

def set_iun_amn(iun_amn):
    libqepy_pp.f90wrap_wannier__set__iun_amn(iun_amn)

def get_iun_band():
    """
    Element iun_band ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_band()

def set_iun_band(iun_band):
    libqepy_pp.f90wrap_wannier__set__iun_band(iun_band)

def get_iun_spn():
    """
    Element iun_spn ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_spn()

def set_iun_spn(iun_spn):
    libqepy_pp.f90wrap_wannier__set__iun_spn(iun_spn)

def get_iun_plot():
    """
    Element iun_plot ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_plot()

def set_iun_plot(iun_plot):
    libqepy_pp.f90wrap_wannier__set__iun_plot(iun_plot)

def get_iun_parity():
    """
    Element iun_parity ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_parity()

def set_iun_parity(iun_parity):
    libqepy_pp.f90wrap_wannier__set__iun_parity(iun_parity)

def get_nnbx():
    """
    Element nnbx ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__nnbx()

def set_nnbx(nnbx):
    libqepy_pp.f90wrap_wannier__set__nnbx(nnbx)

def get_nexband():
    """
    Element nexband ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__nexband()

def set_nexband(nexband):
    libqepy_pp.f90wrap_wannier__set__nexband(nexband)

def get_iun_uhu():
    """
    Element iun_uhu ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_uhu()

def set_iun_uhu(iun_uhu):
    libqepy_pp.f90wrap_wannier__set__iun_uhu(iun_uhu)

def get_iun_uiu():
    """
    Element iun_uiu ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_uiu()

def set_iun_uiu(iun_uiu):
    libqepy_pp.f90wrap_wannier__set__iun_uiu(iun_uiu)

def get_iun_shu():
    """
    Element iun_shu ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_shu()

def set_iun_shu(iun_shu):
    libqepy_pp.f90wrap_wannier__set__iun_shu(iun_shu)

def get_iun_siu():
    """
    Element iun_siu ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 44
    
    """
    return libqepy_pp.f90wrap_wannier__get__iun_siu()

def set_iun_siu(iun_siu):
    libqepy_pp.f90wrap_wannier__set__iun_siu(iun_siu)

def get_n_wannier():
    """
    Element n_wannier ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 45
    
    """
    return libqepy_pp.f90wrap_wannier__get__n_wannier()

def set_n_wannier(n_wannier):
    libqepy_pp.f90wrap_wannier__set__n_wannier(n_wannier)

def get_n_proj():
    """
    Element n_proj ftype=integer   pytype=int
    
    
    Defined at pw2wannier90.fpp line 46
    
    """
    return libqepy_pp.f90wrap_wannier__get__n_proj()

def set_n_proj(n_proj):
    libqepy_pp.f90wrap_wannier__set__n_proj(n_proj)

def get_array_gf():
    """
    Element gf ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 47
    
    """
    global gf
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__gf(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gf = _arrays[array_handle]
    else:
        gf = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__gf)
        _arrays[array_handle] = gf
    return gf

def set_array_gf(gf):
    globals()['gf'][...] = gf

def get_array_gf_spinor():
    """
    Element gf_spinor ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 48
    
    """
    global gf_spinor
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__gf_spinor(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gf_spinor = _arrays[array_handle]
    else:
        gf_spinor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__gf_spinor)
        _arrays[array_handle] = gf_spinor
    return gf_spinor

def set_array_gf_spinor(gf_spinor):
    globals()['gf_spinor'][...] = gf_spinor

def get_array_sgf_spinor():
    """
    Element sgf_spinor ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 49
    
    """
    global sgf_spinor
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__sgf_spinor(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sgf_spinor = _arrays[array_handle]
    else:
        sgf_spinor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__sgf_spinor)
        _arrays[array_handle] = sgf_spinor
    return sgf_spinor

def set_array_sgf_spinor(sgf_spinor):
    globals()['sgf_spinor'][...] = sgf_spinor

def get_ispinw():
    """
    Element ispinw ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 50
    
    """
    return libqepy_pp.f90wrap_wannier__get__ispinw()

def set_ispinw(ispinw):
    libqepy_pp.f90wrap_wannier__set__ispinw(ispinw)

def get_ikstart():
    """
    Element ikstart ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 50
    
    """
    return libqepy_pp.f90wrap_wannier__get__ikstart()

def set_ikstart(ikstart):
    libqepy_pp.f90wrap_wannier__set__ikstart(ikstart)

def get_ikstop():
    """
    Element ikstop ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 50
    
    """
    return libqepy_pp.f90wrap_wannier__get__ikstop()

def set_ikstop(ikstop):
    libqepy_pp.f90wrap_wannier__set__ikstop(ikstop)

def get_iknum():
    """
    Element iknum ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 50
    
    """
    return libqepy_pp.f90wrap_wannier__get__iknum()

def set_iknum(iknum):
    libqepy_pp.f90wrap_wannier__set__iknum(iknum)

def get_wan_mode():
    """
    Element wan_mode ftype=character(len=15) pytype=str
    
    
    Defined at pw2wannier90.fpp line 51
    
    """
    return libqepy_pp.f90wrap_wannier__get__wan_mode()

def set_wan_mode(wan_mode):
    libqepy_pp.f90wrap_wannier__set__wan_mode(wan_mode)

def get_logwann():
    """
    Element logwann ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__logwann()

def set_logwann(logwann):
    libqepy_pp.f90wrap_wannier__set__logwann(logwann)

def get_wvfn_formatted():
    """
    Element wvfn_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__wvfn_formatted()

def set_wvfn_formatted(wvfn_formatted):
    libqepy_pp.f90wrap_wannier__set__wvfn_formatted(wvfn_formatted)

def get_write_unk():
    """
    Element write_unk ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_unk()

def set_write_unk(write_unk):
    libqepy_pp.f90wrap_wannier__set__write_unk(write_unk)

def get_write_eig():
    """
    Element write_eig ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_eig()

def set_write_eig(write_eig):
    libqepy_pp.f90wrap_wannier__set__write_eig(write_eig)

def get_write_amn():
    """
    Element write_amn ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_amn()

def set_write_amn(write_amn):
    libqepy_pp.f90wrap_wannier__set__write_amn(write_amn)

def get_write_mmn():
    """
    Element write_mmn ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_mmn()

def set_write_mmn(write_mmn):
    libqepy_pp.f90wrap_wannier__set__write_mmn(write_mmn)

def get_reduce_unk():
    """
    Element reduce_unk ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__reduce_unk()

def set_reduce_unk(reduce_unk):
    libqepy_pp.f90wrap_wannier__set__reduce_unk(reduce_unk)

def get_write_spn():
    """
    Element write_spn ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_spn()

def set_write_spn(write_spn):
    libqepy_pp.f90wrap_wannier__set__write_spn(write_spn)

def get_write_unkg():
    """
    Element write_unkg ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_unkg()

def set_write_unkg(write_unkg):
    libqepy_pp.f90wrap_wannier__set__write_unkg(write_unkg)

def get_write_uhu():
    """
    Element write_uhu ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_uhu()

def set_write_uhu(write_uhu):
    libqepy_pp.f90wrap_wannier__set__write_uhu(write_uhu)

def get_write_dmn():
    """
    Element write_dmn ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_dmn()

def set_write_dmn(write_dmn):
    libqepy_pp.f90wrap_wannier__set__write_dmn(write_dmn)

def get_read_sym():
    """
    Element read_sym ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__read_sym()

def set_read_sym(read_sym):
    libqepy_pp.f90wrap_wannier__set__read_sym(read_sym)

def get_write_uiu():
    """
    Element write_uiu ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_uiu()

def set_write_uiu(write_uiu):
    libqepy_pp.f90wrap_wannier__set__write_uiu(write_uiu)

def get_spn_formatted():
    """
    Element spn_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__spn_formatted()

def set_spn_formatted(spn_formatted):
    libqepy_pp.f90wrap_wannier__set__spn_formatted(spn_formatted)

def get_uhu_formatted():
    """
    Element uhu_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__uhu_formatted()

def set_uhu_formatted(uhu_formatted):
    libqepy_pp.f90wrap_wannier__set__uhu_formatted(uhu_formatted)

def get_uiu_formatted():
    """
    Element uiu_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__uiu_formatted()

def set_uiu_formatted(uiu_formatted):
    libqepy_pp.f90wrap_wannier__set__uiu_formatted(uiu_formatted)

def get_write_shu():
    """
    Element write_shu ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_shu()

def set_write_shu(write_shu):
    libqepy_pp.f90wrap_wannier__set__write_shu(write_shu)

def get_write_siu():
    """
    Element write_siu ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__write_siu()

def set_write_siu(write_siu):
    libqepy_pp.f90wrap_wannier__set__write_siu(write_siu)

def get_shu_formatted():
    """
    Element shu_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__shu_formatted()

def set_shu_formatted(shu_formatted):
    libqepy_pp.f90wrap_wannier__set__shu_formatted(shu_formatted)

def get_siu_formatted():
    """
    Element siu_formatted ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__siu_formatted()

def set_siu_formatted(siu_formatted):
    libqepy_pp.f90wrap_wannier__set__siu_formatted(siu_formatted)

def get_scdm_proj():
    """
    Element scdm_proj ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 63
    
    """
    return libqepy_pp.f90wrap_wannier__get__scdm_proj()

def set_scdm_proj(scdm_proj):
    libqepy_pp.f90wrap_wannier__set__scdm_proj(scdm_proj)

def get_scdm_entanglement():
    """
    Element scdm_entanglement ftype=character(len=15) pytype=str
    
    
    Defined at pw2wannier90.fpp line 64
    
    """
    return libqepy_pp.f90wrap_wannier__get__scdm_entanglement()

def set_scdm_entanglement(scdm_entanglement):
    libqepy_pp.f90wrap_wannier__set__scdm_entanglement(scdm_entanglement)

def get_scdm_mu():
    """
    Element scdm_mu ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 65
    
    """
    return libqepy_pp.f90wrap_wannier__get__scdm_mu()

def set_scdm_mu(scdm_mu):
    libqepy_pp.f90wrap_wannier__set__scdm_mu(scdm_mu)

def get_scdm_sigma():
    """
    Element scdm_sigma ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 65
    
    """
    return libqepy_pp.f90wrap_wannier__get__scdm_sigma()

def set_scdm_sigma(scdm_sigma):
    libqepy_pp.f90wrap_wannier__set__scdm_sigma(scdm_sigma)

def get_regular_mesh():
    """
    Element regular_mesh ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 68
    
    """
    return libqepy_pp.f90wrap_wannier__get__regular_mesh()

def set_regular_mesh(regular_mesh):
    libqepy_pp.f90wrap_wannier__set__regular_mesh(regular_mesh)

def get_array_center_w():
    """
    Element center_w ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 70
    
    """
    global center_w
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__center_w(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        center_w = _arrays[array_handle]
    else:
        center_w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__center_w)
        _arrays[array_handle] = center_w
    return center_w

def set_array_center_w(center_w):
    globals()['center_w'][...] = center_w

def get_array_spin_eig():
    """
    Element spin_eig ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 71
    
    """
    global spin_eig
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__spin_eig(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        spin_eig = _arrays[array_handle]
    else:
        spin_eig = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__spin_eig)
        _arrays[array_handle] = spin_eig
    return spin_eig

def set_array_spin_eig(spin_eig):
    globals()['spin_eig'][...] = spin_eig

def get_array_spin_qaxis():
    """
    Element spin_qaxis ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 72
    
    """
    global spin_qaxis
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__spin_qaxis(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        spin_qaxis = _arrays[array_handle]
    else:
        spin_qaxis = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__spin_qaxis)
        _arrays[array_handle] = spin_qaxis
    return spin_qaxis

def set_array_spin_qaxis(spin_qaxis):
    globals()['spin_qaxis'][...] = spin_qaxis

def get_array_l_w():
    """
    Element l_w ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 73
    
    """
    global l_w
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__l_w(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        l_w = _arrays[array_handle]
    else:
        l_w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__l_w)
        _arrays[array_handle] = l_w
    return l_w

def set_array_l_w(l_w):
    globals()['l_w'][...] = l_w

def get_array_mr_w():
    """
    Element mr_w ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 73
    
    """
    global mr_w
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__mr_w(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mr_w = _arrays[array_handle]
    else:
        mr_w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__mr_w)
        _arrays[array_handle] = mr_w
    return mr_w

def set_array_mr_w(mr_w):
    globals()['mr_w'][...] = mr_w

def get_array_r_w():
    """
    Element r_w ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 74
    
    """
    global r_w
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__r_w(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        r_w = _arrays[array_handle]
    else:
        r_w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__r_w)
        _arrays[array_handle] = r_w
    return r_w

def set_array_r_w(r_w):
    globals()['r_w'][...] = r_w

def get_array_xaxis():
    """
    Element xaxis ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 75
    
    """
    global xaxis
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__xaxis(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        xaxis = _arrays[array_handle]
    else:
        xaxis = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__xaxis)
        _arrays[array_handle] = xaxis
    return xaxis

def set_array_xaxis(xaxis):
    globals()['xaxis'][...] = xaxis

def get_array_zaxis():
    """
    Element zaxis ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 75
    
    """
    global zaxis
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__zaxis(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        zaxis = _arrays[array_handle]
    else:
        zaxis = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__zaxis)
        _arrays[array_handle] = zaxis
    return zaxis

def set_array_zaxis(zaxis):
    globals()['zaxis'][...] = zaxis

def get_array_alpha_w():
    """
    Element alpha_w ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 76
    
    """
    global alpha_w
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__alpha_w(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        alpha_w = _arrays[array_handle]
    else:
        alpha_w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__alpha_w)
        _arrays[array_handle] = alpha_w
    return alpha_w

def set_array_alpha_w(alpha_w):
    globals()['alpha_w'][...] = alpha_w

def get_array_csph():
    """
    Element csph ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 78
    
    """
    global csph
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__csph(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        csph = _arrays[array_handle]
    else:
        csph = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__csph)
        _arrays[array_handle] = csph
    return csph

def set_array_csph(csph):
    globals()['csph'][...] = csph

def get_seedname():
    """
    Element seedname ftype=character(len=256) pytype=str
    
    
    Defined at pw2wannier90.fpp line 79
    
    """
    return libqepy_pp.f90wrap_wannier__get__seedname()

def set_seedname(seedname):
    libqepy_pp.f90wrap_wannier__set__seedname(seedname)

def get_array_mp_grid():
    """
    Element mp_grid ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 81
    
    """
    global mp_grid
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__mp_grid(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mp_grid = _arrays[array_handle]
    else:
        mp_grid = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__mp_grid)
        _arrays[array_handle] = mp_grid
    return mp_grid

def set_array_mp_grid(mp_grid):
    globals()['mp_grid'][...] = mp_grid

def get_array_rlatt():
    """
    Element rlatt ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 82
    
    """
    global rlatt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__rlatt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rlatt = _arrays[array_handle]
    else:
        rlatt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__rlatt)
        _arrays[array_handle] = rlatt
    return rlatt

def set_array_rlatt(rlatt):
    globals()['rlatt'][...] = rlatt

def get_array_glatt():
    """
    Element glatt ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 82
    
    """
    global glatt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__glatt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        glatt = _arrays[array_handle]
    else:
        glatt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__glatt)
        _arrays[array_handle] = glatt
    return glatt

def set_array_glatt(glatt):
    globals()['glatt'][...] = glatt

def get_array_kpt_latt():
    """
    Element kpt_latt ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 83
    
    """
    global kpt_latt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__kpt_latt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        kpt_latt = _arrays[array_handle]
    else:
        kpt_latt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__kpt_latt)
        _arrays[array_handle] = kpt_latt
    return kpt_latt

def set_array_kpt_latt(kpt_latt):
    globals()['kpt_latt'][...] = kpt_latt

def get_array_atcart():
    """
    Element atcart ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 84
    
    """
    global atcart
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__atcart(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        atcart = _arrays[array_handle]
    else:
        atcart = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__atcart)
        _arrays[array_handle] = atcart
    return atcart

def set_array_atcart(atcart):
    globals()['atcart'][...] = atcart

def get_num_bands():
    """
    Element num_bands ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 85
    
    """
    return libqepy_pp.f90wrap_wannier__get__num_bands()

def set_num_bands(num_bands):
    libqepy_pp.f90wrap_wannier__set__num_bands(num_bands)

def get_array_atsym():
    """
    Element atsym ftype=character(len=3) pytype=str
    
    
    Defined at pw2wannier90.fpp line 86
    
    """
    global atsym
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__atsym(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        atsym = _arrays[array_handle]
    else:
        atsym = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__atsym)
        _arrays[array_handle] = atsym
    return atsym

def set_array_atsym(atsym):
    globals()['atsym'][...] = atsym

def get_num_nnmax():
    """
    Element num_nnmax ftype=integer                pytype=int
    
    
    Defined at pw2wannier90.fpp line 87
    
    """
    return libqepy_pp.f90wrap_wannier__get__num_nnmax()

def set_num_nnmax(num_nnmax):
    libqepy_pp.f90wrap_wannier__set__num_nnmax(num_nnmax)

def get_array_m_mat():
    """
    Element m_mat ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 88
    
    """
    global m_mat
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__m_mat(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m_mat = _arrays[array_handle]
    else:
        m_mat = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__m_mat)
        _arrays[array_handle] = m_mat
    return m_mat

def set_array_m_mat(m_mat):
    globals()['m_mat'][...] = m_mat

def get_array_a_mat():
    """
    Element a_mat ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 88
    
    """
    global a_mat
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__a_mat(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        a_mat = _arrays[array_handle]
    else:
        a_mat = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__a_mat)
        _arrays[array_handle] = a_mat
    return a_mat

def set_array_a_mat(a_mat):
    globals()['a_mat'][...] = a_mat

def get_array_u_mat():
    """
    Element u_mat ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 89
    
    """
    global u_mat
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__u_mat(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        u_mat = _arrays[array_handle]
    else:
        u_mat = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__u_mat)
        _arrays[array_handle] = u_mat
    return u_mat

def set_array_u_mat(u_mat):
    globals()['u_mat'][...] = u_mat

def get_array_u_mat_opt():
    """
    Element u_mat_opt ftype=complex(dp) pytype=complex
    
    
    Defined at pw2wannier90.fpp line 89
    
    """
    global u_mat_opt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__u_mat_opt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        u_mat_opt = _arrays[array_handle]
    else:
        u_mat_opt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__u_mat_opt)
        _arrays[array_handle] = u_mat_opt
    return u_mat_opt

def set_array_u_mat_opt(u_mat_opt):
    globals()['u_mat_opt'][...] = u_mat_opt

def get_array_lwindow():
    """
    Element lwindow ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 90
    
    """
    global lwindow
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__lwindow(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lwindow = _arrays[array_handle]
    else:
        lwindow = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__lwindow)
        _arrays[array_handle] = lwindow
    return lwindow

def set_array_lwindow(lwindow):
    globals()['lwindow'][...] = lwindow

def get_array_wann_centers():
    """
    Element wann_centers ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 91
    
    """
    global wann_centers
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__wann_centers(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wann_centers = _arrays[array_handle]
    else:
        wann_centers = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__wann_centers)
        _arrays[array_handle] = wann_centers
    return wann_centers

def set_array_wann_centers(wann_centers):
    globals()['wann_centers'][...] = wann_centers

def get_array_wann_spreads():
    """
    Element wann_spreads ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 91
    
    """
    global wann_spreads
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__wann_spreads(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wann_spreads = _arrays[array_handle]
    else:
        wann_spreads = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__wann_spreads)
        _arrays[array_handle] = wann_spreads
    return wann_spreads

def set_array_wann_spreads(wann_spreads):
    globals()['wann_spreads'][...] = wann_spreads

def get_array_spreads():
    """
    Element spreads ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 92
    
    """
    global spreads
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__spreads(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        spreads = _arrays[array_handle]
    else:
        spreads = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__spreads)
        _arrays[array_handle] = spreads
    return spreads

def set_array_spreads(spreads):
    globals()['spreads'][...] = spreads

def get_array_eigval():
    """
    Element eigval ftype=real(dp) pytype=float
    
    
    Defined at pw2wannier90.fpp line 93
    
    """
    global eigval
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__eigval(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigval = _arrays[array_handle]
    else:
        eigval = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__eigval)
        _arrays[array_handle] = eigval
    return eigval

def set_array_eigval(eigval):
    globals()['eigval'][...] = eigval

def get_old_spinor_proj():
    """
    Element old_spinor_proj ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 94
    
    """
    return libqepy_pp.f90wrap_wannier__get__old_spinor_proj()

def set_old_spinor_proj(old_spinor_proj):
    libqepy_pp.f90wrap_wannier__set__old_spinor_proj(old_spinor_proj)

def get_array_rir():
    """
    Element rir ftype=integer pytype=int
    
    
    Defined at pw2wannier90.fpp line 95
    
    """
    global rir
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__rir(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rir = _arrays[array_handle]
    else:
        rir = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__rir)
        _arrays[array_handle] = rir
    return rir

def set_array_rir(rir):
    globals()['rir'][...] = rir

def get_array_zerophase():
    """
    Element zerophase ftype=logical pytype=bool
    
    
    Defined at pw2wannier90.fpp line 96
    
    """
    global zerophase
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_wannier__array__zerophase(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        zerophase = _arrays[array_handle]
    else:
        zerophase = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_wannier__array__zerophase)
        _arrays[array_handle] = zerophase
    return zerophase

def set_array_zerophase(zerophase):
    globals()['zerophase'][...] = zerophase


_array_initialisers = [get_array_kpb, get_array_g_kpb, get_array_ig_, \
    get_array_lw, get_array_mw, get_array_num_sph, get_array_excluded_band, \
    get_array_gf, get_array_gf_spinor, get_array_sgf_spinor, get_array_center_w, \
    get_array_spin_eig, get_array_spin_qaxis, get_array_l_w, get_array_mr_w, \
    get_array_r_w, get_array_xaxis, get_array_zaxis, get_array_alpha_w, \
    get_array_csph, get_array_mp_grid, get_array_rlatt, get_array_glatt, \
    get_array_kpt_latt, get_array_atcart, get_array_atsym, get_array_m_mat, \
    get_array_a_mat, get_array_u_mat, get_array_u_mat_opt, get_array_lwindow, \
    get_array_wann_centers, get_array_wann_spreads, get_array_spreads, \
    get_array_eigval, get_array_rir, get_array_zerophase]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "wannier".')

for func in _dt_array_initialisers:
    func()
