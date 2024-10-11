from __future__ import print_function, absolute_import, division
pname = 'libqepy_laxlib'

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
import libqepy_laxlib
import f90wrap.runtime
import logging
import numpy
import qepy_laxlib.laxlib_processors_grid

def laxlib_end():
    """
    laxlib_end()
    
    
    Defined at la_helper.fpp lines 13-16
    
    
    """
    libqepy_laxlib.f90wrap_laxlib_end()

def laxlib_getval_(nproc_ortho=None, leg_ortho=None, np_ortho=None, \
    me_ortho=None, ortho_comm=None, ortho_row_comm=None, ortho_col_comm=None, \
    ortho_comm_id=None, ortho_parent_comm=None, ortho_cntx=None, \
    do_distr_diag_inside_bgrp=None):
    """
    laxlib_getval_([nproc_ortho, leg_ortho, np_ortho, me_ortho, ortho_comm, \
        ortho_row_comm, ortho_col_comm, ortho_comm_id, ortho_parent_comm, \
        ortho_cntx, do_distr_diag_inside_bgrp])
    
    
    Defined at la_helper.fpp lines 18-53
    
    Parameters
    ----------
    nproc_ortho : int
    leg_ortho : int
    np_ortho : int array
    me_ortho : int array
    ortho_comm : int
    ortho_row_comm : int
    ortho_col_comm : int
    ortho_comm_id : int
    ortho_parent_comm : int
    ortho_cntx : int
    do_distr_diag_inside_bgrp : bool
    
    """
    libqepy_laxlib.f90wrap_laxlib_getval_(nproc_ortho=nproc_ortho, \
        leg_ortho=leg_ortho, np_ortho=np_ortho, me_ortho=me_ortho, \
        ortho_comm=ortho_comm, ortho_row_comm=ortho_row_comm, \
        ortho_col_comm=ortho_col_comm, ortho_comm_id=ortho_comm_id, \
        ortho_parent_comm=ortho_parent_comm, ortho_cntx=ortho_cntx, \
        do_distr_diag_inside_bgrp=do_distr_diag_inside_bgrp)

def laxlib_get_status_x(lax_status):
    """
    laxlib_get_status_x(lax_status)
    
    
    Defined at la_helper.fpp lines 56-88
    
    Parameters
    ----------
    lax_status : int array
    
    """
    libqepy_laxlib.f90wrap_laxlib_get_status_x(lax_status=lax_status)

def laxlib_start_drv(ndiag_, parent_comm, do_distr_diag_inside_bgrp_):
    """
    laxlib_start_drv(ndiag_, parent_comm, do_distr_diag_inside_bgrp_)
    
    
    Defined at la_helper.fpp lines 91-150
    
    Parameters
    ----------
    ndiag_ : int
    parent_comm : int
    do_distr_diag_inside_bgrp_ : bool
    
    """
    libqepy_laxlib.f90wrap_laxlib_start_drv(ndiag_=ndiag_, parent_comm=parent_comm, \
        do_distr_diag_inside_bgrp_=do_distr_diag_inside_bgrp_)

def print_lambda_x(lambda_, idesc, n, nshow, nudx, ccc, ionode, iunit):
    """
    print_lambda_x(lambda_, idesc, n, nshow, nudx, ccc, ionode, iunit)
    
    
    Defined at la_helper.fpp lines 153-181
    
    Parameters
    ----------
    lambda_ : float array
    idesc : int array
    n : int
    nshow : int
    nudx : int
    ccc : float
    ionode : bool
    iunit : int
    
    """
    libqepy_laxlib.f90wrap_print_lambda_x(lambda_=lambda_, idesc=idesc, n=n, \
        nshow=nshow, nudx=nudx, ccc=ccc, ionode=ionode, iunit=iunit)

def laxlib_init_desc_x(idesc, n, nx, np, me, comm, cntx, comm_id):
    """
    laxlib_init_desc_x(idesc, n, nx, np, me, comm, cntx, comm_id)
    
    
    Defined at la_helper.fpp lines 275-289
    
    Parameters
    ----------
    idesc : int array
    n : int
    nx : int
    np : int array
    me : int array
    comm : int
    cntx : int
    comm_id : int
    
    """
    libqepy_laxlib.f90wrap_laxlib_init_desc_x(idesc=idesc, n=n, nx=nx, np=np, me=me, \
        comm=comm, cntx=cntx, comm_id=comm_id)

def laxlib_multi_init_desc_x(idesc, idesc_ip, rank_ip, n, nx):
    """
    laxlib_multi_init_desc_x(idesc, idesc_ip, rank_ip, n, nx)
    
    
    Defined at la_helper.fpp lines 291-324
    
    Parameters
    ----------
    idesc : int array
    idesc_ip : int array
    rank_ip : int array
    n : int
    nx : int
    
    """
    libqepy_laxlib.f90wrap_laxlib_multi_init_desc_x(idesc=idesc, idesc_ip=idesc_ip, \
        rank_ip=rank_ip, n=n, nx=nx)

def descla_local_dims(n, nx, np, me):
    """
    i2g, nl = descla_local_dims(n, nx, np, me)
    
    
    Defined at la_helper.fpp lines 326-353
    
    Parameters
    ----------
    n : int
    nx : int
    np : int
    me : int
    
    Returns
    -------
    i2g : int
    nl : int
    
    """
    i2g, nl = libqepy_laxlib.f90wrap_descla_local_dims(n=n, nx=nx, np=np, me=me)
    return i2g, nl

def diagonalize_parallel_x(n, rhos, rhod, s, idesc):
    """
    diagonalize_parallel_x(n, rhos, rhod, s, idesc)
    
    
    Defined at la_helper.fpp lines 357-387
    
    Parameters
    ----------
    n : int
    rhos : float array
    rhod : float array
    s : float array
    idesc : int array
    
    """
    libqepy_laxlib.f90wrap_diagonalize_parallel_x(n=n, rhos=rhos, rhod=rhod, s=s, \
        idesc=idesc)

def diagonalize_serial_x(n, rhos, rhod):
    """
    diagonalize_serial_x(n, rhos, rhod)
    
    
    Defined at la_helper.fpp lines 389-419
    
    Parameters
    ----------
    n : int
    rhos : float array
    rhod : float array
    
    """
    libqepy_laxlib.f90wrap_diagonalize_serial_x(n=n, rhos=rhos, rhod=rhod)

def diagonalize_serial_gpu(m, rhos, rhod, s, info):
    """
    diagonalize_serial_gpu(m, rhos, rhod, s, info)
    
    
    Defined at la_helper.fpp lines 421-431
    
    Parameters
    ----------
    m : int
    rhos : float array
    rhod : float array
    s : float array
    info : int
    
    """
    libqepy_laxlib.f90wrap_diagonalize_serial_gpu(m=m, rhos=rhos, rhod=rhod, s=s, \
        info=info)


laxlib_processors_grid = qepy_laxlib.laxlib_processors_grid
