from __future__ import print_function, absolute_import, division
pname = 'libqepy_pp'

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
import libqepy_pp
import f90wrap.runtime
import logging
import numpy
import qepy_pp.oscdft_pp_mod
import qepy_pp.projections_ldos
import qepy_pp.eps_writer
import qepy_pp.vasp_read_chgcar
import qepy_pp.fermi_proj_routines
import qepy_pp.grid_module
import qepy_pp.vdw_df_scale
import qepy_pp.paw_postproc
import qepy_pp.wannier
import qepy_pp.idwmod
import qepy_pp.adduscore
import qepy_pp.projections
import qepy_pp.fs
import qepy_pp.vasp_xml
import qepy_pp.fermisurfer_common
import qepy_pp.oscdft_et_mod
import qepy_pp.globalmod
import qepy_pp.read_proj
import qepy_pp.fouriermod
import qepy_pp.pp_module
import qepy_pp.chdens_module

def add_shift_cc(shift_cc):
    """
    add_shift_cc(shift_cc)
    
    
    Defined at add_shift_cc.fpp lines 14-108
    
    Parameters
    ----------
    shift_cc : float array
    
    ----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_add_shift_cc(shift_cc=shift_cc)

def add_shift_lc(nat, tau, ityp, alat, omega, ngm, ngl, igtongl, nrxx, g, rho, \
    nl, nspin, gstart, gamma_only, vloc, shift_lc):
    """
    add_shift_lc(nat, tau, ityp, alat, omega, ngm, ngl, igtongl, nrxx, g, rho, nl, \
        nspin, gstart, gamma_only, vloc, shift_lc)
    
    
    Defined at add_shift_lc.fpp lines 15-84
    
    Parameters
    ----------
    nat : int
    tau : float array
    ityp : int array
    alat : float
    omega : float
    ngm : int
    ngl : int
    igtongl : int array
    nrxx : int
    g : float array
    rho : float array
    nl : int array
    nspin : int
    gstart : int
    gamma_only : bool
    vloc : float array
    shift_lc : float array
    
    ----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_add_shift_lc(nat=nat, tau=tau, ityp=ityp, alat=alat, \
        omega=omega, ngm=ngm, ngl=ngl, igtongl=igtongl, nrxx=nrxx, g=g, rho=rho, \
        nl=nl, nspin=nspin, gstart=gstart, gamma_only=gamma_only, vloc=vloc, \
        shift_lc=shift_lc)

def add_shift_us(shift_nl):
    """
    add_shift_us(shift_nl)
    
    
    Defined at add_shift_us.fpp lines 14-222
    
    Parameters
    ----------
    shift_nl : float array
    
    ----------------------------------------------------------------------------
     ... nonlocal potential contribution to forces
     ... wrapper
    """
    libqepy_pp.f90wrap_add_shift_us(shift_nl=shift_nl)

def addusdens1d(plan, prho):
    """
    addusdens1d(plan, prho)
    
    
    Defined at addusdens1d.fpp lines 14-112
    
    Parameters
    ----------
    plan : float array
    prho : complex array
    
    ----------------------------------------------------------------------
      This routine adds to the charge density the part which is due to
      the US augmentation. This is done only along the G_z direction in
      reciprocal space. The output of the routine is the planar average
      of the charge density.
    """
    libqepy_pp.f90wrap_addusdens1d(plan=plan, prho=prho)

def atomic_wfc_nc_proj(ik, wfcatom):
    """
    atomic_wfc_nc_proj(ik, wfcatom)
    
    
    Defined at atomic_wfc_nc_proj.fpp lines 14-232
    
    Parameters
    ----------
    ik : int
    wfcatom : complex array
    
    -----------------------------------------------------------------------
     This routine computes the superposition of atomic wavefunctions
     for k-point "ik" - output in "wfcatom" - noncolinear case only
     If lspinorb=.TRUE. it makes linear combinations of eigenstates of
     the atomic total angular momenta j and j_z; otherwise, of eigenstates of
     the orbital angular momenta l, l_z and of s_z(the z-component of the spin).
    """
    libqepy_pp.f90wrap_atomic_wfc_nc_proj(ik=ik, wfcatom=wfcatom)

def bspline_interpolation(nptx, rg, rhor, rhoint, laue):
    """
    bspline_interpolation(nptx, rg, rhor, rhoint, laue)
    
    
    Defined at chdens_bspline.fpp lines 15-127
    
    Parameters
    ----------
    nptx : int
    rg : float array
    rhor : float array
    rhoint : float array
    laue : bool
    
    ---------------------------------------------------------------------
     Use B-spline interpolation instead of Fourier interpolation
    """
    libqepy_pp.f90wrap_bspline_interpolation(nptx=nptx, rg=rg, rhor=rhor, \
        rhoint=rhoint, laue=laue)

def plot_1d_bspline(nptx, m1, x0, e, rhor, alat, iflag, ounit, laue):
    """
    plot_1d_bspline(nptx, m1, x0, e, rhor, alat, iflag, ounit, laue)
    
    
    Defined at chdens_bspline.fpp lines 130-165
    
    Parameters
    ----------
    nptx : int
    m1 : float
    x0 : float array
    e : float array
    rhor : float array
    alat : float
    iflag : int
    ounit : int
    laue : bool
    
    ---------------------------------------------------------------------
     Use B-spline interpolation instead of Fourier
    """
    libqepy_pp.f90wrap_plot_1d_bspline(nptx=nptx, m1=m1, x0=x0, e=e, rhor=rhor, \
        alat=alat, iflag=iflag, ounit=ounit, laue=laue)

def plot_2d_bspline(nx, ny, m1, m2, x0, e1, e2, rhor, alat, at, nat, tau, atm, \
    ityp, output_format, ounit, laue):
    """
    plot_2d_bspline(nx, ny, m1, m2, x0, e1, e2, rhor, alat, at, nat, tau, atm, ityp, \
        output_format, ounit, laue)
    
    
    Defined at chdens_bspline.fpp lines 169-245
    
    Parameters
    ----------
    nx : int
    ny : int
    m1 : float
    m2 : float
    x0 : float array
    e1 : float array
    e2 : float array
    rhor : float array
    alat : float
    at : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    output_format : int
    ounit : int
    laue : bool
    
    -----------------------------------------------------------------------
     Use B-spline interpolation instead of Fourier
    """
    libqepy_pp.f90wrap_plot_2d_bspline(nx=nx, ny=ny, m1=m1, m2=m2, x0=x0, e1=e1, \
        e2=e2, rhor=rhor, alat=alat, at=at, nat=nat, tau=tau, atm=atm, ityp=ityp, \
        output_format=output_format, ounit=ounit, laue=laue)

def plot_3d_bspline(alat, at, nat, tau, atm, ityp, rhor, nx, ny, nz, m1, m2, m3, \
    x0, e1, e2, e3, output_format, ounit, laue):
    """
    plot_3d_bspline(alat, at, nat, tau, atm, ityp, rhor, nx, ny, nz, m1, m2, m3, x0, \
        e1, e2, e3, output_format, ounit, laue)
    
    
    Defined at chdens_bspline.fpp lines 249-295
    
    Parameters
    ----------
    alat : float
    at : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    rhor : float array
    nx : int
    ny : int
    nz : int
    m1 : float
    m2 : float
    m3 : float
    x0 : float array
    e1 : float array
    e2 : float array
    e3 : float array
    output_format : int
    ounit : int
    laue : bool
    
    -----------------------------------------------------------------------
     Use B-spline interpolation instead of Fourier
    """
    libqepy_pp.f90wrap_plot_3d_bspline(alat=alat, at=at, nat=nat, tau=tau, atm=atm, \
        ityp=ityp, rhor=rhor, nx=nx, ny=ny, nz=nz, m1=m1, m2=m2, m3=m3, x0=x0, \
        e1=e1, e2=e2, e3=e3, output_format=output_format, ounit=ounit, laue=laue)

