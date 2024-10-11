"""
Module wy_pos


Defined at wypos.fpp lines 12-9110

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def wypos(tau, wp, inp, space_group_number, uniqueb, rhombohedral, \
    origin_choice):
    """
    wypos(tau, wp, inp, space_group_number, uniqueb, rhombohedral, origin_choice)
    
    
    Defined at wypos.fpp lines 23-484
    
    Parameters
    ----------
    tau : float array
    wp : str
    inp : float array
    space_group_number : int
    uniqueb : bool
    rhombohedral : bool
    origin_choice : int
    
    -----------------------------------------------------------
     Convert atomic positions given in Wyckoff convention:
     multiplicity-letter + parameter(s), to crystal positions.
    -----------------------------------------------------------
    """
    libqepy_modules.f90wrap_wy_pos__wypos(tau=tau, wp=wp, inp=inp, \
        space_group_number=space_group_number, uniqueb=uniqueb, \
        rhombohedral=rhombohedral, origin_choice=origin_choice)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "wy_pos".')

for func in _dt_array_initialisers:
    func()
