from __future__ import print_function, absolute_import, division
pname = 'libqepy_cpv'

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
import libqepy_cpv
import f90wrap.runtime
import logging
import numpy
import qepy_cpv.wanpar

def cp_postproc():
    """
    cp_postproc()
    
    
    Defined at cppp.fpp lines 22-505
    
    
    ---------------------------------------------------------------------------
    Field |    Column    | FORTRAN |
      No. |     range    | format  | Description
    ---------------------------------------------------------------------------
       1. |    1 -  6    |   A6    | Record ID(eg ATOM, HETATM)
       2. |    7 - 11    |   I5    | Atom serial number
       -  |   12 - 12    |   1X    | Blank
       3. |   13 - 16    |   A4    | Atom name(eg " CA " , " ND1")
       4. |   17 - 17    |   A1    | Alternative location code(if any)
       5. | 18 - 20 | A3 | Standard 3-letter amino acid code for residue
       -  |   21 - 21    |   1X    | Blank
       6. |   22 - 22    |   A1    | Chain identifier code
       7. |   23 - 26    |   I4    | Residue sequence number
       8. |   27 - 27    |   A1    | Insertion code(if any)
       -  |   28 - 30    |   3X    | Blank
       9. |   31 - 38    |  F8.3   | Atom's x-coordinate
      10. |   39 - 46    |  F8.3   | Atom's y-coordinate
      11. |   47 - 54    |  F8.3   | Atom's z-coordinate
      12. |   55 - 60    |  F6.2   | Occupancy value for atom
      13. |   61 - 66    |  F6.2   | B-value(thermal factor)
       -  |   67 - 67    |   1X    | Blank
      14. |   68 - 68    |   I3    | Footnote number
    ---------------------------------------------------------------------------
    """
    libqepy_cpv.f90wrap_cp_postproc()

def main():
    """
    main()
    
    
    Defined at cprstart.fpp lines 22-80
    
    
    ----------------------------------------------------------------------------
     Molecular Dynamics using Density-Functional Theory.
     This is the main routine driver for Car-Parrinello simulations.
     See the documentation coming with the Quantum ESPRESSO distribution
     for credits, references, appropriate citation of this code.
    """
    libqepy_cpv.f90wrap_main()

def manycp():
    """
    manycp()
    
    
    Defined at manycp.fpp lines 13-113
    
    
    ----------------------------------------------------------------------------
     Poor-man cp.x parallel launcher. Usage(for mpirun):
         mpirun -np Np manycp.x -ni Ni [other options]
     or whatever is appropriate for your parallel environment
     Starts Ni cp.x instances each running on Np/Ni processors.
     Each cp.x instances:
     * reads input data from from cp_N.in, N=0,..,,Ni-1 if no input
       file is specified via the -i option; from "input_file"_N
       if command-line options -i "input_file" is specified;
     * saves temporary and final data to "outdir"_N/ directory
    (or to tmp_N/ if outdir='./');
     * writes output to cp_N.out in the current directory if no input
       file is specified via the -i option; to "input_file"_N.out
       if command-line options -i "input_file" is specified.
    """
    libqepy_cpv.f90wrap_manycp()

def wfdd():
    """
    wfdd()
    
    
    Defined at wfdd.fpp lines 64-772
    
    
    ----------------------------------------------------------------------
        This program works on the overlap matrix calculated
            from parallel machine and search the unitary transformation
            Uall corresponding to the Maximally localized Wannier functions.
        The overlap matrix and lattice information are read from fort.38.
        Searching parameters are in the input file:
           cgordd  wfdt   maxwfdt   nit   nsd  q dt fric nsteps
        The final unitary matrix Uall is output to fort.39.
        Some running information is output to fort.24.
                                                Yudong Wu
                                                June 28,2001
           This code has been modified to include Damped dynamics to
           find the maximally localized wannier functions.
                                                    Manu
                                                    September 16,2001
         copyright MANU/YUDONG WU/NICOLA MARZARI/ROBERTO CAR
    ----------------------------------------------------------------------
    """
    libqepy_cpv.f90wrap_wfdd()


wanpar = qepy_cpv.wanpar
