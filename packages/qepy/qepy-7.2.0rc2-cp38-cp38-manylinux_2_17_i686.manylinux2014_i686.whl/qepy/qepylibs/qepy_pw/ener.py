"""
Module ener


Defined at pwcom.fpp lines 313-367

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_etot():
    """
    Element etot ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 321
    
    """
    return libqepy_pw.f90wrap_ener__get__etot()

def set_etot(etot):
    libqepy_pw.f90wrap_ener__set__etot(etot)

def get_hwf_energy():
    """
    Element hwf_energy ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 323
    
    """
    return libqepy_pw.f90wrap_ener__get__hwf_energy()

def set_hwf_energy(hwf_energy):
    libqepy_pw.f90wrap_ener__set__hwf_energy(hwf_energy)

def get_eband():
    """
    Element eband ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 325
    
    """
    return libqepy_pw.f90wrap_ener__get__eband()

def set_eband(eband):
    libqepy_pw.f90wrap_ener__set__eband(eband)

def get_deband():
    """
    Element deband ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 327
    
    """
    return libqepy_pw.f90wrap_ener__get__deband()

def set_deband(deband):
    libqepy_pw.f90wrap_ener__set__deband(deband)

def get_ehart():
    """
    Element ehart ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 329
    
    """
    return libqepy_pw.f90wrap_ener__get__ehart()

def set_ehart(ehart):
    libqepy_pw.f90wrap_ener__set__ehart(ehart)

def get_etxc():
    """
    Element etxc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 331
    
    """
    return libqepy_pw.f90wrap_ener__get__etxc()

def set_etxc(etxc):
    libqepy_pw.f90wrap_ener__set__etxc(etxc)

def get_vtxc():
    """
    Element vtxc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 333
    
    """
    return libqepy_pw.f90wrap_ener__get__vtxc()

def set_vtxc(vtxc):
    libqepy_pw.f90wrap_ener__set__vtxc(vtxc)

def get_etxcc():
    """
    Element etxcc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 335
    
    """
    return libqepy_pw.f90wrap_ener__get__etxcc()

def set_etxcc(etxcc):
    libqepy_pw.f90wrap_ener__set__etxcc(etxcc)

def get_ewld():
    """
    Element ewld ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 337
    
    """
    return libqepy_pw.f90wrap_ener__get__ewld()

def set_ewld(ewld):
    libqepy_pw.f90wrap_ener__set__ewld(ewld)

def get_elondon():
    """
    Element elondon ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 339
    
    """
    return libqepy_pw.f90wrap_ener__get__elondon()

def set_elondon(elondon):
    libqepy_pw.f90wrap_ener__set__elondon(elondon)

def get_edftd3():
    """
    Element edftd3 ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 341
    
    """
    return libqepy_pw.f90wrap_ener__get__edftd3()

def set_edftd3(edftd3):
    libqepy_pw.f90wrap_ener__set__edftd3(edftd3)

def get_exdm():
    """
    Element exdm ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 343
    
    """
    return libqepy_pw.f90wrap_ener__get__exdm()

def set_exdm(exdm):
    libqepy_pw.f90wrap_ener__set__exdm(exdm)

def get_demet():
    """
    Element demet ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 345
    
    """
    return libqepy_pw.f90wrap_ener__get__demet()

def set_demet(demet):
    libqepy_pw.f90wrap_ener__set__demet(demet)

def get_esic():
    """
    Element esic ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 347
    
    """
    return libqepy_pw.f90wrap_ener__get__esic()

def set_esic(esic):
    libqepy_pw.f90wrap_ener__set__esic(esic)

def get_esci():
    """
    Element esci ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 349
    
    """
    return libqepy_pw.f90wrap_ener__get__esci()

def set_esci(esci):
    libqepy_pw.f90wrap_ener__set__esci(esci)

def get_epaw():
    """
    Element epaw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 351
    
    """
    return libqepy_pw.f90wrap_ener__get__epaw()

def set_epaw(epaw):
    libqepy_pw.f90wrap_ener__set__epaw(epaw)

def get_ef():
    """
    Element ef ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 353
    
    """
    return libqepy_pw.f90wrap_ener__get__ef()

def set_ef(ef):
    libqepy_pw.f90wrap_ener__set__ef(ef)

def get_ef_up():
    """
    Element ef_up ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 355
    
    """
    return libqepy_pw.f90wrap_ener__get__ef_up()

def set_ef_up(ef_up):
    libqepy_pw.f90wrap_ener__set__ef_up(ef_up)

def get_ef_dw():
    """
    Element ef_dw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 357
    
    """
    return libqepy_pw.f90wrap_ener__get__ef_dw()

def set_ef_dw(ef_dw):
    libqepy_pw.f90wrap_ener__set__ef_dw(ef_dw)

def get_egrand():
    """
    Element egrand ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 359
    
    """
    return libqepy_pw.f90wrap_ener__get__egrand()

def set_egrand(egrand):
    libqepy_pw.f90wrap_ener__set__egrand(egrand)

def get_esol():
    """
    Element esol ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 361
    
    """
    return libqepy_pw.f90wrap_ener__get__esol()

def set_esol(esol):
    libqepy_pw.f90wrap_ener__set__esol(esol)

def get_vsol():
    """
    Element vsol ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 363
    
    """
    return libqepy_pw.f90wrap_ener__get__vsol()

def set_vsol(vsol):
    libqepy_pw.f90wrap_ener__set__vsol(vsol)

def get_ef_cond():
    """
    Element ef_cond ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 365
    
    """
    return libqepy_pw.f90wrap_ener__get__ef_cond()

def set_ef_cond(ef_cond):
    libqepy_pw.f90wrap_ener__set__ef_cond(ef_cond)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "ener".')

for func in _dt_array_initialisers:
    func()
