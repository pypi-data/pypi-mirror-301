from __future__ import print_function, absolute_import, division
pname = 'libqepy_phonon_ph'

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
import libqepy_phonon_ph
import f90wrap.runtime
import logging
import numpy
import qepy_phonon_ph.alpha2f_vals
import qepy_phonon_ph.ifconstants
import qepy_phonon_ph.alpha2f_routines

def alpha2f():
    """
    alpha2f()
    
    
    Defined at alpha2f.fpp lines 373-413
    
    
    ------------------------------------------------------------------------------
     This routine reads lambda*.dat and compute a^2F, phonon DOS, lambda,
     & omega_ln.
    """
    libqepy_phonon_ph.f90wrap_alpha2f()

def dvscf_q2r():
    """
    dvscf_q2r()
    
    
    Defined at dvscf_q2r.fpp lines 13-1222
    
    
    ------------------------------------------------------------------------------
     dvscf_q2r.x
        Fourier transform the dvscf computed at coarse q points to real space.
        Originally proposed by [1]. For charge neutrality correction see [2].
        Dipole long-range part described in [3].
        Quadrupole long-range part described in [4] (not implemented here).
        Author: Jae-Mo Lihm
     Input data: Namelist "input"
        prefix  : Prepended to input/output filenames; must be the same used
                  in the calculation of the phonon code.
    (character, Default: 'pwscf')
        outdir  : Directory containing input, output, and scratch files; must
                  be the same as specified in the calculation of ph.x.
    (character, Default: value of the ESPRESSO_TMPDIR environment
                   variable if set; current directory('./') otherwise)
        fildyn  : File where the dynamical matrix is written. Normally, this
                  should be the same as specified on the input to ph.x.
                  Only "fildyn"0 is used here.
    (character, Must be specified)
        fildvscf : File where the potential variation is written. This should be
                   the same as specified on the input to ph.x.
    (character, Default: 'dvscf')
        wpot_dir : Directory where the w_pot binary files are written. Real space
                   potential files are stored in wpot_dir with names
                   prefix.wpot.irc$irc//"1".
    (character, Default: outdir // 'w_pot/')
        do_long_range : If .true., subtract the long-range part of the potential
                        before interpolation. Requires epsilon and Born effective
                        charge data in _ph0/prefix.phsave/tensor.xml.
    (logical, Default: .false.)
        do_charge_neutral : If .true., renormalize phonon potential to impose
                        neutrality of Born effective charges. See [2] for
                        details. Both the Hartree and exchange-correlation
                        parts are renormalized, while in [2] only the
                        Hartree part is renormalized.
    (logical, Default: .false.)
        verbosity : If 'high', write more information to stdout. Used by the
                    test-suite.
    (character, Default: 'default'. Only 'high' is allowed.)
     [1] A. Eiguren and C. Ambrosch-Draxl, PRB 78, 045124(2008)
     [2] S. Ponce et al, J. Chem. Phys. 143, 102813(2015)
     [3] Xavier Gonze et al, Comput. Phys. Commun. 248 107042(2020)
     [4] Guillaume Brunin et al, arXiv:2002.00628(2020)
     Not implemented for the following cases:
        - PAW
        - DFPT+U
        - magnetism(both collinear and noncollinear magnetism)
        - 2d Coulomb cutoff
     dvscf = dvscf_ind + dvscf_bare(All are lattice periodic.)
     dvscf_ind: computed in the ph.x run, read from files.
     dvscf_bare: computed on the fly by subroutine calc_dvscf_bare.
     All potentials are computed in the Cartesian basis of atomic displacements.
     * Charge neutrality correction
     If the sum of Born effective charge zeu is not zero, the potential has
     has non-physical divergence around q = Gamma. To correct this problem,
     renormalize the Hartree term by a q-dependent constant factor.
     Since the dvscf file contains the sum of Hartree and xc contribution,
     we renormalize the xc term as well as the Hartree term.
     To renormalize only the Hartree term, one need to read drho and
     compute the corresponding dvscf.
     dvscf_ind_ren(q,iat,idir) = dvscf_ind(q,iat,idir) * coeff
     coeff = ( Z*q_idir - sum_jdir(Z* - Z*avg)_{idir,jdir} * q_jdir / epsil_q )
           / ( Z*q_idir - sum_jdir(Z*)_{idir,jdir} * q_jdir / epsil_q )
     epsil_q = 1/q^2 * (q.T * epsil * q): dielectric constant
     Z = upf(nt)%zp: bare valence charge of the atom iat
     Z*(:,:) = zeu(:,:,iat): Born effective charge. Read from fildyn
     Z*avg(:,:) = 1 / nat * sum_jatm zeu(:,:,jatm): average zeu
     * Long-range part correction
     dvlong: long-range part. Subtracted for smooth Fourier interpolation.
     Taken from Eq.(13) of Ref. [3]
     dvlong(G,q)_{a,x} = 1j * 4pi / Omega
                       * [ (q+G)_y * Zstar_{a,yx} * exp(-i*(q+G)*tau_a)) ]
                       / [ (q+G)_y * epsilon_yz * (q+G)_z ]
      a: atom index, x, y: Cartesian direction index
     w_pot(r,R) = 1/N_q * sum_q exp(-iqR) exp(iqr) (dvscf(r,q) - dvlong(r,q))
     w_pot are computed and written to file.
     Later, dvtot at fine q points can be computed as
     dvscf(r,q) = exp(-iqr) (dvlong(r,q) + sum_R exp(iqR) w_pot(r,R))
     Only the dipole(Frohlich) potential is considered. The quadrupole
     potential [4] is not implemented.
     * Parallelization
     We use PW and pool parallelization.
     Here, the pool parallelization is for the q points, not for the k points.
    ------------------------------------------------------------------------------
    """
    libqepy_phonon_ph.f90wrap_dvscf_q2r()

