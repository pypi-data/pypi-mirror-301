from __future__ import print_function, absolute_import, division
pname = 'libqepy_modules'

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
import libqepy_modules
import f90wrap.runtime
import logging
import numpy
import qepy_modules.mp_bands
import qepy_modules.wy_pos
import qepy_modules.open_close_input_file
import qepy_modules.check_stop
import qepy_modules.environment
import qepy_modules.io_global
import qepy_modules.read_input
import qepy_modules.command_line_options
import qepy_modules.gvect
import qepy_modules.wavefunctions
import qepy_modules.funct
import qepy_modules.mp_global
import qepy_modules.space_group
import qepy_modules.mp_bands_tddfpt
import qepy_modules.wyckoff
import qepy_modules.mp_pools
import qepy_modules.mp_world
import qepy_modules.cell_base
import qepy_modules.mp_orthopools
import qepy_modules.constants
import qepy_modules.gvecs
import qepy_modules.qepy_sys
import qepy_modules.control_flags
import qepy_modules.ions_base
import qepy_modules.qexsd_module

def impose_deviatoric_strain(at_old, at):
    """
    impose_deviatoric_strain(at_old, at)
    
    
    Defined at deviatoric.fpp lines 14-34
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
     Impose a pure deviatoric(volume-conserving) deformation.
     Needed to enforce volume conservation in variable-cell MD/optimization.
    """
    libqepy_modules.f90wrap_impose_deviatoric_strain(at_old=at_old, at=at)

def impose_deviatoric_strain_2d(at_old, at):
    """
    impose_deviatoric_strain_2d(at_old, at)
    
    
    Defined at deviatoric.fpp lines 38-61
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
     Modification of \(\texttt{impose\_deviatoric\_strain}\) but for
     Area conserving deformation(2DSHAPE).
     Added by Richard Charles Andrew, Physics Department, University if Pretoria,
     South Africa, august 2012.
    """
    libqepy_modules.f90wrap_impose_deviatoric_strain_2d(at_old=at_old, at=at)

def impose_deviatoric_stress(sigma):
    """
    impose_deviatoric_stress(sigma)
    
    
    Defined at deviatoric.fpp lines 65-78
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
     Impose a pure deviatoric stress.
    """
    libqepy_modules.f90wrap_impose_deviatoric_stress(sigma=sigma)

def impose_deviatoric_stress_2d(sigma):
    """
    impose_deviatoric_stress_2d(sigma)
    
    
    Defined at deviatoric.fpp lines 82-96
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
     Modification of \(\texttt{impose_deviatoric_stress} but for
     Area conserving deformation(2DSHAPE).
     Added by Richard Charles Andrew, Physics Department, University if Pretoria,
     South Africa, august 2012
    """
    libqepy_modules.f90wrap_impose_deviatoric_stress_2d(sigma=sigma)

def latgen_lib(ibrav, celldm, a1, a2, a3):
    """
    omega, ierr, errormsg = latgen_lib(ibrav, celldm, a1, a2, a3)
    
    
    Defined at latgen.fpp lines 14-386
    
    Parameters
    ----------
    ibrav : int
    celldm : float array
    a1 : float array
    a2 : float array
    a3 : float array
    
    Returns
    -------
    omega : float
    ierr : int
    errormsg : str
    
    -----------------------------------------------------------------------
         sets up the crystallographic vectors a1, a2, and a3.
         ibrav is the structure index:
           1  cubic P(sc)                8  orthorhombic P
           2  cubic F(fcc)               9  1-face(C) centered orthorhombic
           3  cubic I(bcc)              10  all face centered orthorhombic
           4  hexagonal and trigonal P   11  body centered orthorhombic
           5  trigonal R, 3-fold axis c  12  monoclinic P(unique axis: c)
           6  tetragonal P(st)          13  one face(base) centered monoclinic
           7  tetragonal I(bct)         14  triclinic P
         Also accepted:
           0  "free" structure          -12  monoclinic P(unique axis: b)
          -3  cubic bcc with a more symmetric choice of axis
          -5  trigonal R, threefold axis along(111)
          -9  alternate description for base centered orthorhombic
         -13  one face(base) centered monoclinic(unique axis: b)
          91  1-face(A) centered orthorombic
         celldm are parameters which fix the shape of the unit cell
         omega is the unit-cell volume
         NOTA BENE: all axis sets are right-handed
         Boxes for US PPs do not work properly with left-handed axis
    """
    omega, ierr, errormsg = libqepy_modules.f90wrap_latgen_lib(ibrav=ibrav, \
        celldm=celldm, a1=a1, a2=a2, a3=a3)
    return omega, ierr, errormsg

def at2celldm(ibrav, alat, a1, a2, a3, celldm):
    """
    at2celldm(ibrav, alat, a1, a2, a3, celldm)
    
    
    Defined at latgen.fpp lines 390-490
    
    Parameters
    ----------
    ibrav : int
    alat : float
    a1 : float array
    a2 : float array
    a3 : float array
    celldm : float array
    
    -----------------------------------------------------------------------
         Returns celldm parameters computed from lattice vectors a1,a2,a3
         a1, a2, a3 are in "alat" units
         If Bravais lattice index ibrav=0, only celldm(1) is set to alat
         See latgen for definition of celldm and lattice vectors.
         a1, a2, a3, ibrav, alat are not modified
    """
    libqepy_modules.f90wrap_at2celldm(ibrav=ibrav, alat=alat, a1=a1, a2=a2, a3=a3, \
        celldm=celldm)

