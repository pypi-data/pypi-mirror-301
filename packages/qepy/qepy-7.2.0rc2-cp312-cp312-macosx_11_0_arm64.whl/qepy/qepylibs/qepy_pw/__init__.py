from __future__ import print_function, absolute_import, division
pname = 'libqepy_pw'

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
import libqepy_pw
import f90wrap.runtime
import logging
import numpy
import qepy_pw.basis
import qepy_pw.lsda_mod
import qepy_pw.symm_base
import qepy_pw.klist
import qepy_pw.qepy_mod
import qepy_pw.fft_types
import qepy_pw.pw_interfaces
import qepy_pw.relax
import qepy_pw.scf
import qepy_pw.pw_restart_new
import qepy_pw.fixed_occ
import qepy_pw.rap_point_group_so
import qepy_pw.rap_point_group
import qepy_pw.pwcom
import qepy_pw.qepy_common
import qepy_pw.force_mod
import qepy_pw.vlocal
import qepy_pw.ener
import qepy_pw.symme
import qepy_pw.wvfct
import qepy_pw.rap_point_group_is
import qepy_pw.extrapolation
import qepy_pw.cellmd

def add_qexsd_step(i_step):
    """
    add_qexsd_step(i_step)
    
    
    Defined at add_qexsd_step.fpp lines 13-108
    
    Parameters
    ----------
    i_step : int
    
    -----------------------------------------------------------------
     This routine just calls the routine \(\texttt{qexsd_step_addstep}\)
     which adds a new xml element to to the list of steps run by PW.
     In this way the \(\texttt{addstep}\) routine in the
     \(\texttt{qexsd_step_addstep}\) routine does not depend on global
     variables.
     P. Delugas, April 2016.
    ------------------------------------------------------------------------
           START_GLOBAL_VARIABLES( INTENT(IN) )
    --------------------------------------------------------------------------
    """
    libqepy_pw.f90wrap_add_qexsd_step(i_step=i_step)

def close_files(lflag):
    """
    close_files(lflag)
    
    
    Defined at close_files.fpp lines 13-86
    
    Parameters
    ----------
    lflag : bool
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes for a new scf calculation.
    """
    libqepy_pw.f90wrap_close_files(lflag=lflag)

def electrons():
    """
    electrons()
    
    
    Defined at electrons.fpp lines 18-383
    
    
    ----------------------------------------------------------------------------
     General self-consistency loop, also for hybrid functionals.
     For non-hybrid functionals it just calls \(\texttt{electron_scf}\).
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%  Iterate hybrid functional  %%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    libqepy_pw.f90wrap_electrons()

def electrons_scf(printout, exxen):
    """
    electrons_scf(printout, exxen)
    
    
    Defined at electrons.fpp lines 387-1673
    
    Parameters
    ----------
    printout : int
    exxen : float
    
    ----------------------------------------------------------------------------
     This routine is a driver of the self-consistent cycle.
     It uses the routine \(\texttt{c_bands}\) for computing the bands at fixed
     Hamiltonian, the routine \(\texttt{sum_band}\) to compute the charge density,
     the routine \(\texttt{v_of_rho}\) to compute the new potential and the routine
     \(\text{mix_rho}\) to mix input and output charge densities.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%          iterate
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    libqepy_pw.f90wrap_electrons_scf(printout=printout, exxen=exxen)

def exxenergyace():
    """
    exxenergyace = exxenergyace()
    
    
    Defined at electrons.fpp lines 1677-1727
    
    
    Returns
    -------
    exxenergyace : float
    
    --------------------------------------------------------------------------
     Compute exchange energy using ACE
    """
    exxenergyace = libqepy_pw.f90wrap_exxenergyace()
    return exxenergyace

def forces():
    """
    forces()
    
    
    Defined at forces.fpp lines 13-489
    
    
    ----------------------------------------------------------------------------
     This routine is a driver routine which computes the forces
     acting on the atoms. The complete expression of the forces
     contains many parts which are computed by different routines:
     - force_lc: local potential contribution
     - force_us: non-local potential contribution
     - (esm_)force_ew: (ESM) electrostatic ewald term
     - force_cc: nonlinear core correction contribution
     - force_corr: correction term for incomplete self-consistency
     - force_hub: contribution due to the Hubbard term;
     - force_london: Grimme DFT+D dispersion forces
     - force_d3: Grimme-D3(DFT-D3) dispersion forces
     - force_xdm: XDM dispersion forces
     - more terms from external electric fields, Martyna-Tuckerman, etc.
     - force_sol: contribution due to 3D-RISM
    """
    libqepy_pw.f90wrap_forces()

def hinit1():
    """
    hinit1()
    
    
    Defined at hinit1.fpp lines 13-116
    
    
    ----------------------------------------------------------------------------
     Atomic configuration dependent hamiltonian initialization,
     potential, wavefunctions for Hubbard U.
     Important note: it does not recompute structure factors and core charge,
     they must be computed before this routine is called.
    """
    libqepy_pw.f90wrap_hinit1()

