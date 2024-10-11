"""
Module fouriermod


Defined at fouriermod.fpp lines 17-774

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def fourierdiff():
    """
    fourierdiff()
    
    
    Defined at fouriermod.fpp lines 45-156
    
    
    """
    libqepy_pp.f90wrap_fouriermod__fourierdiff()

def fourier():
    """
    fourier()
    
    
    Defined at fouriermod.fpp lines 159-254
    
    
    """
    libqepy_pp.f90wrap_fouriermod__fourier()

def find_stars(nsym, op, at, skip000_=None):
    """
    find_stars(nsym, op, at[, skip000_])
    
    
    Defined at fouriermod.fpp lines 257-389
    
    Parameters
    ----------
    nsym : int
    op : float array
    at : float array
    skip000_ : bool
    
    """
    libqepy_pp.f90wrap_fouriermod__find_stars(nsym=nsym, op=op, at=at, \
        skip000_=skip000_)

def check_stars(np, p, nsym, op, bg):
    """
    check_stars(np, p, nsym, op, bg)
    
    
    Defined at fouriermod.fpp lines 392-454
    
    Parameters
    ----------
    np : int
    p : float array
    nsym : int
    op : float array
    bg : float array
    
    """
    libqepy_pp.f90wrap_fouriermod__check_stars(np=np, p=p, nsym=nsym, op=op, bg=bg)

def compute_stars(a, lda, np, p, nsym, op, ialpha, dodiff_=None, s=None):
    """
    compute_stars(a, lda, np, p, nsym, op, ialpha[, dodiff_, s])
    
    
    Defined at fouriermod.fpp lines 457-533
    
    Parameters
    ----------
    a : complex array
    lda : int
    np : int
    p : float array
    nsym : int
    op : float array
    ialpha : int
    dodiff_ : bool
    s : complex array
    
    """
    libqepy_pp.f90wrap_fouriermod__compute_stars(a=a, lda=lda, np=np, p=p, \
        nsym=nsym, op=op, ialpha=ialpha, dodiff_=dodiff_, s=s)

def star_function(iprint, p, vec, nsym, op):
    """
    star_function = star_function(iprint, p, vec, nsym, op)
    
    
    Defined at fouriermod.fpp lines 536-585
    
    Parameters
    ----------
    iprint : int
    p : float array
    vec : float array
    nsym : int
    op : float array
    
    Returns
    -------
    star_function : complex
    
    """
    star_function = libqepy_pp.f90wrap_fouriermod__star_function(iprint=iprint, p=p, \
        vec=vec, nsym=nsym, op=op)
    return star_function

def sqrt_rho(vec):
    """
    sqrt_rho = sqrt_rho(vec)
    
    
    Defined at fouriermod.fpp lines 588-607
    
    Parameters
    ----------
    vec : float array
    
    Returns
    -------
    sqrt_rho : float
    
    """
    sqrt_rho = libqepy_pp.f90wrap_fouriermod__sqrt_rho(vec=vec)
    return sqrt_rho

def applyop(isym, opmat, vec, vecop):
    """
    applyop(isym, opmat, vec, vecop)
    
    
    Defined at fouriermod.fpp lines 610-633
    
    Parameters
    ----------
    isym : int
    opmat : float array
    vec : float array
    vecop : float array
    
    """
    libqepy_pp.f90wrap_fouriermod__applyop(isym=isym, opmat=opmat, vec=vec, \
        vecop=vecop)

def card_user_stars(input_line):
    """
    card_user_stars(input_line)
    
    
    Defined at fouriermod.fpp lines 636-672
    
    Parameters
    ----------
    input_line : str
    
    """
    libqepy_pp.f90wrap_fouriermod__card_user_stars(input_line=input_line)

def card_roughness(input_line):
    """
    card_roughness(input_line)
    
    
    Defined at fouriermod.fpp lines 675-725
    
    Parameters
    ----------
    input_line : str
    
    """
    libqepy_pp.f90wrap_fouriermod__card_roughness(input_line=input_line)

def print_rough():
    """
    print_rough()
    
    
    Defined at fouriermod.fpp lines 728-772
    
    
    """
    libqepy_pp.f90wrap_fouriermod__print_rough()

def get_eps():
    """
    Element eps ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 22
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__eps()