def plot_sphere_bspline(nr, lebedev, m1, x0, rhor, alat, ounit, laue):
    """
    plot_sphere_bspline(nr, lebedev, m1, x0, rhor, alat, ounit, laue)
    
    
    Defined at chdens_bspline_sphere.fpp lines 15-195
    
    Parameters
    ----------
    nr : int
    lebedev : int
    m1 : float
    x0 : float array
    rhor : float array
    alat : float
    ounit : int
    laue : bool
    
    --------------------------------------------------------------------------
     ... Use B-spline interpolation instead of Fourier,
     ... and calculate spherical average with Lebedev Quadrature.
    """
    libqepy_pp.f90wrap_plot_sphere_bspline(nr=nr, lebedev=lebedev, m1=m1, x0=x0, \
        rhor=rhor, alat=alat, ounit=ounit, laue=laue)

def compute_ppsi(ppsi, ppsi_us, ik, ipol, nbnd_occ, current_spin):
    """
    compute_ppsi(ppsi, ppsi_us, ik, ipol, nbnd_occ, current_spin)
    
    
    Defined at compute_ppsi.fpp lines 14-154
    
    Parameters
    ----------
    ppsi : complex array
    ppsi_us : complex array
    ik : int
    ipol : int
    nbnd_occ : int
    current_spin : int
    
    ----------------------------------------------------------------------
     On output: ppsi contains P_c^+ p | psi_ik > for the ipol cartesian
                coordinate
                ppsi_us contains the additional term required for US PP.
                See J. Chem. Phys. 120, 9935(2004) Eq. 10.
    (important: vkb and evc must have been initialized for this k-point)
    """
    libqepy_pp.f90wrap_compute_ppsi(ppsi=ppsi, ppsi_us=ppsi_us, ik=ik, ipol=ipol, \
        nbnd_occ=nbnd_occ, current_spin=current_spin)

def compute_sigma_avg(sigma_avg, becp_nc, ik, lsigma):
    """
    compute_sigma_avg(sigma_avg, becp_nc, ik, lsigma)
    
    
    Defined at compute_sigma_avg.fpp lines 12-288
    
    Parameters
    ----------
    sigma_avg : float array
    becp_nc : complex array
    ik : int
    lsigma : bool array
    
    """
    libqepy_pp.f90wrap_compute_sigma_avg(sigma_avg=sigma_avg, becp_nc=becp_nc, \
        ik=ik, lsigma=lsigma)

def write_cubefile(alat, at, bg, nat, tau, atm, ityp, rho, nr1, nr2, nr3, nr1x, \
    nr2x, nr3x, ounit):
    """
    write_cubefile(alat, at, bg, nat, tau, atm, ityp, rho, nr1, nr2, nr3, nr1x, \
        nr2x, nr3x, ounit)
    
    
    Defined at cube.fpp lines 27-83
    
    Parameters
    ----------
    alat : float
    at : float array
    bg : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    rho : float array
    nr1 : int
    nr2 : int
    nr3 : int
    nr1x : int
    nr2x : int
    nr3x : int
    ounit : int
    
    """
    libqepy_pp.f90wrap_write_cubefile(alat=alat, at=at, bg=bg, nat=nat, tau=tau, \
        atm=atm, ityp=ityp, rho=rho, nr1=nr1, nr2=nr2, nr3=nr3, nr1x=nr1x, \
        nr2x=nr2x, nr3x=nr3x, ounit=ounit)

def write_cubefile_new(alat, nat, tau, atm, ityp, x0, m1, m2, m3, e1, e2, e3, \
    nx, ny, nz, carica, ounit):
    """
    write_cubefile_new(alat, nat, tau, atm, ityp, x0, m1, m2, m3, e1, e2, e3, nx, \
        ny, nz, carica, ounit)
    
    
    Defined at cube.fpp lines 90-155
    
    Parameters
    ----------
    alat : float
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    x0 : float array
    m1 : float
    m2 : float
    m3 : float
    e1 : float array
    e2 : float array
    e3 : float array
    nx : int
    ny : int
    nz : int
    carica : float array
    ounit : int
    
    """
    libqepy_pp.f90wrap_write_cubefile_new(alat=alat, nat=nat, tau=tau, atm=atm, \
        ityp=ityp, x0=x0, m1=m1, m2=m2, m3=m3, e1=e1, e2=e2, e3=e3, nx=nx, ny=ny, \
        nz=nz, carica=carica, ounit=ounit)

def bbox(r, bbmin, bbmax):
    """
    bbox(r, bbmin, bbmax)
    
    
    Defined at cube.fpp lines 157-166
    
    Parameters
    ----------
    r : float array
    bbmin : float array
    bbmax : float array
    
    """
    libqepy_pp.f90wrap_bbox(r=r, bbmin=bbmin, bbmax=bbmax)

def d_matrix_nc(dy012, dy112, dy212, dy312):
    """
    d_matrix_nc(dy012, dy112, dy212, dy312)
    
    
    Defined at d_matrix_nc.fpp lines 14-243
    
    Parameters
    ----------
    dy012 : complex array
    dy112 : complex array
    dy212 : complex array
    dy312 : complex array
    
    ---------------------------------------------------------------
     Provides symmetry operations in the(l, s) subspaces for l=0,1,2,3
    """
    libqepy_pp.f90wrap_d_matrix_nc(dy012=dy012, dy112=dy112, dy212=dy212, \
        dy312=dy312)

def d_matrix_so(dyj12, dyj32, dyj52, dyj72):
    """
    d_matrix_so(dyj12, dyj32, dyj52, dyj72)
    
    
    Defined at d_matrix_so.fpp lines 14-331
    
    Parameters
    ----------
    dyj12 : complex array
    dyj32 : complex array
    dyj52 : complex array
    dyj72 : complex array
    
    ---------------------------------------------------------------
     Provides symmetry operations in the j=1/2, j=3/2, j=5/2 and j=7/2
     subspaces
    """
    libqepy_pp.f90wrap_d_matrix_so(dyj12=dyj12, dyj32=dyj32, dyj52=dyj52, \
        dyj72=dyj72)

def do_initial_state(excite):
    """
    do_initial_state(excite)
    
    
    Defined at do_initial_state.fpp lines 14-225
    
    Parameters
    ----------
    excite : int array
    
    ----------------------------------------------------------------------
        This routine is a driver routine which computes the initial state
        contribution to the core level shift.
        contains five parts which are computed by different routines:
        a)   add_shift_lc,   contribution due to the local potential
        b)   add_shift_cc,   contribution due to NLCC
        c)   add_shift_us ,  contribution due to the non-local potential
        d)   add_shift_ew,   contribution due to the electrostatic ewald term
    """
    libqepy_pp.f90wrap_do_initial_state(excite=excite)

def do_shift_ew(alat, nat, ntyp, ityp, zv, delta_zv, at, bg, tau, omega, g, gg, \
    ngm, gcutm, gstart, gamma_only, shift_ion):
    """
    do_shift_ew(alat, nat, ntyp, ityp, zv, delta_zv, at, bg, tau, omega, g, gg, ngm, \
        gcutm, gstart, gamma_only, shift_ion)
    
    
    Defined at do_shift_ew.fpp lines 15-170
    
    Parameters
    ----------
    alat : float
    nat : int
    ntyp : int
    ityp : int array
    zv : float array
    delta_zv : float array
    at : float array
    bg : float array
    tau : float array
    omega : float
    g : float array
    gg : float array
    ngm : int
    gcutm : float
    gstart : int
    gamma_only : bool
    shift_ion : float array
    
    -----------------------------------------------------------------------
     Calculates Ewald energy with both G- and R-space terms.
     Determines optimal alpha. Should hopefully work for any structure.
    """
    libqepy_pp.f90wrap_do_shift_ew(alat=alat, nat=nat, ntyp=ntyp, ityp=ityp, zv=zv, \
        delta_zv=delta_zv, at=at, bg=bg, tau=tau, omega=omega, g=g, gg=gg, ngm=ngm, \
        gcutm=gcutm, gstart=gstart, gamma_only=gamma_only, shift_ion=shift_ion)