def move_ions(idone, ions_status):
    """
    optimizer_failed = move_ions(idone, ions_status)
    
    
    Defined at move_ions.fpp lines 13-435
    
    Parameters
    ----------
    idone : int
    ions_status : int
    
    Returns
    -------
    optimizer_failed : bool
    
    ----------------------------------------------------------------------------
     Perform a ionic step, according to the requested scheme:
     * lbfgs: bfgs minimizations
     * lmd: molecular dynamics( all kinds )
     Additional variables affecting the calculation:
     * lmovecell: Variable-cell calculation
     * calc: type of MD
     * lconstrain: constrained MD
     * "idone" is the counter on ionic moves, "nstep" their total number
     * "istep" contains the number of all steps including previous runs.
     Coefficients for potential and wavefunctions extrapolation are
     no longer computed here but in update_pot.
    """
    optimizer_failed = libqepy_pw.f90wrap_move_ions(idone=idone, \
        ions_status=ions_status)
    return optimizer_failed

def non_scf():
    """
    non_scf()
    
    
    Defined at non_scf.fpp lines 14-202
    
    
    -----------------------------------------------------------------------
     Diagonalization of the KS hamiltonian in the non-scf case.
    """
    libqepy_pw.f90wrap_non_scf()

def punch(what):
    """
    punch(what)
    
    
    Defined at punch.fpp lines 13-160
    
    Parameters
    ----------
    what : str
    
    ----------------------------------------------------------------------------
     This routine is called at the end of the run to save on a file
     the information needed for further processing(phonon etc.).
     * what = 'all' : write xml data file and, if io_level > -1, charge
                      density and wavefunctions. For final data.
     * what = 'config' : write xml data file and charge density; also,
                         for nks=1, wavefunctions in plain binary format
    (see why in comments below). For intermediate
                         or incomplete results
     * what = 'config-only' : write xml data file only
     * what = 'config-init' : write xml data file only excluding final results
    (for dry run, can be called at early stages).
    """
    libqepy_pw.f90wrap_punch(what=what)

def pw2casino(istep):
    """
    pw2casino(istep)
    
    
    Defined at pw2casino.fpp lines 16-89
    
    Parameters
    ----------
    istep : int
    
    ----------------------------------------------------------------------------
    """
    libqepy_pw.f90wrap_pw2casino(istep=istep)

def run_pwscf():
    """
    exit_status = run_pwscf()
    
    
    Defined at run_pwscf.fpp lines 13-346
    
    
    Returns
    -------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Author: Paolo Giannozzi
     License: GNU
     Summary: Run an instance of the Plane Wave Self-Consistent Field code
     Run an instance of the Plane Wave Self-Consistent Field code
     MPI initialization and input data reading is performed in the
     calling code - returns in exit_status the exit code for pw.x,
     returned in the shell. Values are:
     * 0: completed successfully
     * 1: an error has occurred(value returned by the errore() routine)
     * 2-127: convergence error
        * 2: scf convergence error
        * 3: ion convergence error
     * 128-255: code exited due to specific trigger
        * 255: exit due to user request, or signal trapped,
              or time > max_seconds
    (note: in the future, check_stop_now could also return a value
         to specify the reason of exiting, and the value could be used
         to return a different value for different reasons)
     @Note
     10/01/17 Samuel Ponce: Add Ford documentation
     @endnote
    """
    exit_status = libqepy_pw.f90wrap_run_pwscf()
    return exit_status

def reset_gvectors():
    """
    reset_gvectors()
    
    
    Defined at run_pwscf.fpp lines 351-391
    
    
    -------------------------------------------------------------
     Prepare a new scf calculation with newly recomputed grids,
     restarting from scratch, not from available data of previous
     steps(dimensions and file lengths will be different in general)
     Useful as a check of variable-cell optimization:
     once convergence is achieved, compare the final energy with the
     energy computed with G-vectors and plane waves for the final cell
    """
    libqepy_pw.f90wrap_reset_gvectors()

def reset_exx():
    """
    reset_exx()
    
    
    Defined at run_pwscf.fpp lines 396-420
    
    
    -------------------------------------------------------------
    """
    libqepy_pw.f90wrap_reset_exx()

def reset_magn():
    """
    reset_magn()
    
    
    Defined at run_pwscf.fpp lines 425-451
    
    
    ----------------------------------------------------------------
     LSDA optimization: a final configuration with zero
     absolute magnetization has been found and we check
     if it is really the minimum energy structure by
     performing a new scf iteration without any "electronic" history.
    """
    libqepy_pw.f90wrap_reset_magn()

def reset_starting_magnetization():
    """
    reset_starting_magnetization()
    
    
    Defined at run_pwscf.fpp lines 456-539
    
    
    -------------------------------------------------------------------
     On input, the scf charge density is needed.
     On output, new values for starting_magnetization, angle1, angle2
     estimated from atomic magnetic moments - to be used in last step.
    """
    libqepy_pw.f90wrap_reset_starting_magnetization()

def scale_h():
    """
    scale_h()
    
    
    Defined at scale_h.fpp lines 14-112
    
    
    -----------------------------------------------------------------------
     When variable cell calculation are performed this routine scales the
     quantities needed in the calculation of the hamiltonian using the
     new and old cell parameters.
    """
    libqepy_pw.f90wrap_scale_h()

