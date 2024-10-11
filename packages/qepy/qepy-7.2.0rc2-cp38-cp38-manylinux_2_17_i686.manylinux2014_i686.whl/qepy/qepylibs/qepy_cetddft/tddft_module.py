"""
Module tddft_module


Defined at tddft_module.fpp lines 14-51

"""
from __future__ import print_function, absolute_import, division
import libqepy_cetddft
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_job():
    """
    Element job ftype=character(80) pytype=str
    
    
    Defined at tddft_module.fpp line 24
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__job()

def set_job(job):
    libqepy_cetddft.f90wrap_tddft_module__set__job(job)

def get_e_direction():
    """
    Element e_direction ftype=integer   pytype=int
    
    
    Defined at tddft_module.fpp line 25
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__e_direction()

def set_e_direction(e_direction):
    libqepy_cetddft.f90wrap_tddft_module__set__e_direction(e_direction)

def get_e_strength():
    """
    Element e_strength ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 26
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__e_strength()

def set_e_strength(e_strength):
    libqepy_cetddft.f90wrap_tddft_module__set__e_strength(e_strength)

def get_nstep():
    """
    Element nstep ftype=integer   pytype=int
    
    
    Defined at tddft_module.fpp line 27
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__nstep()

def set_nstep(nstep):
    libqepy_cetddft.f90wrap_tddft_module__set__nstep(nstep)

def get_conv_threshold():
    """
    Element conv_threshold ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 28
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__conv_threshold()

def set_conv_threshold(conv_threshold):
    libqepy_cetddft.f90wrap_tddft_module__set__conv_threshold(conv_threshold)

def get_nupdate_dnm():
    """
    Element nupdate_dnm ftype=integer   pytype=int
    
    
    Defined at tddft_module.fpp line 29
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__nupdate_dnm()

def set_nupdate_dnm(nupdate_dnm):
    libqepy_cetddft.f90wrap_tddft_module__set__nupdate_dnm(nupdate_dnm)

def get_l_circular_dichroism():
    """
    Element l_circular_dichroism ftype=logical pytype=bool
    
    
    Defined at tddft_module.fpp line 30
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__l_circular_dichroism()

def set_l_circular_dichroism(l_circular_dichroism):
    libqepy_cetddft.f90wrap_tddft_module__set__l_circular_dichroism(l_circular_dichroism)

def get_l_tddft_restart():
    """
    Element l_tddft_restart ftype=logical pytype=bool
    
    
    Defined at tddft_module.fpp line 31
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__l_tddft_restart()

def set_l_tddft_restart(l_tddft_restart):
    libqepy_cetddft.f90wrap_tddft_module__set__l_tddft_restart(l_tddft_restart)

def get_iverbosity():
    """
    Element iverbosity ftype=integer   pytype=int
    
    
    Defined at tddft_module.fpp line 32
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__iverbosity()

def set_iverbosity(iverbosity):
    libqepy_cetddft.f90wrap_tddft_module__set__iverbosity(iverbosity)

def get_molecule():
    """
    Element molecule ftype=logical pytype=bool
    
    
    Defined at tddft_module.fpp line 33
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__molecule()

def set_molecule(molecule):
    libqepy_cetddft.f90wrap_tddft_module__set__molecule(molecule)

def get_ehrenfest():
    """
    Element ehrenfest ftype=logical pytype=bool
    
    
    Defined at tddft_module.fpp line 34
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__ehrenfest()

def set_ehrenfest(ehrenfest):
    libqepy_cetddft.f90wrap_tddft_module__set__ehrenfest(ehrenfest)

def get_i_complex():
    """
    Element i_complex ftype=complex(dp) pytype=complex
    
    
    Defined at tddft_module.fpp line 35
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__i_complex()

i_complex = get_i_complex()

def get_array_r_pos():
    """
    Element r_pos ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 36
    
    """
    global r_pos
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_module__array__r_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        r_pos = _arrays[array_handle]
    else:
        r_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_module__array__r_pos)
        _arrays[array_handle] = r_pos
    return r_pos

def set_array_r_pos(r_pos):
    globals()['r_pos'][...] = r_pos

def get_array_r_pos_s():
    """
    Element r_pos_s ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 37
    
    """
    global r_pos_s
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_module__array__r_pos_s(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        r_pos_s = _arrays[array_handle]
    else:
        r_pos_s = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_module__array__r_pos_s)
        _arrays[array_handle] = r_pos_s
    return r_pos_s

def set_array_r_pos_s(r_pos_s):
    globals()['r_pos_s'][...] = r_pos_s

