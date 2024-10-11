"""
Module cell_base


Defined at cell_base.fpp lines 13-1079

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy_modules.boxdimensions")
class boxdimensions(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=boxdimensions)
    
    
    Defined at cell_base.fpp lines 65-88
    
    """
    def __init__(self, handle=None):
        """
        self = Boxdimensions()
        
        
        Defined at cell_base.fpp lines 65-88
        
        
        Returns
        -------
        this : Boxdimensions
        	Object to be constructed
        
        
        Automatically generated constructor for boxdimensions
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_modules.f90wrap_cell_base__boxdimensions_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Boxdimensions
        
        
        Defined at cell_base.fpp lines 65-88
        
        Parameters
        ----------
        this : Boxdimensions
        	Object to be destructed
        
        
        Automatically generated destructor for boxdimensions
        """
        if self._alloc:
            libqepy_modules.f90wrap_cell_base__boxdimensions_finalise(this=self._handle)
    
    @property
    def a(self):
        """
        Element a ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 68
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__a(self._handle)
        if array_handle in self._arrays:
            a = self._arrays[array_handle]
        else:
            a = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__a)
            self._arrays[array_handle] = a
        return a
    
    @a.setter
    def a(self, a):
        self.a[...] = a
    
    @property
    def m1(self):
        """
        Element m1 ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 70
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__m1(self._handle)
        if array_handle in self._arrays:
            m1 = self._arrays[array_handle]
        else:
            m1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__m1)
            self._arrays[array_handle] = m1
        return m1
    
    @m1.setter
    def m1(self, m1):
        self.m1[...] = m1
    
    @property
    def omega(self):
        """
        Element omega ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 72
        
        """
        return libqepy_modules.f90wrap_boxdimensions__get__omega(self._handle)
    
    @omega.setter
    def omega(self, omega):
        libqepy_modules.f90wrap_boxdimensions__set__omega(self._handle, omega)
    
    @property
    def g(self):
        """
        Element g ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 74
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__g(self._handle)
        if array_handle in self._arrays:
            g = self._arrays[array_handle]
        else:
            g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__g)
            self._arrays[array_handle] = g
        return g
    
    @g.setter
    def g(self, g):
        self.g[...] = g
    
    @property
    def gvel(self):
        """
        Element gvel ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 76
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__gvel(self._handle)
        if array_handle in self._arrays:
            gvel = self._arrays[array_handle]
        else:
            gvel = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__gvel)
            self._arrays[array_handle] = gvel
        return gvel
    
    @gvel.setter
    def gvel(self, gvel):
        self.gvel[...] = gvel
    
    @property
    def pail(self):
        """
        Element pail ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 78
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__pail(self._handle)
        if array_handle in self._arrays:
            pail = self._arrays[array_handle]
        else:
            pail = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__pail)
            self._arrays[array_handle] = pail
        return pail
    
    @pail.setter
    def pail(self, pail):
        self.pail[...] = pail
    
    @property
    def paiu(self):
        """
        Element paiu ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 80
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__paiu(self._handle)
        if array_handle in self._arrays:
            paiu = self._arrays[array_handle]
        else:
            paiu = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__paiu)
            self._arrays[array_handle] = paiu
        return paiu
    
    @paiu.setter
    def paiu(self, paiu):
        self.paiu[...] = paiu
    
    @property
    def hmat(self):
        """
        Element hmat ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 82
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__hmat(self._handle)
        if array_handle in self._arrays:
            hmat = self._arrays[array_handle]
        else:
            hmat = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__hmat)
            self._arrays[array_handle] = hmat
        return hmat
    
    @hmat.setter
    def hmat(self, hmat):
        self.hmat[...] = hmat
    
    @property
    def hvel(self):
        """
        Element hvel ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 84
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__hvel(self._handle)
        if array_handle in self._arrays:
            hvel = self._arrays[array_handle]
        else:
            hvel = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__hvel)
            self._arrays[array_handle] = hvel
        return hvel
    
    @hvel.setter
    def hvel(self, hvel):
        self.hvel[...] = hvel
    
    @property
    def hinv(self):
        """
        Element hinv ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 86
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__hinv(self._handle)
        if array_handle in self._arrays:
            hinv = self._arrays[array_handle]
        else:
            hinv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__hinv)
            self._arrays[array_handle] = hinv
        return hinv
    
    @hinv.setter
    def hinv(self, hinv):
        self.hinv[...] = hinv
    
    @property
    def deth(self):
        """
        Element deth ftype=real(dp) pytype=float
        
        
        Defined at cell_base.fpp line 87
        
        """
        return libqepy_modules.f90wrap_boxdimensions__get__deth(self._handle)
    
    @deth.setter
    def deth(self, deth):
        libqepy_modules.f90wrap_boxdimensions__set__deth(self._handle, deth)
    
    @property
    def perd(self):
        """
        Element perd ftype=integer  pytype=int
        
        
        Defined at cell_base.fpp line 88
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_modules.f90wrap_boxdimensions__array__perd(self._handle)
        if array_handle in self._arrays:
            perd = self._arrays[array_handle]
        else:
            perd = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_modules.f90wrap_boxdimensions__array__perd)
            self._arrays[array_handle] = perd
        return perd
    
    @perd.setter
    def perd(self, perd):
        self.perd[...] = perd
    
    def __str__(self):
        ret = ['<boxdimensions>{\n']
        ret.append('    a : ')
        ret.append(repr(self.a))
        ret.append(',\n    m1 : ')
        ret.append(repr(self.m1))
        ret.append(',\n    omega : ')
        ret.append(repr(self.omega))
        ret.append(',\n    g : ')
        ret.append(repr(self.g))
        ret.append(',\n    gvel : ')
        ret.append(repr(self.gvel))
        ret.append(',\n    pail : ')
        ret.append(repr(self.pail))
        ret.append(',\n    paiu : ')
        ret.append(repr(self.paiu))
        ret.append(',\n    hmat : ')
        ret.append(repr(self.hmat))
        ret.append(',\n    hvel : ')
        ret.append(repr(self.hvel))
        ret.append(',\n    hinv : ')
        ret.append(repr(self.hinv))
        ret.append(',\n    deth : ')
        ret.append(repr(self.deth))
        ret.append(',\n    perd : ')
        ret.append(repr(self.perd))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def cell_base_init(ibrav_, celldm_, a_, b_, c_, cosab_, cosac_, cosbc_, trd_ht, \
    rd_ht, cell_units_):
    """
    cell_base_init(ibrav_, celldm_, a_, b_, c_, cosab_, cosac_, cosbc_, trd_ht, \
        rd_ht, cell_units_)
    
    
    Defined at cell_base.fpp lines 148-271
    
    Parameters
    ----------
    ibrav_ : int
    celldm_ : float array
    a_ : float
    b_ : float
    c_ : float
    cosab_ : float
    cosac_ : float
    cosbc_ : float
    trd_ht : bool
    rd_ht : float array
    cell_units_ : str
    
    -----------------------------------------------------------------------------
     Initialize cell_base module variables, set up crystal lattice.
    """
    libqepy_modules.f90wrap_cell_base__cell_base_init(ibrav_=ibrav_, \
        celldm_=celldm_, a_=a_, b_=b_, c_=c_, cosab_=cosab_, cosac_=cosac_, \
        cosbc_=cosbc_, trd_ht=trd_ht, rd_ht=rd_ht, cell_units_=cell_units_)

