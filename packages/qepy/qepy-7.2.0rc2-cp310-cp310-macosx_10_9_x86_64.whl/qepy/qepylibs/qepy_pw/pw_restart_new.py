"""
Module pw_restart_new


Defined at pw_restart_new.fpp lines 13-1556

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def pw_write_schema(only_init, wf_collect):
    """
    pw_write_schema(only_init, wf_collect)
    
    
    Defined at pw_restart_new.fpp lines 62-844
    
    Parameters
    ----------
    only_init : bool
    wf_collect : bool
    
    ------------------------------------------------------------------------
     only_init  = T  write only variables that are known after the
                     initial steps of initialization(e.g. structure)
                = F  write the complete xml file
     wf_collect = T  if final wavefunctions in portable format are written,
                  F  if wavefunctions are either not written or are written
                     in binary non-portable form(for checkpointing)
                     NB: wavefunctions are not written here in any case
    """
    libqepy_pw.f90wrap_pw_restart_new__pw_write_schema(only_init=only_init, \
        wf_collect=wf_collect)

def write_collected_wfc():
    """
    write_collected_wfc()
    
    
    Defined at pw_restart_new.fpp lines 848-1002
    
    
    ------------------------------------------------------------------------
    """
    libqepy_pw.f90wrap_pw_restart_new__write_collected_wfc()

def read_xml_file():
    """
    wfc_is_collected = read_xml_file()
    
    
    Defined at pw_restart_new.fpp lines 1090-1403
    
    
    Returns
    -------
    wfc_is_collected : bool
    
    ------------------------------------------------------------------------
     ... This routine allocates space for all quantities already computed
     ... in the pwscf program and reads them from the data file.
     ... All quantities that are initialized in subroutine "setup" when
     ... starting from scratch should be initialized here when restarting
    """
    wfc_is_collected = libqepy_pw.f90wrap_pw_restart_new__read_xml_file()
    return wfc_is_collected

def read_collected_wfc(dirname, ik, arr, label_=None, ierr_=None):
    """
    read_collected_wfc(dirname, ik, arr[, label_, ierr_])
    
    
    Defined at pw_restart_new.fpp lines 1407-1554
    
    Parameters
    ----------
    dirname : str
    ik : int
    arr : complex array
    label_ : str
    ierr_ : int
    
    ------------------------------------------------------------------------
     ... reads from directory "dirname" (new file format) for k-point "ik"
     ... wavefunctions from collected format into distributed array "arr"
    """
    libqepy_pw.f90wrap_pw_restart_new__read_collected_wfc(dirname=dirname, ik=ik, \
        arr=arr, label_=label_, ierr_=ierr_)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "pw_restart_new".')

for func in _dt_array_initialisers:
    func()
