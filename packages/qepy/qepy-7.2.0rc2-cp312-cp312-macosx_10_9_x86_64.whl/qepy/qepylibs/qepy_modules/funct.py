"""
Module funct


Defined at funct.fpp lines 13-964

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def set_dft_from_name(dft_):
    """
    set_dft_from_name(dft_)
    
    
    Defined at funct.fpp lines 340-590
    
    Parameters
    ----------
    dft_ : str
    
    -----------------------------------------------------------------------
     It sets the dft functional IDs and parameters from the input name. It
     directly calls the XClib routines and functions to set the LDA, GGA,
     MGGA terms(but not the non-local one).
    """
    libqepy_modules.f90wrap_funct__set_dft_from_name(dft_=dft_)

def enforce_input_dft(dft_, nomsg=None):
    """
    enforce_input_dft(dft_[, nomsg])
    
    
    Defined at funct.fpp lines 630-658
    
    Parameters
    ----------
    dft_ : str
    nomsg : bool
    
    ---------------------------------------------------------------------
     Translates a string containing the exchange-correlation name
     into internal indices and force any subsequent call to
     \(\textrm{set_dft_from_name}\) to return without changing them.
    """
    libqepy_modules.f90wrap_funct__enforce_input_dft(dft_=dft_, nomsg=nomsg)

def get_inlc():
    """
    get_inlc = get_inlc()
    
    
    Defined at funct.fpp lines 663-667
    
    
    Returns
    -------
    get_inlc : int
    
    """
    get_inlc = libqepy_modules.f90wrap_funct__get_inlc()
    return get_inlc

def get_nonlocc_name():
    """
    get_nonlocc_name = get_nonlocc_name()
    
    
    Defined at funct.fpp lines 670-674
    
    
    Returns
    -------
    get_nonlocc_name : str
    
    """
    get_nonlocc_name = libqepy_modules.f90wrap_funct__get_nonlocc_name()
    return get_nonlocc_name

def dft_is_nonlocc():
    """
    dft_is_nonlocc = dft_is_nonlocc()
    
    
    Defined at funct.fpp lines 677-681
    
    
    Returns
    -------
    dft_is_nonlocc : bool
    
    """
    dft_is_nonlocc = libqepy_modules.f90wrap_funct__dft_is_nonlocc()
    return dft_is_nonlocc

def get_dft_name():
    """
    get_dft_name = get_dft_name()
    
    
    Defined at funct.fpp lines 686-690
    
    
    Returns
    -------
    get_dft_name : str
    
    """
    get_dft_name = libqepy_modules.f90wrap_funct__get_dft_name()
    return get_dft_name

def set_dft_from_indices(iexch_, icorr_, igcx_, igcc_, imeta_, inlc_):
    """
    set_dft_from_indices(iexch_, icorr_, igcx_, igcc_, imeta_, inlc_)
    
    
    Defined at funct.fpp lines 695-763
    
    Parameters
    ----------
    iexch_ : int
    icorr_ : int
    igcx_ : int
    igcc_ : int
    imeta_ : int
    inlc_ : int
    
    --------------------------------------------------------------------
     Set dft functional from the IDs of each term - OBSOLESCENT:
     for compatibility with old PPs only, metaGGA not accounted for
    """
    libqepy_modules.f90wrap_funct__set_dft_from_indices(iexch_=iexch_, \
        icorr_=icorr_, igcx_=igcx_, igcc_=igcc_, imeta_=imeta_, inlc_=inlc_)

def get_dft_short():
    """
    get_dft_short = get_dft_short()
    
    
    Defined at funct.fpp lines 768-860
    
    
    Returns
    -------
    get_dft_short : str
    
    ---------------------------------------------------------------------
     It gets a short version(if exists) of the name of the dft in use.
     If there is no non-local term directly calls the xclib analogous
     routine(\(\texttt{xclib_get_dft_short}\)).
    """
    get_dft_short = libqepy_modules.f90wrap_funct__get_dft_short()
    return get_dft_short

def get_dft_long():
    """
    get_dft_long = get_dft_long()
    
    
    Defined at funct.fpp lines 865-881
    
    
    Returns
    -------
    get_dft_long : str
    
    ---------------------------------------------------------------------
     Returns a string containing the name of each term of the dft functional.
    """
    get_dft_long = libqepy_modules.f90wrap_funct__get_dft_long()
    return get_dft_long

def write_dft_name():
    """
    write_dft_name()
    
    
    Defined at funct.fpp lines 886-906
    
    
    -----------------------------------------------------------------------
     Print on output the name of each term of the dft functional.
    """
    libqepy_modules.f90wrap_funct__write_dft_name()

def nlc(rho_valence, rho_core, nspin, enl, vnl, v):
    """
    nlc(rho_valence, rho_core, nspin, enl, vnl, v)
    
    
    Defined at funct.fpp lines 915-962
    
    Parameters
    ----------
    rho_valence : float array
    rho_core : float array
    nspin : int
    enl : float
    vnl : float
    v : float array
    
    -----------------------------------------------------------------------
     Non-local contribution to the correlation energy.
         input      :  rho_valence, rho_core
         definition :  E_nl = \int E_nl(rho',grho',rho'',grho'',|r'-r''|) dr
         output     :  enl = E^nl_c
                       vnl = D(E^nl_c)/D(rho)
                       v   = non-local contribution to the potential
    """
    libqepy_modules.f90wrap_funct__nlc(rho_valence=rho_valence, rho_core=rho_core, \
        nspin=nspin, enl=enl, vnl=vnl, v=v)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "funct".')

for func in _dt_array_initialisers:
    func()
