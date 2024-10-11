"""
Module tddft_cgsolver_module


Defined at tddft_cgsolver.fpp lines 17-29

"""
from __future__ import print_function, absolute_import, division
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_flag():
    """
    Element flag ftype=integer      pytype=int
    
    
    Defined at tddft_cgsolver.fpp line 25
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__flag()

def set_flag(flag):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__flag(flag)

def get_tolb():
    """
    Element tolb ftype=real(dp) pytype=float
    
    
    Defined at tddft_cgsolver.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__tolb()

def set_tolb(tolb):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__tolb(tolb)

def get_normr():
    """
    Element normr ftype=real(dp) pytype=float
    
    
    Defined at tddft_cgsolver.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__normr()

def set_normr(normr):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__normr(normr)

def get_relres():
    """
    Element relres ftype=real(dp) pytype=float
    
    
    Defined at tddft_cgsolver.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__relres()

def set_relres(relres):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__relres(relres)

def get_n2b():
    """
    Element n2b ftype=real(dp) pytype=float
    
    
    Defined at tddft_cgsolver.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__n2b()

def set_n2b(n2b):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__n2b(n2b)

def get_normrmin():
    """
    Element normrmin ftype=real(dp) pytype=float
    
    
    Defined at tddft_cgsolver.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__normrmin()

def set_normrmin(normrmin):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__normrmin(normrmin)

def get_rho():
    """
    Element rho ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__rho()

def set_rho(rho):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__rho(rho)

def get_rho1():
    """
    Element rho1 ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__rho1()

def set_rho1(rho1):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__rho1(rho1)

def get_alpha():
    """
    Element alpha ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__alpha()

def set_alpha(alpha):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__alpha(alpha)

def get_beta():
    """
    Element beta ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__beta()

def set_beta(beta):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__beta(beta)

def get_rtvh():
    """
    Element rtvh ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_cgsolver_module__get__rtvh()

def set_rtvh(rtvh):
    libqepy_cetddft.f90wrap_tddft_cgsolver_module__set__rtvh(rtvh)

def get_array_r():
    """
    Element r ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global r
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__r(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        r = _arrays[array_handle]
    else:
        r = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__r)
        _arrays[array_handle] = r
    return r

def set_array_r(r):
    globals()['r'][...] = r

def get_array_ax():
    """
    Element ax ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global ax
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__ax(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ax = _arrays[array_handle]
    else:
        ax = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__ax)
        _arrays[array_handle] = ax
    return ax

def set_array_ax(ax):
    globals()['ax'][...] = ax

def get_array_rt():
    """
    Element rt ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global rt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__rt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rt = _arrays[array_handle]
    else:
        rt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__rt)
        _arrays[array_handle] = rt
    return rt

def set_array_rt(rt):
    globals()['rt'][...] = rt

def get_array_vh():
    """
    Element vh ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global vh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__vh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vh = _arrays[array_handle]
    else:
        vh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__vh)
        _arrays[array_handle] = vh
    return vh

def set_array_vh(vh):
    globals()['vh'][...] = vh

def get_array_u():
    """
    Element u ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global u
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__u(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        u = _arrays[array_handle]
    else:
        u = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__u)
        _arrays[array_handle] = u
    return u

def set_array_u(u):
    globals()['u'][...] = u

def get_array_uh():
    """
    Element uh ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global uh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__uh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        uh = _arrays[array_handle]
    else:
        uh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__uh)
        _arrays[array_handle] = uh
    return uh

def set_array_uh(uh):
    globals()['uh'][...] = uh

def get_array_q():
    """
    Element q ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global q
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__q(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        q = _arrays[array_handle]
    else:
        q = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__q)
        _arrays[array_handle] = q
    return q

def set_array_q(q):
    globals()['q'][...] = q

def get_array_qh():
    """
    Element qh ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global qh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__qh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qh = _arrays[array_handle]
    else:
        qh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__qh)
        _arrays[array_handle] = qh
    return qh

def set_array_qh(qh):
    globals()['qh'][...] = qh

def get_array_p():
    """
    Element p ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_cgsolver.fpp line 29
    
    """
    global p
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__p(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        p = _arrays[array_handle]
    else:
        p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_cgsolver_module__array__p)
        _arrays[array_handle] = p
    return p

def set_array_p(p):
    globals()['p'][...] = p


_array_initialisers = [get_array_r, get_array_ax, get_array_rt, get_array_vh, \
    get_array_u, get_array_uh, get_array_q, get_array_qh, get_array_p]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "tddft_cgsolver_module".')

for func in _dt_array_initialisers:
    func()