def dynmat():
    """
    dynmat()
    
    
    Defined at dynmat.fpp lines 13-269
    
    
    --------------------------------------------------------------------
     This program:
     * reads a dynamical matrix file produced by the phonon code;
     * adds the nonanalytical part(if Z* and epsilon are read from file),
       applies the chosen Acoustic Sum Rule(if q=0);
     * diagonalise the dynamical matrix;
     * calculates IR and Raman cross sections(if Z* and Raman tensors
       are read from file, respectively);
     * writes the results to files, both for inspection and for plotting.
     Input data(namelist "input"):
     * \(\text{fildyn} [character]: input file containing the dynamical matrix
    (default: fildyn='matdyn')
     * \(q(3)) - [real]: calculate LO modes(add nonanalytic terms) along
       the direction q(cartesian axis, default: q=(0,0,0) )
     * \(\text{amass}(\text{nt})\) - [real]: mass for atom type nt, amu
    (default: amass is read from file fildyn)
     * \(\text{asr}\) - [character]: indicates the type of Acoustic Sum Rule imposed:
        * 'no': no Acoustic Sum Rules imposed(default)
        * 'simple':  previous implementation of the asr used
    (3 translational asr imposed by correction of
          the diagonal elements of the dynamical matrix)
        * 'crystal': 3 translational asr imposed by optimized
          correction of the dyn. matrix(projection).
        * 'one-dim': 3 translational asr + 1 rotational asr
          imposed by optimized correction of the dyn. mat. (the
          rotation axis is the direction of periodicity; it
          will work only if this axis considered is one of
          the cartesian axis).
        * 'zero-dim': 3 translational asr + 3 rotational asr
          imposed by optimized correction of the dyn. mat.
          Note that in certain cases, not all the rotational asr
          can be applied(e.g. if there are only 2 atoms in a
          molecule or if all the atoms are aligned, etc.).
          In these cases the supplementary asr are cancelled
          during the orthonormalization procedure(see below).
          Finally, in all cases except 'no' a simple correction
          on the effective charges is performed(same as in the
          previous implementation).
     * \(\text{axis}\) - [integer]: indicates the rotation axis for a 1D system
    (1=Ox, 2=Oy, 3=Oz ; default =3)
     * \(\text{lperm}\) - [logical]: TRUE to calculate Gamma-point mode contributions \
         to
       dielectric permittivity tensor(default: lperm=.false.)
     * \(\text{lplasma}\) - [logical]: TRUE to calculate Gamma-point mode effective \
         plasma
       frequencies, automatically triggers lperm = TRUE
    (default: lplasma=.false.)
     * \(\text{filout} - [character]: output file containing phonon frequencies and \
         normalized
       phonon displacements(i.e. eigenvectors divided by the
       square root of the mass and then normalized; they are
       not orthogonal). Default: filout='dynmat.out'
     * \(\text{fileig}\) - [character]: output file containing phonon frequencies and \
         eigenvectors
       of the dynamical matrix(they are orthogonal). Default: fileig=' '
     * \(\text{filmol}\) - [character]: as above, in a format suitable for 'molden'
    (default: filmol='dynmat.mold')
     * \(\text{filxsf}\) - [character]: as above, in axsf format suitable for \
         xcrysden
    (default: filxsf='dynmat.axsf')
     * \(\text{loto_2d}\) - [logical]: set to TRUE to activate two-dimensional \
         treatment of
       LO-TO splitting.
    """
    libqepy_phonon_ph.f90wrap_dynmat()

