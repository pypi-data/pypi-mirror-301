from __future__ import print_function, absolute_import, division
pname = 'libqepy_cetddft'

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
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy
import qepy_cetddft.qepy_tddft_mod
import qepy_cetddft.tddft_version
import qepy_cetddft.qepy_tddft_common
import qepy_cetddft.tddft_cgsolver_module
import qepy_cetddft.tddft_module

def qepy_molecule_optical_absorption():
    """
    qepy_molecule_optical_absorption()
    
    
    Defined at qepy_molecule_optical_absorption.fpp lines 13-382
    
    
    ----------------------------------------------------------------------
      ... Compute optical absorption spectrum by real-time TDDFT
      ... References:
    (1) Phys. Rev. B 73, 035408(2006)
    (2) http://www.netlib.org/linalg/html_templates/Templates.html
                                                 Xiaofeng Qian, MIT(2008)
    ----------------------------------------------------------------------
    """
    libqepy_cetddft.f90wrap_qepy_molecule_optical_absorption()

def qepy_tddft_main_initial(infile, my_world_comm=None):
    """
    qepy_tddft_main_initial(infile[, my_world_comm])
    
    
    Defined at qepy_tddft_main.fpp lines 13-79
    
    Parameters
    ----------
    infile : str
    my_world_comm : int
    
    -----------------------------------------------------------------------
     ... This is the main driver of the real time TDDFT propagation.
     ... Authors: Xiaofeng Qian and Davide Ceresoli
     ...
     ... References:
     ...   Xiaofeng Qian, Ju Li, Xi Lin, and Sidney Yip, PRB 73, 035408(2006)
     ...
    """
    libqepy_cetddft.f90wrap_qepy_tddft_main_initial(infile=infile, \
        my_world_comm=my_world_comm)

def qepy_tddft_main_setup():
    """
    qepy_tddft_main_setup()
    
    
    Defined at qepy_tddft_main.fpp lines 82-142
    
    
    -----------------------------------------------------------------------
     ... This is the main driver of the real time TDDFT propagation.
     ... Authors: Xiaofeng Qian and Davide Ceresoli
     ...
     ... References:
     ...   Xiaofeng Qian, Ju Li, Xi Lin, and Sidney Yip, PRB 73, 035408(2006)
     ...
    """
    libqepy_cetddft.f90wrap_qepy_tddft_main_setup()

def qepy_stop_tddft(print_flag=None):
    """
    qepy_stop_tddft([print_flag])
    
    
    Defined at qepy_tddft_main.fpp lines 145-165
    
    Parameters
    ----------
    print_flag : int
    
    """
    libqepy_cetddft.f90wrap_qepy_stop_tddft(print_flag=print_flag)

def qepy_tddft_readin(infile=None):
    """
    qepy_tddft_readin([infile])
    
    
    Defined at qepy_tddft_routines.fpp lines 13-109
    
    Parameters
    ----------
    infile : str
    
    -----------------------------------------------------------------------
     ... Read in the tddft input file. The input file consists of a
     ... single namelist &inputtddft. See doc/user-manual.pdf for the
     ... list of input keywords.
    """
    libqepy_cetddft.f90wrap_qepy_tddft_readin(infile=infile)

def qepy_tddft_allocate():
    """
    qepy_tddft_allocate()
    
    
    Defined at qepy_tddft_routines.fpp lines 147-161
    
    
    -----------------------------------------------------------------------
     ... Allocate memory for TDDFT
    """
    libqepy_cetddft.f90wrap_qepy_tddft_allocate()

def qepy_tddft_closefil():
    """
    qepy_tddft_closefil()
    
    
    Defined at qepy_tddft_routines.fpp lines 239-256
    
    
    -----------------------------------------------------------------------
     ... Close files opened by TDDFT
    """
    libqepy_cetddft.f90wrap_qepy_tddft_closefil()

def qepy_tddft_setup():
    """
    qepy_tddft_setup()
    
    
    Defined at qepy_tddft_setup.fpp lines 13-133
    
    
    -----------------------------------------------------------------------
     ... TDDFT setup
    """
    libqepy_cetddft.f90wrap_qepy_tddft_setup()

def qepy_update_hamiltonian(istep):
    """
    qepy_update_hamiltonian(istep)
    
    
    Defined at qepy_update_ham.fpp lines 13-89
    
    Parameters
    ----------
    istep : int
    
    -----------------------------------------------------------------------
     ... Update the hamiltonian
    """
    libqepy_cetddft.f90wrap_qepy_update_hamiltonian(istep=istep)

def tddft_readin():
    """
    tddft_readin()
    
    
    Defined at tddft_routines.fpp lines 13-79
    
    
    -----------------------------------------------------------------------
     ... Read in the tddft input file. The input file consists of a
     ... single namelist &inputtddft. See doc/user-manual.pdf for the
     ... list of input keywords.
    """
    libqepy_cetddft.f90wrap_tddft_readin()

