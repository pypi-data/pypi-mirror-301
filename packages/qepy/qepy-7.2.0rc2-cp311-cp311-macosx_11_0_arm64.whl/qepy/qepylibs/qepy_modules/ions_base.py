"""
Module ions_base


Defined at ions_base.fpp lines 13-616

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def ions_base_init(nsp_, nat_, na_, ityp_, tau_, vel_, amass_, atm_, if_pos_, \
    tau_format_, alat_, at_, rcmax_, extfor_):
    """
    ions_base_init(nsp_, nat_, na_, ityp_, tau_, vel_, amass_, atm_, if_pos_, \
        tau_format_, alat_, at_, rcmax_, extfor_)
    
    
    Defined at ions_base.fpp lines 77-241
    
    Parameters
    ----------
    nsp_ : int
    nat_ : int
    na_ : int array
    ityp_ : int array
    tau_ : float array
    vel_ : float array
    amass_ : float array
    atm_ : str array
    if_pos_ : int array
    tau_format_ : str
    alat_ : float
    at_ : float array
    rcmax_ : float array
    extfor_ : float array
    
    -------------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_ions_base__ions_base_init(nsp_=nsp_, nat_=nat_, na_=na_, \
        ityp_=ityp_, tau_=tau_, vel_=vel_, amass_=amass_, atm_=atm_, \
        if_pos_=if_pos_, tau_format_=tau_format_, alat_=alat_, at_=at_, \
        rcmax_=rcmax_, extfor_=extfor_)

def deallocate_ions_base():
    """
    deallocate_ions_base()
    
    
    Defined at ions_base.fpp lines 245-261
    
    
    -------------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_ions_base__deallocate_ions_base()

def ions_vel(vel, taup, taum, dt):
    """
    ions_vel(vel, taup, taum, dt)
    
    
    Defined at ions_base.fpp lines 265-276
    
    Parameters
    ----------
    vel : float array
    taup : float array
    taum : float array
    dt : float
    
    -------------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_ions_base__ions_vel(vel=vel, taup=taup, taum=taum, \
        dt=dt)

def ions_cofmass(tau, pmass, nat, ityp, cdm):
    """
    ions_cofmass(tau, pmass, nat, ityp, cdm)
    
    
    Defined at ions_base.fpp lines 279-301
    
    Parameters
    ----------
    tau : float array
    pmass : float array
    nat : int
    ityp : int array
    cdm : float array
    
    """
    libqepy_modules.f90wrap_ions_base__ions_cofmass(tau=tau, pmass=pmass, nat=nat, \
        ityp=ityp, cdm=cdm)

def randpos(tau, nat, ityp, tranp, amprp, hinv, ifor):
    """
    randpos(tau, nat, ityp, tranp, amprp, hinv, ifor)
    
    
    Defined at ions_base.fpp lines 304-336
    
    Parameters
    ----------
    tau : float array
    nat : int
    ityp : int array
    tranp : bool array
    amprp : float array
    hinv : float array
    ifor : int array
    
    """
    libqepy_modules.f90wrap_ions_base__randpos(tau=tau, nat=nat, ityp=ityp, \
        tranp=tranp, amprp=amprp, hinv=hinv, ifor=ifor)

def ions_kinene(vels, nat, ityp, h, pmass):
    """
    ekinp = ions_kinene(vels, nat, ityp, h, pmass)
    
    
    Defined at ions_base.fpp lines 339-358
    
    Parameters
    ----------
    vels : float array
    nat : int
    ityp : int array
    h : float array
    pmass : float array
    
    Returns
    -------
    ekinp : float
    
    """
    ekinp = libqepy_modules.f90wrap_ions_base__ions_kinene(vels=vels, nat=nat, \
        ityp=ityp, h=h, pmass=pmass)
    return ekinp