def epa():
    """
    epa()
    
    
    Defined at epa.fpp lines 13-558
    
    
    ----------------------------------------------------------------------------
     \(\texttt{epa.x}\): reads electron-phonon coupling matrix elements produced
     by the phonon code with electron_phonon = 'epa', and makes a transformation
     from momentum to energy space according to electron-phonon averaged
    (EPA) approximation as described in:
     G. Samsonidze and B. Kozinsky, Adv. Energy Mater. 2018, 1800246
     doi:10.1002/aenm.201800246 arXiv:1511.08115
     For details on how to set up the energy grids please refer to
     online documentation at https://github.com/mir-group/EPA
    """
    libqepy_phonon_ph.f90wrap_epa()

def fqha():
    """
    fqha()
    
    
    Defined at fqha.fpp lines 13-91
    
    
    """
    libqepy_phonon_ph.f90wrap_fqha()

def elph():
    """
    elph()
    
    
    Defined at lambda.fpp lines 19-204
    
    
    -----------------------------------------------------------------------
    """
    libqepy_phonon_ph.f90wrap_elph()

def matdyn():
    """
    matdyn()
    
    
    Defined at matdyn.fpp lines 37-2972
    
    
    -----------------------------------------------------------------------
     This program calculates the phonon frequencies for a list of generic
     q vectors starting from the interatomic force constants generated
     from the dynamical matrices as written by DFPT phonon code through
     the companion program \(\texttt{q2r}\).
     \(\texttt{matdyn}\) can generate a supercell of the original cell for
     mass approximation calculation. If supercell data are not specified
     in input, the unit cell, lattice vectors, atom types and positions
     are read from the force constant file.
      Input cards: namelist &input
         flfrc     file produced by q2r containing force constants(needed)
                   It is the same as in the input of q2r.x(+ the .xml extension
                   if the dynamical matrices produced by ph.x were in xml
                   format). No default value: must be specified.
          asr(character) indicates the type of Acoustic Sum Rule imposed
                   - 'no': no Acoustic Sum Rules imposed(default)
                   - 'simple':  previous implementation of the asr used
    (3 translational asr imposed by correction of
                      the diagonal elements of the force constants matrix)
                   - 'crystal': 3 translational asr imposed by optimized
                      correction of the force constants(projection).
                   - 'all': 3 translational asr + 3 rotational asr + 15 Huang
                      conditions for vanishing stress tensor, imposed by
                      optimized correction of the force constants(projection).
                      Remember to set write_lr to .true. to write long-range
                      force constants into file when running q2r and set read_lr
                      to .true. when running matdyn for the case of polar system.
                   - 'one-dim': 3 translational asr + 1 rotational asr
                      imposed by optimized correction of the force constants
    (the rotation axis is the direction of periodicity;
                       it will work only if this axis considered is one of
                       the cartesian axis).
                   - 'zero-dim': 3 translational asr + 3 rotational asr
                      imposed by optimized correction of the force constants
                   Note that in certain cases, not all the rotational asr
                   can be applied(e.g. if there are only 2 atoms in a
                   molecule or if all the atoms are aligned, etc.).
                   In these cases the supplementary asr are cancelled
                   during the orthonormalization procedure(see below).
         huang     if .true. (default) Huang conditions for vanishing
                   stress tensor are included in asr='all'.
         dos       if .true. calculate phonon Density of States(DOS)
                   using tetrahedra and a uniform q-point grid(see below)
                   NB: may not work properly in noncubic materials
                   if .false. calculate phonon bands from the list of q-points
                   supplied in input(default)
         nk1,nk2,nk3  uniform q-point grid for DOS calculation(includes q=0)
    (must be specified if dos=.true., ignored otherwise)
         deltaE    energy step, in cm^(-1), for DOS calculation: from min
                   to max phonon energy(default: 1 cm^(-1) if ndos, see
                   below, is not specified)
         ndos      number of energy steps for DOS calculations
    (default: calculated from deltaE if not specified)
         degauss   DOS broadening(in cm^-1). Default 0 - meaning use tetrahedra
         fldos     output file for dos(default: 'matdyn.dos')
                   the dos is in states/cm(-1) plotted vs omega in cm(-1)
                   and is normalised to 3*nat, i.e. the number of phonons
         flfrq     output file for frequencies(default: 'matdyn.freq')
         flvec     output file for normalized phonon displacements
    (default: 'matdyn.modes'). The normalized phonon displacements
                   are the eigenvectors divided by the square root of the mass,
                   then normalized. As such they are not orthogonal.
         fleig     output file for phonon eigenvectors(default: 'matdyn.eig')
                   The phonon eigenvectors are the eigenvectors of the dynamical
                   matrix. They are orthogonal.
         fldyn output file for dynamical matrix(default: ' ' i.e. not written)
         at        supercell lattice vectors - must form a superlattice of the
                   original lattice(default: use original cell)
         l1,l2,l3  supercell lattice vectors are original cell vectors times
                   l1, l2, l3 respectively(default: 1, ignored if at specified)
         ntyp      number of atom types in the supercell(default: ntyp of the
                   original cell)
         amass     masses of atoms in the supercell(a.m.u.), one per atom type
    (default: use masses read from file flfrc)
         readtau   read  atomic positions of the supercell from input
    (used to specify different masses) (default: .false.)
         fltau     write atomic positions of the supercell to file "fltau"
    (default: fltau=' ', do not write)
         la2F      if .true. interpolates also the el-ph coefficients.
         q_in_band_form if .true. the q points are given in band form:
                   Only the first and last point of one or more lines
                   are given. See below. (default: .false.).
         q_in_cryst_coord if .true. input q points are in crystalline
                  coordinates(default: .false.)
         eigen_similarity: use similarity of the displacements to order
                           frequencies(default: .false.)
                    NB: You cannot use this option with the symmetry
                    analysis of the modes.
         fd(logical) if .t. the ifc come from the finite displacement calculation
         na_ifc(logical) add non analitic contributions to the interatomic force
                    constants if finite displacement method is used(as in Wang et al.
                    Phys. Rev. B 85, 224303(2012)) [to be used in conjunction with fd.x]
         nosym      if .true., no symmetry and no time reversal are imposed
         loto_2d set to .true. to activate two-dimensional treatment of LO-TO splitting.
         loto_disable(logical) if .true. do not apply LO-TO splitting for q=0
    (default: .false.)
         read_lr    set to .true. to read long-range force constants from file,
                    when enforcing asr='all' for polar solids in matdyn.
         write_frc  set to .true. to write force constants into file.
                    The filename would be flfrc+".matdyn".
      if(readtau) atom types and positions in the supercell follow:
    (tau(i,na),i=1,3), ityp(na)
      IF(q_in_band_form.and..not.dos) THEN
         nq
     number of q points
    (q(i,n),i=1,3), nptq   nptq is the number of points between this point
                                and the next. These points are automatically
                                generated. the q points are given in Cartesian
                                coordinates, 2pi/a units(a=lattice parameters)
      ELSE, if(.not.dos) :
         nq         number of q-points
    (q(i,n), i=1,3)    nq q-points in cartesian coordinates, 2pi/a units
      If q = 0, the direction qhat(q=>0) for the non-analytic part
      is extracted from the sequence of q-points as follows:
         qhat = q(n) - q(n-1)  or   qhat = q(n) - q(n+1)
      depending on which one is available and nonzero.
      For low-symmetry crystals, specify twice q = 0 in the list
      if you want to have q = 0 results for two different directions
    """
    libqepy_phonon_ph.f90wrap_matdyn()

