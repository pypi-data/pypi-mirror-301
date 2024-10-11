"""
Module fermisurfer_common


Defined at fermisurfer_common.fpp lines 13-189

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def rotate_k_fs(equiv):
    """
    rotate_k_fs(equiv)
    
    
    Defined at fermisurfer_common.fpp lines 24-119
    
    Parameters
    ----------
    equiv : int array
    
    --------------------------------------------------------------------------
     This routine find the equivalent k-point in irr-BZ for the whole BZ
     Also compute the max. and min. band index containing Fermi surfaces.
    """
    libqepy_pp.f90wrap_fermisurfer_common__rotate_k_fs(equiv=equiv)

def write_fermisurfer(eig, mat, filename):
    """
    write_fermisurfer(eig, mat, filename)
    
    
    Defined at fermisurfer_common.fpp lines 123-188
    
    Parameters
    ----------
    eig : float array
    mat : float array
    filename : str
    
    ----------------------------------------------------------------------------
     This routine output a matrix element on the Fermi surface
    """
    libqepy_pp.f90wrap_fermisurfer_common__write_fermisurfer(eig=eig, mat=mat, \
        filename=filename)

def get_b_low():
    """
    Element b_low ftype=integer pytype=int
    
    
    Defined at fermisurfer_common.fpp line 19
    
    """
    return libqepy_pp.f90wrap_fermisurfer_common__get__b_low()

def set_b_low(b_low):
    libqepy_pp.f90wrap_fermisurfer_common__set__b_low(b_low)

def get_b_high():
    """
    Element b_high ftype=integer pytype=int
    
    
    Defined at fermisurfer_common.fpp line 19
    
    """
    return libqepy_pp.f90wrap_fermisurfer_common__get__b_high()

def set_b_high(b_high):
    libqepy_pp.f90wrap_fermisurfer_common__set__b_high(b_high)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "fermisurfer_common".')

for func in _dt_array_initialisers:
    func()