def stop_run(exit_status):
    """
    stop_run(exit_status)
    
    
    Defined at stop_run.fpp lines 13-59
    
    Parameters
    ----------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping:
     * exit_status = 0: successfull execution, remove temporary files;
     * exit_status =-1: code stopped by user request;
     * exit_status = 1: convergence not achieved.
     Do not remove temporary files needed for restart.
    """
    libqepy_pw.f90wrap_stop_run(exit_status=exit_status)

def do_stop(exit_status):
    """
    do_stop(exit_status)
    
    
    Defined at stop_run.fpp lines 63-97
    
    Parameters
    ----------
    exit_status : int
    
    ---------------------------------------
     Stop the run.
    """
    libqepy_pw.f90wrap_do_stop(exit_status=exit_status)

def closefile():
    """
    closefile()
    
    
    Defined at stop_run.fpp lines 101-112
    
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping.
     Called by "sigcatch" when it receives a signal.
    """
    libqepy_pw.f90wrap_closefile()

def stress(sigma):
    """
    stress(sigma)
    
    
    Defined at stress.fpp lines 14-281
    
    Parameters
    ----------
    sigma : float array
    
    ----------------------------------------------------------------------
     Computes the total stress.
    """
    libqepy_pw.f90wrap_stress(sigma=sigma)

def sum_band():
    """
    sum_band()
    
    
    Defined at sum_band.fpp lines 14-812
    
    
    ----------------------------------------------------------------------------
     Calculates the symmetrized charge density and related quantities.
     Also computes the occupations and the sum of occupied eigenvalues.
    """
    libqepy_pw.f90wrap_sum_band()

def sum_bec(ik, current_spin, ibnd_start, ibnd_end, this_bgrp_nbnd):
    """
    sum_bec(ik, current_spin, ibnd_start, ibnd_end, this_bgrp_nbnd)
    
    
    Defined at sum_band.fpp lines 815-1069
    
    Parameters
    ----------
    ik : int
    current_spin : int
    ibnd_start : int
    ibnd_end : int
    this_bgrp_nbnd : int
    
    ----------------------------------------------------------------------------
     This routine computes the sum over bands:
     \[ \sum_i \langle\psi_i|\beta_l\rangle w_i \langle\beta_m|\psi_i\rangle \]
     for point "ik" and, for LSDA, spin "current_spin".
     Calls calbec to compute \(\text{"becp"}=\langle \beta_m|\psi_i \rangle\).
     Output is accumulated(unsymmetrized) into "becsum", module "uspp".
     Routine used in sum_band(if okvan) and in compute_becsum, called by hinit1(if \
         okpaw).
    """
    libqepy_pw.f90wrap_sum_bec(ik=ik, current_spin=current_spin, \
        ibnd_start=ibnd_start, ibnd_end=ibnd_end, this_bgrp_nbnd=this_bgrp_nbnd)

def add_becsum_nc(na, np, becsum_nc, becsum):
    """
    add_becsum_nc(na, np, becsum_nc, becsum)
    
    
    Defined at sum_band.fpp lines 1073-1116
    
    Parameters
    ----------
    na : int
    np : int
    becsum_nc : complex array
    becsum : float array
    
    ----------------------------------------------------------------------------
     This routine multiplies \(\text{becsum_nc}\) by the identity and the
     Pauli matrices, saves it in \(\text{becsum}\) for the calculation of
     augmentation charge and magnetization.
    """
    libqepy_pw.f90wrap_add_becsum_nc(na=na, np=np, becsum_nc=becsum_nc, \
        becsum=becsum)

def add_becsum_so(na, np, becsum_nc, becsum):
    """
    add_becsum_so(na, np, becsum_nc, becsum)
    
    
    Defined at sum_band.fpp lines 1120-1189
    
    Parameters
    ----------
    na : int
    np : int
    becsum_nc : complex array
    becsum : float array
    
    ----------------------------------------------------------------------------
     This routine multiplies \(\text{becsum_nc}\) by the identity and the Pauli
     matrices, rotates it as appropriate for the spin-orbit case, saves it in
     \(\text{becsum}\) for the calculation of augmentation charge and magnetization.
    """
    libqepy_pw.f90wrap_add_becsum_so(na=na, np=np, becsum_nc=becsum_nc, \
        becsum=becsum)

def v_of_rho(self, rho_core, rhog_core, etotefield, v):
    """
    ehart, etxc, vtxc, eth, charge = v_of_rho(self, rho_core, rhog_core, etotefield, \
        v)
    
    
    Defined at v_of_rho.fpp lines 14-151
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etotefield : float
    v : Scf_Type
    
    Returns
    -------
    ehart : float
    etxc : float
    vtxc : float
    eth : float
    charge : float
    
    ----------------------------------------------------------------------------
     This routine computes the Hartree and Exchange and Correlation
     potential and energies which corresponds to a given charge density
     The XC potential is computed in real space, while the
     Hartree potential is computed in reciprocal space.
    """
    ehart, etxc, vtxc, eth, charge = libqepy_pw.f90wrap_v_of_rho(rho=self._handle, \
        rho_core=rho_core, rhog_core=rhog_core, etotefield=etotefield, v=v._handle)
    return ehart, etxc, vtxc, eth, charge