def get_array_nbnd_occ():
    """
    Element nbnd_occ ftype=integer pytype=int
    
    
    Defined at tddft_module.fpp line 38
    
    """
    global nbnd_occ
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_module__array__nbnd_occ(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nbnd_occ = _arrays[array_handle]
    else:
        nbnd_occ = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_module__array__nbnd_occ)
        _arrays[array_handle] = nbnd_occ
    return nbnd_occ

def set_array_nbnd_occ(nbnd_occ):
    globals()['nbnd_occ'][...] = nbnd_occ

def get_nbnd_occ_max():
    """
    Element nbnd_occ_max ftype=integer  pytype=int
    
    
    Defined at tddft_module.fpp line 39
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__nbnd_occ_max()

def set_nbnd_occ_max(nbnd_occ_max):
    libqepy_cetddft.f90wrap_tddft_module__set__nbnd_occ_max(nbnd_occ_max)

def get_iuntdwfc():
    """
    Element iuntdwfc ftype=integer pytype=int
    
    
    Defined at tddft_module.fpp line 40
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__iuntdwfc()

iuntdwfc = get_iuntdwfc()

def get_nwordtdwfc():
    """
    Element nwordtdwfc ftype=integer  pytype=int
    
    
    Defined at tddft_module.fpp line 41
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__nwordtdwfc()

def set_nwordtdwfc(nwordtdwfc):
    libqepy_cetddft.f90wrap_tddft_module__set__nwordtdwfc(nwordtdwfc)

def get_iunevcn():
    """
    Element iunevcn ftype=integer pytype=int
    
    
    Defined at tddft_module.fpp line 42
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__iunevcn()

iunevcn = get_iunevcn()

def get_alpha_pv():
    """
    Element alpha_pv ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 43
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__alpha_pv()

def set_alpha_pv(alpha_pv):
    libqepy_cetddft.f90wrap_tddft_module__set__alpha_pv(alpha_pv)

def get_max_seconds():
    """
    Element max_seconds ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 44
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__max_seconds()

def set_max_seconds(max_seconds):
    libqepy_cetddft.f90wrap_tddft_module__set__max_seconds(max_seconds)

def get_isave_rho():
    """
    Element isave_rho ftype=integer  pytype=int
    
    
    Defined at tddft_module.fpp line 45
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__isave_rho()

def set_isave_rho(isave_rho):
    libqepy_cetddft.f90wrap_tddft_module__set__isave_rho(isave_rho)

def get_wavepacket():
    """
    Element wavepacket ftype=logical pytype=bool
    
    
    Defined at tddft_module.fpp line 47
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__wavepacket()

def set_wavepacket(wavepacket):
    libqepy_cetddft.f90wrap_tddft_module__set__wavepacket(wavepacket)

def get_array_wp_pos():
    """
    Element wp_pos ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 48
    
    """
    global wp_pos
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_module__array__wp_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wp_pos = _arrays[array_handle]
    else:
        wp_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_module__array__wp_pos)
        _arrays[array_handle] = wp_pos
    return wp_pos

def set_array_wp_pos(wp_pos):
    globals()['wp_pos'][...] = wp_pos

def get_array_wp_d():
    """
    Element wp_d ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 49
    
    """
    global wp_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_cetddft.f90wrap_tddft_module__array__wp_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wp_d = _arrays[array_handle]
    else:
        wp_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_cetddft.f90wrap_tddft_module__array__wp_d)
        _arrays[array_handle] = wp_d
    return wp_d

def set_array_wp_d(wp_d):
    globals()['wp_d'][...] = wp_d

def get_wp_ekin():
    """
    Element wp_ekin ftype=real(dp) pytype=float
    
    
    Defined at tddft_module.fpp line 50
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__wp_ekin()

def set_wp_ekin(wp_ekin):
    libqepy_cetddft.f90wrap_tddft_module__set__wp_ekin(wp_ekin)

def get_wp_ibnd():
    """
    Element wp_ibnd ftype=integer  pytype=int
    
    
    Defined at tddft_module.fpp line 51
    
    """
    return libqepy_cetddft.f90wrap_tddft_module__get__wp_ibnd()

def set_wp_ibnd(wp_ibnd):
    libqepy_cetddft.f90wrap_tddft_module__set__wp_ibnd(wp_ibnd)


_array_initialisers = [get_array_r_pos, get_array_r_pos_s, get_array_nbnd_occ, \
    get_array_wp_pos, get_array_wp_d]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "tddft_module".')

for func in _dt_array_initialisers:
    func()