def tddft_allocate():
    """
    tddft_allocate()
    
    
    Defined at tddft_routines.fpp lines 83-95
    
    
    -----------------------------------------------------------------------
     ... Allocate memory for TDDFT
    """
    libqepy_cetddft.f90wrap_tddft_allocate()

def tddft_summary():
    """
    tddft_summary()
    
    
    Defined at tddft_routines.fpp lines 98-135
    
    
    -----------------------------------------------------------------------
     ... Print a short summary of the calculation
    """
    libqepy_cetddft.f90wrap_tddft_summary()

def tddft_openfil():
    """
    tddft_openfil()
    
    
    Defined at tddft_routines.fpp lines 138-170
    
    
    -----------------------------------------------------------------------
     ... Open files needed for TDDFT
    """
    libqepy_cetddft.f90wrap_tddft_openfil()

def tddft_closefil():
    """
    tddft_closefil()
    
    
    Defined at tddft_routines.fpp lines 173-185
    
    
    -----------------------------------------------------------------------
     ... Close files opened by TDDFT
    """
    libqepy_cetddft.f90wrap_tddft_closefil()

def print_clock_tddft():
    """
    print_clock_tddft()
    
    
    Defined at tddft_routines.fpp lines 188-219
    
    
    -----------------------------------------------------------------------
     ... Print clocks
    """
    libqepy_cetddft.f90wrap_print_clock_tddft()

def tddft_memory_report():
    """
    tddft_memory_report()
    
    
    Defined at tddft_routines.fpp lines 222-244
    
    
    -----------------------------------------------------------------------
     ... Print estimated memory usage
    """
    libqepy_cetddft.f90wrap_tddft_memory_report()

def tddft_setup():
    """
    tddft_setup()
    
    
    Defined at tddft_setup.fpp lines 13-129
    
    
    -----------------------------------------------------------------------
     ... TDDFT setup
    """
    libqepy_cetddft.f90wrap_tddft_setup()

def tddft_ch_psi_all(n, h, ah, ee, ik, m):
    """
    tddft_ch_psi_all(n, h, ah, ee, ik, m)
    
    
    Defined at tddft_ch_psi_all.fpp lines 13-57
    
    Parameters
    ----------
    n : int
    h : complex array
    ah : complex array
    ee : complex
    ik : int
    m : int
    
    -----------------------------------------------------------------------
     This routine applies the operator( S + ee * H), where, ee = i * dt/2
     to a vector h. The result is given in Ah.
    """
    libqepy_cetddft.f90wrap_tddft_ch_psi_all(n=n, h=h, ah=ah, ee=ee, ik=ik, m=m)

def tddft_cgsolver_initialize(ndmx, nbnd):
    """
    tddft_cgsolver_initialize(ndmx, nbnd)
    
    
    Defined at tddft_cgsolver.fpp lines 32-42
    
    Parameters
    ----------
    ndmx : int
    nbnd : int
    
    -----------------------------------------------------------------------
     ... allocate memory for the solver
    """
    libqepy_cetddft.f90wrap_tddft_cgsolver_initialize(ndmx=ndmx, nbnd=nbnd)

def tddft_cgsolver_finalize():
    """
    tddft_cgsolver_finalize()
    
    
    Defined at tddft_cgsolver.fpp lines 45-52
    
    
    -----------------------------------------------------------------------
     ... deallocate memory
    """
    libqepy_cetddft.f90wrap_tddft_cgsolver_finalize()

def tddft_cgsolver(a, b, x, ndmx, ndim, tol, ik, nbnd, ee):
    """
    iter, flag_global, anorm = tddft_cgsolver(a, b, x, ndmx, ndim, tol, ik, nbnd, \
        ee)
    
    
    Defined at tddft_cgsolver.fpp lines 56-184
    
    Parameters
    ----------
    a : float
    b : complex array
    x : complex array
    ndmx : int
    ndim : int
    tol : float
    ik : int
    nbnd : int
    ee : complex
    
    Returns
    -------
    iter : int
    flag_global : int
    anorm : float
    
    ----------------------------------------------------------------------
     ... Conjugate-Gradient Square method for solving:   A * x = b
     ... where: A*x is evaluated by subroutine 'A', and 'A' is implicit
     ... general square-matrix.
                                                Xiaofeng Qian, MIT(2008)
    """
    iter, flag_global, anorm = libqepy_cetddft.f90wrap_tddft_cgsolver(a=a, b=b, x=x, \
        ndmx=ndmx, ndim=ndim, tol=tol, ik=ik, nbnd=nbnd, ee=ee)
    return iter, flag_global, anorm

def update_hamiltonian(istep):
    """
    update_hamiltonian(istep)
    
    
    Defined at update_ham.fpp lines 13-74
    
    Parameters
    ----------
    istep : int
    
    -----------------------------------------------------------------------
     ... Update the hamiltonian
    """
    libqepy_cetddft.f90wrap_update_hamiltonian(istep=istep)