def dos_g(et, nspin, nbnd, nks, wk, degauss, ngauss, e, dosg):
    """
    dos_g(et, nspin, nbnd, nks, wk, degauss, ngauss, e, dosg)
    
    
    Defined at dosg.fpp lines 14-51
    
    Parameters
    ----------
    et : float array
    nspin : int
    nbnd : int
    nks : int
    wk : float array
    degauss : float
    ngauss : int
    e : float
    dosg : float array
    
    --------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_dos_g(et=et, nspin=nspin, nbnd=nbnd, nks=nks, wk=wk, \
        degauss=degauss, ngauss=ngauss, e=e, dosg=dosg)

def do_elf(elf):
    """
    do_elf(elf)
    
    
    Defined at elf.fpp lines 13-188
    
    Parameters
    ----------
    elf : float array
    
    -----------------------------------------------------------------------
      calculation of the electron localization function;
         elf = 1/(1+d**2)
      where
         d = ( t(r) - t_von_Weizacker(r) ) / t_Thomas-Fermi(r)
      and
         t(r) = (hbar**2/2m) * \sum_{k,i} |grad psi_{k,i}|**2
    (kinetic energy density)
         t_von_Weizaecker(r) = (hbar**2/2m) * 0.25 * |grad rho(r)|**2/rho
    (non-interacting boson)
         t_Thomas-Fermi(r) = (hbar**2/2m) * 3/5 * (3*pi**2)**(2/3) * rho**(5/3)
    (free electron gas)
      see also http://en.wikipedia.org/wiki/Electron_localization_function
    """
    libqepy_pp.f90wrap_do_elf(elf=elf)

def do_rdg(rdg):
    """
    do_rdg(rdg)
    
    
    Defined at elf.fpp lines 191-223
    
    Parameters
    ----------
    rdg : float array
    
    -----------------------------------------------------------------------
      reduced density gradient
         rdg(r) = (1/2) (1/(3*pi**2))**(1/3) * |\nabla rho(r)|/rho(r)**(4/3)
    """
    libqepy_pp.f90wrap_do_rdg(rdg=rdg)

def do_sl2rho(sl2rho):
    """
    do_sl2rho(sl2rho)
    
    
    Defined at elf.fpp lines 226-273
    
    Parameters
    ----------
    sl2rho : float array
    
    -----------------------------------------------------------------------
      Computes sign(l2)*rho(r), where l2 is the second largest eigenvalue
      of the electron-density Hessian matrix
    """
    libqepy_pp.f90wrap_do_sl2rho(sl2rho=sl2rho)

def do_dori(dori):
    """
    do_dori(dori)
    
    
    Defined at elf.fpp lines 276-318
    
    Parameters
    ----------
    dori : float array
    
    -----------------------------------------------------------------------
     D. Yang & Q.Liu
     density overlap regions indicator（DOI: 10.1021/ct500490b）
     theta(r) = 4 * (laplacian(rho(r)) * grad(rho(r)) * rho(r)
                + | grad(rho(r)) |**2 * grad(rho(r)))
                / (| grad(rho(r)) |**2)**3
     DORI(r) = theta(r) / (1 + theta(r))
    """
    libqepy_pp.f90wrap_do_dori(dori=dori)

def ggen1d(ngm1d, g1d, gg1d, ig1dto3d, nl1d, igtongl1d):
    """
    ggen1d(ngm1d, g1d, gg1d, ig1dto3d, nl1d, igtongl1d)
    
    
    Defined at ggen1d.fpp lines 12-59
    
    Parameters
    ----------
    ngm1d : int
    g1d : float array
    gg1d : float array
    ig1dto3d : int array
    nl1d : int array
    igtongl1d : int array
    
    """
    libqepy_pp.f90wrap_ggen1d(ngm1d=ngm1d, g1d=g1d, gg1d=gg1d, ig1dto3d=ig1dto3d, \
        nl1d=nl1d, igtongl1d=igtongl1d)

def local_dos(iflag, lsign, kpoint, kband, spin_component, emin, emax, dos):
    """
    local_dos(iflag, lsign, kpoint, kband, spin_component, emin, emax, dos)
    
    
    Defined at local_dos.fpp lines 15-425
    
    Parameters
    ----------
    iflag : int
    lsign : bool
    kpoint : int
    kband : int
    spin_component : int
    emin : float
    emax : float
    dos : float array
    
    --------------------------------------------------------------------
         iflag=0: calculates |psi|^2 for band "kband" at point "kpoint"
         iflag=1: calculates the local density of state at e_fermi
    (only for metals)
         iflag=2: calculates the local density of  electronic entropy
    (only for metals with fermi spreading)
         iflag=3: calculates the integral of local dos from "emin" to "emax"
    (emin, emax in Ry)
         iflag=4: calculates |psi|^2 for all kpoints/bands that have
                  energy between "emin" and "emax" (emin, emax in Ry)
                  and spin = spin_component
         lsign:   if true and k=gamma and iflag=0, write |psi|^2 * sign(psi)
         spin_component: for iflag=3 and LSDA calculations only
                         0 for up+down dos,  1 for up dos, 2 for down dos
    """
    libqepy_pp.f90wrap_local_dos(iflag=iflag, lsign=lsign, kpoint=kpoint, \
        kband=kband, spin_component=spin_component, emin=emin, emax=emax, dos=dos)

def local_dos1d(ik, kband, plan):
    """
    local_dos1d(ik, kband, plan)
    
    
    Defined at local_dos1d.fpp lines 14-224
    
    Parameters
    ----------
    ik : int
    kband : int
    plan : float array
    
    --------------------------------------------------------------------
         calculates |psi|^2 for band kband at point ik
    """
    libqepy_pp.f90wrap_local_dos1d(ik=ik, kband=kband, plan=plan)

def local_dos_mag(spin_component, kpoint, kband, raux):
    """
    local_dos_mag(spin_component, kpoint, kband, raux)
    
    
    Defined at local_dos_mag.fpp lines 14-276
    
    Parameters
    ----------
    spin_component : int
    kpoint : int
    kband : int
    raux : float array
    
    ----------------------------------------------------------------------------
     ... compute the contribution of band "kband" at k-point "kpoint"
     ... to the noncolinear magnetization for the given "spin_component"
    """
    libqepy_pp.f90wrap_local_dos_mag(spin_component=spin_component, kpoint=kpoint, \
        kband=kband, raux=raux)

def openfil_pp():
    """
    openfil_pp()
    
    
    Defined at openfil_pp.fpp lines 14-51
    
    
    ----------------------------------------------------------------------------
     ... This routine opens all files needed to the self consistent run,
     ... sets various file names, units, record lengths
    """
    libqepy_pp.f90wrap_openfil_pp()

def partialdos(emin, emax, deltae, kresolveddos, filpdos):
    """
    partialdos(emin, emax, deltae, kresolveddos, filpdos)
    
    
    Defined at partialdos.fpp lines 13-262
    
    Parameters
    ----------
    emin : float
    emax : float
    deltae : float
    kresolveddos : bool
    filpdos : str
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_partialdos(emin=emin, emax=emax, deltae=deltae, \
        kresolveddos=kresolveddos, filpdos=filpdos)