def ref_cell_base_init(ref_alat, rd_ref_ht, ref_cell_units):
    """
    ref_cell_base_init(ref_alat, rd_ref_ht, ref_cell_units)
    
    
    Defined at cell_base.fpp lines 275-334
    
    Parameters
    ----------
    ref_alat : float
    rd_ref_ht : float array
    ref_cell_units : str
    
    --------------------------------------------------------------------
     Initialize cell_base module variables, set up crystal lattice
    """
    libqepy_modules.f90wrap_cell_base__ref_cell_base_init(ref_alat=ref_alat, \
        rd_ref_ht=rd_ref_ht, ref_cell_units=ref_cell_units)

def gethinv(self):
    """
    gethinv(self)
    
    
    Defined at cell_base.fpp lines 480-489
    
    Parameters
    ----------
    box : Boxdimensions
    
    """
    libqepy_modules.f90wrap_cell_base__gethinv(box=self._handle)

def get_volume(hmat):
    """
    get_volume = get_volume(hmat)
    
    
    Defined at cell_base.fpp lines 491-498
    
    Parameters
    ----------
    hmat : float array
    
    Returns
    -------
    get_volume : float
    
    """
    get_volume = libqepy_modules.f90wrap_cell_base__get_volume(hmat=hmat)
    return get_volume

