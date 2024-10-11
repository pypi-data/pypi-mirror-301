from __future__ import print_function, absolute_import, division
pname = 'libqepy_gww_pw4gww'

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
import libqepy_gww_pw4gww
import f90wrap.runtime
import logging
import numpy
import qepy_gww_pw4gww.io_base_export

def gwl_punch():
    """
    gwl_punch()
    
    
    Defined at pw4gww.fpp lines 29-765
    
    
    -----------------------------------------------------------------------
     read in PWSCF data in XML format using IOTK lib
     then prepare matrices for GWL calculation
     input:  namelist "&inputpp", with variables
       prefix       prefix of input files saved by program pwscf
       outdir       temporary directory where files resides
       pp_file      output file. If it is omitted, a directory
                    "prefix.export/" is created in outdir and
                    some output files are put there. Anyway all the data
                    are accessible through the "prefix.export/index.xml" file which
                    contains implicit pointers to all the other files in the
                    export directory. If reading is done by the IOTK library
                    all data appear to be in index.xml even if physically it
                    is not.
       uspp_spsi    using US PP if set .TRUE. writes S | psi >
                    and | psi > separately in the output file
       single_file  one-file output is produced
       ascii        ....
       pseudo_dir   pseudopotential directory
       psfile(:)    name of the pp file for each species
    """
    libqepy_gww_pw4gww.f90wrap_gwl_punch()


io_base_export = qepy_gww_pw4gww.io_base_export