def delta_eband():
    """
    delta_e = delta_eband()
    
    
    Defined at update_ham.fpp lines 77-131
    
    
    Returns
    -------
    delta_e : float
    
    -----------------------------------------------------------------------
     ... delta_e = - \int rho%of_r(r)  v%of_r(r)
                   - \int rho%kin_r(r) v%kin_r(r) [for Meta-GGA]
                   - \sum rho%ns       v%ns       [for LDA+U]
                   - \sum becsum       D1_Hxc     [for PAW]
    """
    delta_e = libqepy_cetddft.f90wrap_delta_eband()
    return delta_e

def sum_energies():
    """
    sum_energies()
    
    
    Defined at update_ham.fpp lines 134-170
    
    
    -----------------------------------------------------------------------
    """
    libqepy_cetddft.f90wrap_sum_energies()

def apply_electric_field(tddft_psi):
    """
    apply_electric_field(tddft_psi)
    
    
    Defined at apply_efield.fpp lines 13-51
    
    Parameters
    ----------
    tddft_psi : complex array
    
    -----------------------------------------------------------------------
     ... Apply an electric field impuse at t = 0, a homogeneous phase-shift
     ... to each band
    """
    libqepy_cetddft.f90wrap_apply_electric_field(tddft_psi=tddft_psi)

def molecule_optical_absorption():
    """
    molecule_optical_absorption()
    
    
    Defined at molecule_optical_absorption.fpp lines 13-315
    
    
    ----------------------------------------------------------------------
      ... Compute optical absorption spectrum by real-time TDDFT
      ... References:
    (1) Phys. Rev. B 73, 035408(2006)
    (2) http://www.netlib.org/linalg/html_templates/Templates.html
                                                 Xiaofeng Qian, MIT(2008)
    ----------------------------------------------------------------------
    """
    libqepy_cetddft.f90wrap_molecule_optical_absorption()

def molecule_setup_r():
    """
    molecule_setup_r()
    
    
    Defined at molecule_operators.fpp lines 13-97
    
    
    -----------------------------------------------------------------------
     ... Setup the position operator in real space. The origin is set to center
     ... of ionic charge. (r is in units of alat)
    """
    libqepy_cetddft.f90wrap_molecule_setup_r()

def molecule_compute_dipole(charge, dip):
    """
    molecule_compute_dipole(charge, dip)
    
    
    Defined at molecule_operators.fpp lines 100-126
    
    Parameters
    ----------
    charge : float array
    dip : float array
    
    -----------------------------------------------------------------------
     ... Compute electron dipole moment using total charge density
    """
    libqepy_cetddft.f90wrap_molecule_compute_dipole(charge=charge, dip=dip)

def molecule_compute_quadrupole(quad):
    """
    molecule_compute_quadrupole(quad)
    
    
    Defined at molecule_operators.fpp lines 129-155
    
    Parameters
    ----------
    quad : float array
    
    -----------------------------------------------------------------------
     ... Compute electron quadrupoledipole moment using total charge density
    """
    libqepy_cetddft.f90wrap_molecule_compute_quadrupole(quad=quad)

def stop_code(flag):
    """
    stop_code(flag)
    
    
    Defined at stop_code.fpp lines 13-38
    
    Parameters
    ----------
    flag : bool
    
    ----------------------------------------------------------------------------
     ... Synchronize processes before stopping.
    """
    libqepy_cetddft.f90wrap_stop_code(flag=flag)

def trajectoryxyz():
    """
    trajectoryxyz()
    
    
    Defined at trajectory.fpp lines 13-34
    
    
    -----------------------------------------------------------------------
    """
    libqepy_cetddft.f90wrap_trajectoryxyz()

def save_rho(istep):
    """
    save_rho(istep)
    
    
    Defined at trajectory.fpp lines 38-65
    
    Parameters
    ----------
    istep : int
    
    -----------------------------------------------------------------------
    """
    libqepy_cetddft.f90wrap_save_rho(istep=istep)

def setup_wavepacket():
    """
    setup_wavepacket()
    
    
    Defined at wavepacket.fpp lines 13-106
    
    
    -----------------------------------------------------------------------
     ... Setup a wavepacket in real space. The wavepacket is moving
     ... in the -z direction.
    """
    libqepy_cetddft.f90wrap_setup_wavepacket()

def tddft_main():
    """
    tddft_main()
    
    
    Defined at tddft_main.fpp lines 13-100
    
    
    -----------------------------------------------------------------------
     ... This is the main driver of the real time TDDFT propagation.
     ... Authors: Xiaofeng Qian and Davide Ceresoli
     ...
     ... References:
     ...   Xiaofeng Qian, Ju Li, Xi Lin, and Sidney Yip, PRB 73, 035408(2006)
     ...
    """
    libqepy_cetddft.f90wrap_tddft_main()


qepy_tddft_mod = qepy_cetddft.qepy_tddft_mod
tddft_version = qepy_cetddft.tddft_version
qepy_tddft_common = qepy_cetddft.qepy_tddft_common
tddft_cgsolver_module = qepy_cetddft.tddft_cgsolver_module
tddft_module = qepy_cetddft.tddft_module