def v_xc_meta(self, rho_core, rhog_core, etxc, vtxc, v, kedtaur):
    """
    v_xc_meta(self, rho_core, rhog_core, etxc, vtxc, v, kedtaur)
    
    
    Defined at v_of_rho.fpp lines 156-402
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etxc : float
    vtxc : float
    v : float array
    kedtaur : float array
    
    ----------------------------------------------------------------------------
     Exchange-Correlation potential(meta) Vxc(r) from n(r)
    """
    libqepy_pw.f90wrap_v_xc_meta(rho=self._handle, rho_core=rho_core, \
        rhog_core=rhog_core, etxc=etxc, vtxc=vtxc, v=v, kedtaur=kedtaur)

def v_xc(self, rho_core, rhog_core, v):
    """
    etxc, vtxc = v_xc(self, rho_core, rhog_core, v)
    
    
    Defined at v_of_rho.fpp lines 406-591
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    v : float array
    
    Returns
    -------
    etxc : float
    vtxc : float
    
    ----------------------------------------------------------------------------
     Exchange-Correlation potential from charge density.
    """
    etxc, vtxc = libqepy_pw.f90wrap_v_xc(rho=self._handle, rho_core=rho_core, \
        rhog_core=rhog_core, v=v)
    return etxc, vtxc

def v_h(rhog, v):
    """
    ehart, charge = v_h(rhog, v)
    
    
    Defined at v_of_rho.fpp lines 595-735
    
    Parameters
    ----------
    rhog : complex array
    v : float array
    
    Returns
    -------
    ehart : float
    charge : float
    
    ----------------------------------------------------------------------------
     Hartree potential VH(r) from n(G)
    """
    ehart, charge = libqepy_pw.f90wrap_v_h(rhog=rhog, v=v)
    return ehart, charge

def v_h_without_esm(rhog, v):
    """
    ehart, charge = v_h_without_esm(rhog, v)
    
    
    Defined at v_of_rho.fpp lines 739-764
    
    Parameters
    ----------
    rhog : complex array
    v : float array
    
    Returns
    -------
    ehart : float
    charge : float
    
    ----------------------------------------------------------------------------
     ... Hartree potential VH(r) from n(G), with do_comp_esm = .FALSE.
    """
    ehart, charge = libqepy_pw.f90wrap_v_h_without_esm(rhog=rhog, v=v)
    return ehart, charge

def v_hubbard(ns, v_hub):
    """
    eth = v_hubbard(ns, v_hub)
    
    
    Defined at v_of_rho.fpp lines 768-860
    
    Parameters
    ----------
    ns : float array
    v_hub : float array
    
    Returns
    -------
    eth : float
    
    ---------------------------------------------------------------------
     Computes Hubbard potential and Hubbard energy.
     DFT+U: Simplified rotationally-invariant formulation by
     Dudarev et al., Phys. Rev. B 57, 1505(1998).
     DFT+U+J0: B. Himmetoglu et al., Phys. Rev. B 84, 115108(2011).
    """
    eth = libqepy_pw.f90wrap_v_hubbard(ns=ns, v_hub=v_hub)
    return eth

def v_hubbard_b(ns, v_hub):
    """
    eth = v_hubbard_b(ns, v_hub)
    
    
    Defined at v_of_rho.fpp lines 864-940
    
    Parameters
    ----------
    ns : float array
    v_hub : float array
    
    Returns
    -------
    eth : float
    
    -------------------------------------------------------------------------
     Computes Hubbard potential and Hubbard energy for background states.
     DFT+U: Simplified rotationally-invariant formulation by
     Dudarev et al., Phys. Rev. B 57, 1505(1998).
    """
    eth = libqepy_pw.f90wrap_v_hubbard_b(ns=ns, v_hub=v_hub)
    return eth

def v_hubbard_full(ns, v_hub):
    """
    eth = v_hubbard_full(ns, v_hub)
    
    
    Defined at v_of_rho.fpp lines 944-1076
    
    Parameters
    ----------
    ns : float array
    v_hub : float array
    
    Returns
    -------
    eth : float
    
    ---------------------------------------------------------------------
     Computes Hubbard potential and Hubbard energy.
     DFT+U(+J) : Formulation by Liechtenstein et al., Phys. Rev. B 52, R5467(1995).
    """
    eth = libqepy_pw.f90wrap_v_hubbard_full(ns=ns, v_hub=v_hub)
    return eth

def v_hubbard_full_nc(ns, v_hub, eth):
    """
    v_hubbard_full_nc(ns, v_hub, eth)
    
    
    Defined at v_of_rho.fpp lines 1080-1266
    
    Parameters
    ----------
    ns : complex array
    v_hub : complex array
    eth : float
    
    -------------------------------------------------------------
     Computes Hubbard potential and Hubbard energy(noncollinear case).
     DFT+U(+J) : Formulation by Liechtenstein et al., Phys. Rev. B 52, R5467(1995).
    """
    libqepy_pw.f90wrap_v_hubbard_full_nc(ns=ns, v_hub=v_hub, eth=eth)

