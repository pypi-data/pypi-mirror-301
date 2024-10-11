"""
Module tddft_version


Defined at tddft_version.fpp lines 14-20

"""
from __future__ import print_function, absolute_import, division
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_tddft_git_revision():
    """
    Element tddft_git_revision ftype=character(len=40) pytype=str
    
    
    Defined at tddft_version.fpp line 20
    
    """
    return libqepy_cetddft.f90wrap_tddft_version__get__tddft_git_revision()

def set_tddft_git_revision(tddft_git_revision):
    libqepy_cetddft.f90wrap_tddft_version__set__tddft_git_revision(tddft_git_revision)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "tddft_version".')

for func in _dt_array_initialisers:
    func()
