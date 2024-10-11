"""
Module symm_base


Defined at symm_base.fpp lines 14-1319

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def inverse_s():
    """
    inverse_s()
    
    
    Defined at symm_base.fpp lines 102-125
    
    
    -----------------------------------------------------------------------
     Locate index of \(S^{-1}\).
    """
    libqepy_pw.f90wrap_symm_base__inverse_s()

def set_sym_bl():
    """
    set_sym_bl()
    
    
    Defined at symm_base.fpp lines 130-352
    
    
    ---------------------------------------------------------------------
     Provides symmetry operations for all bravais lattices.
     Tests the 24 proper rotations for the cubic lattice first, then
     the 8 rotations specific for the hexagonal axis(special axis c),
     then inversion is added.
    """
    libqepy_pw.f90wrap_symm_base__set_sym_bl()

def find_sym(nat, tau, ityp, magnetic_sym, m_loc, no_z_inv=None):
    """
    find_sym(nat, tau, ityp, magnetic_sym, m_loc[, no_z_inv])
    
    
    Defined at symm_base.fpp lines 357-435
    
    Parameters
    ----------
    nat : int
    tau : float array
    ityp : int array
    magnetic_sym : bool
    m_loc : float array
    no_z_inv : bool
    
    -----------------------------------------------------------------------
     This routine finds the point group of the crystal, by eliminating
     the symmetries of the Bravais lattice which are not allowed
     by the atomic positions(or by the magnetization if present).
    """
    libqepy_pw.f90wrap_symm_base__find_sym(nat=nat, tau=tau, ityp=ityp, \
        magnetic_sym=magnetic_sym, m_loc=m_loc, no_z_inv=no_z_inv)

def set_sym(nat, tau, ityp, nspin_mag, m_loc):
    """
    set_sym(nat, tau, ityp, nspin_mag, m_loc)
    
    
    Defined at symm_base.fpp lines 703-732
    
    Parameters
    ----------
    nat : int
    tau : float array
    ityp : int array
    nspin_mag : int
    m_loc : float array
    
    -----------------------------------------------------------------------
     This routine receives as input atomic types and positions, if there
     is noncollinear magnetism and the initial magnetic moments
     it sets the symmetry elements of this module.
     Note that \(at\) and \(bg\) are those in \(\textrm{cell_base}\). It sets nrot, \
         nsym, s,
     sname, sr, invs, ft, irt, t_rev,  time_reversal, and invsym.
    """
    libqepy_pw.f90wrap_symm_base__set_sym(nat=nat, tau=tau, ityp=ityp, \
        nspin_mag=nspin_mag, m_loc=m_loc)

def copy_sym(nrot_, sym):
    """
    copy_sym = copy_sym(nrot_, sym)
    
    
    Defined at symm_base.fpp lines 737-799
    
    Parameters
    ----------
    nrot_ : int
    sym : bool array
    
    Returns
    -------
    copy_sym : int
    
    -----------------------------------------------------------------------
     Copy symmetry operations in sequential order so that:
     * \(s(i,j,\text{irot})\), with \(\text{irot} \leq \text{nsym}\) are the symmetry
       operations of the crystal;
     * \(s(i,j,\text{irot})\), with \(\text{nsym}+1<\text{irot}\leq \text{nrot}\) are
       the symmetry operations of the lattice.
     On exit \(\textrm{copy_sym}\) returns nsym.
    """
    copy_sym = libqepy_pw.f90wrap_symm_base__copy_sym(nrot_=nrot_, sym=sym)
    return copy_sym

def checkallsym(nat, tau, ityp):
    """
    checkallsym(nat, tau, ityp)
    
    
    Defined at symm_base.fpp lines 921-1002
    
    Parameters
    ----------
    nat : int
    tau : float array
    ityp : int array
    
    -----------------------------------------------------------------------
     Given a crystal group this routine checks that the actual atomic
     positions and bravais lattice vectors are compatible with it.
     Used in relaxation/MD runs to check that atomic motion is
     consistent with assumed symmetry.
    """
    libqepy_pw.f90wrap_symm_base__checkallsym(nat=nat, tau=tau, ityp=ityp)

def s_axis_to_cart():
    """
    s_axis_to_cart()
    
    
    Defined at symm_base.fpp lines 1007-1022
    
    
    ----------------------------------------------------------------------
     This routine transforms symmetry matrices expressed in the
     basis of the crystal axis into rotations in cartesian axis.
    """
    libqepy_pw.f90wrap_symm_base__s_axis_to_cart()

def find_sym_ifc(nat, tau, ityp):
    """
    find_sym_ifc(nat, tau, ityp)
    
    
    Defined at symm_base.fpp lines 1027-1067
    
    Parameters
    ----------
    nat : int
    tau : float array
    ityp : int array
    
    -----------------------------------------------------------------------
     This routine finds the point group of the crystal, by eliminating
     the symmetries of the Bravais lattice which are not allowed
     by the atomic positions(for use in the FD package).
    """
    libqepy_pw.f90wrap_symm_base__find_sym_ifc(nat=nat, tau=tau, ityp=ityp)

def check_grid_sym(nr1, nr2, nr3):
    """
    compatible = check_grid_sym(nr1, nr2, nr3)
    
    
    Defined at symm_base.fpp lines 1190-1218
    
    Parameters
    ----------
    nr1 : int
    nr2 : int
    nr3 : int
    
    Returns
    -------
    compatible : bool
    
    ---------------------------------------------------------------------
     Check that symmetry operations and FFT grid are compatible
     Needed to prevent trouble with real-space symmetrization
    """
    compatible = libqepy_pw.f90wrap_symm_base__check_grid_sym(nr1=nr1, nr2=nr2, \
        nr3=nr3)
    return compatible

def remove_sym(nr1, nr2, nr3):
    """
    remove_sym(nr1, nr2, nr3)
    
    
    Defined at symm_base.fpp lines 1222-1291
    
    Parameters
    ----------
    nr1 : int
    nr2 : int
    nr3 : int
    
    ---------------------------------------------------------------------
     Compute ftau used for symmetrization in real space(phonon, exx)
     ensure that they are commensurated with the FFT grid.
    """
    libqepy_pw.f90wrap_symm_base__remove_sym(nr1=nr1, nr2=nr2, nr3=nr3)

def get_array_s():
    """
    Element s ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 37
    
    """
    global s
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__s(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        s = _arrays[array_handle]
    else:
        s = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__s)
        _arrays[array_handle] = s
    return s

def set_array_s(s):
    globals()['s'][...] = s

def get_array_invs():
    """
    Element invs ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 39
    
    """
    global invs
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__invs(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        invs = _arrays[array_handle]
    else:
        invs = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__invs)
        _arrays[array_handle] = invs
    return invs

def set_array_invs(invs):
    globals()['invs'][...] = invs

def get_array_fft_fact():
    """
    Element fft_fact ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 41
    
    """
    global fft_fact
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__fft_fact(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fft_fact = _arrays[array_handle]
    else:
        fft_fact = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__fft_fact)
        _arrays[array_handle] = fft_fact
    return fft_fact

def set_array_fft_fact(fft_fact):
    globals()['fft_fact'][...] = fft_fact

def get_nrot():
    """
    Element nrot ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 43
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nrot()

