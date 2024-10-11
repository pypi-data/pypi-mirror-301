"""
Module lr_dav_debug


Defined at lr_dav_debug.fpp lines 13-230

"""
from __future__ import print_function, absolute_import, division
import libqepy_tddfpt
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def check_orth():
    """
    check_orth()
    
    
    Defined at lr_dav_debug.fpp lines 19-53
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check_orth()

def check(flag_check):
    """
    check(flag_check)
    
    
    Defined at lr_dav_debug.fpp lines 56-108
    
    Parameters
    ----------
    flag_check : str
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     For debuging
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check(flag_check=flag_check)

def check_overlap(vec):
    """
    check_overlap(vec)
    
    
    Defined at lr_dav_debug.fpp lines 111-132
    
    Parameters
    ----------
    vec : complex array
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Apr. 2013
    -------------------------------------------------------------------------------
     To see if the vector is othogonal to occupied space
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check_overlap(vec=vec)

def check_overlap_basis(vec):
    """
    check_overlap_basis(vec)
    
    
    Defined at lr_dav_debug.fpp lines 135-154
    
    Parameters
    ----------
    vec : complex array
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Apr. 2013
    -------------------------------------------------------------------------------
     Check the overlap between residue and basis
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check_overlap_basis(vec=vec)

def check_revc0():
    """
    check_revc0()
    
    
    Defined at lr_dav_debug.fpp lines 157-195
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Apr. 2013
    -------------------------------------------------------------------------------
     Due to the bug of virt_read, this is to check if revc0 is correct
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check_revc0()

def check_hermitian():
    """
    check_hermitian()
    
    
    Defined at lr_dav_debug.fpp lines 198-229
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Apr. 2013
    -------------------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_lr_dav_debug__check_hermitian()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "lr_dav_debug".')

for func in _dt_array_initialisers:
    func()
