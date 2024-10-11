"""
Module check_stop


Defined at check_stop.fpp lines 14-177

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def check_stop_init(max_seconds_=None):
    """
    check_stop_init([max_seconds_])
    
    
    Defined at check_stop.fpp lines 44-76
    
    Parameters
    ----------
    max_seconds_ : float
    
    -----------------------------------------------------------------------
     See module \(\texttt{check_stop}\). Must be called(only once) at the
     beginning of the calculation, optionally setting \(\text{max_seconds}\).
    """
    libqepy_modules.f90wrap_check_stop__check_stop_init(max_seconds_=max_seconds_)

def check_stop_now(inunit=None):
    """
    check_stop_now = check_stop_now([inunit])
    
    
    Defined at check_stop.fpp lines 80-176
    
    Parameters
    ----------
    inunit : int
    
    Returns
    -------
    check_stop_now : bool
    
    -----------------------------------------------------------------------
     Returns TRUE if either the user has created an 'exit' file, or if
     the elapsed wall time is larger than 'max\_seconds', or if these
     conditions have been met in a previous call.
     Moreover, this function removes the exit file and sets variable
     \(\text{stopped_by_user}\) to TRUE.
    """
    check_stop_now = \
        libqepy_modules.f90wrap_check_stop__check_stop_now(inunit=inunit)
    return check_stop_now

def get_max_seconds():
    """
    Element max_seconds ftype=real(dp) pytype=float
    
    
    Defined at check_stop.fpp line 31
    
    """
    return libqepy_modules.f90wrap_check_stop__get__max_seconds()

def set_max_seconds(max_seconds):
    libqepy_modules.f90wrap_check_stop__set__max_seconds(max_seconds)

def get_stopped_by_user():
    """
    Element stopped_by_user ftype=logical pytype=bool
    
    
    Defined at check_stop.fpp line 33
    
    """
    return libqepy_modules.f90wrap_check_stop__get__stopped_by_user()

def set_stopped_by_user(stopped_by_user):
    libqepy_modules.f90wrap_check_stop__set__stopped_by_user(stopped_by_user)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "check_stop".')

for func in _dt_array_initialisers:
    func()