def partialdos_nc(emin, emax, deltae, kresolveddos, filpdos):
    """
    partialdos_nc(emin, emax, deltae, kresolveddos, filpdos)
    
    
    Defined at partialdos.fpp lines 266-575
    
    Parameters
    ----------
    emin : float
    emax : float
    deltae : float
    kresolveddos : bool
    filpdos : str
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_partialdos_nc(emin=emin, emax=emax, deltae=deltae, \
        kresolveddos=kresolveddos, filpdos=filpdos)

def projwave_boxes(filpdos, filproj, n_proj_boxes, irmin, irmax, plotboxes):
    """
    projwave_boxes(filpdos, filproj, n_proj_boxes, irmin, irmax, plotboxes)
    
    
    Defined at projwfc_box.fpp lines 20-302
    
    Parameters
    ----------
    filpdos : str
    filproj : str
    n_proj_boxes : int
    irmin : int array
    irmax : int array
    plotboxes : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_projwave_boxes(filpdos=filpdos, filproj=filproj, \
        n_proj_boxes=n_proj_boxes, irmin=irmin, irmax=irmax, plotboxes=plotboxes)

def partialdos_boxes(emin, emax, deltae, kresolveddos, filpdos, n_proj_boxes):
    """
    partialdos_boxes(emin, emax, deltae, kresolveddos, filpdos, n_proj_boxes)
    
    
    Defined at projwfc_box.fpp lines 306-463
    
    Parameters
    ----------
    emin : float
    emax : float
    deltae : float
    kresolveddos : bool
    filpdos : str
    n_proj_boxes : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_partialdos_boxes(emin=emin, emax=emax, deltae=deltae, \
        kresolveddos=kresolveddos, filpdos=filpdos, n_proj_boxes=n_proj_boxes)

def punch_plot(filplot, plot_num, sample_bias, z, dz, emin, emax, kpoint, kband, \
    spin_component, lsign):
    """
    punch_plot(filplot, plot_num, sample_bias, z, dz, emin, emax, kpoint, kband, \
        spin_component, lsign)
    
    
    Defined at punch_plot.fpp lines 15-284
    
    Parameters
    ----------
    filplot : str
    plot_num : int
    sample_bias : float
    z : float
    dz : float
    emin : float
    emax : float
    kpoint : int
    kband : int
    spin_component : int
    lsign : bool
    
    -----------------------------------------------------------------------
         This subroutine writes on output several quantities
         in a real space 3D mesh for subsequent processing or plotting
         The integer variable plot_num is used to choose the output quantity
         See file Doc/INPUT_PP.* for a description of plotted quantities
         The output quantity is written(formatted) on file filplot.
    """
    libqepy_pp.f90wrap_punch_plot(filplot=filplot, plot_num=plot_num, \
        sample_bias=sample_bias, z=z, dz=dz, emin=emin, emax=emax, kpoint=kpoint, \
        kband=kband, spin_component=spin_component, lsign=lsign)

def punch_rism(filplot):
    """
    punch_rism(filplot)
    
    
    Defined at punch_rism.fpp lines 15-550
    
    Parameters
    ----------
    filplot : str
    
    --------------------------------------------------------------------------
     ... This subroutine writes data of 3D-RISM or Laue-RISM on file filplot.
     ... The data are following:
     ...   1) charge of solvent
     ...   2) potential of solvent
     ...   3) potential of solute
     ...   4) total potential
     ...   5) solvent-atomic densities
    """
    libqepy_pp.f90wrap_punch_rism(filplot=filplot)

def smallgk(xk, at, bg, s, ft, t_rev, sname, nsym, sk, ftk, gk, t_revk, invsk, \
    snamek, nsymk):
    """
    smallgk(xk, at, bg, s, ft, t_rev, sname, nsym, sk, ftk, gk, t_revk, invsk, \
        snamek, nsymk)
    
    
    Defined at smallgk.fpp lines 14-105
    
    Parameters
    ----------
    xk : float array
    at : float array
    bg : float array
    s : int array
    ft : float array
    t_rev : int array
    sname : str array
    nsym : int
    sk : int array
    ftk : float array
    gk : int array
    t_revk : int array
    invsk : int array
    snamek : str array
    nsymk : int
    
    -----------------------------------------------------------------------
     This routine selects, among the symmetry matrices of the point group
     of a crystal, the symmetry operations which leave k unchanged.
    """
    libqepy_pp.f90wrap_smallgk(xk=xk, at=at, bg=bg, s=s, ft=ft, t_rev=t_rev, \
        sname=sname, nsym=nsym, sk=sk, ftk=ftk, gk=gk, t_revk=t_revk, invsk=invsk, \
        snamek=snamek, nsymk=nsymk)

def solvdens(filplot, lpunch):
    """
    solvdens(filplot, lpunch)
    
    
    Defined at solvdens.fpp lines 15-728
    
    Parameters
    ----------
    filplot : str
    lpunch : bool
    
    --------------------------------------------------------------------------
     ... Writes the solvent density and potential
     ... into a file format suitable for plotting
    """
    libqepy_pp.f90wrap_solvdens(filplot=filplot, lpunch=lpunch)

def stm(sample_bias, stmdos):
    """
    istates = stm(sample_bias, stmdos)
    
    
    Defined at stm.fpp lines 14-223
    
    Parameters
    ----------
    sample_bias : float
    stmdos : float array
    
    Returns
    -------
    istates : int
    
    --------------------------------------------------------------------
         This routine calculates an stm image defined as the local density
         of states at the fermi energy.
         The bias of the sample is decided by sample_bias, states between
         ef and ef + sample_bias are taken into account.
         On output istates is the number of states used to compute the image.
         The slab must be oriented with the main axis along celldm(3).
         It may not properly work if the slab has two symmetric surfaces.
    """
    istates = libqepy_pp.f90wrap_stm(sample_bias=sample_bias, stmdos=stmdos)
    return istates

def stop_pp():
    """
    stop_pp()
    
    
    Defined at stop_pp.fpp lines 13-20
    
    
    --------------------------------------------------------------------
     Synchronize processes before stopping.
    """
    libqepy_pp.f90wrap_stop_pp()

def sum_band_kin(kin_r):
    """
    sum_band_kin(kin_r)
    
    
    Defined at sum_band_kin.fpp lines 10-395
    
    Parameters
    ----------
    kin_r : float array
    
    ----------------------------------------------------------------------------
     ... Calculates the Kohn-Sham kinetic-energy density t_{KS}
     ... adapted from the original sum_band subroutine
    """
    libqepy_pp.f90wrap_sum_band_kin(kin_r=kin_r)

def sym_band(filband, spin_component, firstk, lastk):
    """
    sym_band(filband, spin_component, firstk, lastk)
    
    
    Defined at sym_band.fpp lines 14-295
    
    Parameters
    ----------
    filband : str
    spin_component : int
    firstk : int
    lastk : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_band(filband=filband, spin_component=spin_component, \
        firstk=firstk, lastk=lastk)

def find_band_sym(ik, evc, et, nsym, s, ft, gk, invs, rap_et, times, ngroup, \
    istart, accuracy):
    """
    find_band_sym(ik, evc, et, nsym, s, ft, gk, invs, rap_et, times, ngroup, istart, \
        accuracy)
    
    
    Defined at sym_band.fpp lines 299-489
    
    Parameters
    ----------
    ik : int
    evc : complex array
    et : float array
    nsym : int
    s : int array
    ft : float array
    gk : int array
    invs : int array
    rap_et : int array
    times : complex array
    ngroup : int
    istart : int array
    accuracy : float
    
    """
    libqepy_pp.f90wrap_find_band_sym(ik=ik, evc=evc, et=et, nsym=nsym, s=s, ft=ft, \
        gk=gk, invs=invs, rap_et=rap_et, times=times, ngroup=ngroup, istart=istart, \
        accuracy=accuracy)

def rotate_all_psi(ik, psic, evcr, s, ftau, gk):
    """
    rotate_all_psi(ik, psic, evcr, s, ftau, gk)
    
    
    Defined at sym_band.fpp lines 491-568
    
    Parameters
    ----------
    ik : int
    psic : complex array
    evcr : complex array
    s : int array
    ftau : int array
    gk : int array
    
    """
    libqepy_pp.f90wrap_rotate_all_psi(ik=ik, psic=psic, evcr=evcr, s=s, ftau=ftau, \
        gk=gk)

