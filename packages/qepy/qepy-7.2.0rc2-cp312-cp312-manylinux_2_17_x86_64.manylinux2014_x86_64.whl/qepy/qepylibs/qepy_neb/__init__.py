from __future__ import print_function, absolute_import, division
pname = 'libqepy_neb'

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
import libqepy_neb
import f90wrap.runtime
import logging
import numpy
import qepy_neb.int_global_variables

def neb():
    """
    neb()
    
    
    Defined at neb.fpp lines 13-124
    
    
    ----------------------------------------------------------------------------
     ... Nudged Elastic Band / Strings Method algorithm
    """
    libqepy_neb.f90wrap_neb()

def images_interpolator():
    """
    images_interpolator()
    
    
    Defined at path_interpolation.fpp lines 35-365
    
    
    """
    libqepy_neb.f90wrap_images_interpolator()

def input_images_getarg():
    """
    input_images = input_images_getarg()
    
    
    Defined at path_io_tools.fpp lines 11-48
    
    
    Returns
    -------
    input_images : int
    
    -----------------------------------------------------------------------------
     check for command-line option "-input_images N" or "--input_images N",
     return N(0 if not found)
    """
    input_images = libqepy_neb.f90wrap_input_images_getarg()
    return input_images

def close_io_units(myunit):
    """
    close_io_units(myunit)
    
    
    Defined at path_io_tools.fpp lines 51-65
    
    Parameters
    ----------
    myunit : int
    
    -----------------------------------------------------------------------------
    """
    libqepy_neb.f90wrap_close_io_units(myunit=myunit)

def open_io_units(myunit, file_name, lappend):
    """
    open_io_units(myunit, file_name, lappend)
    
    
    Defined at path_io_tools.fpp lines 69-86
    
    Parameters
    ----------
    myunit : int
    file_name : str
    lappend : bool
    
    -----------------------------------------------------------------------------
    """
    libqepy_neb.f90wrap_open_io_units(myunit=myunit, file_name=file_name, \
        lappend=lappend)


int_global_variables = qepy_neb.int_global_variables
