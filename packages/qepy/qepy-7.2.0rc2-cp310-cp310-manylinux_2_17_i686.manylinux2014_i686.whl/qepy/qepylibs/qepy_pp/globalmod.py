"""
Module globalmod


Defined at globalmod.fpp lines 17-191

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def read_xml_input():
    """
    read_xml_input()
    
    
    Defined at globalmod.fpp lines 45-126
    
    
    """
    libqepy_pp.f90wrap_globalmod__read_xml_input()

def deallocate_global():
    """
    deallocate_global()
    
    
    Defined at globalmod.fpp lines 129-132
    
    
    """
    libqepy_pp.f90wrap_globalmod__deallocate_global()

def s_axis_to_cart():
    """
    s_axis_to_cart()
    
    
    Defined at globalmod.fpp lines 135-153
    
    
    ----------------------------------------------------------------------
     This routine transforms symmetry matrices expressed in the
     basis of the crystal axis into rotations in cartesian axis.
    civn 2FIX: better remove this one and use PW/src/symm_base.f90 instead
    (change Op_tmp --> sr and   Op --> s)
    """
    libqepy_pp.f90wrap_globalmod__s_axis_to_cart()

def print_bands(label):
    """
    print_bands(label)
    
    
    Defined at globalmod.fpp lines 156-189
    
    Parameters
    ----------
    label : str
    
    """
    libqepy_pp.f90wrap_globalmod__print_bands(label=label)

def get_method():
    """
    Element method ftype=character(len=80) pytype=str
    
    
    Defined at globalmod.fpp line 23
    
    """
    return libqepy_pp.f90wrap_globalmod__get__method()

def set_method(method):
    libqepy_pp.f90wrap_globalmod__set__method(method)

def get_nb():
    """
    Element nb ftype=integer  pytype=int
    
    
    Defined at globalmod.fpp line 26
    
    """
    return libqepy_pp.f90wrap_globalmod__get__nb()

def set_nb(nb):
    libqepy_pp.f90wrap_globalmod__set__nb(nb)

def get_nq():
    """
    Element nq ftype=integer  pytype=int
    
    
    Defined at globalmod.fpp line 29
    
    """
    return libqepy_pp.f90wrap_globalmod__get__nq()

def set_nq(nq):
    libqepy_pp.f90wrap_globalmod__set__nq(nq)

def get_array_q():
    """
    Element q ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 30
    
    """
    global q
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__q(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        q = _arrays[array_handle]
    else:
        q = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__q)
        _arrays[array_handle] = q
    return q

def set_array_q(q):
    globals()['q'][...] = q

def get_array_eq():
    """
    Element eq ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 30
    
    """
    global eq
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__eq(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eq = _arrays[array_handle]
    else:
        eq = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__eq)
        _arrays[array_handle] = eq
    return eq

def set_array_eq(eq):
    globals()['eq'][...] = eq

def get_array_ek():
    """
    Element ek ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 33
    
    """
    global ek
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__ek(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ek = _arrays[array_handle]
    else:
        ek = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__ek)
        _arrays[array_handle] = ek
    return ek

def set_array_ek(ek):
    globals()['ek'][...] = ek

def get_array_at():
    """
    Element at ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 36
    
    """
    global at
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at = _arrays[array_handle]
    else:
        at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__at)
        _arrays[array_handle] = at
    return at

def set_array_at(at):
    globals()['at'][...] = at

def get_array_bg():
    """
    Element bg ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 37
    
    """
    global bg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__bg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        bg = _arrays[array_handle]
    else:
        bg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__bg)
        _arrays[array_handle] = bg
    return bg

def set_array_bg(bg):
    globals()['bg'][...] = bg

def get_nsym():
    """
    Element nsym ftype=integer  pytype=int
    
    
    Defined at globalmod.fpp line 38
    
    """
    return libqepy_pp.f90wrap_globalmod__get__nsym()

def set_nsym(nsym):
    libqepy_pp.f90wrap_globalmod__set__nsym(nsym)

def get_array_op():
    """
    Element op ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 39
    
    """
    global op
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__op(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        op = _arrays[array_handle]
    else:
        op = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__op)
        _arrays[array_handle] = op
    return op

def set_array_op(op):
    globals()['op'][...] = op

def get_array_op_tmp():
    """
    Element op_tmp ftype=real(dp) pytype=float
    
    
    Defined at globalmod.fpp line 40
    
    """
    global op_tmp
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_globalmod__array__op_tmp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        op_tmp = _arrays[array_handle]
    else:
        op_tmp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_globalmod__array__op_tmp)
        _arrays[array_handle] = op_tmp
    return op_tmp

def set_array_op_tmp(op_tmp):
    globals()['op_tmp'][...] = op_tmp


_array_initialisers = [get_array_q, get_array_eq, get_array_ek, get_array_at, \
    get_array_bg, get_array_op, get_array_op_tmp]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "globalmod".')

for func in _dt_array_initialisers:
    func()