def phonon():
    """
    phonon()
    
    
    Defined at phonon.fpp lines 13-105
    
    
    -----------------------------------------------------------------------
     This is the main driver of the phonon code.
     It reads all the quantities calculated by \(\texttt{pwscf}\), it
     checks if some recover file is present and determines which
     calculation needs to be done. Finally, it calls \(\texttt{do_phonon}\)
     that does the loop over the q points.
     Presently implemented:
     * dynamical matrix(\(q\neq 0\))   NC [4], US [4], PAW [4]
     * dynamical matrix(\(q=0\))       NC [5], US [5], PAW [4]
     * dielectric constant              NC [5], US [5], PAW [3]
     * Born effective charges           NC [5], US [5], PAW [3]
     * polarizability(iu)              NC [2], US [2]
     * electron-phonon                  NC [3], US [3]
     * electro-optic                    NC [1]
     * Raman tensor                     NC [1]
     NC = norm conserving pseudopotentials
     US = ultrasoft pseudopotentials
     PAW = projector augmented-wave
     [1] LDA,
     [2] [1] + GGA,
     [3] [2] + LSDA/sGGA,
     [4] [3] + Spin-orbit/nonmagnetic, non-local vdW functionals, DFT-D2
     [5] [4] + Spin-orbit/magnetic(experimental when available)
     Not implemented in \(\texttt{ph.x}\):
     [6] [5] + constraints on the magnetization
     [7] Tkatchenko-Scheffler, DFT-D3
     [8] Hybrid and meta-GGA functionals
     [9] External Electric field
     [10] nonperiodic boundary conditions.
    """
    libqepy_phonon_ph.f90wrap_phonon()

