"""
Module dft_setting_routines


Defined at dft_setting_routines.fpp lines 13-1153

"""
from __future__ import print_function, absolute_import, division
import libqepy_xclib
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def xclib_set_dft_from_name(dft_):
    """
    xclib_set_dft_from_name(dft_)
    
    
    Defined at dft_setting_routines.fpp lines 41-204
    
    Parameters
    ----------
    dft_ : str
    
    -----------------------------------------------------------------------
     Translates a string containing the exchange-correlation name
     into internal indices iexch, icorr, igcx, igcc, inlc, imeta.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_dft_from_name(dft_=dft_)

def xclib_set_dft_ids(iexch_, icorr_, igcx_, igcc_, imeta_, imetac_):
    """
    xclib_set_dft_ids = xclib_set_dft_ids(iexch_, icorr_, igcx_, igcc_, imeta_, \
        imetac_)
    
    
    Defined at dft_setting_routines.fpp lines 208-234
    
    Parameters
    ----------
    iexch_ : int
    icorr_ : int
    igcx_ : int
    igcc_ : int
    imeta_ : int
    imetac_ : int
    
    Returns
    -------
    xclib_set_dft_ids : bool
    
    --------------------------------------------------------------------------------
     Set XC functional IDs. It can be easily extended to include libxc functionals
     by adding the 'is_libxc_' array as argument.
    """
    xclib_set_dft_ids = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_dft_ids(iexch_=iexch_, \
        icorr_=icorr_, igcx_=igcx_, igcc_=igcc_, imeta_=imeta_, imetac_=imetac_)
    return xclib_set_dft_ids

def xclib_set_auxiliary_flags(isnonlocc):
    """
    xclib_set_auxiliary_flags(isnonlocc)
    
    
    Defined at dft_setting_routines.fpp lines 360-435
    
    Parameters
    ----------
    isnonlocc : bool
    
    -------------------------------------------------------------------------
     Set logical flags describing the complexity of the xc functional
     define the fraction of exact exchange used by hybrid fuctionals.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_auxiliary_flags(isnonlocc=isnonlocc)

def start_exx():
    """
    start_exx()
    
    
    Defined at dft_setting_routines.fpp lines 485-491
    
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__start_exx()

def stop_exx():
    """
    stop_exx()
    
    
    Defined at dft_setting_routines.fpp lines 494-500
    
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__stop_exx()

def xclib_set_exx_fraction(exx_fraction_):
    """
    xclib_set_exx_fraction(exx_fraction_)
    
    
    Defined at dft_setting_routines.fpp lines 503-512
    
    Parameters
    ----------
    exx_fraction_ : float
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_exx_fraction(exx_fraction_=exx_fraction_)

def dft_force_hybrid(request=None):
    """
    dft_force_hybrid([request])
    
    
    Defined at dft_setting_routines.fpp lines 515-529
    
    Parameters
    ----------
    request : bool
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__dft_force_hybrid(request=request)

def exx_is_active():
    """
    exx_is_active = exx_is_active()
    
    
    Defined at dft_setting_routines.fpp lines 532-537
    
    
    Returns
    -------
    exx_is_active : bool
    
    """
    exx_is_active = libqepy_xclib.f90wrap_dft_setting_routines__exx_is_active()
    return exx_is_active

def xclib_get_exx_fraction():
    """
    xclib_get_exx_fraction = xclib_get_exx_fraction()
    
    
    Defined at dft_setting_routines.fpp lines 540-547
    
    
    Returns
    -------
    xclib_get_exx_fraction : float
    
    """
    xclib_get_exx_fraction = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_exx_fraction()
    return xclib_get_exx_fraction

def set_screening_parameter(scrparm_):
    """
    set_screening_parameter(scrparm_)
    
    
    Defined at dft_setting_routines.fpp lines 555-576
    
    Parameters
    ----------
    scrparm_ : float
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__set_screening_parameter(scrparm_=scrparm_)

def get_screening_parameter():
    """
    get_screening_parameter = get_screening_parameter()
    
    
    Defined at dft_setting_routines.fpp lines 579-586
    
    
    Returns
    -------
    get_screening_parameter : float
    
    """
    get_screening_parameter = \
        libqepy_xclib.f90wrap_dft_setting_routines__get_screening_parameter()
    return get_screening_parameter

def set_gau_parameter(gauparm_):
    """
    set_gau_parameter(gauparm_)
    
    
    Defined at dft_setting_routines.fpp lines 589-603
    
    Parameters
    ----------
    gauparm_ : float
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__set_gau_parameter(gauparm_=gauparm_)