def at2ibrav(a1, a2, a3):
    """
    ibrav = at2ibrav(a1, a2, a3)
    
    
    Defined at latgen.fpp lines 493-626
    
    Parameters
    ----------
    a1 : float array
    a2 : float array
    a3 : float array
    
    Returns
    -------
    ibrav : int
    
    """
    ibrav = libqepy_modules.f90wrap_at2ibrav(a1=a1, a2=a2, a3=a3)
    return ibrav

def abc2celldm(ibrav, a, b, c, cosab, cosac, cosbc, celldm):
    """
    abc2celldm(ibrav, a, b, c, cosab, cosac, cosbc, celldm)
    
    
    Defined at latgen.fpp lines 629-686
    
    Parameters
    ----------
    ibrav : int
    a : float
    b : float
    c : float
    cosab : float
    cosac : float
    cosbc : float
    celldm : float array
    
    """
    libqepy_modules.f90wrap_abc2celldm(ibrav=ibrav, a=a, b=b, c=c, cosab=cosab, \
        cosac=cosac, cosbc=cosbc, celldm=celldm)

def celldm2abc(ibrav, celldm):
    """
    a, b, c, cosab, cosac, cosbc = celldm2abc(ibrav, celldm)
    
    
    Defined at latgen.fpp lines 689-735
    
    Parameters
    ----------
    ibrav : int
    celldm : float array
    
    Returns
    -------
    a : float
    b : float
    c : float
    cosab : float
    cosac : float
    cosbc : float
    
    """
    a, b, c, cosab, cosac, cosbc = libqepy_modules.f90wrap_celldm2abc(ibrav=ibrav, \
        celldm=celldm)
    return a, b, c, cosab, cosac, cosbc

def remake_cell(ibrav, alat, a1, a2, a3):
    """
    new_alat = remake_cell(ibrav, alat, a1, a2, a3)
    
    
    Defined at latgen.fpp lines 737-788
    
    Parameters
    ----------
    ibrav : int
    alat : float
    a1 : float array
    a2 : float array
    a3 : float array
    
    Returns
    -------
    new_alat : float
    
    """
    new_alat = libqepy_modules.f90wrap_remake_cell(ibrav=ibrav, alat=alat, a1=a1, \
        a2=a2, a3=a3)
    return new_alat

def latgen(ibrav, celldm, a1, a2, a3):
    """
    omega = latgen(ibrav, celldm, a1, a2, a3)
    
    
    Defined at latgen.fpp lines 791-808
    
    Parameters
    ----------
    ibrav : int
    celldm : float array
    a1 : float array
    a2 : float array
    a3 : float array
    
    Returns
    -------
    omega : float
    
    -----------------------------------------------------------------------
    """
    omega = libqepy_modules.f90wrap_latgen(ibrav=ibrav, celldm=celldm, a1=a1, a2=a2, \
        a3=a3)
    return omega

def set_para_diag(nbnd, use_para_diag):
    """
    set_para_diag(nbnd, use_para_diag)
    
    
    Defined at set_para_diag.fpp lines 13-61
    
    Parameters
    ----------
    nbnd : int
    use_para_diag : bool
    
    -----------------------------------------------------------------------------
     Sets up the communicator used for parallel diagonalization in LAXlib.
     Merges previous code executed at startup with function "check_para_diag".
     To be called after the initialization of variables is completed and
     the dimension of matrices to be diagonalized is known
    """
    libqepy_modules.f90wrap_set_para_diag(nbnd=nbnd, use_para_diag=use_para_diag)

def plugin_arguments():
    """
    plugin_arguments()
    
    
    Defined at plugin_arguments.fpp lines 13-74
    
    
    -----------------------------------------------------------------------------
     Check for presence of command-line option "-plugin\_name" or "--plugin_name"
     where "plugin\_name" has to be set here. If such option is found, variable
     \(\text{use_plugin_name}\) is set and usage of "plugin\_name" is thus enabled.
     Currently implemented: "plumed", "pw2casino" (both case-sensitive).
    """
    libqepy_modules.f90wrap_plugin_arguments()

def plugin_arguments_bcast(root, comm):
    """
    plugin_arguments_bcast(root, comm)
    
    
    Defined at plugin_arguments.fpp lines 78-107
    
    Parameters
    ----------
    root : int
    comm : int
    
    ----------------------------------------------------------------------------
     Broadcast plugin arguments.
    """
    libqepy_modules.f90wrap_plugin_arguments_bcast(root=root, comm=comm)


mp_bands = qepy_modules.mp_bands
wy_pos = qepy_modules.wy_pos
open_close_input_file = qepy_modules.open_close_input_file
check_stop = qepy_modules.check_stop
environment = qepy_modules.environment
io_global = qepy_modules.io_global
read_input = qepy_modules.read_input
command_line_options = qepy_modules.command_line_options
gvect = qepy_modules.gvect
wavefunctions = qepy_modules.wavefunctions
funct = qepy_modules.funct
mp_global = qepy_modules.mp_global
space_group = qepy_modules.space_group
mp_bands_tddfpt = qepy_modules.mp_bands_tddfpt
wyckoff = qepy_modules.wyckoff
mp_pools = qepy_modules.mp_pools
mp_world = qepy_modules.mp_world
cell_base = qepy_modules.cell_base
mp_orthopools = qepy_modules.mp_orthopools
constants = qepy_modules.constants
gvecs = qepy_modules.gvecs
qepy_sys = qepy_modules.qepy_sys
control_flags = qepy_modules.control_flags
ions_base = qepy_modules.ions_base
qexsd_module = qepy_modules.qexsd_module