eps = get_eps()

def get_zero():
    """
    Element zero ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 22
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__zero()

Zero = get_zero()

def get_one():
    """
    Element one ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 22
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__one()

One = get_one()

def get_two():
    """
    Element two ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 22
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__two()

Two = get_two()

def get_four():
    """
    Element four ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 22
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__four()

Four = get_four()

def get_pi():
    """
    Element pi ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 23
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__pi()

Pi = get_pi()

def get_check_periodicity():
    """
    Element check_periodicity ftype=logical pytype=bool
    
    
    Defined at fouriermod.fpp line 26
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__check_periodicity()

def set_check_periodicity(check_periodicity):
    libqepy_pp.f90wrap_fouriermod__set__check_periodicity(check_periodicity)

def get_miller_max():
    """
    Element miller_max ftype=integer  pytype=int
    
    
    Defined at fouriermod.fpp line 29
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__miller_max()

def set_miller_max(miller_max):
    libqepy_pp.f90wrap_fouriermod__set__miller_max(miller_max)

def get_roughn():
    """
    Element roughn ftype=integer  pytype=int
    
    
    Defined at fouriermod.fpp line 32
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__roughn()

def set_roughn(roughn):
    libqepy_pp.f90wrap_fouriermod__set__roughn(roughn)

def get_array_roughc():
    """
    Element roughc ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 33
    
    """
    global roughc
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_fouriermod__array__roughc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        roughc = _arrays[array_handle]
    else:
        roughc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_fouriermod__array__roughc)
        _arrays[array_handle] = roughc
    return roughc

def set_array_roughc(roughc):
    globals()['roughc'][...] = roughc

def get_nstars():
    """
    Element nstars ftype=integer  pytype=int
    
    
    Defined at fouriermod.fpp line 35
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__nstars()

def set_nstars(nstars):
    libqepy_pp.f90wrap_fouriermod__set__nstars(nstars)

def get_array_vecstars():
    """
    Element vecstars ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 36
    
    """
    global vecstars
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_fouriermod__array__vecstars(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vecstars = _arrays[array_handle]
    else:
        vecstars = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_fouriermod__array__vecstars)
        _arrays[array_handle] = vecstars
    return vecstars

def set_array_vecstars(vecstars):
    globals()['vecstars'][...] = vecstars

def get_nuser():
    """
    Element nuser ftype=integer  pytype=int
    
    
    Defined at fouriermod.fpp line 37
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__nuser()

def set_nuser(nuser):
    libqepy_pp.f90wrap_fouriermod__set__nuser(nuser)

def get_array_vecuser():
    """
    Element vecuser ftype=real(dp) pytype=float
    
    
    Defined at fouriermod.fpp line 38
    
    """
    global vecuser
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_fouriermod__array__vecuser(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vecuser = _arrays[array_handle]
    else:
        vecuser = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_fouriermod__array__vecuser)
        _arrays[array_handle] = vecuser
    return vecuser

def set_array_vecuser(vecuser):
    globals()['vecuser'][...] = vecuser

def get_trough():
    """
    Element trough ftype=logical pytype=bool
    
    
    Defined at fouriermod.fpp line 40
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__trough()

def set_trough(trough):
    libqepy_pp.f90wrap_fouriermod__set__trough(trough)

def get_tuser():
    """
    Element tuser ftype=logical pytype=bool
    
    
    Defined at fouriermod.fpp line 41
    
    """
    return libqepy_pp.f90wrap_fouriermod__get__tuser()

def set_tuser(tuser):
    libqepy_pp.f90wrap_fouriermod__set__tuser(tuser)


_array_initialisers = [get_array_roughc, get_array_vecstars, get_array_vecuser]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "fouriermod".')

for func in _dt_array_initialisers:
    func()