def pbc(rin, box, nl=None):
    """
    rout = pbc(rin, box[, nl])
    
    
    Defined at cell_base.fpp lines 503-515
    
    Parameters
    ----------
    rin : float array
    box : Boxdimensions
    nl : int array
    
    Returns
    -------
    rout : float array
    
    """
    rout = libqepy_modules.f90wrap_cell_base__pbc(rin=rin, box=box._handle, nl=nl)
    return rout

def get_cell_param(self, cell, ang=None):
    """
    get_cell_param(self, cell[, ang])
    
    
    Defined at cell_base.fpp lines 520-549
    
    Parameters
    ----------
    box : Boxdimensions
    cell : float array
    ang : float array
    
    """
    libqepy_modules.f90wrap_cell_base__get_cell_param(box=self._handle, cell=cell, \
        ang=ang)

def set_h_ainv():
    """
    set_h_ainv()
    
    
    Defined at cell_base.fpp lines 582-596
    
    
    """
    libqepy_modules.f90wrap_cell_base__set_h_ainv()

def cell_dyn_init(trd_ht, rd_ht, wc_, total_ions_mass, press_, frich_, greash_, \
    cell_dofree):
    """
    cell_dyn_init(trd_ht, rd_ht, wc_, total_ions_mass, press_, frich_, greash_, \
        cell_dofree)
    
    
    Defined at cell_base.fpp lines 600-670
    
    Parameters
    ----------
    trd_ht : bool
    rd_ht : float array
    wc_ : float
    total_ions_mass : float
    press_ : float
    frich_ : float
    greash_ : float
    cell_dofree : str
    
    """
    libqepy_modules.f90wrap_cell_base__cell_dyn_init(trd_ht=trd_ht, rd_ht=rd_ht, \
        wc_=wc_, total_ions_mass=total_ions_mass, press_=press_, frich_=frich_, \
        greash_=greash_, cell_dofree=cell_dofree)

def init_dofree(cell_dofree):
    """
    init_dofree(cell_dofree)
    
    
    Defined at cell_base.fpp lines 673-804
    
    Parameters
    ----------
    cell_dofree : str
    
    """
    libqepy_modules.f90wrap_cell_base__init_dofree(cell_dofree=cell_dofree)

def cell_base_reinit(ht):
    """
    cell_base_reinit(ht)
    
    
    Defined at cell_base.fpp lines 807-856
    
    Parameters
    ----------
    ht : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_base_reinit(ht=ht)

def cell_steepest(hnew, h, delt, iforceh, fcell):
    """
    cell_steepest(hnew, h, delt, iforceh, fcell)
    
    
    Defined at cell_base.fpp lines 859-890
    
    Parameters
    ----------
    hnew : float array
    h : float array
    delt : float
    iforceh : int array
    fcell : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_steepest(hnew=hnew, h=h, delt=delt, \
        iforceh=iforceh, fcell=fcell)

