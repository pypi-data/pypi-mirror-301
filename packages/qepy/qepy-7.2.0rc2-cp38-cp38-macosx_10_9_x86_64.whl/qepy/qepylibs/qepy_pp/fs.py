"""
Module fs


Defined at fermisurface.fpp lines 24-355

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def read_input_fs():
    """
    read_input_fs()
    
    
    Defined at fermisurface.fpp lines 52-98
    
    
    --------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fs__read_input_fs()

def fill_fs_grid():
    """
    fill_fs_grid()
    
    
    Defined at fermisurface.fpp lines 102-200
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fs__fill_fs_grid()

def write_xcrysden_fs():
    """
    write_xcrysden_fs()
    
    
    Defined at fermisurface.fpp lines 204-311
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fs__write_xcrysden_fs()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "fs".')

for func in _dt_array_initialisers:
    func()