def v_hubbard_extended(nsg, v_hub):
    """
    eth = v_hubbard_extended(nsg, v_hub)
    
    
    Defined at v_of_rho.fpp lines 1270-1442
    
    Parameters
    ----------
    nsg : complex array
    v_hub : complex array
    
    Returns
    -------
    eth : float
    
    -----------------------------------------------------------------------------------
     Computes extended Hubbard potential and Hubbard energy.
     DFT+U+V: Simplified rotationally-invariant formulation by
     V.L. Campo Jr and M. Cococcioni, J. Phys.: Condens. Matter 22, 055602(2010).
    """
    eth = libqepy_pw.f90wrap_v_hubbard_extended(nsg=nsg, v_hub=v_hub)
    return eth

def v_h_of_rho_r(rhor, v):
    """
    ehart, charge = v_h_of_rho_r(rhor, v)
    
    
    Defined at v_of_rho.fpp lines 1446-1490
    
    Parameters
    ----------
    rhor : float array
    v : float array
    
    Returns
    -------
    ehart : float
    charge : float
    
    ----------------------------------------------------------------------------
     Hartree potential VH(r) from a density in R space n(r)
    """
    ehart, charge = libqepy_pw.f90wrap_v_h_of_rho_r(rhor=rhor, v=v)
    return ehart, charge

def gradv_h_of_rho_r(rho, gradv):
    """
    gradv_h_of_rho_r(rho, gradv)
    
    
    Defined at v_of_rho.fpp lines 1493-1582
    
    Parameters
    ----------
    rho : float array
    gradv : float array
    
    ----------------------------------------------------------------------------
     Gradient of Hartree potential in R space from a total
    (spinless) density in R space n(r)
    """
    libqepy_pw.f90wrap_gradv_h_of_rho_r(rho=rho, gradv=gradv)

def symmetrize_at(nsym, s, invs, ft, irt, nat, tau, at, bg, alat, omega):
    """
    symmetrize_at(nsym, s, invs, ft, irt, nat, tau, at, bg, alat, omega)
    
    
    Defined at symmetrize_at.fpp lines 13-130
    
    Parameters
    ----------
    nsym : int
    s : int array
    invs : int array
    ft : float array
    irt : int array
    nat : int
    tau : float array
    at : float array
    bg : float array
    alat : float
    omega : float
    
    -------------------------------------------------------------------------------
     Forces atomic coordinates to have the symmetry of a given point group.
    """
    libqepy_pw.f90wrap_symmetrize_at(nsym=nsym, s=s, invs=invs, ft=ft, irt=irt, \
        nat=nat, tau=tau, at=at, bg=bg, alat=alat, omega=omega)

def qepy_delta_e(vr):
    """
    qepy_delta_e = qepy_delta_e(vr)
    
    
    Defined at qepy_delta_e.fpp lines 14-165
    
    Parameters
    ----------
    vr : float array
    
    Returns
    -------
    qepy_delta_e : float
    
    -----------------------------------------------------------------------
     This function computes delta_e, where:
     ... delta_e =  - \int rho%of_r(r)  v%of_r(r)
                    - \int rho%kin_r(r) v%kin_r(r) [for Meta-GGA]
                    - \sum rho%ns       v%ns       [for DFT+Hubbard]
                    - \sum becsum       D1_Hxc     [for PAW]
    """
    qepy_delta_e = libqepy_pw.f90wrap_qepy_delta_e(vr=vr)
    return qepy_delta_e

def qepy_electrons():
    """
    qepy_electrons()
    
    
    Defined at qepy_electrons.fpp lines 18-392
    
    
    ----------------------------------------------------------------------------
     General self-consistency loop, also for hybrid functionals.
     For non-hybrid functionals it just calls \(\texttt{electron_scf}\).
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%  Iterate hybrid functional  %%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    libqepy_pw.f90wrap_qepy_electrons()

def qepy_electrons_scf(printout, exxen):
    """
    qepy_electrons_scf(printout, exxen)
    
    
    Defined at qepy_electrons.fpp lines 396-1831
    
    Parameters
    ----------
    printout : int
    exxen : float
    
    ----------------------------------------------------------------------------
     This routine is a driver of the self-consistent cycle.
     It uses the routine \(\texttt{c_bands}\) for computing the bands at fixed
     Hamiltonian, the routine \(\texttt{sum_band}\) to compute the charge density,
     the routine \(\texttt{v_of_rho}\) to compute the new potential and the routine
     \(\text{mix_rho}\) to mix input and output charge densities.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%          iterate
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    libqepy_pw.f90wrap_qepy_electrons_scf(printout=printout, exxen=exxen)

