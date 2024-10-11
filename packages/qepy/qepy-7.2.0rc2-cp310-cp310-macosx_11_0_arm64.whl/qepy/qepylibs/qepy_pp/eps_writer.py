"""
Module eps_writer


Defined at epsilon.fpp lines 130-179

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def eps_writetofile(namein, desc, nw, wgrid, ncol, var, desc2=None):
    """
    eps_writetofile(namein, desc, nw, wgrid, ncol, var[, desc2])
    
    
    Defined at epsilon.fpp lines 141-177
    
    Parameters
    ----------
    namein : str
    desc : str
    nw : int
    wgrid : float array
    ncol : int
    var : float array
    desc2 : str
    
    ------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_eps_writer__eps_writetofile(namein=namein, desc=desc, nw=nw, \
        wgrid=wgrid, ncol=ncol, var=var, desc2=desc2)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "eps_writer".')

for func in _dt_array_initialisers:
    func()
