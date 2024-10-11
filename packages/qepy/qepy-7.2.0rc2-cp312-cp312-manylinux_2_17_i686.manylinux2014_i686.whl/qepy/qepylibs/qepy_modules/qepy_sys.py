"""
Module qepy_sys


Defined at qepy_sys.fpp lines 12-75

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qepy_my_iargc():
    """
    qepy_my_iargc = qepy_my_iargc()
    
    
    Defined at qepy_sys.fpp lines 33-47
    
    
    Returns
    -------
    qepy_my_iargc : int
    
    """
    qepy_my_iargc = libqepy_modules.f90wrap_qepy_sys__qepy_my_iargc()
    return qepy_my_iargc

def qepy_my_getarg(narg):
    """
    arg = qepy_my_getarg(narg)
    
    
    Defined at qepy_sys.fpp lines 50-75
    
    Parameters
    ----------
    narg : int
    
    Returns
    -------
    arg : str
    
    """
    arg = libqepy_modules.f90wrap_qepy_sys__qepy_my_getarg(narg=narg)
    return arg

def get_command_line():
    """
    Element command_line ftype=character(len=512) pytype=str
    
    
    Defined at qepy_sys.fpp line 18
    
    """
    return libqepy_modules.f90wrap_qepy_sys__get__command_line()

def set_command_line(command_line):
    libqepy_modules.f90wrap_qepy_sys__set__command_line(command_line)

def get_is_mpi():
    """
    Element is_mpi ftype=logical pytype=bool
    
    
    Defined at qepy_sys.fpp line 20
    
    """
    return libqepy_modules.f90wrap_qepy_sys__get__is_mpi()

def set_is_mpi(is_mpi):
    libqepy_modules.f90wrap_qepy_sys__set__is_mpi(is_mpi)

def get_is_openmp():
    """
    Element is_openmp ftype=logical pytype=bool
    
    
    Defined at qepy_sys.fpp line 21
    
    """
    return libqepy_modules.f90wrap_qepy_sys__get__is_openmp()

def set_is_openmp(is_openmp):
    libqepy_modules.f90wrap_qepy_sys__set__is_openmp(is_openmp)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "qepy_sys".')

for func in _dt_array_initialisers:
    func()