def qepy_forces(icalc=None):
    """
    qepy_forces([icalc])
    
    
    Defined at qepy_forces.fpp lines 13-527
    
    Parameters
    ----------
    icalc : int
    
    ----------------------------------------------------------------------------
     This routine is a driver routine which computes the forces
     acting on the atoms. The complete expression of the forces
     contains many parts which are computed by different routines:
     - force_lc: local potential contribution
     - force_us: non-local potential contribution
     - (esm_)force_ew: (ESM) electrostatic ewald term
     - force_cc: nonlinear core correction contribution
     - force_corr: correction term for incomplete self-consistency
     - force_hub: contribution due to the Hubbard term;
     - force_london: Grimme DFT+D dispersion forces
     - force_d3: Grimme-D3(DFT-D3) dispersion forces
     - force_xdm: XDM dispersion forces
     - more terms from external electric fields, Martyna-Tuckerman, etc.
     - force_sol: contribution due to 3D-RISM
    """
    libqepy_pw.f90wrap_qepy_forces(icalc=icalc)

def qepy_hinit1():
    """
    qepy_hinit1()
    
    
    Defined at qepy_hinit1.fpp lines 13-116
    
    
    ----------------------------------------------------------------------------
     Atomic configuration dependent hamiltonian initialization,
     potential, wavefunctions for Hubbard U.
     Important note: it does not recompute structure factors and core charge,
     they must be computed before this routine is called.
    """
    libqepy_pw.f90wrap_qepy_hinit1()

def qepy_calc_energies():
    """
    qepy_calc_energies()
    
    
    Defined at qepy_pw2casino_write.fpp lines 302-848
    
    
    """
    libqepy_pw.f90wrap_qepy_calc_energies()

def qepy_pwscf(infile, my_world_comm=None, embed=None):
    """
    qepy_pwscf(infile[, my_world_comm, embed])
    
    
    Defined at qepy_pwscf.fpp lines 13-81
    
    Parameters
    ----------
    infile : str
    my_world_comm : int
    embed : Embed_Base
    
    """
    libqepy_pw.f90wrap_qepy_pwscf(infile=infile, my_world_comm=my_world_comm, \
        embed=None if embed is None else embed._handle)

def qepy_pwscf_finalise():
    """
    qepy_pwscf_finalise()
    
    
    Defined at qepy_pwscf.fpp lines 83-88
    
    
    """
    libqepy_pw.f90wrap_qepy_pwscf_finalise()

def qepy_initial(self=None, embed=None):
    """
    qepy_initial([self, embed])
    
    
    Defined at qepy_pwscf.fpp lines 90-132
    
    Parameters
    ----------
    input : Input_Base
    embed : Embed_Base
    
    """
    libqepy_pw.f90wrap_qepy_initial(input=None if self is None else self._handle, \
        embed=None if embed is None else embed._handle)

def qepy_finalise_end(self=None):
    """
    qepy_finalise_end([self])
    
    
    Defined at qepy_pwscf.fpp lines 134-146
    
    Parameters
    ----------
    input : Input_Base
    
    """
    libqepy_pw.f90wrap_qepy_finalise_end(input=None if self is None else \
        self._handle)

def qepy_run_pwscf():
    """
    exit_status = qepy_run_pwscf()
    
    
    Defined at qepy_run_pwscf.fpp lines 13-371
    
    
    Returns
    -------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Author: Paolo Giannozzi
     License: GNU
     Summary: Run an instance of the Plane Wave Self-Consistent Field code
     Run an instance of the Plane Wave Self-Consistent Field code
     MPI initialization and input data reading is performed in the
     calling code - returns in exit_status the exit code for pw.x,
     returned in the shell. Values are:
     * 0: completed successfully
     * 1: an error has occurred(value returned by the errore() routine)
     * 2-127: convergence error
        * 2: scf convergence error
        * 3: ion convergence error
     * 128-255: code exited due to specific trigger
        * 255: exit due to user request, or signal trapped,
              or time > max_seconds
    (note: in the future, check_stop_now could also return a value
         to specify the reason of exiting, and the value could be used
         to return a different value for different reasons)
     @Note
     10/01/17 Samuel Ponce: Add Ford documentation
     @endnote
    """
    exit_status = libqepy_pw.f90wrap_qepy_run_pwscf()
    return exit_status

def qepy_setlocal():
    """
    qepy_setlocal()
    
    
    Defined at qepy_setlocal.fpp lines 18-153
    
    
    ----------------------------------------------------------------------
     This routine computes the local potential in real space vltot(ir).
    """
    libqepy_pw.f90wrap_qepy_setlocal()

def qepy_stop_run(exit_status, print_flag=None, what=None, finalize=None):
    """
    qepy_stop_run(exit_status[, print_flag, what, finalize])
    
    
    Defined at qepy_stop_run.fpp lines 13-148
    
    Parameters
    ----------
    exit_status : int
    print_flag : int
    what : str
    finalize : bool
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping:
     * exit_status = 0: successfull execution, remove temporary files;
     * exit_status =-1: code stopped by user request;
     * exit_status = 1: convergence not achieved.
     Do not remove temporary files needed for restart.
    qepy -->
     Also add some from pwscf and run_pwscf
     Merge and modify the mp_global.mp_global_end
    qepy <--
    """
    libqepy_pw.f90wrap_qepy_stop_run(exit_status=exit_status, print_flag=print_flag, \
        what=what, finalize=finalize)