def cell_verlet(hnew, h, hold, delt, iforceh, fcell, frich, tnoseh, hnos):
    """
    cell_verlet(hnew, h, hold, delt, iforceh, fcell, frich, tnoseh, hnos)
    
    
    Defined at cell_base.fpp lines 893-939
    
    Parameters
    ----------
    hnew : float array
    h : float array
    hold : float array
    delt : float
    iforceh : int array
    fcell : float array
    frich : float
    tnoseh : bool
    hnos : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_verlet(hnew=hnew, h=h, hold=hold, \
        delt=delt, iforceh=iforceh, fcell=fcell, frich=frich, tnoseh=tnoseh, \
        hnos=hnos)

def cell_hmove(h, hold, delt, iforceh, fcell):
    """
    cell_hmove(h, hold, delt, iforceh, fcell)
    
    
    Defined at cell_base.fpp lines 942-956
    
    Parameters
    ----------
    h : float array
    hold : float array
    delt : float
    iforceh : int array
    fcell : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_hmove(h=h, hold=hold, delt=delt, \
        iforceh=iforceh, fcell=fcell)

def cell_force(fcell, ainv, stress, omega, press, wmassin=None):
    """
    cell_force(fcell, ainv, stress, omega, press[, wmassin])
    
    
    Defined at cell_base.fpp lines 959-996
    
    Parameters
    ----------
    fcell : float array
    ainv : float array
    stress : float array
    omega : float
    press : float
    wmassin : float
    
    """
    libqepy_modules.f90wrap_cell_base__cell_force(fcell=fcell, ainv=ainv, \
        stress=stress, omega=omega, press=press, wmassin=wmassin)

def cell_move(hnew, h, hold, delt, iforceh, fcell, frich, tnoseh, vnhh, velh, \
    tsdc):
    """
    cell_move(hnew, h, hold, delt, iforceh, fcell, frich, tnoseh, vnhh, velh, tsdc)
    
    
    Defined at cell_base.fpp lines 999-1019
    
    Parameters
    ----------
    hnew : float array
    h : float array
    hold : float array
    delt : float
    iforceh : int array
    fcell : float array
    frich : float
    tnoseh : bool
    vnhh : float array
    velh : float array
    tsdc : bool
    
    """
    libqepy_modules.f90wrap_cell_base__cell_move(hnew=hnew, h=h, hold=hold, \
        delt=delt, iforceh=iforceh, fcell=fcell, frich=frich, tnoseh=tnoseh, \
        vnhh=vnhh, velh=velh, tsdc=tsdc)

def cell_gamma(hgamma, ainv, h, velh):
    """
    cell_gamma(hgamma, ainv, h, velh)
    
    
    Defined at cell_base.fpp lines 1022-1040
    
    Parameters
    ----------
    hgamma : float array
    ainv : float array
    h : float array
    velh : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_gamma(hgamma=hgamma, ainv=ainv, h=h, \
        velh=velh)

def cell_update_vel(self, ht0, htm, delt, velh):
    """
    cell_update_vel(self, ht0, htm, delt, velh)
    
    
    Defined at cell_base.fpp lines 1043-1052
    
    Parameters
    ----------
    htp : Boxdimensions
    ht0 : Boxdimensions
    htm : Boxdimensions
    delt : float
    velh : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_update_vel(htp=self._handle, \
        ht0=ht0._handle, htm=htm._handle, delt=delt, velh=velh)

def cell_kinene(temphh, velh):
    """
    ekinh = cell_kinene(temphh, velh)
    
    
    Defined at cell_base.fpp lines 1055-1068
    
    Parameters
    ----------
    temphh : float array
    velh : float array
    
    Returns
    -------
    ekinh : float
    
    """
    ekinh = libqepy_modules.f90wrap_cell_base__cell_kinene(temphh=temphh, velh=velh)
    return ekinh

def cell_alat():
    """
    cell_alat = cell_alat()
    
    
    Defined at cell_base.fpp lines 1071-1076
    
    
    Returns
    -------
    cell_alat : float
    
    """
    cell_alat = libqepy_modules.f90wrap_cell_base__cell_alat()
    return cell_alat