def ions_temp(temps, vels, nsp, na, nat, ityp, h, pmass, ndega, nhpdim, atm2nhp, \
    ekin2nhp):
    """
    tempp, ekinpr = ions_temp(temps, vels, nsp, na, nat, ityp, h, pmass, ndega, \
        nhpdim, atm2nhp, ekin2nhp)
    
    
    Defined at ions_base.fpp lines 361-410
    
    Parameters
    ----------
    temps : float array
    vels : float array
    nsp : int
    na : int array
    nat : int
    ityp : int array
    h : float array
    pmass : float array
    ndega : int
    nhpdim : int
    atm2nhp : int array
    ekin2nhp : float array
    
    Returns
    -------
    tempp : float
    ekinpr : float
    
    """
    tempp, ekinpr = libqepy_modules.f90wrap_ions_base__ions_temp(temps=temps, \
        vels=vels, nsp=nsp, na=na, nat=nat, ityp=ityp, h=h, pmass=pmass, \
        ndega=ndega, nhpdim=nhpdim, atm2nhp=atm2nhp, ekin2nhp=ekin2nhp)
    return tempp, ekinpr

def ions_thermal_stress(stress, nstress, pmass, omega, h, vels, nat, ityp):
    """
    ions_thermal_stress(stress, nstress, pmass, omega, h, vels, nat, ityp)
    
    
    Defined at ions_base.fpp lines 413-435
    
    Parameters
    ----------
    stress : float array
    nstress : float array
    pmass : float array
    omega : float
    h : float array
    vels : float array
    nat : int
    ityp : int array
    
    """
    libqepy_modules.f90wrap_ions_base__ions_thermal_stress(stress=stress, \
        nstress=nstress, pmass=pmass, omega=omega, h=h, vels=vels, nat=nat, \
        ityp=ityp)

def randvel(tempw, tau0, taum, nat, ityp, iforce, amass, delt):
    """
    randvel(tempw, tau0, taum, nat, ityp, iforce, amass, delt)
    
    
    Defined at ions_base.fpp lines 438-469
    
    Parameters
    ----------
    tempw : float
    tau0 : float array
    taum : float array
    nat : int
    ityp : int array
    iforce : int array
    amass : float array
    delt : float
    
    """
    libqepy_modules.f90wrap_ions_base__randvel(tempw=tempw, tau0=tau0, taum=taum, \
        nat=nat, ityp=ityp, iforce=iforce, amass=amass, delt=delt)

def ions_vrescal(tcap, tempw, tempp, taup, tau0, taum, nat, ityp, fion, iforce, \
    pmass, delt):
    """
    ions_vrescal(tcap, tempw, tempp, taup, tau0, taum, nat, ityp, fion, iforce, \
        pmass, delt)
    
    
    Defined at ions_base.fpp lines 472-516
    
    Parameters
    ----------
    tcap : bool
    tempw : float
    tempp : float
    taup : float array
    tau0 : float array
    taum : float array
    nat : int
    ityp : int array
    fion : float array
    iforce : int array
    pmass : float array
    delt : float
    
    """
    libqepy_modules.f90wrap_ions_base__ions_vrescal(tcap=tcap, tempw=tempw, \
        tempp=tempp, taup=taup, tau0=tau0, taum=taum, nat=nat, ityp=ityp, fion=fion, \
        iforce=iforce, pmass=pmass, delt=delt)

def ions_shiftvar(varp, var0, varm):
    """
    ions_shiftvar(varp, var0, varm)
    
    
    Defined at ions_base.fpp lines 519-525
    
    Parameters
    ----------
    varp : float array
    var0 : float array
    varm : float array
    
    """
    libqepy_modules.f90wrap_ions_base__ions_shiftvar(varp=varp, var0=var0, \
        varm=varm)

def ions_reference_positions(tau):
    """
    ions_reference_positions(tau)
    
    
    Defined at ions_base.fpp lines 528-539
    
    Parameters
    ----------
    tau : float array
    
    """
    libqepy_modules.f90wrap_ions_base__ions_reference_positions(tau=tau)

def ions_displacement(dis, tau, nsp, nat, ityp):
    """
    ions_displacement(dis, tau, nsp, nat, ityp)
    
    
    Defined at ions_base.fpp lines 542-565
    
    Parameters
    ----------
    dis : float array
    tau : float array
    nsp : int
    nat : int
    ityp : int array
    
    """
    libqepy_modules.f90wrap_ions_base__ions_displacement(dis=dis, tau=tau, nsp=nsp, \
        nat=nat, ityp=ityp)