def set_nrot(nrot):
    libqepy_pw.f90wrap_symm_base__set__nrot(nrot)

def get_spacegroup():
    """
    Element spacegroup ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 45
    
    """
    return libqepy_pw.f90wrap_symm_base__get__spacegroup()

def set_spacegroup(spacegroup):
    libqepy_pw.f90wrap_symm_base__set__spacegroup(spacegroup)

def get_nsym():
    """
    Element nsym ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 47
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nsym()

def set_nsym(nsym):
    libqepy_pw.f90wrap_symm_base__set__nsym(nsym)

def get_nsym_ns():
    """
    Element nsym_ns ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 49
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nsym_ns()

def set_nsym_ns(nsym_ns):
    libqepy_pw.f90wrap_symm_base__set__nsym_ns(nsym_ns)

def get_nsym_na():
    """
    Element nsym_na ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 51
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nsym_na()

def set_nsym_na(nsym_na):
    libqepy_pw.f90wrap_symm_base__set__nsym_na(nsym_na)

def get_array_ft():
    """
    Element ft ftype=real(dp) pytype=float
    
    
    Defined at symm_base.fpp line 54
    
    """
    global ft
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__ft(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ft = _arrays[array_handle]
    else:
        ft = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__ft)
        _arrays[array_handle] = ft
    return ft

def set_array_ft(ft):
    globals()['ft'][...] = ft

def get_array_sr():
    """
    Element sr ftype=real(dp) pytype=float
    
    
    Defined at symm_base.fpp line 56
    
    """
    global sr
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__sr(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sr = _arrays[array_handle]
    else:
        sr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__sr)
        _arrays[array_handle] = sr
    return sr

def set_array_sr(sr):
    globals()['sr'][...] = sr

def get_array_sname():
    """
    Element sname ftype=character(len=45) pytype=str
    
    
    Defined at symm_base.fpp line 62
    
    """
    global sname
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__sname(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sname = _arrays[array_handle]
    else:
        sname = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__sname)
        _arrays[array_handle] = sname
    return sname

def set_array_sname(sname):
    globals()['sname'][...] = sname

def get_array_t_rev():
    """
    Element t_rev ftype=integer  pytype=int
    
    
    Defined at symm_base.fpp line 64
    
    """
    global t_rev
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__t_rev(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        t_rev = _arrays[array_handle]
    else:
        t_rev = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__t_rev)
        _arrays[array_handle] = t_rev
    return t_rev

def set_array_t_rev(t_rev):
    globals()['t_rev'][...] = t_rev

def get_array_irt():
    """
    Element irt ftype=integer pytype=int
    
    
    Defined at symm_base.fpp line 66
    
    """
    global irt
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__irt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        irt = _arrays[array_handle]
    else:
        irt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__irt)
        _arrays[array_handle] = irt
    return irt

def set_array_irt(irt):
    globals()['irt'][...] = irt

def get_time_reversal():
    """
    Element time_reversal ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 68
    
    """
    return libqepy_pw.f90wrap_symm_base__get__time_reversal()

def set_time_reversal(time_reversal):
    libqepy_pw.f90wrap_symm_base__set__time_reversal(time_reversal)

def get_invsym():
    """
    Element invsym ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 70
    
    """
    return libqepy_pw.f90wrap_symm_base__get__invsym()

def set_invsym(invsym):
    libqepy_pw.f90wrap_symm_base__set__invsym(invsym)

def get_nofrac():
    """
    Element nofrac ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 72
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nofrac()

