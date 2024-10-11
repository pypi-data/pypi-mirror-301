"""
Module open_close_input_file


Defined at open_close_input_file.fpp lines 16-203

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_file_name():
    """
    get_file_name = get_file_name()
    
    
    Defined at open_close_input_file.fpp lines 28-64
    
    
    Returns
    -------
    get_file_name : str
    
    """
    get_file_name = libqepy_modules.f90wrap_open_close_input_file__get_file_name()
    return get_file_name

def open_input_file(input_file_=None, is_xml=None):
    """
    ierr = open_input_file([input_file_, is_xml])
    
    
    Defined at open_close_input_file.fpp lines 68-176
    
    Parameters
    ----------
    input_file_ : str
    is_xml : bool
    
    Returns
    -------
    ierr : int
    
    -----------------------------------------------------------------------------
     Open file for input read, connecting it to unit \(\text{qestdin}\).
     If optional variable \(\text{is_xml}\) is present, test if the file is a
     valid xml file.
     In parallel execution, must be called by a single processor.
     Module variable input_file is set to the file name actually read.
    ---------------------------------------------------------------
    """
    ierr = \
        libqepy_modules.f90wrap_open_close_input_file__open_input_file(input_file_=input_file_, \
        is_xml=is_xml)
    return ierr

def close_input_file():
    """
    ierr = close_input_file()
    
    
    Defined at open_close_input_file.fpp lines 178-202
    
    
    Returns
    -------
    ierr : int
    
    """
    ierr = libqepy_modules.f90wrap_open_close_input_file__close_input_file()
    return ierr


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "open_close_input_file".')

for func in _dt_array_initialisers:
    func()
