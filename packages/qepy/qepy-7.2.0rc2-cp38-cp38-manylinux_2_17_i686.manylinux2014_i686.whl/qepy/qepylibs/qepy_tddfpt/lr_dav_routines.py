"""
Module lr_dav_routines


Defined at lr_dav_routines.fpp lines 13-1610

"""
from __future__ import print_function, absolute_import, division
import libqepy_tddfpt
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def lr_dav_cvcouple():
    """
    lr_dav_cvcouple()
    
    
    Defined at lr_dav_routines.fpp lines 18-64
    
    
    -----------------------------------------------------------------------
      Created by Xiaochuan Ge(Oct, 2012)
    -----------------------------------------------------------------------
      This subroutine returns num_init couples of occ/virt states to be used
      as the initial vectors of lr davidson algorithm
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_dav_cvcouple()

def lr_dav_alloc_init():
    """
    lr_dav_alloc_init()
    
    
    Defined at lr_dav_routines.fpp lines 67-153
    
    
    ---------------------------------------------------------------------
     Created by X.Ge in Oct.2012
    ---------------------------------------------------------------------
     Allocates and initialises variables for lr_davidson algorithm
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_dav_alloc_init()

def lr_dav_set_init():
    """
    lr_dav_set_init()
    
    
    Defined at lr_dav_routines.fpp lines 156-212
    
    
    ---------------------------------------------------------------------
     Created by X.Ge in Jan.2013
    ---------------------------------------------------------------------
      This routine use the cvcouple and the dft wavefunction to set the
      initial sub space
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_dav_set_init()

def lr_write_restart_dav():
    """
    lr_write_restart_dav()
    
    
    Defined at lr_dav_routines.fpp lines 215-285
    
    
    ---------------------------------------------------------------------
      Created by I. Timrov in May 2014
    ---------------------------------------------------------------------
      This routine writes information for restart.
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_write_restart_dav()

def lr_restart_dav():
    """
    lr_restart_dav()
    
    
    Defined at lr_dav_routines.fpp lines 287-373
    
    
    ---------------------------------------------------------------------
      Created by I. Timrov in May 2014
    ---------------------------------------------------------------------
      This routine reads information for restart.
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_restart_dav()

def one_dav_step():
    """
    one_dav_step()
    
    
    Defined at lr_dav_routines.fpp lines 375-455
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     Non-Hermitian diagonalization
     In one david step, M_C,M_D and M_DC are first constructed; then will be
     solved rigorously; then the solution in the subspace left_M() will
     be transformed into full space left_full()
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__one_dav_step()

def solve_m_dc():
    """
    solve_m_dc()
    
    
    Defined at lr_dav_routines.fpp lines 458-525
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     Calculate matrix M_DC and solve the problem in subspace
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__solve_m_dc()

def xc_sort_array_get_order(array, n, sort_order):
    """
    xc_sort_array_get_order(array, n, sort_order)
    
    
    Defined at lr_dav_routines.fpp lines 528-552
    
    Parameters
    ----------
    array : float array
    n : int
    sort_order : int array
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     As it is self-explained by its name
     Sort the array by the distance to the reference
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__xc_sort_array_get_order(array=array, \
        n=n, sort_order=sort_order)

def dav_calc_residue():
    """
    dav_calc_residue()
    
    
    Defined at lr_dav_routines.fpp lines 555-634
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     Calculate the residue of appro. eigen vector
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__dav_calc_residue()

def dav_expan_basis():
    """
    dav_expan_basis()
    
    
    Defined at lr_dav_routines.fpp lines 637-718
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__dav_expan_basis()

def lr_mgs_orth():
    """
    lr_mgs_orth()
    
    
    Defined at lr_dav_routines.fpp lines 721-771
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     Modified GS algorithm to ortholize the new basis respect to the old basis
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_mgs_orth()

def lr_mgs_orth_pp():
    """
    lr_mgs_orth_pp()
    
    
    Defined at lr_dav_routines.fpp lines 774-813
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     After MGS, this pp routine try to exclude duplicate vectors and then
     normalize the rest
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_mgs_orth_pp()

def lr_norm(vect):
    """
    lr_norm(vect)
    
    
    Defined at lr_dav_routines.fpp lines 816-830
    
    Parameters
    ----------
    vect : complex array
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     Normalizes vect, returns vect/sqrt(<svect|vect>)
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_norm(vect=vect)

def lr_1to1orth(vect1, vect2):
    """
    lr_1to1orth(vect1, vect2)
    
    
    Defined at lr_dav_routines.fpp lines 833-846
    
    Parameters
    ----------
    vect1 : complex array
    vect2 : complex array
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     This routine calculate the components of vect1 which is "vertical" to
     vect2
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_1to1orth(vect1=vect1, vect2=vect2)

def lr_bi_1to1orth(vect1, vect2, svect2):
    """
    lr_bi_1to1orth(vect1, vect2, svect2)
    
    
    Defined at lr_dav_routines.fpp lines 849-862
    
    Parameters
    ----------
    vect1 : complex array
    vect2 : complex array
    svect2 : complex array
    
    -------------------------------------------------------------------------------
     This routine calculate the components of vect1 which is "vertical" to
     vect2. In the case of USPP, svect2 is explicitly treated as input so one
     dose need to spend time calculating it
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_bi_1to1orth(vect1=vect1, vect2=vect2, \
        svect2=svect2)

def treat_residue(vect, ieign):
    """
    treat_residue(vect, ieign)
    
    
    Defined at lr_dav_routines.fpp lines 865-890
    
    Parameters
    ----------
    vect : complex array
    ieign : int
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     This routine apply pre-condition to the residue to speed up the
     convergence
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__treat_residue(vect=vect, ieign=ieign)

