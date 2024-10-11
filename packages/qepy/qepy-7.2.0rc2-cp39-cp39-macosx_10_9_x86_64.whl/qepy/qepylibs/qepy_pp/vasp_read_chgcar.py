"""
Module vasp_read_chgcar


Defined at vasp_read_chgcar_mod.fpp lines 14-176

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def vaspread_rho():
    """
    ierr = vaspread_rho()
    
    
    Defined at vasp_read_chgcar_mod.fpp lines 48-175
    
    
    Returns
    -------
    ierr : int
    
    -----------------------------------------------------------------------
     This subroutine will read information from VASP output
        rho from CHARCAR
    """
    ierr = libqepy_pp.f90wrap_vasp_read_chgcar__vaspread_rho()
    return ierr


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "vasp_read_chgcar".')

for func in _dt_array_initialisers:
    func()
