"""
Module read_input


Defined at read_input.fpp lines 14-80

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def read_input_file(prog, input_file_):
    """
    read_input_file(prog, input_file_)
    
    
    Defined at read_input.fpp lines 33-79
    
    Parameters
    ----------
    prog : str
    input_file_ : str
    
    -------------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_read_input__read_input_file(prog=prog, \
        input_file_=input_file_)

def get_has_been_read():
    """
    Element has_been_read ftype=logical pytype=bool
    
    
    Defined at read_input.fpp line 28
    
    """
    return libqepy_modules.f90wrap_read_input__get__has_been_read()

def set_has_been_read(has_been_read):
    libqepy_modules.f90wrap_read_input__set__has_been_read(has_been_read)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "read_input".')

for func in _dt_array_initialisers:
    func()