def interpret_eign(message):
    """
    interpret_eign(message)
    
    
    Defined at lr_dav_routines.fpp lines 893-1025
    
    Parameters
    ----------
    message : str
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     This routine try to interpret physical information from the solution of
     casider's equation
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__interpret_eign(message=message)

def dav_calc_chi(flag_calc, ieign, ipol):
    """
    dav_calc_chi = dav_calc_chi(flag_calc, ieign, ipol)
    
    
    Defined at lr_dav_routines.fpp lines 1028-1045
    
    Parameters
    ----------
    flag_calc : str
    ieign : int
    ipol : int
    
    Returns
    -------
    dav_calc_chi : float
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Feb. 2013
    -------------------------------------------------------------------------------
     This routine calculates the CHi from the igenvector
    """
    dav_calc_chi = \
        libqepy_tddfpt.f90wrap_lr_dav_routines__dav_calc_chi(flag_calc=flag_calc, \
        ieign=ieign, ipol=ipol)
    return dav_calc_chi

def write_spectrum(message):
    """
    write_spectrum(message)
    
    
    Defined at lr_dav_routines.fpp lines 1048-1093
    
    Parameters
    ----------
    message : str
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Feb. 2013
    -------------------------------------------------------------------------------
     write the spectrum to ${prefix}.plot file
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__write_spectrum(message=message)

def func_broadening(delta):
    """
    func_broadening = func_broadening(delta)
    
    
    Defined at lr_dav_routines.fpp lines 1096-1106
    
    Parameters
    ----------
    delta : float
    
    Returns
    -------
    func_broadening : float
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Feb. 2013
    -------------------------------------------------------------------------------
     Calculate the broadening with the energy diff
    """
    func_broadening = \
        libqepy_tddfpt.f90wrap_lr_dav_routines__func_broadening(delta=delta)
    return func_broadening

def print_principle_components():
    """
    print_principle_components()
    
    
    Defined at lr_dav_routines.fpp lines 1109-1132
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Feb. 2013
    -------------------------------------------------------------------------------
     Print out the principle transition
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__print_principle_components()

def calc_inter(v1, c1, v2, c2):
    """
    calc_inter = calc_inter(v1, c1, v2, c2)
    
    
    Defined at lr_dav_routines.fpp lines 1135-1185
    
    Parameters
    ----------
    v1 : int
    c1 : int
    v2 : int
    c2 : int
    
    Returns
    -------
    calc_inter : float
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     calculate the interaction between two electron-hole pairs
    """
    calc_inter = libqepy_tddfpt.f90wrap_lr_dav_routines__calc_inter(v1=v1, c1=c1, \
        v2=v2, c2=c2)
    return calc_inter

def wfc_dot(x, y):
    """
    wfc_dot = wfc_dot(x, y)
    
    
    Defined at lr_dav_routines.fpp lines 1188-1207
    
    Parameters
    ----------
    x : complex array
    y : complex array
    
    Returns
    -------
    wfc_dot : float
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     calculate the inner product between two wfcs
    """
    wfc_dot = libqepy_tddfpt.f90wrap_lr_dav_routines__wfc_dot(x=x, y=y)
    return wfc_dot

def lr_calc_fxy(ieign):
    """
    lr_calc_fxy(ieign)
    
    
    Defined at lr_dav_routines.fpp lines 1210-1226
    
    Parameters
    ----------
    ieign : int
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jan. 2013
    -------------------------------------------------------------------------------
     This routine calculates the Fx and Fy for the ieign-th eigen vector
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_calc_fxy(ieign=ieign)

def random_init():
    """
    random_init()
    
    
    Defined at lr_dav_routines.fpp lines 1229-1284
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in May. 2013
    -------------------------------------------------------------------------------
     This routine initiate basis set with radom vectors
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__random_init()

def write_eigenvalues(message):
    """
    write_eigenvalues(message)
    
    
    Defined at lr_dav_routines.fpp lines 1287-1310
    
    Parameters
    ----------
    message : str
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Feb. 2013
    -------------------------------------------------------------------------------
     write the eigenvalues and their oscilator strength
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__write_eigenvalues(message=message)

def estimate_ram():
    """
    estimate_ram()
    
    
    Defined at lr_dav_routines.fpp lines 1313-1340
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jun. 2013
    -------------------------------------------------------------------------------
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__estimate_ram()

def lr_discharge():
    """
    lr_discharge()
    
    
    Defined at lr_dav_routines.fpp lines 1343-1469
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Jun. 2014
    -------------------------------------------------------------------------------
     This routine discharges the basis set keeping only n( num_eign <= n <= \
         2*num_eign )
     best vectors for the basis and through aways others in order to make space for \
         the
     new vectors
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__lr_discharge()

def dft_spectrum():
    """
    dft_spectrum()
    
    
    Defined at lr_dav_routines.fpp lines 1472-1529
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Aug. 2013
    -------------------------------------------------------------------------------
     This routine calculates the dft_spectrum(KS_spectrum), of which the energy
     of the peak is the KS energy difference and the oscillation strength is
     energy*|R_ij|^2
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__dft_spectrum()

def plot_drho():
    """
    plot_drho()
    
    
    Defined at lr_dav_routines.fpp lines 1532-1609
    
    
    -------------------------------------------------------------------------------
     Created by X.Ge in Aug. 2013
    -------------------------------------------------------------------------------
     This routine generates the plot file for the drho
    """
    libqepy_tddfpt.f90wrap_lr_dav_routines__plot_drho()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "lr_dav_routines".')

for func in _dt_array_initialisers:
    func()
