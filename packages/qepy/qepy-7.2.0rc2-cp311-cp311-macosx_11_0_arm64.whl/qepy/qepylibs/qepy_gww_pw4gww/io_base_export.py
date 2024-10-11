"""
Module io_base_export


Defined at pw4gww.fpp lines 20-26

"""
from __future__ import print_function, absolute_import, division
import libqepy_gww_pw4gww
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_file_version():
    """
    Element file_version ftype=integer pytype=int
    
    
    Defined at pw4gww.fpp line 25
    
    """
    return libqepy_gww_pw4gww.f90wrap_io_base_export__get__file_version()

file_version = get_file_version()

def get_restart_module_verbosity():
    """
    Element restart_module_verbosity ftype=integer  pytype=int
    
    
    Defined at pw4gww.fpp line 26
    
    """
    return \
        libqepy_gww_pw4gww.f90wrap_io_base_export__get__restart_module_verbosity()

def set_restart_module_verbosity(restart_module_verbosity):
    libqepy_gww_pw4gww.f90wrap_io_base_export__set__restart_module_verbosity(restart_module_verbosity)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "io_base_export".')

for func in _dt_array_initialisers:
    func()