def find_band_sym_so(ik, evc, et, nsym, s, ft, d_spin, gk, invs, rap_et, times, \
    ngroup, istart, accuracy):
    """
    find_band_sym_so(ik, evc, et, nsym, s, ft, d_spin, gk, invs, rap_et, times, \
        ngroup, istart, accuracy)
    
    
    Defined at sym_band.fpp lines 570-759
    
    Parameters
    ----------
    ik : int
    evc : complex array
    et : float array
    nsym : int
    s : int array
    ft : float array
    d_spin : complex array
    gk : int array
    invs : int array
    rap_et : int array
    times : complex array
    ngroup : int
    istart : int array
    accuracy : float
    
    """
    libqepy_pp.f90wrap_find_band_sym_so(ik=ik, evc=evc, et=et, nsym=nsym, s=s, \
        ft=ft, d_spin=d_spin, gk=gk, invs=invs, rap_et=rap_et, times=times, \
        ngroup=ngroup, istart=istart, accuracy=accuracy)

def rotate_all_psi_so(ik, evc_nc, evcr, s, ftau, d_spin, has_e, gk):
    """
    rotate_all_psi_so(ik, evc_nc, evcr, s, ftau, d_spin, has_e, gk)
    
    
    Defined at sym_band.fpp lines 761-868
    
    Parameters
    ----------
    ik : int
    evc_nc : complex array
    evcr : complex array
    s : int array
    ftau : int array
    d_spin : complex array
    has_e : int
    gk : int array
    
    """
    libqepy_pp.f90wrap_rotate_all_psi_so(ik=ik, evc_nc=evc_nc, evcr=evcr, s=s, \
        ftau=ftau, d_spin=d_spin, has_e=has_e, gk=gk)

def find_nks1nks2(firstk, lastk, spin_component):
    """
    nks1tot, nks1, nks2tot, nks2 = find_nks1nks2(firstk, lastk, spin_component)
    
    
    Defined at sym_band.fpp lines 870-898
    
    Parameters
    ----------
    firstk : int
    lastk : int
    spin_component : int
    
    Returns
    -------
    nks1tot : int
    nks1 : int
    nks2tot : int
    nks2 : int
    
    """
    nks1tot, nks1, nks2tot, nks2 = libqepy_pp.f90wrap_find_nks1nks2(firstk=firstk, \
        lastk=lastk, spin_component=spin_component)
    return nks1tot, nks1, nks2tot, nks2

def find_info_group(nsym, s, t_rev, ft, d_spink, gk, sname, s_is, d_spin_is, \
    gk_is, invs_is):
    """
    is_symmorphic, search_sym = find_info_group(nsym, s, t_rev, ft, d_spink, gk, \
        sname, s_is, d_spin_is, gk_is, invs_is)
    
    
    Defined at sym_band.fpp lines 900-1034
    
    Parameters
    ----------
    nsym : int
    s : int array
    t_rev : int array
    ft : float array
    d_spink : complex array
    gk : int array
    sname : str array
    s_is : int array
    d_spin_is : complex array
    gk_is : int array
    invs_is : int array
    
    Returns
    -------
    is_symmorphic : bool
    search_sym : bool
    
    """
    is_symmorphic, search_sym = libqepy_pp.f90wrap_find_info_group(nsym=nsym, s=s, \
        t_rev=t_rev, ft=ft, d_spink=d_spink, gk=gk, sname=sname, s_is=s_is, \
        d_spin_is=d_spin_is, gk_is=gk_is, invs_is=invs_is)
    return is_symmorphic, search_sym

def s_axis_to_cart(s, sr, at, bg):
    """
    s_axis_to_cart(s, sr, at, bg)
    
    
    Defined at sym_band.fpp lines 1045-1083
    
    Parameters
    ----------
    s : int array
    sr : float array
    at : float array
    bg : float array
    
    ----------------------------------------------------------------------
         This routine transform a symmetry matrix expressed in the
         basis of the crystal axis in the cartesian basis.
         last revised 3 may 1995 by A. Dal Corso
    """
    libqepy_pp.f90wrap_s_axis_to_cart(s=s, sr=sr, at=at, bg=bg)

def wannier_enrg(enrg):
    """
    wannier_enrg(enrg)
    
    
    Defined at wannier_enrg.fpp lines 12-41
    
    Parameters
    ----------
    enrg : float array
    
    ----------------------------------------------------------------------
     ... This routine computes energy of each wannier. It is assumed that WF \
         generated already and stored if the buffer.
    """
    libqepy_pp.f90wrap_wannier_enrg(enrg=enrg)

def wannier_proj(ik, wan_func):
    """
    wannier_proj(ik, wan_func)
    
    
    Defined at wannier_proj.fpp lines 11-105
    
    Parameters
    ----------
    ik : int
    wan_func : complex array
    
    """
    libqepy_pp.f90wrap_wannier_proj(ik=ik, wan_func=wan_func)

def work_function(wf):
    """
    work_function(wf)
    
    
    Defined at work_function.fpp lines 12-124
    
    Parameters
    ----------
    wf : float
    
    """
    libqepy_pp.f90wrap_work_function(wf=wf)

def write_hamiltonian_default(nwan, hamk, iunhamilt):
    """
    write_hamiltonian_default(nwan, hamk, iunhamilt)
    
    
    Defined at write_hamiltonians.fpp lines 12-45
    
    Parameters
    ----------
    nwan : int
    hamk : complex array
    iunhamilt : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_write_hamiltonian_default(nwan=nwan, hamk=hamk, \
        iunhamilt=iunhamilt)

def write_hamiltonian_amulet(nwan, hamk, hash, iunhamilt):
    """
    write_hamiltonian_amulet(nwan, hamk, hash, iunhamilt)
    
    
    Defined at write_hamiltonians.fpp lines 48-109
    
    Parameters
    ----------
    nwan : int
    hamk : complex array
    hash : int
    iunhamilt : int
    
    -----------------------------------------------------------------------
     Special hamiltonian format for the AMULET code instegration
     www.amulet-code.org
    """
    libqepy_pp.f90wrap_write_hamiltonian_amulet(nwan=nwan, hamk=hamk, hash=hash, \
        iunhamilt=iunhamilt)

def write_systemdata_amulet(hash, nelec, iunsystem):
    """
    write_systemdata_amulet(hash, nelec, iunsystem)
    
    
    Defined at write_hamiltonians.fpp lines 112-188
    
    Parameters
    ----------
    hash : int
    nelec : float
    iunsystem : int
    
    -----------------------------------------------------------------------
     Damp of the system data for the AMULET code instegration
     www.amulet-code.org
    """
    libqepy_pp.f90wrap_write_systemdata_amulet(hash=hash, nelec=nelec, \
        iunsystem=iunsystem)

def split_basis_into_blocks(block_dim, block_l, block_atom, block_wannier, \
    block_start):
    """
    nblocks = split_basis_into_blocks(block_dim, block_l, block_atom, block_wannier, \
        block_start)
    
    
    Defined at write_hamiltonians.fpp lines 190-227
    
    Parameters
    ----------
    block_dim : int array
    block_l : int array
    block_atom : int array
    block_wannier : int array
    block_start : int array
    
    Returns
    -------
    nblocks : int
    
    """
    nblocks = libqepy_pp.f90wrap_split_basis_into_blocks(block_dim=block_dim, \
        block_l=block_l, block_atom=block_atom, block_wannier=block_wannier, \
        block_start=block_start)
    return nblocks

def write_io_header(filplot, iunplot, title, nr1x, nr2x, nr3x, nr1, nr2, nr3, \
    nat, ntyp, ibrav, celldm, at, gcutm, dual, ecutwfc, nkstot, nbnd, natomwfc):
    """
    write_io_header(filplot, iunplot, title, nr1x, nr2x, nr3x, nr1, nr2, nr3, nat, \
        ntyp, ibrav, celldm, at, gcutm, dual, ecutwfc, nkstot, nbnd, natomwfc)
    
    
    Defined at write_io_header.fpp lines 15-46
    
    Parameters
    ----------
    filplot : str
    iunplot : int
    title : str
    nr1x : int
    nr2x : int
    nr3x : int
    nr1 : int
    nr2 : int
    nr3 : int
    nat : int
    ntyp : int
    ibrav : int
    celldm : float array
    at : float array
    gcutm : float
    dual : float
    ecutwfc : float
    nkstot : int
    nbnd : int
    natomwfc : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_write_io_header(filplot=filplot, iunplot=iunplot, \
        title=title, nr1x=nr1x, nr2x=nr2x, nr3x=nr3x, nr1=nr1, nr2=nr2, nr3=nr3, \
        nat=nat, ntyp=ntyp, ibrav=ibrav, celldm=celldm, at=at, gcutm=gcutm, \
        dual=dual, ecutwfc=ecutwfc, nkstot=nkstot, nbnd=nbnd, natomwfc=natomwfc)

