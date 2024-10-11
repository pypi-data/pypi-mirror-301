"""
Module vdw_df_scale


Defined at xc_vdW_scale_mod.fpp lines 10-439

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def fs(s):
    """
    fs = fs(s)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 32-37
    
    Parameters
    ----------
    s : float
    
    Returns
    -------
    fs : float
    
    """
    fs = libqepy_pp.f90wrap_vdw_df_scale__fs(s=s)
    return fs

def kf(rho):
    """
    kf = kf(rho)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 39-42
    
    Parameters
    ----------
    rho : float
    
    Returns
    -------
    kf : float
    
    """
    kf = libqepy_pp.f90wrap_vdw_df_scale__kf(rho=rho)
    return kf

def saturate_q(q, q_cutoff):
    """
    q0, dq0_dq = saturate_q(q, q_cutoff)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 44-60
    
    Parameters
    ----------
    q : float
    q_cutoff : float
    
    Returns
    -------
    q0 : float
    dq0_dq : float
    
    """
    q0, dq0_dq = libqepy_pp.f90wrap_vdw_df_scale__saturate_q(q=q, q_cutoff=q_cutoff)
    return q0, dq0_dq

def xc_vdw_df_ncc(cc, lecnl_qx, etcnlccc):
    """
    xc_vdw_df_ncc(cc, lecnl_qx, etcnlccc)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 66-136
    
    Parameters
    ----------
    cc : float
    lecnl_qx : bool
    etcnlccc : float
    
    """
    libqepy_pp.f90wrap_vdw_df_scale__xc_vdw_df_ncc(cc=cc, lecnl_qx=lecnl_qx, \
        etcnlccc=etcnlccc)

def xc_vdw_df_spin_ncc(cc, lecnl_qx, etcnlccc):
    """
    xc_vdw_df_spin_ncc(cc, lecnl_qx, etcnlccc)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 145-235
    
    Parameters
    ----------
    cc : float
    lecnl_qx : bool
    etcnlccc : float
    
    """
    libqepy_pp.f90wrap_vdw_df_scale__xc_vdw_df_spin_ncc(cc=cc, lecnl_qx=lecnl_qx, \
        etcnlccc=etcnlccc)

def get_q0cc_on_grid(cc, lecnl_qx, total_rho, grad_rho, q0, thetas):
    """
    get_q0cc_on_grid(cc, lecnl_qx, total_rho, grad_rho, q0, thetas)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 247-322
    
    Parameters
    ----------
    cc : float
    lecnl_qx : bool
    total_rho : float array
    grad_rho : float array
    q0 : float array
    thetas : complex array
    
    """
    libqepy_pp.f90wrap_vdw_df_scale__get_q0cc_on_grid(cc=cc, lecnl_qx=lecnl_qx, \
        total_rho=total_rho, grad_rho=grad_rho, q0=q0, thetas=thetas)

def get_q0cc_on_grid_spin(cc, lecnl_qx, total_rho, rho_up, rho_down, grad_rho, \
    grad_rho_up, grad_rho_down, q0, thetas):
    """
    get_q0cc_on_grid_spin(cc, lecnl_qx, total_rho, rho_up, rho_down, grad_rho, \
        grad_rho_up, grad_rho_down, q0, thetas)
    
    
    Defined at xc_vdW_scale_mod.fpp lines 329-439
    
    Parameters
    ----------
    cc : float
    lecnl_qx : bool
    total_rho : float array
    rho_up : float array
    rho_down : float array
    grad_rho : float array
    grad_rho_up : float array
    grad_rho_down : float array
    q0 : float array
    thetas : complex array
    
    """
    libqepy_pp.f90wrap_vdw_df_scale__get_q0cc_on_grid_spin(cc=cc, lecnl_qx=lecnl_qx, \
        total_rho=total_rho, rho_up=rho_up, rho_down=rho_down, grad_rho=grad_rho, \
        grad_rho_up=grad_rho_up, grad_rho_down=grad_rho_down, q0=q0, thetas=thetas)

def get_epsr():
    """
    Element epsr ftype=real(dp) pytype=float
    
    
    Defined at xc_vdW_scale_mod.fpp line 30
    
    """
    return libqepy_pp.f90wrap_vdw_df_scale__get__epsr()

epsr = get_epsr()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "vdw_df_scale".')

for func in _dt_array_initialisers:
    func()
