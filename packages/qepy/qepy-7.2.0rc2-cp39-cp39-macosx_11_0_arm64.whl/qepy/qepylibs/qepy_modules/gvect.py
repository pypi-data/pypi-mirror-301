"""
Module gvect


Defined at recvec.fpp lines 13-241

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def gvect_init(ngm_, comm):
    """
    gvect_init(ngm_, comm)
    
    
    Defined at recvec.fpp lines 78-117
    
    Parameters
    ----------
    ngm_ : int
    comm : int
    
    """
    libqepy_modules.f90wrap_gvect__gvect_init(ngm_=ngm_, comm=comm)

def deallocate_gvect(vc=None):
    """
    deallocate_gvect([vc])
    
    
    Defined at recvec.fpp lines 119-174
    
    Parameters
    ----------
    vc : bool
    
    """
    libqepy_modules.f90wrap_gvect__deallocate_gvect(vc=vc)

def deallocate_gvect_exx():
    """
    deallocate_gvect_exx()
    
    
    Defined at recvec.fpp lines 176-187
    
    
    """
    libqepy_modules.f90wrap_gvect__deallocate_gvect_exx()

def gshells(vc):
    """
    gshells(vc)
    
    
    Defined at recvec.fpp lines 191-239
    
    Parameters
    ----------
    vc : bool
    
    ----------------------------------------------------------------------
     Calculate number of G shells: ngl, and the index ng = igtongl(ig)
     that gives the shell index ng for(local) G-vector of index ig.
    """
    libqepy_modules.f90wrap_gvect__gshells(vc=vc)

def get_ngm():
    """
    Element ngm ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 23
    
    """
    return libqepy_modules.f90wrap_gvect__get__ngm()

def set_ngm(ngm):
    libqepy_modules.f90wrap_gvect__set__ngm(ngm)

def get_ngm_g():
    """
    Element ngm_g ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 26
    
    """
    return libqepy_modules.f90wrap_gvect__get__ngm_g()

def set_ngm_g(ngm_g):
    libqepy_modules.f90wrap_gvect__set__ngm_g(ngm_g)

def get_ngl():
    """
    Element ngl ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 29
    
    """
    return libqepy_modules.f90wrap_gvect__get__ngl()

def set_ngl(ngl):
    libqepy_modules.f90wrap_gvect__set__ngl(ngl)

def get_ngmx():
    """
    Element ngmx ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 31
    
    """
    return libqepy_modules.f90wrap_gvect__get__ngmx()

def set_ngmx(ngmx):
    libqepy_modules.f90wrap_gvect__set__ngmx(ngmx)

def get_ecutrho():
    """
    Element ecutrho ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 33
    
    """
    return libqepy_modules.f90wrap_gvect__get__ecutrho()

def set_ecutrho(ecutrho):
    libqepy_modules.f90wrap_gvect__set__ecutrho(ecutrho)

def get_gcutm():
    """
    Element gcutm ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 35
    
    """
    return libqepy_modules.f90wrap_gvect__get__gcutm()

def set_gcutm(gcutm):
    libqepy_modules.f90wrap_gvect__set__gcutm(gcutm)

def get_gstart():
    """
    Element gstart ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 37
    
    """
    return libqepy_modules.f90wrap_gvect__get__gstart()

def set_gstart(gstart):
    libqepy_modules.f90wrap_gvect__set__gstart(gstart)

def get_array_gg():
    """
    Element gg ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 40
    
    """
    global gg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__gg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gg = _arrays[array_handle]
    else:
        gg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__gg)
        _arrays[array_handle] = gg
    return gg

def set_array_gg(gg):
    globals()['gg'][...] = gg

def get_array_gg_d():
    """
    Element gg_d ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 42
    
    """
    global gg_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__gg_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gg_d = _arrays[array_handle]
    else:
        gg_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__gg_d)
        _arrays[array_handle] = gg_d
    return gg_d

def set_array_gg_d(gg_d):
    globals()['gg_d'][...] = gg_d

def get_array_gl_d():
    """
    Element gl_d ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 49
    
    """
    global gl_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__gl_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gl_d = _arrays[array_handle]
    else:
        gl_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__gl_d)
        _arrays[array_handle] = gl_d
    return gl_d

def set_array_gl_d(gl_d):
    globals()['gl_d'][...] = gl_d

def get_array_igtongl_d():
    """
    Element igtongl_d ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 50
    
    """
    global igtongl_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__igtongl_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        igtongl_d = _arrays[array_handle]
    else:
        igtongl_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__igtongl_d)
        _arrays[array_handle] = igtongl_d
    return igtongl_d

def set_array_igtongl_d(igtongl_d):
    globals()['igtongl_d'][...] = igtongl_d

def get_array_g():
    """
    Element g ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 52
    
    """
    global g
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        g = _arrays[array_handle]
    else:
        g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__g)
        _arrays[array_handle] = g
    return g

def set_array_g(g):
    globals()['g'][...] = g

def get_array_g_d():
    """
    Element g_d ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 54
    
    """
    global g_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__g_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        g_d = _arrays[array_handle]
    else:
        g_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__g_d)
        _arrays[array_handle] = g_d
    return g_d

def set_array_g_d(g_d):
    globals()['g_d'][...] = g_d

def get_array_mill():
    """
    Element mill ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 56
    
    """
    global mill
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__mill(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mill = _arrays[array_handle]
    else:
        mill = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__mill)
        _arrays[array_handle] = mill
    return mill

def set_array_mill(mill):
    globals()['mill'][...] = mill

def get_array_mill_d():
    """
    Element mill_d ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 60
    
    """
    global mill_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__mill_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mill_d = _arrays[array_handle]
    else:
        mill_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__mill_d)
        _arrays[array_handle] = mill_d
    return mill_d

def set_array_mill_d(mill_d):
    globals()['mill_d'][...] = mill_d

def get_array_ig_l2g():
    """
    Element ig_l2g ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 62
    
    """
    global ig_l2g
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__ig_l2g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ig_l2g = _arrays[array_handle]
    else:
        ig_l2g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__ig_l2g)
        _arrays[array_handle] = ig_l2g
    return ig_l2g

def set_array_ig_l2g(ig_l2g):
    globals()['ig_l2g'][...] = ig_l2g

def get_array_mill_g():
    """
    Element mill_g ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 67
    
    """
    global mill_g
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__mill_g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mill_g = _arrays[array_handle]
    else:
        mill_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__mill_g)
        _arrays[array_handle] = mill_g
    return mill_g

def set_array_mill_g(mill_g):
    globals()['mill_g'][...] = mill_g

def get_array_eigts1():
    """
    Element eigts1 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 70
    
    """
    global eigts1
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts1 = _arrays[array_handle]
    else:
        eigts1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts1)
        _arrays[array_handle] = eigts1
    return eigts1

def set_array_eigts1(eigts1):
    globals()['eigts1'][...] = eigts1

def get_array_eigts2():
    """
    Element eigts2 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 72
    
    """
    global eigts2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts2 = _arrays[array_handle]
    else:
        eigts2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts2)
        _arrays[array_handle] = eigts2
    return eigts2

def set_array_eigts2(eigts2):
    globals()['eigts2'][...] = eigts2

def get_array_eigts3():
    """
    Element eigts3 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 72
    
    """
    global eigts3
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts3(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts3 = _arrays[array_handle]
    else:
        eigts3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts3)
        _arrays[array_handle] = eigts3
    return eigts3

def set_array_eigts3(eigts3):
    globals()['eigts3'][...] = eigts3

def get_array_eigts1_d():
    """
    Element eigts1_d ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 73
    
    """
    global eigts1_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts1_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts1_d = _arrays[array_handle]
    else:
        eigts1_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts1_d)
        _arrays[array_handle] = eigts1_d
    return eigts1_d

def set_array_eigts1_d(eigts1_d):
    globals()['eigts1_d'][...] = eigts1_d

def get_array_eigts2_d():
    """
    Element eigts2_d ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 74
    
    """
    global eigts2_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts2_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts2_d = _arrays[array_handle]
    else:
        eigts2_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts2_d)
        _arrays[array_handle] = eigts2_d
    return eigts2_d

def set_array_eigts2_d(eigts2_d):
    globals()['eigts2_d'][...] = eigts2_d

def get_array_eigts3_d():
    """
    Element eigts3_d ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 75
    
    """
    global eigts3_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_gvect__array__eigts3_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts3_d = _arrays[array_handle]
    else:
        eigts3_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_gvect__array__eigts3_d)
        _arrays[array_handle] = eigts3_d
    return eigts3_d

def set_array_eigts3_d(eigts3_d):
    globals()['eigts3_d'][...] = eigts3_d


_array_initialisers = [get_array_gg, get_array_gg_d, get_array_gl_d, \
    get_array_igtongl_d, get_array_g, get_array_g_d, get_array_mill, \
    get_array_mill_d, get_array_ig_l2g, get_array_mill_g, get_array_eigts1, \
    get_array_eigts2, get_array_eigts3, get_array_eigts1_d, get_array_eigts2_d, \
    get_array_eigts3_d]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "gvect".')

for func in _dt_array_initialisers:
    func()
