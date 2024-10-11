"""
Module environment


Defined at environment.fpp lines 17-212

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def environment_start(code):
    """
    environment_start(code)
    
    
    Defined at environment.fpp lines 46-98
    
    Parameters
    ----------
    code : str
    
    """
    libqepy_modules.f90wrap_environment__environment_start(code=code)

def environment_end(code):
    """
    environment_end(code)
    
    
    Defined at environment.fpp lines 101-113
    
    Parameters
    ----------
    code : str
    
    """
    libqepy_modules.f90wrap_environment__environment_end(code=code)

def opening_message(code_version):
    """
    opening_message(code_version)
    
    
    Defined at environment.fpp lines 116-137
    
    Parameters
    ----------
    code_version : str
    
    """
    libqepy_modules.f90wrap_environment__opening_message(code_version=code_version)

def parallel_info(code):
    """
    parallel_info(code)
    
    
    Defined at environment.fpp lines 155-179
    
    Parameters
    ----------
    code : str
    
    """
    libqepy_modules.f90wrap_environment__parallel_info(code=code)

def compilation_info():
    """
    compilation_info()
    
    
    Defined at environment.fpp lines 189-193
    
    
    """
    libqepy_modules.f90wrap_environment__compilation_info()

def print_cuda_info(check_use_gpu=None):
    """
    print_cuda_info([check_use_gpu])
    
    
    Defined at environment.fpp lines 197-210
    
    Parameters
    ----------
    check_use_gpu : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_environment__print_cuda_info(check_use_gpu=check_use_gpu)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "environment".')

for func in _dt_array_initialisers:
    func()