def get_gau_parameter():
    """
    get_gau_parameter = get_gau_parameter()
    
    
    Defined at dft_setting_routines.fpp lines 606-613
    
    
    Returns
    -------
    get_gau_parameter : float
    
    """
    get_gau_parameter = \
        libqepy_xclib.f90wrap_dft_setting_routines__get_gau_parameter()
    return get_gau_parameter

def xclib_get_id(family, kindf):
    """
    xclib_get_id = xclib_get_id(family, kindf)
    
    
    Defined at dft_setting_routines.fpp lines 621-662
    
    Parameters
    ----------
    family : str
    kindf : str
    
    Returns
    -------
    xclib_get_id : int
    
    --------------------------------------------------------------------
     Get functionals index of \(\text{family}\) and \(\text{kind}\).
    """
    xclib_get_id = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_id(family=family, \
        kindf=kindf)
    return xclib_get_id

def xclib_get_name(family, kindf, name):
    """
    xclib_get_name(family, kindf, name)
    
    
    Defined at dft_setting_routines.fpp lines 666-708
    
    Parameters
    ----------
    family : str
    kindf : str
    name : str
    
    ----------------------------------------------------------------
     Gets QE name for 'family'-'kind' term of the XC functional.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_name(family=family, \
        kindf=kindf, name=name)

def xclib_dft_is_libxc(family, kindf=None):
    """
    xclib_dft_is_libxc = xclib_dft_is_libxc(family[, kindf])
    
    
    Defined at dft_setting_routines.fpp lines 712-759
    
    Parameters
    ----------
    family : str
    kindf : str
    
    Returns
    -------
    xclib_dft_is_libxc : bool
    
    -----------------------------------------------------------------
     Establish if the XC term family-kind is Libxc or not.
    """
    xclib_dft_is_libxc = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_dft_is_libxc(family=family, \
        kindf=kindf)
    return xclib_dft_is_libxc

def xclib_reset_dft():
    """
    xclib_reset_dft()
    
    
    Defined at dft_setting_routines.fpp lines 763-786
    
    
    ---------------------------------------------------------------------
     Unset DFT indexes and main parameters.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_reset_dft()

def xclib_dft_is(what):
    """
    xclib_dft_is = xclib_dft_is(what)
    
    
    Defined at dft_setting_routines.fpp lines 801-834
    
    Parameters
    ----------
    what : str
    
    Returns
    -------
    xclib_dft_is : bool
    
    ---------------------------------------------------------------------
     Find if DFT has gradient correction, meta or hybrid.
    """
    xclib_dft_is = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_dft_is(what=what)
    return xclib_dft_is

def igcc_is_lyp():
    """
    igcc_is_lyp = igcc_is_lyp()
    
    
    Defined at dft_setting_routines.fpp lines 838-844
    
    
    Returns
    -------
    igcc_is_lyp : bool
    
    """
    igcc_is_lyp = libqepy_xclib.f90wrap_dft_setting_routines__igcc_is_lyp()
    return igcc_is_lyp

def dft_has_finite_size_correction():
    """
    dft_has_finite_size_correction = dft_has_finite_size_correction()
    
    
    Defined at dft_setting_routines.fpp lines 847-853
    
    
    Returns
    -------
    dft_has_finite_size_correction : bool
    
    """
    dft_has_finite_size_correction = \
        libqepy_xclib.f90wrap_dft_setting_routines__dft_has_finite_size_correction()
    return dft_has_finite_size_correction

def xclib_set_finite_size_volume(volume):
    """
    xclib_set_finite_size_volume(volume)
    
    
    Defined at dft_setting_routines.fpp lines 856-871
    
    Parameters
    ----------
    volume : float
    
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_finite_size_volume(volume=volume)

def xclib_get_finite_size_cell_volume():
    """
    is_present, volume = xclib_get_finite_size_cell_volume()
    
    
    Defined at dft_setting_routines.fpp lines 874-885
    
    
    Returns
    -------
    is_present : bool
    volume : float
    
    """
    is_present, volume = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_finite_size_cell_volume()
    return is_present, volume

def xclib_init_libxc(xclib_nspin, domag):
    """
    xclib_init_libxc(xclib_nspin, domag)
    
    
    Defined at dft_setting_routines.fpp lines 889-903
    
    Parameters
    ----------
    xclib_nspin : int
    domag : bool
    
    ------------------------------------------------------------------------
     Initialize Libxc functionals, if present.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_init_libxc(xclib_nspin=xclib_nspin, \
        domag=domag)

