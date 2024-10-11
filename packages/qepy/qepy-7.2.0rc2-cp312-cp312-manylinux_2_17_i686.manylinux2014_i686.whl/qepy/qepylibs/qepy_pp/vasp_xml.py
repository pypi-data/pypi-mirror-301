"""
Module vasp_xml


Defined at vasp_xml_module.fpp lines 15-1106

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def readxmlfile_vasp():
    """
    iexch, icorr, igcx, igcc, inlc, ierr = readxmlfile_vasp()
    
    
    Defined at vasp_xml_module.fpp lines 98-210
    
    
    Returns
    -------
    iexch : int
    icorr : int
    igcx : int
    igcc : int
    inlc : int
    ierr : int
    
    ----------------------------------------------------------------------
    """
    iexch, icorr, igcx, igcc, inlc, ierr = \
        libqepy_pp.f90wrap_vasp_xml__readxmlfile_vasp()
    return iexch, icorr, igcx, igcc, inlc, ierr


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "vasp_xml".')

for func in _dt_array_initialisers:
    func()
