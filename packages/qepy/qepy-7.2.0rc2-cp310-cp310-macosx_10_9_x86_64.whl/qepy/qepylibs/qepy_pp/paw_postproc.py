"""
Module paw_postproc


Defined at paw_postproc.fpp lines 5-171

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "paw_postproc".')

for func in _dt_array_initialisers:
    func()