def _cell_init_ht(what, box, hval):
    """
    _cell_init_ht(what, box, hval)
    
    
    Defined at cell_base.fpp lines 343-362
    
    Parameters
    ----------
    what : str
    box : Boxdimensions
    hval : float array
    
    """
    libqepy_modules.f90wrap_cell_base__cell_init_ht(what=what, box=box._handle, \
        hval=hval)

def _cell_init_a(alat, at, box):
    """
    _cell_init_a(alat, at, box)
    
    
    Defined at cell_base.fpp lines 365-385
    
    Parameters
    ----------
    alat : float
    at : float array
    box : Boxdimensions
    
    """
    libqepy_modules.f90wrap_cell_base__cell_init_a(alat=alat, at=at, \
        box=box._handle)

def cell_init(*args, **kwargs):
    """
    cell_init(*args, **kwargs)
    
    
    Defined at cell_base.fpp lines 128-129
    
    Overloaded interface containing the following procedures:
      _cell_init_ht
      _cell_init_a
    
    """
    for proc in [_cell_init_ht, _cell_init_a]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _pbcs_components(x1, y1, z1, m):
    """
    x2, y2, z2 = _pbcs_components(x1, y1, z1, m)
    
    
    Defined at cell_base.fpp lines 552-564
    
    Parameters
    ----------
    x1 : float
    y1 : float
    z1 : float
    m : int
    
    Returns
    -------
    x2 : float
    y2 : float
    z2 : float
    
    """
    x2, y2, z2 = libqepy_modules.f90wrap_cell_base__pbcs_components(x1=x1, y1=y1, \
        z1=z1, m=m)
    return x2, y2, z2

def _pbcs_vectors(v, w, m):
    """
    _pbcs_vectors(v, w, m)
    
    
    Defined at cell_base.fpp lines 567-579
    
    Parameters
    ----------
    v : float array
    w : float array
    m : int
    
    """
    libqepy_modules.f90wrap_cell_base__pbcs_vectors(v=v, w=w, m=m)

def pbcs(*args, **kwargs):
    """
    pbcs(*args, **kwargs)
    
    
    Defined at cell_base.fpp lines 132-133
    
    Overloaded interface containing the following procedures:
      _pbcs_components
      _pbcs_vectors
    
    """
    for proc in [_pbcs_components, _pbcs_vectors]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _s_to_r1(s, r, box):
    """
    _s_to_r1(s, r, box)
    
    
    Defined at cell_base.fpp lines 433-444
    
    Parameters
    ----------
    s : float array
    r : float array
    box : Boxdimensions
    
    """
    libqepy_modules.f90wrap_cell_base__s_to_r1(s=s, r=r, box=box._handle)

def _s_to_r1b(s, r, h):
    """
    _s_to_r1b(s, r, h)
    
    
    Defined at cell_base.fpp lines 447-458
    
    Parameters
    ----------
    s : float array
    r : float array
    h : float array
    
    """
    libqepy_modules.f90wrap_cell_base__s_to_r1b(s=s, r=r, h=h)

def _s_to_r3(s, r, nat, h):
    """
    _s_to_r3(s, r, nat, h)
    
    
    Defined at cell_base.fpp lines 461-475
    
    Parameters
    ----------
    s : float array
    r : float array
    nat : int
    h : float array
    
    """
    libqepy_modules.f90wrap_cell_base__s_to_r3(s=s, r=r, nat=nat, h=h)

def s_to_r(*args, **kwargs):
    """
    s_to_r(*args, **kwargs)
    
    
    Defined at cell_base.fpp lines 136-137
    
    Overloaded interface containing the following procedures:
      _s_to_r1
      _s_to_r1b
      _s_to_r3
    
    """
    for proc in [_s_to_r1, _s_to_r1b, _s_to_r3]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _r_to_s1(r, s, box):
    """
    _r_to_s1(r, s, box)
    
    
    Defined at cell_base.fpp lines 388-399
    
    Parameters
    ----------
    r : float array
    s : float array
    box : Boxdimensions
    
    """
    libqepy_modules.f90wrap_cell_base__r_to_s1(r=r, s=s, box=box._handle)