def ions_cofmsub(tausp, iforce, nat, cdm, cdm0):
    """
    ions_cofmsub(tausp, iforce, nat, cdm, cdm0)
    
    
    Defined at ions_base.fpp lines 568-591
    
    Parameters
    ----------
    tausp : float array
    iforce : int array
    nat : int
    cdm : float array
    cdm0 : float array
    
    --------------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_ions_base__ions_cofmsub(tausp=tausp, iforce=iforce, \
        nat=nat, cdm=cdm, cdm0=cdm0)

def compute_eextfor(tau0=None):
    """
    compute_eextfor = compute_eextfor([tau0])
    
    
    Defined at ions_base.fpp lines 593-614
    
    Parameters
    ----------
    tau0 : float array
    
    Returns
    -------
    compute_eextfor : float
    
    """
    compute_eextfor = libqepy_modules.f90wrap_ions_base__compute_eextfor(tau0=tau0)
    return compute_eextfor

def get_nax():
    """
    Element nax ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 27
    
    """
    return libqepy_modules.f90wrap_ions_base__get__nax()

def set_nax(nax):
    libqepy_modules.f90wrap_ions_base__set__nax(nax)

def get_nat():
    """
    Element nat ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 28
    
    """
    return libqepy_modules.f90wrap_ions_base__get__nat()

def set_nat(nat):
    libqepy_modules.f90wrap_ions_base__set__nat(nat)

def get_array_na():
    """
    Element na ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 29
    
    """
    global na
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__na(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        na = _arrays[array_handle]
    else:
        na = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__na)
        _arrays[array_handle] = na
    return na

def set_array_na(na):
    globals()['na'][...] = na

def get_array_ityp():
    """
    Element ityp ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 31
    
    """
    global ityp
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__ityp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ityp = _arrays[array_handle]
    else:
        ityp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__ityp)
        _arrays[array_handle] = ityp
    return ityp

def set_array_ityp(ityp):
    globals()['ityp'][...] = ityp

def get_array_zv():
    """
    Element zv ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 35
    
    """
    global zv
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__zv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        zv = _arrays[array_handle]
    else:
        zv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__zv)
        _arrays[array_handle] = zv
    return zv

def set_array_zv(zv):
    globals()['zv'][...] = zv

def get_array_amass():
    """
    Element amass ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 36
    
    """
    global amass
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__amass(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        amass = _arrays[array_handle]
    else:
        amass = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__amass)
        _arrays[array_handle] = amass
    return amass

def set_array_amass(amass):
    globals()['amass'][...] = amass

def get_array_rcmax():
    """
    Element rcmax ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 37
    
    """
    global rcmax
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__rcmax(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rcmax = _arrays[array_handle]
    else:
        rcmax = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__rcmax)
        _arrays[array_handle] = rcmax
    return rcmax

def set_array_rcmax(rcmax):
    globals()['rcmax'][...] = rcmax

def get_array_tau():
    """
    Element tau ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 41
    
    """
    global tau
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__tau(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tau = _arrays[array_handle]
    else:
        tau = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__tau)
        _arrays[array_handle] = tau
    return tau

def set_array_tau(tau):
    globals()['tau'][...] = tau

def get_array_vel():
    """
    Element vel ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 42
    
    """
    global vel
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__vel(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vel = _arrays[array_handle]
    else:
        vel = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__vel)
        _arrays[array_handle] = vel
    return vel

def set_array_vel(vel):
    globals()['vel'][...] = vel

def get_array_atm():
    """
    Element atm ftype=character(len=3) pytype=str
    
    
    Defined at ions_base.fpp line 43
    
    """
    global atm
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__atm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        atm = _arrays[array_handle]
    else:
        atm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__atm)
        _arrays[array_handle] = atm
    return atm

def set_array_atm(atm):
    globals()['atm'][...] = atm

def get_tau_format():
    """
    Element tau_format ftype=character(len=80) pytype=str
    
    
    Defined at ions_base.fpp line 44
    
    """
    return libqepy_modules.f90wrap_ions_base__get__tau_format()

def set_tau_format(tau_format):
    libqepy_modules.f90wrap_ions_base__set__tau_format(tau_format)

def get_array_if_pos():
    """
    Element if_pos ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 47
    
    """
    global if_pos
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__if_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        if_pos = _arrays[array_handle]
    else:
        if_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__if_pos)
        _arrays[array_handle] = if_pos
    return if_pos

def set_array_if_pos(if_pos):
    globals()['if_pos'][...] = if_pos

def get_array_iforce():
    """
    Element iforce ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 48
    
    """
    global iforce
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__iforce(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        iforce = _arrays[array_handle]
    else:
        iforce = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__iforce)
        _arrays[array_handle] = iforce
    return iforce

def set_array_iforce(iforce):
    globals()['iforce'][...] = iforce

def get_fixatom():
    """
    Element fixatom ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 49
    
    """
    return libqepy_modules.f90wrap_ions_base__get__fixatom()

def set_fixatom(fixatom):
    libqepy_modules.f90wrap_ions_base__set__fixatom(fixatom)

def get_ndofp():
    """
    Element ndofp ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 50
    
    """
    return libqepy_modules.f90wrap_ions_base__get__ndofp()

def set_ndofp(ndofp):
    libqepy_modules.f90wrap_ions_base__set__ndofp(ndofp)

def get_ndfrz():
    """
    Element ndfrz ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 51
    
    """
    return libqepy_modules.f90wrap_ions_base__get__ndfrz()

def set_ndfrz(ndfrz):
    libqepy_modules.f90wrap_ions_base__set__ndfrz(ndfrz)

def get_fricp():
    """
    Element fricp ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 52
    
    """
    return libqepy_modules.f90wrap_ions_base__get__fricp()

def set_fricp(fricp):
    libqepy_modules.f90wrap_ions_base__set__fricp(fricp)

def get_greasp():
    """
    Element greasp ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 53
    
    """
    return libqepy_modules.f90wrap_ions_base__get__greasp()

def set_greasp(greasp):
    libqepy_modules.f90wrap_ions_base__set__greasp(greasp)

def get_array_taui():
    """
    Element taui ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 60
    
    """
    global taui
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__taui(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        taui = _arrays[array_handle]
    else:
        taui = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__taui)
        _arrays[array_handle] = taui
    return taui

def set_array_taui(taui):
    globals()['taui'][...] = taui

def get_array_cdmi():
    """
    Element cdmi ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 64
    
    """
    global cdmi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__cdmi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdmi = _arrays[array_handle]
    else:
        cdmi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__cdmi)
        _arrays[array_handle] = cdmi
    return cdmi

def set_array_cdmi(cdmi):
    globals()['cdmi'][...] = cdmi

def get_array_cdm():
    """
    Element cdm ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 64
    
    """
    global cdm
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__cdm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdm = _arrays[array_handle]
    else:
        cdm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__cdm)
        _arrays[array_handle] = cdm
    return cdm

def set_array_cdm(cdm):
    globals()['cdm'][...] = cdm

def get_array_cdms():
    """
    Element cdms ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 66
    
    """
    global cdms
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__cdms(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdms = _arrays[array_handle]
    else:
        cdms = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__cdms)
        _arrays[array_handle] = cdms
    return cdms

def set_array_cdms(cdms):
    globals()['cdms'][...] = cdms

def get_array_extfor():
    """
    Element extfor ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 68
    
    """
    global extfor
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_modules.f90wrap_ions_base__array__extfor(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        extfor = _arrays[array_handle]
    else:
        extfor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_modules.f90wrap_ions_base__array__extfor)
        _arrays[array_handle] = extfor
    return extfor

def set_array_extfor(extfor):
    globals()['extfor'][...] = extfor

def get_tions_base_init():
    """
    Element tions_base_init ftype=logical pytype=bool
    
    
    Defined at ions_base.fpp line 69
    
    """
    return libqepy_modules.f90wrap_ions_base__get__tions_base_init()

def set_tions_base_init(tions_base_init):
    libqepy_modules.f90wrap_ions_base__set__tions_base_init(tions_base_init)


_array_initialisers = [get_array_na, get_array_ityp, get_array_zv, \
    get_array_amass, get_array_rcmax, get_array_tau, get_array_vel, \
    get_array_atm, get_array_if_pos, get_array_iforce, get_array_taui, \
    get_array_cdmi, get_array_cdm, get_array_cdms, get_array_extfor]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "ions_base".')

for func in _dt_array_initialisers:
    func()
