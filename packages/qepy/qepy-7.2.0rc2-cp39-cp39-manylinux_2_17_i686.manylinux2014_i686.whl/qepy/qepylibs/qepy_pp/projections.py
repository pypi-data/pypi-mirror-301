"""
Module projections


Defined at projections_mod.fpp lines 12-168

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy_pp.wfc_label")
class wfc_label(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=wfc_label)
    
    
    Defined at projections_mod.fpp lines 14-17
    
    """
    def __init__(self, handle=None):
        """
        self = Wfc_Label()
        
        
        Defined at projections_mod.fpp lines 14-17
        
        
        Returns
        -------
        this : Wfc_Label
        	Object to be constructed
        
        
        Automatically generated constructor for wfc_label
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pp.f90wrap_projections__wfc_label_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Wfc_Label
        
        
        Defined at projections_mod.fpp lines 14-17
        
        Parameters
        ----------
        this : Wfc_Label
        	Object to be destructed
        
        
        Automatically generated destructor for wfc_label
        """
        if self._alloc:
            libqepy_pp.f90wrap_projections__wfc_label_finalise(this=self._handle)
    
    @property
    def na(self):
        """
        Element na ftype=integer  pytype=int
        
        
        Defined at projections_mod.fpp line 15
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__na(self._handle)
    
    @na.setter
    def na(self, na):
        libqepy_pp.f90wrap_wfc_label__set__na(self._handle, na)
    
    @property
    def n(self):
        """
        Element n ftype=integer  pytype=int
        
        
        Defined at projections_mod.fpp line 15
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__n(self._handle)
    
    @n.setter
    def n(self, n):
        libqepy_pp.f90wrap_wfc_label__set__n(self._handle, n)
    
    @property
    def l(self):
        """
        Element l ftype=integer  pytype=int
        
        
        Defined at projections_mod.fpp line 15
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__l(self._handle)
    
    @l.setter
    def l(self, l):
        libqepy_pp.f90wrap_wfc_label__set__l(self._handle, l)
    
    @property
    def m(self):
        """
        Element m ftype=integer  pytype=int
        
        
        Defined at projections_mod.fpp line 15
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__m(self._handle)
    
    @m.setter
    def m(self, m):
        libqepy_pp.f90wrap_wfc_label__set__m(self._handle, m)
    
    @property
    def ind(self):
        """
        Element ind ftype=integer  pytype=int
        
        
        Defined at projections_mod.fpp line 15
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__ind(self._handle)
    
    @ind.setter
    def ind(self, ind):
        libqepy_pp.f90wrap_wfc_label__set__ind(self._handle, ind)
    
    @property
    def jj(self):
        """
        Element jj ftype=real(dp) pytype=float
        
        
        Defined at projections_mod.fpp line 16
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__jj(self._handle)
    
    @jj.setter
    def jj(self, jj):
        libqepy_pp.f90wrap_wfc_label__set__jj(self._handle, jj)
    
    @property
    def els(self):
        """
        Element els ftype=character(len=2) pytype=str
        
        
        Defined at projections_mod.fpp line 17
        
        """
        return libqepy_pp.f90wrap_wfc_label__get__els(self._handle)
    
    @els.setter
    def els(self, els):
        libqepy_pp.f90wrap_wfc_label__set__els(self._handle, els)
    
    def __str__(self):
        ret = ['<wfc_label>{\n']
        ret.append('    na : ')
        ret.append(repr(self.na))
        ret.append(',\n    n : ')
        ret.append(repr(self.n))
        ret.append(',\n    l : ')
        ret.append(repr(self.l))
        ret.append(',\n    m : ')
        ret.append(repr(self.m))
        ret.append(',\n    ind : ')
        ret.append(repr(self.ind))
        ret.append(',\n    jj : ')
        ret.append(repr(self.jj))
        ret.append(',\n    els : ')
        ret.append(repr(self.els))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def fill_nlmchi():
    """
    natomwfc, lmax_wfc = fill_nlmchi()
    
    
    Defined at projections_mod.fpp lines 25-133
    
    
    Returns
    -------
    natomwfc : int
    lmax_wfc : int
    
    """
    natomwfc, lmax_wfc = libqepy_pp.f90wrap_projections__fill_nlmchi()
    return natomwfc, lmax_wfc

def fill_nlmbeta(nkb):
    """
    nwfc = fill_nlmbeta(nkb)
    
    
    Defined at projections_mod.fpp lines 136-167
    
    Parameters
    ----------
    nkb : int
    
    Returns
    -------
    nwfc : int
    
    """
    nwfc = libqepy_pp.f90wrap_projections__fill_nlmbeta(nkb=nkb)
    return nwfc

def get_array_proj():
    """
    Element proj ftype=real(dp) pytype=float
    
    
    Defined at projections_mod.fpp line 20
    
    """
    global proj
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_projections__array__proj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        proj = _arrays[array_handle]
    else:
        proj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_projections__array__proj)
        _arrays[array_handle] = proj
    return proj

def set_array_proj(proj):
    globals()['proj'][...] = proj

def get_array_proj_aux():
    """
    Element proj_aux ftype=complex(dp) pytype=complex
    
    
    Defined at projections_mod.fpp line 21
    
    """
    global proj_aux
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_projections__array__proj_aux(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        proj_aux = _arrays[array_handle]
    else:
        proj_aux = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_projections__array__proj_aux)
        _arrays[array_handle] = proj_aux
    return proj_aux

def set_array_proj_aux(proj_aux):
    globals()['proj_aux'][...] = proj_aux

def get_array_ovps_aux():
    """
    Element ovps_aux ftype=complex(dp) pytype=complex
    
    
    Defined at projections_mod.fpp line 22
    
    """
    global ovps_aux
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pp.f90wrap_projections__array__ovps_aux(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ovps_aux = _arrays[array_handle]
    else:
        ovps_aux = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pp.f90wrap_projections__array__ovps_aux)
        _arrays[array_handle] = ovps_aux
    return ovps_aux

def set_array_ovps_aux(ovps_aux):
    globals()['ovps_aux'][...] = ovps_aux


_array_initialisers = [get_array_proj, get_array_proj_aux, get_array_ovps_aux]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "projections".')

for func in _dt_array_initialisers:
    func()
