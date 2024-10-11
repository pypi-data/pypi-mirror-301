"""
Module wanpar


Defined at wfdd.fpp lines 12-61

"""
from __future__ import print_function, absolute_import, division
import libqepy_cpv
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nw():
    """
    Element nw ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 14
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__nw()

def set_nw(nw):
    libqepy_cpv.f90wrap_wanpar__set__nw(nw)

def get_nit():
    """
    Element nit ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 16
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__nit()

def set_nit(nit):
    libqepy_cpv.f90wrap_wanpar__set__nit(nit)

def get_nsd():
    """
    Element nsd ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 18
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__nsd()

def set_nsd(nsd):
    libqepy_cpv.f90wrap_wanpar__set__nsd(nsd)

def get_ibrav():
    """
    Element ibrav ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 20
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__ibrav()

def set_ibrav(ibrav):
    libqepy_cpv.f90wrap_wanpar__set__ibrav(ibrav)

def get_adapt():
    """
    Element adapt ftype=logical pytype=bool
    
    
    Defined at wfdd.fpp line 22
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__adapt()

def set_adapt(adapt):
    libqepy_cpv.f90wrap_wanpar__set__adapt(adapt)

def get_restart():
    """
    Element restart ftype=logical pytype=bool
    
    
    Defined at wfdd.fpp line 22
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__restart()

def set_restart(restart):
    libqepy_cpv.f90wrap_wanpar__set__restart(restart)

def get_wfdt():
    """
    Element wfdt ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 24
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__wfdt()

def set_wfdt(wfdt):
    libqepy_cpv.f90wrap_wanpar__set__wfdt(wfdt)

def get_maxwfdt():
    """
    Element maxwfdt ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 26
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__maxwfdt()

def set_maxwfdt(maxwfdt):
    libqepy_cpv.f90wrap_wanpar__set__maxwfdt(maxwfdt)

def get_array_b1():
    """
    Element b1 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 28
    
    """
    global b1
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__b1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        b1 = _arrays[array_handle]
    else:
        b1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__b1)
        _arrays[array_handle] = b1
    return b1

def set_array_b1(b1):
    globals()['b1'][...] = b1

def get_array_b2():
    """
    Element b2 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 30
    
    """
    global b2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__b2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        b2 = _arrays[array_handle]
    else:
        b2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__b2)
        _arrays[array_handle] = b2
    return b2

def set_array_b2(b2):
    globals()['b2'][...] = b2

def get_array_b3():
    """
    Element b3 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 32
    
    """
    global b3
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__b3(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        b3 = _arrays[array_handle]
    else:
        b3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__b3)
        _arrays[array_handle] = b3
    return b3

def set_array_b3(b3):
    globals()['b3'][...] = b3

def get_alat():
    """
    Element alat ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 34
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__alat()

def set_alat(alat):
    libqepy_cpv.f90wrap_wanpar__set__alat(alat)

def get_array_a1():
    """
    Element a1 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 36
    
    """
    global a1
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__a1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        a1 = _arrays[array_handle]
    else:
        a1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__a1)
        _arrays[array_handle] = a1
    return a1

def set_array_a1(a1):
    globals()['a1'][...] = a1

def get_array_a2():
    """
    Element a2 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 38
    
    """
    global a2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__a2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        a2 = _arrays[array_handle]
    else:
        a2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__a2)
        _arrays[array_handle] = a2
    return a2

def set_array_a2(a2):
    globals()['a2'][...] = a2

def get_array_a3():
    """
    Element a3 ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 40
    
    """
    global a3
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__a3(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        a3 = _arrays[array_handle]
    else:
        a3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__a3)
        _arrays[array_handle] = a3
    return a3

def set_array_a3(a3):
    globals()['a3'][...] = a3

def get_tolw():
    """
    Element tolw ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 42
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__tolw()

def set_tolw(tolw):
    libqepy_cpv.f90wrap_wanpar__set__tolw(tolw)

def get_array_wfg():
    """
    Element wfg ftype=integer pytype=int
    
    
    Defined at wfdd.fpp line 43
    
    """
    global wfg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__wfg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wfg = _arrays[array_handle]
    else:
        wfg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__wfg)
        _arrays[array_handle] = wfg
    return wfg

def set_array_wfg(wfg):
    globals()['wfg'][...] = wfg

def get_array_weight():
    """
    Element weight ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 47
    
    """
    global weight
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cpv.f90wrap_wanpar__array__weight(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        weight = _arrays[array_handle]
    else:
        weight = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cpv.f90wrap_wanpar__array__weight)
        _arrays[array_handle] = weight
    return weight

def set_array_weight(weight):
    globals()['weight'][...] = weight

def get_q():
    """
    Element q ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 52
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__q()

def set_q(q):
    libqepy_cpv.f90wrap_wanpar__set__q(q)

def get_dt():
    """
    Element dt ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 54
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__dt()

def set_dt(dt):
    libqepy_cpv.f90wrap_wanpar__set__dt(dt)

def get_fric():
    """
    Element fric ftype=real(kind=8) pytype=float
    
    
    Defined at wfdd.fpp line 56
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__fric()

def set_fric(fric):
    libqepy_cpv.f90wrap_wanpar__set__fric(fric)

def get_cgordd():
    """
    Element cgordd ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 58
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__cgordd()

def set_cgordd(cgordd):
    libqepy_cpv.f90wrap_wanpar__set__cgordd(cgordd)

def get_nsteps():
    """
    Element nsteps ftype=integer  pytype=int
    
    
    Defined at wfdd.fpp line 60
    
    """
    return libqepy_cpv.f90wrap_wanpar__get__nsteps()

def set_nsteps(nsteps):
    libqepy_cpv.f90wrap_wanpar__set__nsteps(nsteps)


_array_initialisers = [get_array_b1, get_array_b2, get_array_b3, get_array_a1, \
    get_array_a2, get_array_a3, get_array_wfg, get_array_weight]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "wanpar".')

for func in _dt_array_initialisers:
    func()
