"""
Module space_group


Defined at space_group.fpp lines 12-16421

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def sym_brav(space_group_number):
    """
    sym_n, ibrav = sym_brav(space_group_number)
    
    
    Defined at space_group.fpp lines 24-730
    
    Parameters
    ----------
    space_group_number : int
    
    Returns
    -------
    sym_n : int
    ibrav : int
    
    """
    sym_n, ibrav = \
        libqepy_modules.f90wrap_space_group__sym_brav(space_group_number=space_group_number)
    return sym_n, ibrav

def find_equivalent_tau(space_group_number, inco, outco, i, unique):
    """
    find_equivalent_tau(space_group_number, inco, outco, i, unique)
    
    
    Defined at space_group.fpp lines 732-1205
    
    Parameters
    ----------
    space_group_number : int
    inco : float array
    outco : float array
    i : int
    unique : str
    
    """
    libqepy_modules.f90wrap_space_group__find_equivalent_tau(space_group_number=space_group_number, \
        inco=inco, outco=outco, i=i, unique=unique)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "space_group".')

for func in _dt_array_initialisers:
    func()