def _r_to_s1b(r, s, hinv):
    """
    _r_to_s1b(r, s, hinv)
    
    
    Defined at cell_base.fpp lines 419-430
    
    Parameters
    ----------
    r : float array
    s : float array
    hinv : float array
    
    """
    libqepy_modules.f90wrap_cell_base__r_to_s1b(r=r, s=s, hinv=hinv)

def _r_to_s3(r, s, nat, hinv):
    """
    _r_to_s3(r, s, nat, hinv)
    
    
    Defined at cell_base.fpp lines 402-416
    
    Parameters
    ----------
    r : float array
    s : float array
    nat : int
    hinv : float array
    
    """
    libqepy_modules.f90wrap_cell_base__r_to_s3(r=r, s=s, nat=nat, hinv=hinv)

def r_to_s(*args, **kwargs):
    """
    r_to_s(*args, **kwargs)
    
    
    Defined at cell_base.fpp lines 140-141
    
    Overloaded interface containing the following procedures:
      _r_to_s1
      _r_to_s1b
      _r_to_s3
    
    """
    for proc in [_r_to_s1, _r_to_s1b, _r_to_s3]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def get_ibrav():
    """
    Element ibrav ftype=integer  pytype=int
    
    
    Defined at cell_base.fpp line 24
    
    """
    return libqepy_modules.f90wrap_cell_base__get__ibrav()

def set_ibrav(ibrav):
    libqepy_modules.f90wrap_cell_base__set__ibrav(ibrav)

def get_array_celldm():
    """
    Element celldm ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 26
    
    """
    global celldm
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__celldm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        celldm = _arrays[array_handle]
    else:
        celldm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__celldm)
        _arrays[array_handle] = celldm
    return celldm

def set_array_celldm(celldm):
    globals()['celldm'][...] = celldm

def get_a():
    """
    Element a ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 28
    
    """
    return libqepy_modules.f90wrap_cell_base__get__a()

def set_a(a):
    libqepy_modules.f90wrap_cell_base__set__a(a)

def get_b():
    """
    Element b ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 30
    
    """
    return libqepy_modules.f90wrap_cell_base__get__b()

def set_b(b):
    libqepy_modules.f90wrap_cell_base__set__b(b)

def get_c():
    """
    Element c ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 30
    
    """
    return libqepy_modules.f90wrap_cell_base__get__c()

def set_c(c):
    libqepy_modules.f90wrap_cell_base__set__c(c)

def get_cosab():
    """
    Element cosab ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 30
    
    """
    return libqepy_modules.f90wrap_cell_base__get__cosab()

def set_cosab(cosab):
    libqepy_modules.f90wrap_cell_base__set__cosab(cosab)

def get_cosac():
    """
    Element cosac ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 30
    
    """
    return libqepy_modules.f90wrap_cell_base__get__cosac()

def set_cosac(cosac):
    libqepy_modules.f90wrap_cell_base__set__cosac(cosac)

def get_cosbc():
    """
    Element cosbc ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 30
    
    """
    return libqepy_modules.f90wrap_cell_base__get__cosbc()

def set_cosbc(cosbc):
    libqepy_modules.f90wrap_cell_base__set__cosbc(cosbc)

def get_cell_units():
    """
    Element cell_units ftype=character(len=80) pytype=str
    
    
    Defined at cell_base.fpp line 32
    
    """
    return libqepy_modules.f90wrap_cell_base__get__cell_units()

def set_cell_units(cell_units):
    libqepy_modules.f90wrap_cell_base__set__cell_units(cell_units)

def get_alat():
    """
    Element alat ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 34
    
    """
    return libqepy_modules.f90wrap_cell_base__get__alat()

def set_alat(alat):
    libqepy_modules.f90wrap_cell_base__set__alat(alat)