def set_nofrac(nofrac):
    libqepy_pw.f90wrap_symm_base__set__nofrac(nofrac)

def get_allfrac():
    """
    Element allfrac ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 74
    
    """
    return libqepy_pw.f90wrap_symm_base__get__allfrac()

def set_allfrac(allfrac):
    libqepy_pw.f90wrap_symm_base__set__allfrac(allfrac)

def get_nosym():
    """
    Element nosym ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 77
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nosym()

def set_nosym(nosym):
    libqepy_pw.f90wrap_symm_base__set__nosym(nosym)

def get_nosym_evc():
    """
    Element nosym_evc ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 79
    
    """
    return libqepy_pw.f90wrap_symm_base__get__nosym_evc()

def set_nosym_evc(nosym_evc):
    libqepy_pw.f90wrap_symm_base__set__nosym_evc(nosym_evc)

def get_no_t_rev():
    """
    Element no_t_rev ftype=logical pytype=bool
    
    
    Defined at symm_base.fpp line 82
    
    """
    return libqepy_pw.f90wrap_symm_base__get__no_t_rev()

def set_no_t_rev(no_t_rev):
    libqepy_pw.f90wrap_symm_base__set__no_t_rev(no_t_rev)

def get_array_d1():
    """
    Element d1 ftype=real(dp) pytype=float
    
    
    Defined at symm_base.fpp line 85
    
    """
    global d1
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__d1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d1 = _arrays[array_handle]
    else:
        d1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__d1)
        _arrays[array_handle] = d1
    return d1

def set_array_d1(d1):
    globals()['d1'][...] = d1

def get_array_d2():
    """
    Element d2 ftype=real(dp) pytype=float
    
    
    Defined at symm_base.fpp line 87
    
    """
    global d2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__d2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d2 = _arrays[array_handle]
    else:
        d2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__d2)
        _arrays[array_handle] = d2
    return d2

def set_array_d2(d2):
    globals()['d2'][...] = d2

def get_array_d3():
    """
    Element d3 ftype=real(dp) pytype=float
    
    
    Defined at symm_base.fpp line 89
    
    """
    global d3
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_symm_base__array__d3(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d3 = _arrays[array_handle]
    else:
        d3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_symm_base__array__d3)
        _arrays[array_handle] = d3
    return d3

def set_array_d3(d3):
    globals()['d3'][...] = d3


_array_initialisers = [get_array_s, get_array_invs, get_array_fft_fact, \
    get_array_ft, get_array_sr, get_array_sname, get_array_t_rev, get_array_irt, \
    get_array_d1, get_array_d2, get_array_d3]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "symm_base".')

for func in _dt_array_initialisers:
    func()