def write_p_avg(filp, spin_component, firstk, lastk):
    """
    write_p_avg(filp, spin_component, firstk, lastk)
    
    
    Defined at write_p_avg.fpp lines 14-140
    
    Parameters
    ----------
    filp : str
    spin_component : int
    firstk : int
    lastk : int
    
    ---------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_write_p_avg(filp=filp, spin_component=spin_component, \
        firstk=firstk, lastk=lastk)

def write_xml_proj(filename, projs, lwrite_ovp, ovps):
    """
    write_xml_proj(filename, projs, lwrite_ovp, ovps)
    
    
    Defined at write_proj.fpp lines 13-105
    
    Parameters
    ----------
    filename : str
    projs : complex array
    lwrite_ovp : bool
    ovps : complex array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_write_xml_proj(filename=filename, projs=projs, \
        lwrite_ovp=lwrite_ovp, ovps=ovps)

def write_proj_file(filproj, proj):
    """
    write_proj_file(filproj, proj)
    
    
    Defined at write_proj.fpp lines 109-179
    
    Parameters
    ----------
    filproj : str
    proj : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_write_proj_file(filproj=filproj, proj=proj)

def average():
    """
    average()
    
    
    Defined at average.fpp lines 13-373
    
    
    -----------------------------------------------------------------------
          Compute planar and macroscopic averages of a quantity(e.g. charge)
          in real space on a 3D FFT mesh. The quantity is read from a file
          produced by "pp.x", or from multiple files as follows:
              Q(i,j,k) = \sum_n w_n q_n(i,j,k)
          where q_n is the quantity for file n, w_n is a user-supplied weight
          The planar average is defined as
             p(k) = \sum_{i=1}^{N_1} \sum_{j=1}^{N_2} Q(i,j,k) / (N_1 N_2)
          along direction 3, and the like for directions 1 and 2;
          N_1, N_2, N_3 are the three dimensions of the 3D FFT.
          Note that if Q is a charge density whose integral is Z_v:
             Z_v = \int p(z) dV = \sum_k p(k) \Omega/N_3
          where \Omega is the size of the unit cell(or supercell)
          The planar average is then interpolated on the specified number
          of points supplied in input and written to file "avg.dat"
          The macroscopic average is defined as
             m(z) = \int_z^{z+a} p(z) dz
          where a is the size of the window(supplied in input)
          Input variables
          nfile        the number of files contaning the desired quantities
                       All files must refer to the same physical system
     for each file:
          filename     the name of the n-th file
          weight       the weight w_n of the quantity read from n-th file
          .
          .
     end
          npt          the number of points for the final interpolation of
                       the planar and macroscopic averages, as written to file
                       If npt <= N_idir(see below) no interpolation is done,
                       the N_idir FFT points in direction idir are printed.
          idir         1,2 or 3. Planar average is done in the plane orthogonal
                       to direction "idir", as defined for the crystal cell
          awin         the size of the window for macroscopic average(a.u.)
     Format of output file avg.dat:
        x   p(x)   m(x)
     where
        x = coordinate(a.u) along direction idir
            x runs from 0 to the length of primitive vector idir
      p(x)= planar average, as defined above
      m(x)= macroscopic average, as defined above
    """
    libqepy_pp.f90wrap_average()

def band_interpolation():
    """
    band_interpolation()
    
    
    Defined at band_interpolation.fpp lines 17-172
    
    
    ----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_band_interpolation()

def do_bands():
    """
    do_bands()
    
    
    Defined at bands.fpp lines 14-627
    
    
    -----------------------------------------------------------------------
     See files INPUT_BANDS.* in Doc/ directory for usage
    """
    libqepy_pp.f90wrap_do_bands()

def d3hess():
    """
    d3hess()
    
    
    Defined at d3hess.fpp lines 13-373
    
    
    ---------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_d3hess()

def do_dos():
    """
    do_dos()
    
    
    Defined at dos.fpp lines 14-238
    
    
    --------------------------------------------------------------------
     Calculates the Density of States(DOS),
     separated into up and down components for LSDA
     See files INPUT_DOS.* in Doc/ directory for usage
     IMPORTANT: since v.5 namelist name is &dos and no longer &inputpp
    """
    libqepy_pp.f90wrap_do_dos()

def epsilon():
    """
    epsilon()
    
    
    Defined at epsilon.fpp lines 183-356
    
    
    ------------------------------
     Compute the complex macroscopic dielectric function,
     at the RPA level, neglecting local field effects.
     Eps is computed both on the real or immaginary axis
     Authors:
         2006 Andrea Benassi, Andrea Ferretti, Carlo Cavazzoni: basic \
             implementation(partly taken from pw2gw.f90)
         2007 Andrea Benassi: intraband contribution, nspin=2
         2016    Tae-Yun Kim, Cheol-Hwan Park:                       bugs fixed
         2016 Tae-Yun Kim, Cheol-Hwan Park, Andrea Ferretti: non-collinear magnetism \
             implemented
                                                                     code significantly restructured
    """
    libqepy_pp.f90wrap_epsilon()

def eps_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin):
    """
    eps_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin)
    
    
    Defined at epsilon.fpp lines 359-560
    
    Parameters
    ----------
    intersmear : float
    intrasmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    metalcalc : bool
    nspin : int
    
    -----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_eps_calc(intersmear=intersmear, intrasmear=intrasmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, metalcalc=metalcalc, \
        nspin=nspin)

def jdos_calc(smeartype, intersmear, nbndmin, nbndmax, shift, nspin):
    """
    jdos_calc(smeartype, intersmear, nbndmin, nbndmax, shift, nspin)
    
    
    Defined at epsilon.fpp lines 563-825
    
    Parameters
    ----------
    smeartype : str
    intersmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    nspin : int
    
    --------------------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_jdos_calc(smeartype=smeartype, intersmear=intersmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, nspin=nspin)

def offdiag_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, \
    nspin):
    """
    offdiag_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin)
    
    
    Defined at epsilon.fpp lines 828-1017
    
    Parameters
    ----------
    intersmear : float
    intrasmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    metalcalc : bool
    nspin : int
    
    -----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_offdiag_calc(intersmear=intersmear, intrasmear=intrasmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, metalcalc=metalcalc, \
        nspin=nspin)