def postahc():
    """
    postahc()
    
    
    Defined at postahc.fpp lines 13-978
    
    
    ------------------------------------------------------------------------------
     This program
       - Reads the electron-phonon quantities calculated by ph.x with the
         electron_phonon='ahc' option.
       - Calculate the phonon-induced electron self-energy in the full matrix
         form at a given temperature.
     Input data(namelist "input") is described in Doc/INPUT_POSTAHC.
    ------------------------------------------------------------------------------
    """
    libqepy_phonon_ph.f90wrap_postahc()

def q2qstar():
    """
    q2qstar()
    
    
    Defined at q2qstar.fpp lines 14-242
    
    
    ----------------------------------------------------------------------------
     A small utility that reads the first q from a dynamical matrix file(either
     xml or plain text), recomputes the system symmetry(starting from the lattice)
     and generates the star of q.
     Useful for debugging and for producing the star of the wannier-phonon code \
         output.
     Syntax:
       \(\texttt{q2qstar.x}\) filein [fileout]
     fileout default: rot_filein(old format) or rot_filein.xml(new format)
    """
    libqepy_phonon_ph.f90wrap_q2qstar()

def q2r():
    """
    q2r()
    
    
    Defined at q2r.fpp lines 13-119
    
    
    ----------------------------------------------------------------------------
     Reads force constant matrices \(C(q)\) produced by the PHonon code
     for a grid of q-points, calculates the corresponding set of
     interatomic force constants(IFC), \(C(R)\).
     If a file "fildyn"0 is not found, the code will ignore the variable
     "fildyn" and will try to read from the following cards the missing
     information on the q-point grid and file names:
     - nr1,nr2,nr3: dimensions of the FFT grid formed by the q-point grid;
     - nfile: number of files containing \(C(q_n)\), \(n=1,\text{nfile}\);
     - followed by nfile cards: \(\text{filin}\).
     The name and order of files is not important as long as \(q=0\) is
     the first.
    """
    libqepy_phonon_ph.f90wrap_q2r()


alpha2f_vals = qepy_phonon_ph.alpha2f_vals
ifconstants = qepy_phonon_ph.ifconstants
alpha2f_routines = qepy_phonon_ph.alpha2f_routines
