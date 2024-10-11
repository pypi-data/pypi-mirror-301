from __future__ import print_function, absolute_import, division
pname = 'libqepy_gww_simple_bse'

# control the output
import sys
from importlib import import_module
from qepy.core import Logger, env
class QEpyLib :
    def __init__(self, **kwargs):
        qepylib = import_module(pname)
        sys.modules[pname] = self
        self.qepylib = qepylib

    def __getattr__(self, attr):
        attr_value = getattr(self.qepylib, attr)
        if '__array__' not in attr :
            attr_value = Logger.stdout2file(attr_value, fileobj=env['STDOUT'])
        return attr_value
qepylib = QEpyLib()
import libqepy_gww_simple_bse
import f90wrap.runtime
import logging
import numpy

def simple_bse():
    """
    simple_bse()
    
    
    Defined at simple_bse.fpp lines 5-21
    
    
    """
    libqepy_gww_simple_bse.f90wrap_simple_bse()