def dipole_calc(ik, dipole_aux, metalcalc, nbndmin, nbndmax):
    """
    dipole_calc(ik, dipole_aux, metalcalc, nbndmin, nbndmax)
    
    
    Defined at epsilon.fpp lines 1020-1114
    
    Parameters
    ----------
    ik : int
    dipole_aux : complex array
    metalcalc : bool
    nbndmin : int
    nbndmax : int
    
    ------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_dipole_calc(ik=ik, dipole_aux=dipole_aux, \
        metalcalc=metalcalc, nbndmin=nbndmin, nbndmax=nbndmax)

def fermi_proj():
    """
    fermi_proj()
    
    
    Defined at fermi_proj.fpp lines 182-293
    
    
    ----------------------------------------------------------------------------
     Usage :
     $ proj_fermi.x -in {input file}
     Then it generates proj.frmsf(for nspin = 1, 4) or
     proj1.frmsf and proj2.frmsf(for nspin = 2)
     Input file format(projwfc.x + tail):
     &PROJWFC
     prefix = "..."
     outdir = "..."
     ...
     /
     {Number of target WFCs}
     {Index of WFC1} {Index of WFC2} {Index of WFC3} ...
    """
    libqepy_pp.f90wrap_fermi_proj()

def fermi_velocity():
    """
    fermi_velocity()
    
    
    Defined at fermi_velocity.fpp lines 20-155
    
    
    --------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fermi_velocity()

def fermisurface():
    """
    fermisurface()
    
    
    Defined at fermisurface.fpp lines 359-382
    
    
    --------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fermisurface()

def initial_state():
    """
    initial_state()
    
    
    Defined at initial_state.fpp lines 13-89
    
    
    -----------------------------------------------------------------------
      compute initial-state contribution to core level shift
     input: namelist "&inputpp", with variables
       prefix      prefix of input files saved by program pwscf
       outdir      temporary directory where files resides
    """
    libqepy_pp.f90wrap_initial_state()

def molecularpdos():
    """
    molecularpdos()
    
    
    Defined at molecularpdos.fpp lines 13-416
    
    
    -----------------------------------------------------------------------
     Takes the projections onto orthogonalized atomic wavefunctions
     as computed by projwfc.x(see outdir/prefix.save/atomic_proj.xml)
     to build an LCAO-like representation of the eigenvalues of a system
     "full" and "part" of it(each should provide its own atomic_proj.xml file).
     Then the eigenvectors of the full system are projected onto the ones of the
     part.
     An explanation of the keywords and the implementation is provided in
     Scientific Reports | 6:24603 | DOI: 10.1038/srep24603(2016) (Supp. Info)
     Typical application: decompose the PDOS of an adsorbed molecule into
     its molecular orbital, as determined by a gas-phase calculation.
     The user has to specify which atomic functions(range beg:end) to use in
     both the full system and the part(the same atomic set should be used).
     MOPDOS(E,ibnd_part) = \sum_k w_k [ \sum_{ibnd_full}
                                        <psi_{ibnd_part,k}|psi_{ibnd_full,k}>
                                        * \delta(E-\epsilon_{ibnd_full,k}) *
                                        <psi_{ibnd_full,k}|psi_{ibnd_part,k}> ]
     where <psi_{ibnd_part,k}|psi_{ibnd_full,k}> are computed by using the LCAO
     representations:
     |psi_{ibnd_full,k}> =
            \sum_iatmwfc projs_full(iatmwfc,ibnd_full,k) |phi_{iatmwfc}>
     |psi_{ibnd_part,k}> =
            \sum_iatmwfc projs_part(iatmwfc,ibnd_part,k) |phi_{iatmwfc}>
     <psi_{ibnd_part,k}|psi_{ibnd_full,k}> =: projs_mo(ibnd_part,ibnd_full,k)
          = \sum_iatmwfc CONJG(projs_part(iatmwfc,ibnd_part,k))
                             * projs_full(iatmwfc,ibnd_full,k)
     If kresolveddos=.true. from input, the summation over k is not performed
     and individual k-resolved contributions are given in output.
    """
    libqepy_pp.f90wrap_molecularpdos()

def open_grid():
    """
    open_grid()
    
    
    Defined at open_grid.fpp lines 6-243
    
    
    ------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_open_grid()

def oscdft_et():
    """
    oscdft_et()
    
    
    Defined at oscdft_et.fpp lines 5-7
    
    
    """
    libqepy_pp.f90wrap_oscdft_et()

def oscdft_pp():
    """
    oscdft_pp()
    
    
    Defined at oscdft_pp.fpp lines 5-7
    
    
    """
    libqepy_pp.f90wrap_oscdft_pp()

def plan_avg():
    """
    plan_avg()
    
    
    Defined at plan_avg.fpp lines 14-283
    
    
    -----------------------------------------------------------------------
     calculate planar averages of each wavefunction
    """
    libqepy_pp.f90wrap_plan_avg()

def plotband():
    """
    plotband()
    
    
    Defined at plotband.fpp lines 12-785
    
    
    """
    libqepy_pp.f90wrap_plotband()

def plotproj():
    """
    plotproj()
    
    
    Defined at plotproj.fpp lines 12-150
    
    
    """
    libqepy_pp.f90wrap_plotproj()

def plotrho():
    """
    plotrho()
    
    
    Defined at plotrho.fpp lines 14-984
    
    
    -----------------------------------------------------------------------
       2D contour plot - logarithmically or linearly spaced levels
                       - Postscript printable output
       if " cplot" is called:
                       - contour lines plus gray levels
                       - negative values are shaded
       if "psplot" is called:
                       - contour lines of various kinds(solid, dashed, etc)
    """
    libqepy_pp.f90wrap_plotrho()

def pmw():
    """
    pmw()
    
    
    Defined at poormanwannier.fpp lines 14-392
    
    
    -----------------------------------------------------------------------
     projects wavefunctions onto atomic wavefunctions,
     input: namelist "&inputpp", with variables
       prefix      prefix of input files saved by program pwscf
       outdir      temporary directory where files resides
    """
    libqepy_pp.f90wrap_pmw()

def pp():
    """
    pp()
    
    
    Defined at postproc.fpp lines 257-293
    
    
    -----------------------------------------------------------------------
        Program for data analysis and plotting. The two basic steps are:
        1) read the output file produced by pw.x, extract and calculate
           the desired quantity(rho, V, ...)
        2) write the desired quantity to file in a suitable format for
           various types of plotting and various plotting programs
        The two steps can be performed independently. Intermediate data
        can be saved to file in step 1 and read from file in step 2.
        DESCRIPTION of the INPUT : see file Doc/INPUT_PP.*
    """
    libqepy_pp.f90wrap_pp()

def pprism():
    """
    pprism()
    
    
    Defined at postrism.fpp lines 15-115
    
    
    --------------------------------------------------------------------------
     ... Program to plot solvent distributions
     ... calculated by 3D-RISM or Laue-RISM
    """
    libqepy_pp.f90wrap_pprism()

def do_ppacf():
    """
    do_ppacf()
    
    
    Defined at ppacf.fpp lines 14-1229
    
    
    -----------------------------------------------------------------------
     This routine computes the coupling constant dependency of exchange
     correlation potential \( E_{\text{xc},\lambda}, \lambda \in \[0:1\]
     and the spatial distribution of exchange correlation energy
     density and kinetic correlation energy density according to:
     Y. Jiao, E. Schr\"oder, and P. Hyldgaard, Phys. Rev. B 97, 085115(2018).
     For an illustration of how to use this routine to set hybrid
     mixing parameter, please refer to:
     Y. Jiao, E. Schr\"oder, and P. Hyldgaard, J. Chem. Phys. 148, 194115(2018).
     Finally, this routine can also be used to set isolate the
      Ashcroft-type pure-dispersion component of E_{c;vdw}^nl
    (or the cumulant reminder, E_{c;alpha}^nl, defining a local-field \
        susceptibility):
     P. Hyldgaard, Y. Jiao, and V. Shukla, J. Phys.: Condens. Matt. 32, 393001(2020):
     https://iopscience.iop.org/article/10.1088/1361-648X/ab8250
    """
    libqepy_pp.f90wrap_do_ppacf()

