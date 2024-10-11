"""
Module pw_interfaces


Defined at pwcom.fpp lines 475-487

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
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
        "pw_interfaces".')

for func in _dt_array_initialisers:
    func()