def xclib_finalize_libxc():
    """
    xclib_finalize_libxc()
    
    
    Defined at dft_setting_routines.fpp lines 910-920
    
    
    ------------------------------------------------------------------------
     Finalize Libxc functionals, if present.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_finalize_libxc()

def set_libxc_ext_param(sid, i_param, param):
    """
    set_libxc_ext_param(sid, i_param, param)
    
    
    Defined at dft_setting_routines.fpp lines 924-941
    
    Parameters
    ----------
    sid : int
    i_param : int
    param : float
    
    ------------------------------------------------------------------------
     Routine to set external parameters of some Libxc functionals.
     In order to get a list and description of all the available parameters
     for a given Libxc functional you can use the \(\texttt{xclib_test}
     program with input \(\text{test}=\text{'dft-info'}\).
    """
    libqepy_xclib.f90wrap_dft_setting_routines__set_libxc_ext_param(sid=sid, \
        i_param=i_param, param=param)

def get_libxc_ext_param(sid, i_param):
    """
    get_libxc_ext_param = get_libxc_ext_param(sid, i_param)
    
    
    Defined at dft_setting_routines.fpp lines 945-960
    
    Parameters
    ----------
    sid : int
    i_param : int
    
    Returns
    -------
    get_libxc_ext_param : float
    
    --------------------------------------------------------------------------
     Get the value of the i-th external parameter of Libxc functional with
     \(ID = \text{func_id}\)
    """
    get_libxc_ext_param = \
        libqepy_xclib.f90wrap_dft_setting_routines__get_libxc_ext_param(sid=sid, \
        i_param=i_param)
    return get_libxc_ext_param

def xclib_get_dft_short():
    """
    xclib_get_dft_short = xclib_get_dft_short()
    
    
    Defined at dft_setting_routines.fpp lines 964-1022
    
    
    Returns
    -------
    xclib_get_dft_short : str
    
    ---------------------------------------------------------------------
     Get DFT name in short notation.
    """
    xclib_get_dft_short = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_dft_short()
    return xclib_get_dft_short

def xclib_get_dft_long():
    """
    xclib_get_dft_long = xclib_get_dft_long()
    
    
    Defined at dft_setting_routines.fpp lines 1027-1046
    
    
    Returns
    -------
    xclib_get_dft_long : str
    
    ---------------------------------------------------------------------
     Get DFT name in long notation.
    """
    xclib_get_dft_long = \
        libqepy_xclib.f90wrap_dft_setting_routines__xclib_get_dft_long()
    return xclib_get_dft_long

def xclib_set_threshold(family, rho_threshold_, grho_threshold_=None, \
    tau_threshold_=None):
    """
    xclib_set_threshold(family, rho_threshold_[, grho_threshold_, tau_threshold_])
    
    
    Defined at dft_setting_routines.fpp lines 1050-1092
    
    Parameters
    ----------
    family : str
    rho_threshold_ : float
    grho_threshold_ : float
    tau_threshold_ : float
    
    --------------------------------------------------------------------------
     Set input threshold for \(\text{family}\)-term of XC functional.
    """
    libqepy_xclib.f90wrap_dft_setting_routines__xclib_set_threshold(family=family, \
        rho_threshold_=rho_threshold_, grho_threshold_=grho_threshold_, \
        tau_threshold_=tau_threshold_)

def capital(in_char):
    """
    capital = capital(in_char)
    
    
    Defined at dft_setting_routines.fpp lines 1128-1151
    
    Parameters
    ----------
    in_char : str
    
    Returns
    -------
    capital : str
    
    -----------------------------------------------------------------------
     Converts character to capital if lowercase.
     Copies character to output in all other cases.
    """
    capital = libqepy_xclib.f90wrap_dft_setting_routines__capital(in_char=in_char)
    return capital


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "dft_setting_routines".')

for func in _dt_array_initialisers:
    func()
