from __future__ import print_function, absolute_import, division
pname = 'libqepy_hp'

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
import libqepy_hp
import f90wrap.runtime
import logging
import numpy

def hp_main():
    """
    hp_main()
    
    
    Defined at hp_main.fpp lines 13-265
    
    
    -----------------------------------------------------------------------
     This is the main driver of the HP code.
    """
    libqepy_hp.f90wrap_hp_main()