def do_projwfc():
    """
    do_projwfc()
    
    
    Defined at projwfc.fpp lines 13-244
    
    
    -----------------------------------------------------------------------
     projects wavefunctions onto orthogonalized atomic wavefunctions,
     calculates Lowdin charges, spilling parameter, projected DOS
     or computes the LDOS in a volume given in input as function of energy
     See files INPUT_PROJWFC.* in Doc/ directory for usage
     IMPORTANT: since v.5 namelist name is &projwfc and no longer &inputpp
    """
    libqepy_pp.f90wrap_do_projwfc()

def get_et_from_gww(nbnd, et):
    """
    get_et_from_gww(nbnd, et)
    
    
    Defined at projwfc.fpp lines 246-280
    
    Parameters
    ----------
    nbnd : int
    et : float array
    
    """
    libqepy_pp.f90wrap_get_et_from_gww(nbnd=nbnd, et=et)

def print_lowdin(unit, nat, lmax_wfc, nspin, diag_basis, charges, \
    charges_lm=None):
    """
    print_lowdin(unit, nat, lmax_wfc, nspin, diag_basis, charges[, charges_lm])
    
    
    Defined at projwfc.fpp lines 283-377
    
    Parameters
    ----------
    unit : int
    nat : int
    lmax_wfc : int
    nspin : int
    diag_basis : bool
    charges : float array
    charges_lm : float array
    
    """
    libqepy_pp.f90wrap_print_lowdin(unit=unit, nat=nat, lmax_wfc=lmax_wfc, \
        nspin=nspin, diag_basis=diag_basis, charges=charges, charges_lm=charges_lm)

def sym_proj_g(rproj0, proj_out):
    """
    sym_proj_g(rproj0, proj_out)
    
    
    Defined at projwfc.fpp lines 381-452
    
    Parameters
    ----------
    rproj0 : float array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_g(rproj0=rproj0, proj_out=proj_out)

def sym_proj_k(proj0, proj_out):
    """
    sym_proj_k(proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 456-527
    
    Parameters
    ----------
    proj0 : complex array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_k(proj0=proj0, proj_out=proj_out)

def sym_proj_so(domag, proj0, proj_out):
    """
    sym_proj_so(domag, proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 531-633
    
    Parameters
    ----------
    domag : bool
    proj0 : complex array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_so(domag=domag, proj0=proj0, proj_out=proj_out)

def sym_proj_nc(proj0, proj_out):
    """
    sym_proj_nc(proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 636-721
    
    Parameters
    ----------
    proj0 : complex array
    proj_out : float array
    
    """
    libqepy_pp.f90wrap_sym_proj_nc(proj0=proj0, proj_out=proj_out)

def print_proj(lmax_wfc, proj, lowdin_unit, diag_basis):
    """
    print_proj(lmax_wfc, proj, lowdin_unit, diag_basis)
    
    
    Defined at projwfc.fpp lines 724-882
    
    Parameters
    ----------
    lmax_wfc : int
    proj : float array
    lowdin_unit : int
    diag_basis : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_print_proj(lmax_wfc=lmax_wfc, proj=proj, \
        lowdin_unit=lowdin_unit, diag_basis=diag_basis)

def force_theorem(ef_0, filproj):
    """
    force_theorem(ef_0, filproj)
    
    
    Defined at projwfc.fpp lines 885-981
    
    Parameters
    ----------
    ef_0 : float
    filproj : str
    
    """
    libqepy_pp.f90wrap_force_theorem(ef_0=ef_0, filproj=filproj)

def projwave_paw():
    """
    projwave_paw()
    
    
    Defined at projwfc.fpp lines 985-1078
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_projwave_paw()

def compute_mj(j, l, m):
    """
    compute_mj = compute_mj(j, l, m)
    
    
    Defined at projwfc.fpp lines 1082-1096
    
    Parameters
    ----------
    j : float
    l : int
    m : int
    
    Returns
    -------
    compute_mj : float
    
    -----------------------------------------------------------------------
    """
    compute_mj = libqepy_pp.f90wrap_compute_mj(j=j, l=l, m=m)
    return compute_mj

def projwave(filproj, filowdin, lsym, diag_basis, lwrite_ovp):
    """
    projwave(filproj, filowdin, lsym, diag_basis, lwrite_ovp)
    
    
    Defined at projwfc.fpp lines 1103-1729
    
    Parameters
    ----------
    filproj : str
    filowdin : str
    lsym : bool
    diag_basis : bool
    lwrite_ovp : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_projwave(filproj=filproj, filowdin=filowdin, lsym=lsym, \
        diag_basis=diag_basis, lwrite_ovp=lwrite_ovp)

def rotate_basis(iuwfc):
    """
    lrotated = rotate_basis(iuwfc)
    
    
    Defined at projwfc.fpp lines 1732-2090
    
    Parameters
    ----------
    iuwfc : int
    
    Returns
    -------
    lrotated : bool
    
    """
    lrotated = libqepy_pp.f90wrap_rotate_basis(iuwfc=iuwfc)
    return lrotated

def pw2bgw():
    """
    pw2bgw()
    
    
    Defined at pw2bgw.fpp lines 117-4504
    
    
    -------------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_pw2bgw()

def pw2critic():
    """
    pw2critic()
    
    
    Defined at pw2critic.fpp lines 37-148
    
    
    """
    libqepy_pp.f90wrap_pw2critic()

def pw2gw():
    """
    pw2gw()
    
    
    Defined at pw2gw.fpp lines 26-1096
    
    
    -----------------------------------------------------------------------
     This subroutine writes files containing plane wave coefficients
     and other stuff needed by GW codes
    """
    libqepy_pp.f90wrap_pw2gw()

def pw2wannier90():
    """
    pw2wannier90()
    
    
    Defined at pw2wannier90.fpp lines 100-5184
    
    
    ------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_pw2wannier90()

def sumpdos():
    """
    sumpdos()
    
    
    Defined at sumpdos.fpp lines 13-305
    
    
    """
    libqepy_pp.f90wrap_sumpdos()

def wannier_ham():
    """
    wannier_ham()
    
    
    Defined at wannier_ham.fpp lines 12-308
    
    
    -----------------------------------------------------------------------
     This program generates Hamiltonian matrix on Wannier-functions basis
    """
    libqepy_pp.f90wrap_wannier_ham()

def wannier_plot():
    """
    wannier_plot()
    
    
    Defined at wannier_plot.fpp lines 12-227
    
    
    -----------------------------------------------------------------------
     This program plots charge density of selected wannier function in
     IBM Data Explorer format
    """
    libqepy_pp.f90wrap_wannier_plot()

def wfck2r():
    """
    wfck2r()
    
    
    Defined at wfck2r.fpp lines 39-236
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_wfck2r()


oscdft_pp_mod = qepy_pp.oscdft_pp_mod
projections_ldos = qepy_pp.projections_ldos
eps_writer = qepy_pp.eps_writer
vasp_read_chgcar = qepy_pp.vasp_read_chgcar
fermi_proj_routines = qepy_pp.fermi_proj_routines
grid_module = qepy_pp.grid_module
vdw_df_scale = qepy_pp.vdw_df_scale
paw_postproc = qepy_pp.paw_postproc
wannier = qepy_pp.wannier
idwmod = qepy_pp.idwmod
adduscore = qepy_pp.adduscore
projections = qepy_pp.projections
fs = qepy_pp.fs
vasp_xml = qepy_pp.vasp_xml
fermisurfer_common = qepy_pp.fermisurfer_common
oscdft_et_mod = qepy_pp.oscdft_et_mod
globalmod = qepy_pp.globalmod
read_proj = qepy_pp.read_proj
fouriermod = qepy_pp.fouriermod
pp_module = qepy_pp.pp_module
chdens_module = qepy_pp.chdens_module