def qepy_stress(sigma, icalc=None):
    """
    qepy_stress(sigma[, icalc])
    
    
    Defined at qepy_stress.fpp lines 14-295
    
    Parameters
    ----------
    sigma : float array
    icalc : int
    
    ----------------------------------------------------------------------
     Computes the total stress.
    """
    libqepy_pw.f90wrap_qepy_stress(sigma=sigma, icalc=icalc)

def qepy_v_of_rho(self, rho_core, rhog_core, etotefield, v):
    """
    ehart, etxc, vtxc, eth, charge = qepy_v_of_rho(self, rho_core, rhog_core, \
        etotefield, v)
    
    
    Defined at qepy_v_of_rho.fpp lines 14-162
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etotefield : float
    v : Scf_Type
    
    Returns
    -------
    ehart : float
    etxc : float
    vtxc : float
    eth : float
    charge : float
    
    ----------------------------------------------------------------------------
     This routine computes the Hartree and Exchange and Correlation
     potential and energies which corresponds to a given charge density
     The XC potential is computed in real space, while the
     Hartree potential is computed in reciprocal space.
    """
    ehart, etxc, vtxc, eth, charge = \
        libqepy_pw.f90wrap_qepy_v_of_rho(rho=self._handle, rho_core=rho_core, \
        rhog_core=rhog_core, etotefield=etotefield, v=v._handle)
    return ehart, etxc, vtxc, eth, charge

def qepy_v_of_rho_all(self, rho_core, rhog_core, etotefield, v):
    """
    ehart, etxc, vtxc, eth, charge = qepy_v_of_rho_all(self, rho_core, rhog_core, \
        etotefield, v)
    
    
    Defined at qepy_v_of_rho_all.fpp lines 14-124
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etotefield : float
    v : Scf_Type
    
    Returns
    -------
    ehart : float
    etxc : float
    vtxc : float
    eth : float
    charge : float
    
    ----------------------------------------------------------------------------
     This routine computes the Hartree and Exchange and Correlation
     potential and energies which corresponds to a given charge density
     The XC potential is computed in real space, while the
     Hartree potential is computed in reciprocal space.
    """
    ehart, etxc, vtxc, eth, charge = \
        libqepy_pw.f90wrap_qepy_v_of_rho_all(rho=self._handle, rho_core=rho_core, \
        rhog_core=rhog_core, etotefield=etotefield, v=v._handle)
    return ehart, etxc, vtxc, eth, charge

def aceinit0():
    """
    aceinit0()
    
    
    Defined at wfcinit.fpp lines 14-69
    
    
    ----------------------------------------------------------------------------
     ... This routine reads the ACE potential from files in non-scf calculations
    """
    libqepy_pw.f90wrap_aceinit0()

def wfcinit():
    """
    wfcinit()
    
    
    Defined at wfcinit.fpp lines 73-274
    
    
    ----------------------------------------------------------------------------
     ... This routine computes an estimate of the starting wavefunctions
     ... from superposition of atomic wavefunctions and/or random wavefunctions.
     ... It also open needed files or memory buffers
    """
    libqepy_pw.f90wrap_wfcinit()

def init_wfc(ik):
    """
    init_wfc(ik)
    
    
    Defined at wfcinit.fpp lines 278-442
    
    Parameters
    ----------
    ik : int
    
    ----------------------------------------------------------------------------
     ... This routine computes starting wavefunctions for k-point ik
    """
    libqepy_pw.f90wrap_init_wfc(ik=ik)

def setup():
    """
    setup()
    
    
    Defined at setup.fpp lines 14-692
    
    
    ----------------------------------------------------------------------------
     This routine is called once at the beginning of the calculation and:
     1) determines various parameters of the calculation:
      * zv:        charge of each atomic type;
      * nelec:     total number of electrons(if not given in input);
      * nbnd:      total number of bands(if not given in input);
      * nbndx:     max number of bands used in iterative diagonalization;
      * tpiba:     2 pi / a(a = lattice parameter);
      * tpiba2:    square of tpiba;
      * gcutm:     cut-off in g space for charge/potentials;
      * gcutms:    cut-off in g space for smooth charge;
      * ethr:      convergence threshold for iterative diagonalization;
     2) finds actual crystal symmetry:
      * s:         symmetry matrices in the direct lattice vectors basis;
      * nsym:      number of crystal symmetry operations;
      * nrot:      number of lattice symmetry operations;
      * ft:        fractionary translations;
      * irt:       for each atom gives the corresponding symmetric;
      * invsym:    if true the system has inversion symmetry;
     3) generates k-points corresponding to the actual crystal symmetry;
     4) calculates various quantities used in magnetic, spin-orbit, PAW
        electric-field, DFT+U(+V) calculations
    """
    libqepy_pw.f90wrap_setup()

def setup_para(nr3, nkstot, nbnd):
    """
    setup_para(nr3, nkstot, nbnd)
    
    
    Defined at setup.fpp lines 696-817
    
    Parameters
    ----------
    nr3 : int
    nkstot : int
    nbnd : int
    
    ----------------------------------------------------------------------------
     Initialize the various parallelization levels, trying to guess decent
     parameters for npool, ndiag, ntg, if not specified in the command line
     Must be called at the end of "setup" but before "setup_exx",
     only once per run
    """
    libqepy_pw.f90wrap_setup_para(nr3=nr3, nkstot=nkstot, nbnd=nbnd)