def get_omega():
    """
    Element omega ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 37
    
    """
    return libqepy_modules.f90wrap_cell_base__get__omega()

def set_omega(omega):
    libqepy_modules.f90wrap_cell_base__set__omega(omega)

def get_tpiba():
    """
    Element tpiba ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 39
    
    """
    return libqepy_modules.f90wrap_cell_base__get__tpiba()

def set_tpiba(tpiba):
    libqepy_modules.f90wrap_cell_base__set__tpiba(tpiba)

def get_tpiba2():
    """
    Element tpiba2 ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 41
    
    """
    return libqepy_modules.f90wrap_cell_base__get__tpiba2()

def set_tpiba2(tpiba2):
    libqepy_modules.f90wrap_cell_base__set__tpiba2(tpiba2)

def get_array_at():
    """
    Element at ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 45
    
    """
    global at
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at = _arrays[array_handle]
    else:
        at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__at)
        _arrays[array_handle] = at
    return at

def set_array_at(at):
    globals()['at'][...] = at

def get_array_bg():
    """
    Element bg ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 48
    
    """
    global bg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__bg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        bg = _arrays[array_handle]
    else:
        bg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__bg)
        _arrays[array_handle] = bg
    return bg

def set_array_bg(bg):
    globals()['bg'][...] = bg

def get_ref_tpiba2():
    """
    Element ref_tpiba2 ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 53
    
    """
    return libqepy_modules.f90wrap_cell_base__get__ref_tpiba2()

def set_ref_tpiba2(ref_tpiba2):
    libqepy_modules.f90wrap_cell_base__set__ref_tpiba2(ref_tpiba2)

def get_array_ref_at():
    """
    Element ref_at ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 55
    
    """
    global ref_at
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__ref_at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ref_at = _arrays[array_handle]
    else:
        ref_at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__ref_at)
        _arrays[array_handle] = ref_at
    return ref_at

def set_array_ref_at(ref_at):
    globals()['ref_at'][...] = ref_at

def get_array_ref_bg():
    """
    Element ref_bg ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 56
    
    """
    global ref_bg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__ref_bg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ref_bg = _arrays[array_handle]
    else:
        ref_bg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__ref_bg)
        _arrays[array_handle] = ref_bg
    return ref_bg

def set_array_ref_bg(ref_bg):
    globals()['ref_bg'][...] = ref_bg

def get_init_tpiba2():
    """
    Element init_tpiba2 ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 58
    
    """
    return libqepy_modules.f90wrap_cell_base__get__init_tpiba2()

def set_init_tpiba2(init_tpiba2):
    libqepy_modules.f90wrap_cell_base__set__init_tpiba2(init_tpiba2)

def get_array_h():
    """
    Element h ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 94
    
    """
    global h
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__h(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        h = _arrays[array_handle]
    else:
        h = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__h)
        _arrays[array_handle] = h
    return h

def set_array_h(h):
    globals()['h'][...] = h

def get_array_ainv():
    """
    Element ainv ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 96
    
    """
    global ainv
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__ainv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ainv = _arrays[array_handle]
    else:
        ainv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__ainv)
        _arrays[array_handle] = ainv
    return ainv

def set_array_ainv(ainv):
    globals()['ainv'][...] = ainv

def get_array_hold():
    """
    Element hold ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 97
    
    """
    global hold
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__hold(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        hold = _arrays[array_handle]
    else:
        hold = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__hold)
        _arrays[array_handle] = hold
    return hold

def set_array_hold(hold):
    globals()['hold'][...] = hold

def get_array_hnew():
    """
    Element hnew ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 99
    
    """
    global hnew
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__hnew(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        hnew = _arrays[array_handle]
    else:
        hnew = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__hnew)
        _arrays[array_handle] = hnew
    return hnew

def set_array_hnew(hnew):
    globals()['hnew'][...] = hnew

def get_array_velh():
    """
    Element velh ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 101
    
    """
    global velh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__velh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        velh = _arrays[array_handle]
    else:
        velh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__velh)
        _arrays[array_handle] = velh
    return velh

