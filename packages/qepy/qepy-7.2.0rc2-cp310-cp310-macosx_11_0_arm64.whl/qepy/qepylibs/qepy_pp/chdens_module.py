"""
Module chdens_module


Defined at chdens_module.fpp lines 14-1228

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def plot_1d(nx, m1, x0, e, ngm, g, rhog, alat, iflag, ounit):
    """
    plot_1d(nx, m1, x0, e, ngm, g, rhog, alat, iflag, ounit)
    
    
    Defined at chdens_module.fpp lines 527-641
    
    Parameters
    ----------
    nx : int
    m1 : float
    x0 : float array
    e : float array
    ngm : int
    g : float array
    rhog : complex array
    alat : float
    iflag : int
    ounit : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_chdens_module__plot_1d(nx=nx, m1=m1, x0=x0, e=e, ngm=ngm, \
        g=g, rhog=rhog, alat=alat, iflag=iflag, ounit=ounit)

def plot_2d(nx, ny, m1, m2, x0, e1, e2, ngm, g, rhog, alat, at, nat, tau, atm, \
    ityp, output_format, ounit):
    """
    plot_2d(nx, ny, m1, m2, x0, e1, e2, ngm, g, rhog, alat, at, nat, tau, atm, ityp, \
        output_format, ounit)
    
    
    Defined at chdens_module.fpp lines 646-774
    
    Parameters
    ----------
    nx : int
    ny : int
    m1 : float
    m2 : float
    x0 : float array
    e1 : float array
    e2 : float array
    ngm : int
    g : float array
    rhog : complex array
    alat : float
    at : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    output_format : int
    ounit : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_chdens_module__plot_2d(nx=nx, ny=ny, m1=m1, m2=m2, x0=x0, \
        e1=e1, e2=e2, ngm=ngm, g=g, rhog=rhog, alat=alat, at=at, nat=nat, tau=tau, \
        atm=atm, ityp=ityp, output_format=output_format, ounit=ounit)

def plot_2ds(nx, ny, x0, ngm, g, rhog, output_format, ounit):
    """
    plot_2ds(nx, ny, x0, ngm, g, rhog, output_format, ounit)
    
    
    Defined at chdens_module.fpp lines 778-873
    
    Parameters
    ----------
    nx : int
    ny : int
    x0 : float
    ngm : int
    g : float array
    rhog : complex array
    output_format : int
    ounit : int
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_chdens_module__plot_2ds(nx=nx, ny=ny, x0=x0, ngm=ngm, g=g, \
        rhog=rhog, output_format=output_format, ounit=ounit)

def plot_3d(alat, at, nat, tau, atm, ityp, ngm, g, rhog, nx, ny, nz, m1, m2, m3, \
    x0, e1, e2, e3, output_format, ounit, rhotot):
    """
    plot_3d(alat, at, nat, tau, atm, ityp, ngm, g, rhog, nx, ny, nz, m1, m2, m3, x0, \
        e1, e2, e3, output_format, ounit, rhotot)
    
    
    Defined at chdens_module.fpp lines 879-975
    
    Parameters
    ----------
    alat : float
    at : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    ngm : int
    g : float array
    rhog : complex array
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
    rhotot : float
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_chdens_module__plot_3d(alat=alat, at=at, nat=nat, tau=tau, \
        atm=atm, ityp=ityp, ngm=ngm, g=g, rhog=rhog, nx=nx, ny=ny, nz=nz, m1=m1, \
        m2=m2, m3=m3, x0=x0, e1=e1, e2=e2, e3=e3, output_format=output_format, \
        ounit=ounit, rhotot=rhotot)

def plot_fast(alat, at, nat, tau, atm, ityp, nr1x, nr2x, nr3x, nr1, nr2, nr3, \
    rho, bg, m1, m2, m3, x0, e1, e2, e3, output_format, ounit, rhotot):
    """
    plot_fast(alat, at, nat, tau, atm, ityp, nr1x, nr2x, nr3x, nr1, nr2, nr3, rho, \
        bg, m1, m2, m3, x0, e1, e2, e3, output_format, ounit, rhotot)
    
    
    Defined at chdens_module.fpp lines 981-1083
    
    Parameters
    ----------
    alat : float
    at : float array
    nat : int
    tau : float array
    atm : str array
    ityp : int array
    nr1x : int
    nr2x : int
    nr3x : int
    nr1 : int
    nr2 : int
    nr3 : int
    rho : float array
    bg : float array
    m1 : float
    m2 : float
    m3 : float
    x0 : float array
    e1 : float array
    e2 : float array
    e3 : float array
    output_format : int
    ounit : int
    rhotot : float
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_chdens_module__plot_fast(alat=alat, at=at, nat=nat, tau=tau, \
        atm=atm, ityp=ityp, nr1x=nr1x, nr2x=nr2x, nr3x=nr3x, nr1=nr1, nr2=nr2, \
        nr3=nr3, rho=rho, bg=bg, m1=m1, m2=m2, m3=m3, x0=x0, e1=e1, e2=e2, e3=e3, \
        output_format=output_format, ounit=ounit, rhotot=rhotot)

def isostm_plot(rhor, nr1x, nr2x, nr3x, isovalue, heightmin, heightmax, \
    direction):
    """
    isostm_plot(rhor, nr1x, nr2x, nr3x, isovalue, heightmin, heightmax, direction)
    
    
    Defined at chdens_module.fpp lines 1087-1228
    
    Parameters
    ----------
    rhor : float array
    nr1x : int
    nr2x : int
    nr3x : int
    isovalue : float
    heightmin : float
    heightmax : float
    direction : int
    
    -----------------------------------------------------------------------
       Written by Andrea Cepellotti(2011), modified by Marco Pividori(2014)
       to better interface with the postprocessing suite of QE
          This subroutine calculates 2D images of STM as isosurface of
          integrated ldos.
          It receives as input the STM charge density(that will be
          overwritten
    ) and the dimension of the grid in the real space.
          Works only for surfaces perpendicular to idir=3, searching for the
          highest isovalue found from heightmax to heightmin or viceversa
          according to the variable direction.
          DESCRIPTION of the INPUT CARD  ISOSTM :
          isovalue
    (real) value of the charge of the isosurface
     default value -> 0.0d0
          heightmin
    (real) minimum value of the plane in which searching for the isosurface
     default value -> 0.0d0
          heightmax
    (real) maximum value of the plane in which searching for the isosurface
     default value -> 1.0d0
     the two parameters above are in percentage with respect to the
     height of the cell, i.e. between 0.0 and 1.0.
     If heightmax < heightmin, it treats it as if it's in the
      upper periodically repeated slab.
     Put heightmin somewhere in the bulk and heightmax in the vacuum
          direction
    (integer) direction along z of the scan for the stm image:
     if direction = 1 generates the isosurface as seen from heightmax to heightmin
     if direction =-1 generates the isosurface as seen from heightmin to heightmax
     default value -> 1
    """
    libqepy_pp.f90wrap_chdens_module__isostm_plot(rhor=rhor, nr1x=nr1x, nr2x=nr2x, \
        nr3x=nr3x, isovalue=isovalue, heightmin=heightmin, heightmax=heightmax, \
        direction=direction)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "chdens_module".')

for func in _dt_array_initialisers:
    func()