def check_gpu_support():
    """
    check_gpu_support = check_gpu_support()
    
    
    Defined at setup.fpp lines 821-826
    
    
    Returns
    -------
    check_gpu_support : bool
    
    """
    check_gpu_support = libqepy_pw.f90wrap_check_gpu_support()
    return check_gpu_support

def setup_exx():
    """
    setup_exx()
    
    
    Defined at setup.fpp lines 830-845
    
    
    ----------------------------------------------------------------------------
     Must be called after setup_para, before init_run, only once
    """
    libqepy_pw.f90wrap_setup_exx()

def read_file():
    """
    read_file()
    
    
    Defined at read_file_new.fpp lines 13-67
    
    
    ----------------------------------------------------------------------------
     Wrapper routine, for backwards compatibility: reads the xml file,
     then reads the wavefunctions in "collected" format and writes them
     into "distributed" format, forcing write to file(not to buffer).
     NOT TO BE USED IN NEW CODE. Use "read_file_new" instead.
    """
    libqepy_pw.f90wrap_read_file()

def read_file_ph(needwf_ph):
    """
    read_file_ph(needwf_ph)
    
    
    Defined at read_file_new.fpp lines 71-165
    
    Parameters
    ----------
    needwf_ph : bool
    
    ----------------------------------------------------------------------------
     Wrapper routine, for compatibility with the phonon code: as "read_file",
     but pool parallelization is done just after the reading of the xml file,
     before reading the wavefunction files. To be used ONLY for codes that
     can split processors into pools at run-time depending upon the number
     of k-points(unless the number of pools is explicitly specified)
    """
    libqepy_pw.f90wrap_read_file_ph(needwf_ph=needwf_ph)

def read_file_new(needwf):
    """
    read_file_new(needwf)
    
    
    Defined at read_file_new.fpp lines 169-231
    
    Parameters
    ----------
    needwf : bool
    
    ----------------------------------------------------------------------------
     Reads xml data file produced by pw.x or cp.x;
     performs initializations related to the contents of the xml file;
     if needwf=.t. performs wavefunction-related initialization as well.
     Does not actually read wfcs. Returns in "needwf" info on the wfc file
    """
    libqepy_pw.f90wrap_read_file_new(needwf=needwf)

def post_xml_init():
    """
    post_xml_init()
    
    
    Defined at read_file_new.fpp lines 234-488
    
    
    ----------------------------------------------------------------------------
     ... Various initializations needed to start a calculation:
     ... pseudopotentials, G vectors, FFT arrays, rho, potential
    """
    libqepy_pw.f90wrap_post_xml_init()

def potinit():
    """
    potinit()
    
    
    Defined at potinit.fpp lines 14-303
    
    
    ----------------------------------------------------------------------------
     ... This routine initializes the self consistent potential in the array
     ... vr. There are three possible cases:
     ... a) the code is restarting from a broken run:
     ...    read rho from data stored during the previous run
     ... b) the code is performing a non-scf calculation following a scf one:
     ...    read rho from the file produced by the scf calculation
     ... c) the code starts a new calculation:
     ...    calculate rho as a sum of atomic charges
     ... In all cases the scf potential is recalculated and saved in vr
    """
    libqepy_pw.f90wrap_potinit()

def nc_magnetization_from_lsda(ngm, nspin, rho):
    """
    nc_magnetization_from_lsda(ngm, nspin, rho)
    
    
    Defined at potinit.fpp lines 307-337
    
    Parameters
    ----------
    ngm : int
    nspin : int
    rho : complex array
    
    -------------
    """
    libqepy_pw.f90wrap_nc_magnetization_from_lsda(ngm=ngm, nspin=nspin, rho=rho)

def pwscf():
    """
    pwscf()
    
    
    Defined at pwscf.fpp lines 13-107
    
    
    """
    libqepy_pw.f90wrap_pwscf()


basis = qepy_pw.basis
lsda_mod = qepy_pw.lsda_mod
symm_base = qepy_pw.symm_base
klist = qepy_pw.klist
qepy_mod = qepy_pw.qepy_mod
fft_types = qepy_pw.fft_types
pw_interfaces = qepy_pw.pw_interfaces
relax = qepy_pw.relax
scf = qepy_pw.scf
pw_restart_new = qepy_pw.pw_restart_new
fixed_occ = qepy_pw.fixed_occ
rap_point_group_so = qepy_pw.rap_point_group_so
rap_point_group = qepy_pw.rap_point_group
pwcom = qepy_pw.pwcom
qepy_common = qepy_pw.qepy_common
force_mod = qepy_pw.force_mod
vlocal = qepy_pw.vlocal
ener = qepy_pw.ener
symme = qepy_pw.symme
wvfct = qepy_pw.wvfct
rap_point_group_is = qepy_pw.rap_point_group_is
extrapolation = qepy_pw.extrapolation
cellmd = qepy_pw.cellmd
