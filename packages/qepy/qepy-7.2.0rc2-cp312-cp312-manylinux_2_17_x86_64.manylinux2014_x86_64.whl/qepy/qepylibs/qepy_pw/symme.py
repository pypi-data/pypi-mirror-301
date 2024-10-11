"""
Module symme


Defined at symme.fpp lines 13-859

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def symscalar(nat, scalar):
    """
    symscalar(nat, scalar)
    
    
    Defined at symme.fpp lines 57-80
    
    Parameters
    ----------
    nat : int
    scalar : float array
    
    -----------------------------------------------------------------------
     Symmetrize a scalar function \(f(na)\), where na is the atom index.
    """
    libqepy_pw.f90wrap_symme__symscalar(nat=nat, scalar=scalar)

def symvector(nat, vect):
    """
    symvector(nat, vect)
    
    
    Defined at symme.fpp lines 84-136
    
    Parameters
    ----------
    nat : int
    vect : float array
    
    -----------------------------------------------------------------------
     Symmetrize a function \(f(i,na)\) (e.g. the forces in cartesian axis),
     where \(i\) is the cartesian component, \(na\) the atom index.
    """
    libqepy_pw.f90wrap_symme__symvector(nat=nat, vect=vect)

def symtensor(nat, tens):
    """
    symtensor(nat, tens)
    
    
    Defined at symme.fpp lines 140-194
    
    Parameters
    ----------
    nat : int
    tens : float array
    
    -----------------------------------------------------------------------
     Symmetrize a function \(f(i,j,na)\) (e.g. the effective charges in
     cartesian axis), where \(i,j\) are the cartesian components and \(na\)
     is the atom index.
    """
    libqepy_pw.f90wrap_symme__symtensor(nat=nat, tens=tens)

def symv(vect):
    """
    symv(vect)
    
    
    Defined at symme.fpp lines 198-236
    
    Parameters
    ----------
    vect : float array
    
    --------------------------------------------------------------------
     Symmetrize a vector \(f(i)\), i=cartesian components
     The vector is supposed to be axial: inversion does not change it.
     Time reversal changes its sign. Note that only groups compatible with
     a finite magnetization give a nonzero output vector.
    """
    libqepy_pw.f90wrap_symme__symv(vect=vect)

def symmatrix(matr):
    """
    symmatrix(matr)
    
    
    Defined at symme.fpp lines 240-281
    
    Parameters
    ----------
    matr : float array
    
    -----------------------------------------------------------------------
     Symmetrize a function \(f(i,j)\) (e.g. stress, dielectric tensor in
     cartesian axis), where \(i,j\) are the cartesian components.
    """
    libqepy_pw.f90wrap_symme__symmatrix(matr=matr)

def symmatrix3(mat3):
    """
    symmatrix3(mat3)
    
    
    Defined at symme.fpp lines 285-328
    
    Parameters
    ----------
    mat3 : float array
    
    -----------------------------------------------------------------------
     Symmetrize a function \(f(i,j,k)\) (e.g. nonlinear susceptibility),
     where \(i,j,k\) are the cartesian components.
     BEWARE: input in crystal axis, output in cartesian axis.
    """
    libqepy_pw.f90wrap_symme__symmatrix3(mat3=mat3)

def symtensor3(nat, tens3):
    """
    symtensor3(nat, tens3)
    
    
    Defined at symme.fpp lines 332-386
    
    Parameters
    ----------
    nat : int
    tens3 : float array
    
    -----------------------------------------------------------------------
     Symmetrize a function \(f(i,j,k, na)\) (e.g. the Raman tensor), where
     \(i,j,k\) are the cartesian axes, \(na\) is the atom index.
     BEWARE: input in crystal axis, output in cartesian axis
    """
    libqepy_pw.f90wrap_symme__symtensor3(nat=nat, tens3=tens3)

def cart_to_crys(matr):
    """
    cart_to_crys(matr)
    
    
    Defined at symme.fpp lines 399-425
    
    Parameters
    ----------
    matr : float array
    
    -----------------------------------------------------------------------
     Cartesian to crystal axis conversion.
    """
    libqepy_pw.f90wrap_symme__cart_to_crys(matr=matr)

def crys_to_cart(matr):
    """
    crys_to_cart(matr)
    
    
    Defined at symme.fpp lines 429-455
    
    Parameters
    ----------
    matr : float array
    
    -----------------------------------------------------------------------
     Crystal to cartesian axis conversion.
    """
    libqepy_pw.f90wrap_symme__crys_to_cart(matr=matr)

def sym_rho_init(gamma_only):
    """
    sym_rho_init(gamma_only)
    
    
    Defined at symme.fpp lines 495-506
    
    Parameters
    ----------
    gamma_only : bool
    
    -----------------------------------------------------------------------
     Initialize arrays needed for symmetrization in reciprocal space.
    """
    libqepy_pw.f90wrap_symme__sym_rho_init(gamma_only=gamma_only)

def sym_rho(nspin, rhog):
    """
    sym_rho(nspin, rhog)
    
    
    Defined at symme.fpp lines 619-653
    
    Parameters
    ----------
    nspin : int
    rhog : complex array
    
    -----------------------------------------------------------------------
     Symmetrize the charge density rho in reciprocal space.
     Distributed parallel algorithm: collects entire shells of G-vectors
     and corresponding rho(G), calls sym_rho_serial to perform the
     symmetrization, re-distributed rho(G) into original ordering.
    """
    libqepy_pw.f90wrap_symme__sym_rho(nspin=nspin, rhog=rhog)

def sym_rho_deallocate():
    """
    sym_rho_deallocate()
    
    
    Defined at symme.fpp lines 840-858
    
    
    -------------------------------------------------------------------
     Deallocates symmetrization objects.
    """
    libqepy_pw.f90wrap_symme__sym_rho_deallocate()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "symme".')

for func in _dt_array_initialisers:
    func()
