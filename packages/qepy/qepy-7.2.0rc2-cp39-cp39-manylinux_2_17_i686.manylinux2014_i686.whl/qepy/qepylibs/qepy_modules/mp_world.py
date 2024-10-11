"""
Module mp_world


Defined at mp_world.fpp lines 13-86

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_world_start(my_world_comm):
    """
    mp_world_start(my_world_comm)
    
    
    Defined at mp_world.fpp lines 48-76
    
    Parameters
    ----------
    my_world_comm : int
    
    -----------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_mp_world__mp_world_start(my_world_comm=my_world_comm)

def mp_world_end():
    """
    mp_world_end()
    
    
    Defined at mp_world.fpp lines 80-85
    
    
    -----------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_mp_world__mp_world_end()

def get_nnode():
    """
    Element nnode ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 30
    
    """
    return libqepy_modules.f90wrap_mp_world__get__nnode()

def set_nnode(nnode):
    libqepy_modules.f90wrap_mp_world__set__nnode(nnode)

def get_nproc():
    """
    Element nproc ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 32
    
    """
    return libqepy_modules.f90wrap_mp_world__get__nproc()

def set_nproc(nproc):
    libqepy_modules.f90wrap_mp_world__set__nproc(nproc)

def get_mpime():
    """
    Element mpime ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 34
    
    """
    return libqepy_modules.f90wrap_mp_world__get__mpime()

def set_mpime(mpime):
    libqepy_modules.f90wrap_mp_world__set__mpime(mpime)

def get_root():
    """
    Element root ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 36
    
    """
    return libqepy_modules.f90wrap_mp_world__get__root()

def set_root(root):
    libqepy_modules.f90wrap_mp_world__set__root(root)

def get_world_comm():
    """
    Element world_comm ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 38
    
    """
    return libqepy_modules.f90wrap_mp_world__get__world_comm()

def set_world_comm(world_comm):
    libqepy_modules.f90wrap_mp_world__set__world_comm(world_comm)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_world".')

for func in _dt_array_initialisers:
    func()
