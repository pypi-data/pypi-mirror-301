"""
Module extrapolation


Defined at update_pot.fpp lines 15-957

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def update_file():
    """
    update_file()
    
    
    Defined at update_pot.fpp lines 39-91
    
    
    ----------------------------------------------------------------------------
     Reads, updates and rewrites the file containing atomic positions at
     two previous steps, used by potential and wavefunction extrapolation.
     Requires the number of atoms(nat), current atomic positions(tau).
     Produces the length of history and tau at current and two previous steps
     written to file $prefix.update.
    """
    libqepy_pw.f90wrap_extrapolation__update_file()

def update_neb():
    """
    update_neb()
    
    
    Defined at update_pot.fpp lines 95-194
    
    
    ----------------------------------------------------------------------------
     Potential and wavefunction extrapolation for NEB.
     Prepares file with previous steps for usage by \(\texttt{update_pot}\).
     ... Must be merged soon with update_file for MD in PWscf.
    """
    libqepy_pw.f90wrap_extrapolation__update_neb()

def update_pot():
    """
    update_pot()
    
    
    Defined at update_pot.fpp lines 198-371
    
    
    ----------------------------------------------------------------------------
     Update the potential by extrapolating the charge density and extrapolates
     the wave-functions.
     Charge density extrapolation:
     * pot_order=0 \(\rightarrow\) copy the old potential(nothing is done);
     * pot_order=1 \(\rightarrow\) subtract old atomic charge density and sum
                                   the new if dynamics is done the routine
                                   extrapolates also the difference between
                                   the scf charge and the atomic one;
     * pot_order=2 \(\rightarrow\) first order extrapolation:
                                   \[ \rho(t+dt) =
                                      2\ \rho(t)-\rho(t-dt); \]
     * pot_order=3 \(\rightarrow\) second order extrapolation:
                                   \[ \rho(t+dt) = \rho(t) + \alpha_0\ (\rho(t)
                                      -\rho(t-dt)) + \beta_0\ (\rho(t-dt)-
                                       \rho(t-2 dt)). \]
     Wave-function extrapolation:
     * wfc_order = 0 \(\rightarrow\) nothing is done;
     * wfc_order = 2 \(\rightarrow\) first order extrapolation:
                                     \[ |\psi(t+dt)\rangle = 2\ |\psi(t)\rangle-
                                     |\psi(t-dt)\rangle; \]
     * wfc_order = 3 \(\rightarrow\) second order extrapolation:
                                     \[ |\psi(t+dt)\rangle = |\psi(t)\rangle
                                   + \alpha_0\ ( |\psi(t)\rangle - |\psi(t-dt)\rangle)
                                   + \beta_0\ ( |\psi(t-dt)\rangle - |\psi(t-2 dt)\rangle). \]
     The \(\alpha_0\) and \(\beta_0\) parameters are calculated in \
         \(\texttt{find_alpha_and_beta}\)
     so that \(|\tau'-\tau(t+dt)|\) is minimum. \(\tau'\) and \(\tau(t+dt)\) are \
         respectively
     the atomic positions at time t+dt and the extrapolated one:
     \[ \tau(t+dt) = \tau(t) + \alpha_0\ ( \tau(t)    - \tau(t-dt)   )
                             + \beta_0\ ( \tau(t-dt) - \tau(t-2 dt) ). \]
    """
    libqepy_pw.f90wrap_extrapolation__update_pot()

def extrapolate_charge(dirname, rho_extr):
    """
    extrapolate_charge(dirname, rho_extr)
    
    
    Defined at update_pot.fpp lines 375-610
    
    Parameters
    ----------
    dirname : str
    rho_extr : int
    
    ----------------------------------------------------------------------------
     Charge density extrapolation.
    """
    libqepy_pw.f90wrap_extrapolation__extrapolate_charge(dirname=dirname, \
        rho_extr=rho_extr)

def get_pot_order():
    """
    Element pot_order ftype=integer  pytype=int
    
    
    Defined at update_pot.fpp line 27
    
    """
    return libqepy_pw.f90wrap_extrapolation__get__pot_order()

def set_pot_order(pot_order):
    libqepy_pw.f90wrap_extrapolation__set__pot_order(pot_order)

def get_wfc_order():
    """
    Element wfc_order ftype=integer  pytype=int
    
    
    Defined at update_pot.fpp line 29
    
    """
    return libqepy_pw.f90wrap_extrapolation__get__wfc_order()

def set_wfc_order(wfc_order):
    libqepy_pw.f90wrap_extrapolation__set__wfc_order(wfc_order)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "extrapolation".')

for func in _dt_array_initialisers:
    func()
