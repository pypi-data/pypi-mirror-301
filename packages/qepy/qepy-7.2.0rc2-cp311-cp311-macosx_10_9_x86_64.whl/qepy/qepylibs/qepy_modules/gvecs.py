"""
Module gvecs


Defined at recvec.fpp lines 245-299

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def gvecs_init(ngs_, comm):
    """
    gvecs_init(ngs_, comm)
    
    
    Defined at recvec.fpp lines 271-297
    
    Parameters
    ----------
    ngs_ : int
    comm : int
    
    """
    libqepy_modules.f90wrap_gvecs__gvecs_init(ngs_=ngs_, comm=comm)

def get_ngms():
    """
    Element ngms ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 255
    
    """
    return libqepy_modules.f90wrap_gvecs__get__ngms()

def set_ngms(ngms):
    libqepy_modules.f90wrap_gvecs__set__ngms(ngms)

def get_ngms_g():
    """
    Element ngms_g ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 257
    
    """
    return libqepy_modules.f90wrap_gvecs__get__ngms_g()

def set_ngms_g(ngms_g):
    libqepy_modules.f90wrap_gvecs__set__ngms_g(ngms_g)

def get_ngsx():
    """
    Element ngsx ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 260
    
    """
    return libqepy_modules.f90wrap_gvecs__get__ngsx()

def set_ngsx(ngsx):
    libqepy_modules.f90wrap_gvecs__set__ngsx(ngsx)

def get_ecuts():
    """
    Element ecuts ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 262
    
    """
    return libqepy_modules.f90wrap_gvecs__get__ecuts()

def set_ecuts(ecuts):
    libqepy_modules.f90wrap_gvecs__set__ecuts(ecuts)

def get_gcutms():
    """
    Element gcutms ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 264
    
    """
    return libqepy_modules.f90wrap_gvecs__get__gcutms()

def set_gcutms(gcutms):
    libqepy_modules.f90wrap_gvecs__set__gcutms(gcutms)

def get_dual():
    """
    Element dual ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 266
    
    """
    return libqepy_modules.f90wrap_gvecs__get__dual()

def set_dual(dual):
    libqepy_modules.f90wrap_gvecs__set__dual(dual)

def get_doublegrid():
    """
    Element doublegrid ftype=logical pytype=bool
    
    
    Defined at recvec.fpp line 268
    
    """
    return libqepy_modules.f90wrap_gvecs__get__doublegrid()

def set_doublegrid(doublegrid):
    libqepy_modules.f90wrap_gvecs__set__doublegrid(doublegrid)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "gvecs".')

for func in _dt_array_initialisers:
    func()
