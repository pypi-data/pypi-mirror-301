"""
Module laxlib_processors_grid


Defined at mp_diag.fpp lines 13-116

"""
from __future__ import print_function, absolute_import, division
import libqepy_laxlib
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def laxlib_end_drv():
    """
    laxlib_end_drv()
    
    
    Defined at mp_diag.fpp lines 44-74
    
    
    """
    libqepy_laxlib.f90wrap_laxlib_processors_grid__laxlib_end_drv()

def laxlib_rank(comm):
    """
    laxlib_rank = laxlib_rank(comm)
    
    
    Defined at mp_diag.fpp lines 78-86
    
    Parameters
    ----------
    comm : int
    
    Returns
    -------
    laxlib_rank : int
    
    """
    laxlib_rank = \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__laxlib_rank(comm=comm)
    return laxlib_rank

def laxlib_size(comm):
    """
    laxlib_size = laxlib_size(comm)
    
    
    Defined at mp_diag.fpp lines 89-97
    
    Parameters
    ----------
    comm : int
    
    Returns
    -------
    laxlib_size : int
    
    """
    laxlib_size = \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__laxlib_size(comm=comm)
    return laxlib_size

def laxlib_comm_split(old_comm, color, key):
    """
    new_comm = laxlib_comm_split(old_comm, color, key)
    
    
    Defined at mp_diag.fpp lines 99-107
    
    Parameters
    ----------
    old_comm : int
    color : int
    key : int
    
    Returns
    -------
    new_comm : int
    
    """
    new_comm = \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__laxlib_comm_split(old_comm=old_comm, \
        color=color, key=key)
    return new_comm

def laxlib_comm_free(comm):
    """
    laxlib_comm_free(comm)
    
    
    Defined at mp_diag.fpp lines 109-115
    
    Parameters
    ----------
    comm : int
    
    """
    libqepy_laxlib.f90wrap_laxlib_processors_grid__laxlib_comm_free(comm=comm)

def get_array_np_ortho():
    """
    Element np_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 23
    
    """
    global np_ortho
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__array__np_ortho(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        np_ortho = _arrays[array_handle]
    else:
        np_ortho = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_laxlib.f90wrap_laxlib_processors_grid__array__np_ortho)
        _arrays[array_handle] = np_ortho
    return np_ortho

def set_array_np_ortho(np_ortho):
    globals()['np_ortho'][...] = np_ortho

def get_array_me_ortho():
    """
    Element me_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 24
    
    """
    global me_ortho
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__array__me_ortho(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        me_ortho = _arrays[array_handle]
    else:
        me_ortho = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_laxlib.f90wrap_laxlib_processors_grid__array__me_ortho)
        _arrays[array_handle] = me_ortho
    return me_ortho

def set_array_me_ortho(me_ortho):
    globals()['me_ortho'][...] = me_ortho

def get_me_ortho1():
    """
    Element me_ortho1 ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 25
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__me_ortho1()

def set_me_ortho1(me_ortho1):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__me_ortho1(me_ortho1)

def get_nproc_ortho():
    """
    Element nproc_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 26
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__nproc_ortho()

def set_nproc_ortho(nproc_ortho):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__nproc_ortho(nproc_ortho)

def get_leg_ortho():
    """
    Element leg_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 27
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__leg_ortho()

def set_leg_ortho(leg_ortho):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__leg_ortho(leg_ortho)

def get_ortho_comm():
    """
    Element ortho_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 29
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_comm()

def set_ortho_comm(ortho_comm):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_comm(ortho_comm)

def get_ortho_row_comm():
    """
    Element ortho_row_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 30
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_row_comm()

def set_ortho_row_comm(ortho_row_comm):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_row_comm(ortho_row_comm)

def get_ortho_col_comm():
    """
    Element ortho_col_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 31
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_col_comm()

def set_ortho_col_comm(ortho_col_comm):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_col_comm(ortho_col_comm)

def get_ortho_comm_id():
    """
    Element ortho_comm_id ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 32
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_comm_id()

def set_ortho_comm_id(ortho_comm_id):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_comm_id(ortho_comm_id)

def get_ortho_parent_comm():
    """
    Element ortho_parent_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 33
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_parent_comm()

def set_ortho_parent_comm(ortho_parent_comm):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_parent_comm(ortho_parent_comm)

def get_ortho_cntx():
    """
    Element ortho_cntx ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 35
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__ortho_cntx()

def set_ortho_cntx(ortho_cntx):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__ortho_cntx(ortho_cntx)

def get_do_distr_diag_inside_bgrp():
    """
    Element do_distr_diag_inside_bgrp ftype=logical pytype=bool
    
    
    Defined at mp_diag.fpp line 37
    
    """
    return \
        libqepy_laxlib.f90wrap_laxlib_processors_grid__get__do_distr_diag_inside_bgrp()

def set_do_distr_diag_inside_bgrp(do_distr_diag_inside_bgrp):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__do_distr_diag_inside_bgrp(do_distr_diag_inside_bgrp)

def get_lax_is_initialized():
    """
    Element lax_is_initialized ftype=logical pytype=bool
    
    
    Defined at mp_diag.fpp line 40
    
    """
    return libqepy_laxlib.f90wrap_laxlib_processors_grid__get__lax_is_initialized()

def set_lax_is_initialized(lax_is_initialized):
    libqepy_laxlib.f90wrap_laxlib_processors_grid__set__lax_is_initialized(lax_is_initialized)


_array_initialisers = [get_array_np_ortho, get_array_me_ortho]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "laxlib_processors_grid".')

for func in _dt_array_initialisers:
    func()