def set_array_velh(velh):
    globals()['velh'][...] = velh

def get_deth():
    """
    Element deth ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 103
    
    """
    return libqepy_modules.f90wrap_cell_base__get__deth()

def set_deth(deth):
    libqepy_modules.f90wrap_cell_base__set__deth(deth)

def get_array_iforceh():
    """
    Element iforceh ftype=integer    pytype=int
    
    
    Defined at cell_base.fpp line 106
    
    """
    global iforceh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_cell_base__array__iforceh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        iforceh = _arrays[array_handle]
    else:
        iforceh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_cell_base__array__iforceh)
        _arrays[array_handle] = iforceh
    return iforceh

def set_array_iforceh(iforceh):
    globals()['iforceh'][...] = iforceh

def get_enforce_ibrav():
    """
    Element enforce_ibrav ftype=logical pytype=bool
    
    
    Defined at cell_base.fpp line 108
    
    """
    return libqepy_modules.f90wrap_cell_base__get__enforce_ibrav()

def set_enforce_ibrav(enforce_ibrav):
    libqepy_modules.f90wrap_cell_base__set__enforce_ibrav(enforce_ibrav)

def get_fix_volume():
    """
    Element fix_volume ftype=logical pytype=bool
    
    
    Defined at cell_base.fpp line 110
    
    """
    return libqepy_modules.f90wrap_cell_base__get__fix_volume()

def set_fix_volume(fix_volume):
    libqepy_modules.f90wrap_cell_base__set__fix_volume(fix_volume)

def get_fix_area():
    """
    Element fix_area ftype=logical pytype=bool
    
    
    Defined at cell_base.fpp line 112
    
    """
    return libqepy_modules.f90wrap_cell_base__get__fix_area()

def set_fix_area(fix_area):
    libqepy_modules.f90wrap_cell_base__set__fix_area(fix_area)

def get_isotropic():
    """
    Element isotropic ftype=logical pytype=bool
    
    
    Defined at cell_base.fpp line 114
    
    """
    return libqepy_modules.f90wrap_cell_base__get__isotropic()

def set_isotropic(isotropic):
    libqepy_modules.f90wrap_cell_base__set__isotropic(isotropic)

def get_wmass():
    """
    Element wmass ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 116
    
    """
    return libqepy_modules.f90wrap_cell_base__get__wmass()

def set_wmass(wmass):
    libqepy_modules.f90wrap_cell_base__set__wmass(wmass)

def get_press():
    """
    Element press ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 118
    
    """
    return libqepy_modules.f90wrap_cell_base__get__press()

def set_press(press):
    libqepy_modules.f90wrap_cell_base__set__press(press)

def get_frich():
    """
    Element frich ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 121
    
    """
    return libqepy_modules.f90wrap_cell_base__get__frich()

def set_frich(frich):
    libqepy_modules.f90wrap_cell_base__set__frich(frich)

def get_greash():
    """
    Element greash ftype=real(dp) pytype=float
    
    
    Defined at cell_base.fpp line 123
    
    """
    return libqepy_modules.f90wrap_cell_base__get__greash()

def set_greash(greash):
    libqepy_modules.f90wrap_cell_base__set__greash(greash)

def get_tcell_base_init():
    """
    Element tcell_base_init ftype=logical pytype=bool
    
    
    Defined at cell_base.fpp line 126
    
    """
    return libqepy_modules.f90wrap_cell_base__get__tcell_base_init()

def set_tcell_base_init(tcell_base_init):
    libqepy_modules.f90wrap_cell_base__set__tcell_base_init(tcell_base_init)


_array_initialisers = [get_array_celldm, get_array_at, get_array_bg, \
    get_array_ref_at, get_array_ref_bg, get_array_h, get_array_ainv, \
    get_array_hold, get_array_hnew, get_array_velh, get_array_iforceh]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "cell_base".')

for func in _dt_array_initialisers:
    func()
