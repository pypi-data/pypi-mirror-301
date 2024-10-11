"""
Module lr_dav_variables


Defined at lr_dav_variables.fpp lines 13-74

"""
from __future__ import print_function, absolute_import, division
import libqepy_tddfpt
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_zero():
    """
    Element zero ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 24
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__zero()

zero = get_zero()

def get_pi():
    """
    Element pi ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 25
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__pi()

PI = get_pi()

def get_num_eign():
    """
    Element num_eign ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_eign()

def set_num_eign(num_eign):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_eign(num_eign)

def get_num_init():
    """
    Element num_init ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_init()

def set_num_init(num_init):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_init(num_init)

def get_num_basis_max():
    """
    Element num_basis_max ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_basis_max()

def set_num_basis_max(num_basis_max):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_basis_max(num_basis_max)

def get_max_iter():
    """
    Element max_iter ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__max_iter()

def set_max_iter(max_iter):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__max_iter(max_iter)

def get_p_nbnd_occ():
    """
    Element p_nbnd_occ ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__p_nbnd_occ()

def set_p_nbnd_occ(p_nbnd_occ):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__p_nbnd_occ(p_nbnd_occ)

def get_p_nbnd_virt():
    """
    Element p_nbnd_virt ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 30
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__p_nbnd_virt()

def set_p_nbnd_virt(p_nbnd_virt):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__p_nbnd_virt(p_nbnd_virt)

def get_residue_conv_thr():
    """
    Element residue_conv_thr ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__residue_conv_thr()

def set_residue_conv_thr(residue_conv_thr):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__residue_conv_thr(residue_conv_thr)

def get_reference():
    """
    Element reference ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__reference()

def set_reference(reference):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__reference(reference)

def get_close_pre():
    """
    Element close_pre ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__close_pre()

def set_close_pre(close_pre):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__close_pre(close_pre)

def get_broadening():
    """
    Element broadening ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__broadening()

def set_broadening(broadening):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__broadening(broadening)

def get_start():
    """
    Element start ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__start()

def set_start(start):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__start(start)

def get_finish():
    """
    Element finish ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__finish()

def set_finish(finish):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__finish(finish)

def get_step():
    """
    Element step ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__step()

def set_step(step):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__step(step)

def get_turn2planb():
    """
    Element turn2planb ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__turn2planb()

def set_turn2planb(turn2planb):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__turn2planb(turn2planb)

def get_vccouple_shift():
    """
    Element vccouple_shift ftype=real(kind=dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 32
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__vccouple_shift()

def set_vccouple_shift(vccouple_shift):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__vccouple_shift(vccouple_shift)

def get_precondition():
    """
    Element precondition ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__precondition()

def set_precondition(precondition):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__precondition(precondition)

def get_dav_debug():
    """
    Element dav_debug ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__dav_debug()

def set_dav_debug(dav_debug):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__dav_debug(dav_debug)

def get_single_pole():
    """
    Element single_pole ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__single_pole()

def set_single_pole(single_pole):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__single_pole(single_pole)

def get_sort_contr():
    """
    Element sort_contr ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__sort_contr()

def set_sort_contr(sort_contr):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__sort_contr(sort_contr)

def get_diag_of_h():
    """
    Element diag_of_h ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__diag_of_h()

def set_diag_of_h(diag_of_h):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__diag_of_h(diag_of_h)

def get_print_spectrum():
    """
    Element print_spectrum ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__print_spectrum()

def set_print_spectrum(print_spectrum):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__print_spectrum(print_spectrum)

def get_if_check_orth():
    """
    Element if_check_orth ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__if_check_orth()

def set_if_check_orth(if_check_orth):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__if_check_orth(if_check_orth)

def get_if_random_init():
    """
    Element if_random_init ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__if_random_init()

def set_if_random_init(if_random_init):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__if_random_init(if_random_init)

def get_if_check_her():
    """
    Element if_check_her ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__if_check_her()

def set_if_check_her(if_check_her):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__if_check_her(if_check_her)

def get_poor_of_ram():
    """
    Element poor_of_ram ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__poor_of_ram()

def set_poor_of_ram(poor_of_ram):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__poor_of_ram(poor_of_ram)

def get_poor_of_ram2():
    """
    Element poor_of_ram2 ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__poor_of_ram2()

def set_poor_of_ram2(poor_of_ram2):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__poor_of_ram2(poor_of_ram2)

def get_conv_assistant():
    """
    Element conv_assistant ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__conv_assistant()

def set_conv_assistant(conv_assistant):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__conv_assistant(conv_assistant)

def get_if_dft_spectrum():
    """
    Element if_dft_spectrum ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__if_dft_spectrum()

def set_if_dft_spectrum(if_dft_spectrum):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__if_dft_spectrum(if_dft_spectrum)

def get_lplot_drho():
    """
    Element lplot_drho ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 36
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__lplot_drho()

def set_lplot_drho(lplot_drho):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__lplot_drho(lplot_drho)

def get_array_vc_couple():
    """
    Element vc_couple ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 42
    
    """
    global vc_couple
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__vc_couple(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vc_couple = _arrays[array_handle]
    else:
        vc_couple = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__vc_couple)
        _arrays[array_handle] = vc_couple
    return vc_couple

def set_array_vc_couple(vc_couple):
    globals()['vc_couple'][...] = vc_couple

def get_array_eign_value_order():
    """
    Element eign_value_order ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 42
    
    """
    global eign_value_order
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__eign_value_order(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eign_value_order = _arrays[array_handle]
    else:
        eign_value_order = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__eign_value_order)
        _arrays[array_handle] = eign_value_order
    return eign_value_order

def set_array_eign_value_order(eign_value_order):
    globals()['eign_value_order'][...] = eign_value_order

def get_array_energy_dif_order():
    """
    Element energy_dif_order ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 42
    
    """
    global energy_dif_order
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__energy_dif_order(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        energy_dif_order = _arrays[array_handle]
    else:
        energy_dif_order = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__energy_dif_order)
        _arrays[array_handle] = energy_dif_order
    return energy_dif_order

def set_array_energy_dif_order(energy_dif_order):
    globals()['energy_dif_order'][...] = energy_dif_order

def get_dav_conv():
    """
    Element dav_conv ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 43
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__dav_conv()

def set_dav_conv(dav_conv):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__dav_conv(dav_conv)

def get_array_ploted():
    """
    Element ploted ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 44
    
    """
    global ploted
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__ploted(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ploted = _arrays[array_handle]
    else:
        ploted = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__ploted)
        _arrays[array_handle] = ploted
    return ploted

def set_array_ploted(ploted):
    globals()['ploted'][...] = ploted

def get_done_calc_r():
    """
    Element done_calc_r ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 44
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__done_calc_r()

def set_done_calc_r(done_calc_r):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__done_calc_r(done_calc_r)

def get_max_res():
    """
    Element max_res ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 45
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__max_res()

def set_max_res(max_res):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__max_res(max_res)

def get_array_kill_left():
    """
    Element kill_left ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 46
    
    """
    global kill_left
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__kill_left(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        kill_left = _arrays[array_handle]
    else:
        kill_left = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__kill_left)
        _arrays[array_handle] = kill_left
    return kill_left

def set_array_kill_left(kill_left):
    globals()['kill_left'][...] = kill_left

def get_array_kill_right():
    """
    Element kill_right ftype=logical pytype=bool
    
    
    Defined at lr_dav_variables.fpp line 46
    
    """
    global kill_right
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__kill_right(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        kill_right = _arrays[array_handle]
    else:
        kill_right = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__kill_right)
        _arrays[array_handle] = kill_right
    return kill_right

def set_array_kill_right(kill_right):
    globals()['kill_right'][...] = kill_right

def get_num_basis_old():
    """
    Element num_basis_old ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_basis_old()

def set_num_basis_old(num_basis_old):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_basis_old(num_basis_old)

def get_num_basis():
    """
    Element num_basis ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_basis()

def set_num_basis(num_basis):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_basis(num_basis)

def get_toadd():
    """
    Element toadd ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__toadd()

def set_toadd(toadd):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__toadd(toadd)

def get_lwork():
    """
    Element lwork ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__lwork()

def set_lwork(lwork):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__lwork(lwork)

def get_info():
    """
    Element info ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__info()

def set_info(info):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__info(info)

def get_dav_iter():
    """
    Element dav_iter ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__dav_iter()

def set_dav_iter(dav_iter):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__dav_iter(dav_iter)

def get_num_basis_tot():
    """
    Element num_basis_tot ftype=integer  pytype=int
    
    
    Defined at lr_dav_variables.fpp line 50
    
    """
    return libqepy_tddfpt.f90wrap_lr_dav_variables__get__num_basis_tot()

def set_num_basis_tot(num_basis_tot):
    libqepy_tddfpt.f90wrap_lr_dav_variables__set__num_basis_tot(num_basis_tot)

def get_array_vec_b():
    """
    Element vec_b ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global vec_b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__vec_b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vec_b = _arrays[array_handle]
    else:
        vec_b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__vec_b)
        _arrays[array_handle] = vec_b
    return vec_b

def set_array_vec_b(vec_b):
    globals()['vec_b'][...] = vec_b

def get_array_svec_b():
    """
    Element svec_b ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global svec_b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__svec_b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        svec_b = _arrays[array_handle]
    else:
        svec_b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__svec_b)
        _arrays[array_handle] = svec_b
    return svec_b

def set_array_svec_b(svec_b):
    globals()['svec_b'][...] = svec_b

def get_array_left_full():
    """
    Element left_full ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global left_full
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_full(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        left_full = _arrays[array_handle]
    else:
        left_full = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_full)
        _arrays[array_handle] = left_full
    return left_full

def set_array_left_full(left_full):
    globals()['left_full'][...] = left_full

def get_array_right_full():
    """
    Element right_full ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global right_full
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_full(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        right_full = _arrays[array_handle]
    else:
        right_full = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_full)
        _arrays[array_handle] = right_full
    return right_full

def set_array_right_full(right_full):
    globals()['right_full'][...] = right_full

def get_array_left_res():
    """
    Element left_res ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global left_res
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_res(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        left_res = _arrays[array_handle]
    else:
        left_res = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_res)
        _arrays[array_handle] = left_res
    return left_res

def set_array_left_res(left_res):
    globals()['left_res'][...] = left_res

def get_array_right_res():
    """
    Element right_res ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global right_res
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_res(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        right_res = _arrays[array_handle]
    else:
        right_res = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_res)
        _arrays[array_handle] = right_res
    return right_res

def set_array_right_res(right_res):
    globals()['right_res'][...] = right_res

def get_array_vecwork():
    """
    Element vecwork ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global vecwork
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__vecwork(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vecwork = _arrays[array_handle]
    else:
        vecwork = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__vecwork)
        _arrays[array_handle] = vecwork
    return vecwork

def set_array_vecwork(vecwork):
    globals()['vecwork'][...] = vecwork

def get_array_left2():
    """
    Element left2 ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global left2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__left2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        left2 = _arrays[array_handle]
    else:
        left2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__left2)
        _arrays[array_handle] = left2
    return left2

def set_array_left2(left2):
    globals()['left2'][...] = left2

def get_array_right2():
    """
    Element right2 ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global right2
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__right2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        right2 = _arrays[array_handle]
    else:
        right2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__right2)
        _arrays[array_handle] = right2
    return right2

def set_array_right2(right2):
    globals()['right2'][...] = right2

def get_array_m_c():
    """
    Element m_c ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global m_c
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_c(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m_c = _arrays[array_handle]
    else:
        m_c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_c)
        _arrays[array_handle] = m_c
    return m_c

def set_array_m_c(m_c):
    globals()['m_c'][...] = m_c

def get_array_m_d():
    """
    Element m_d ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global m_d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m_d = _arrays[array_handle]
    else:
        m_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_d)
        _arrays[array_handle] = m_d
    return m_d

def set_array_m_d(m_d):
    globals()['m_d'][...] = m_d

def get_array_m():
    """
    Element m ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global m
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__m(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m = _arrays[array_handle]
    else:
        m = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__m)
        _arrays[array_handle] = m
    return m

def set_array_m(m):
    globals()['m'][...] = m

def get_array_ground_state():
    """
    Element ground_state ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global ground_state
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__ground_state(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ground_state = _arrays[array_handle]
    else:
        ground_state = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__ground_state)
        _arrays[array_handle] = ground_state
    return ground_state

def set_array_ground_state(ground_state):
    globals()['ground_state'][...] = ground_state

def get_array_c_vec_b():
    """
    Element c_vec_b ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global c_vec_b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__c_vec_b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        c_vec_b = _arrays[array_handle]
    else:
        c_vec_b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__c_vec_b)
        _arrays[array_handle] = c_vec_b
    return c_vec_b

def set_array_c_vec_b(c_vec_b):
    globals()['c_vec_b'][...] = c_vec_b

def get_array_d_vec_b():
    """
    Element d_vec_b ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global d_vec_b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__d_vec_b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d_vec_b = _arrays[array_handle]
    else:
        d_vec_b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__d_vec_b)
        _arrays[array_handle] = d_vec_b
    return d_vec_b

def set_array_d_vec_b(d_vec_b):
    globals()['d_vec_b'][...] = d_vec_b

def get_array_fx():
    """
    Element fx ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global fx
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__fx(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fx = _arrays[array_handle]
    else:
        fx = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__fx)
        _arrays[array_handle] = fx
    return fx

def set_array_fx(fx):
    globals()['fx'][...] = fx

def get_array_fy():
    """
    Element fy ftype=complex(dp) pytype=complex
    
    
    Defined at lr_dav_variables.fpp line 63
    
    """
    global fy
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__fy(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fy = _arrays[array_handle]
    else:
        fy = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__fy)
        _arrays[array_handle] = fy
    return fy

def set_array_fy(fy):
    globals()['fy'][...] = fy

def get_array_fxr():
    """
    Element fxr ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 64
    
    """
    global fxr
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__fxr(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fxr = _arrays[array_handle]
    else:
        fxr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__fxr)
        _arrays[array_handle] = fxr
    return fxr

def set_array_fxr(fxr):
    globals()['fxr'][...] = fxr

def get_array_fyr():
    """
    Element fyr ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 64
    
    """
    global fyr
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__fyr(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fyr = _arrays[array_handle]
    else:
        fyr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__fyr)
        _arrays[array_handle] = fyr
    return fyr

def set_array_fyr(fyr):
    globals()['fyr'][...] = fyr

def get_array_work():
    """
    Element work ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global work
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__work(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        work = _arrays[array_handle]
    else:
        work = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__work)
        _arrays[array_handle] = work
    return work

def set_array_work(work):
    globals()['work'][...] = work

def get_array_left_m():
    """
    Element left_m ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global left_m
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_m(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        left_m = _arrays[array_handle]
    else:
        left_m = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__left_m)
        _arrays[array_handle] = left_m
    return left_m

def set_array_left_m(left_m):
    globals()['left_m'][...] = left_m

def get_array_right_m():
    """
    Element right_m ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global right_m
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_m(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        right_m = _arrays[array_handle]
    else:
        right_m = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__right_m)
        _arrays[array_handle] = right_m
    return right_m

def set_array_right_m(right_m):
    globals()['right_m'][...] = right_m

def get_array_eign_value():
    """
    Element eign_value ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global eign_value
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__eign_value(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eign_value = _arrays[array_handle]
    else:
        eign_value = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__eign_value)
        _arrays[array_handle] = eign_value
    return eign_value

def set_array_eign_value(eign_value):
    globals()['eign_value'][...] = eign_value

def get_array_m_shadow_avatar():
    """
    Element m_shadow_avatar ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global m_shadow_avatar
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_shadow_avatar(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        m_shadow_avatar = _arrays[array_handle]
    else:
        m_shadow_avatar = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__m_shadow_avatar)
        _arrays[array_handle] = m_shadow_avatar
    return m_shadow_avatar

def set_array_m_shadow_avatar(m_shadow_avatar):
    globals()['m_shadow_avatar'][...] = m_shadow_avatar

def get_array_inner_matrix():
    """
    Element inner_matrix ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global inner_matrix
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__inner_matrix(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        inner_matrix = _arrays[array_handle]
    else:
        inner_matrix = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__inner_matrix)
        _arrays[array_handle] = inner_matrix
    return inner_matrix

def set_array_inner_matrix(inner_matrix):
    globals()['inner_matrix'][...] = inner_matrix

def get_array_tr_energy():
    """
    Element tr_energy ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global tr_energy
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__tr_energy(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tr_energy = _arrays[array_handle]
    else:
        tr_energy = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__tr_energy)
        _arrays[array_handle] = tr_energy
    return tr_energy

def set_array_tr_energy(tr_energy):
    globals()['tr_energy'][...] = tr_energy

def get_array_energy_dif():
    """
    Element energy_dif ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global energy_dif
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__energy_dif(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        energy_dif = _arrays[array_handle]
    else:
        energy_dif = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__energy_dif)
        _arrays[array_handle] = energy_dif
    return energy_dif

def set_array_energy_dif(energy_dif):
    globals()['energy_dif'][...] = energy_dif

def get_array_contribute():
    """
    Element contribute ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global contribute
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__contribute(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        contribute = _arrays[array_handle]
    else:
        contribute = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__contribute)
        _arrays[array_handle] = contribute
    return contribute

def set_array_contribute(contribute):
    globals()['contribute'][...] = contribute

def get_array_chi_dav():
    """
    Element chi_dav ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global chi_dav
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__chi_dav(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        chi_dav = _arrays[array_handle]
    else:
        chi_dav = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__chi_dav)
        _arrays[array_handle] = chi_dav
    return chi_dav

def set_array_chi_dav(chi_dav):
    globals()['chi_dav'][...] = chi_dav

def get_array_total_chi():
    """
    Element total_chi ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global total_chi
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__total_chi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        total_chi = _arrays[array_handle]
    else:
        total_chi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__total_chi)
        _arrays[array_handle] = total_chi
    return total_chi

def set_array_total_chi(total_chi):
    globals()['total_chi'][...] = total_chi

def get_array_norm_f():
    """
    Element norm_f ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global norm_f
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__norm_f(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        norm_f = _arrays[array_handle]
    else:
        norm_f = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__norm_f)
        _arrays[array_handle] = norm_f
    return norm_f

def set_array_norm_f(norm_f):
    globals()['norm_f'][...] = norm_f

def get_array_omegal():
    """
    Element omegal ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global omegal
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__omegal(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        omegal = _arrays[array_handle]
    else:
        omegal = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__omegal)
        _arrays[array_handle] = omegal
    return omegal

def set_array_omegal(omegal):
    globals()['omegal'][...] = omegal

def get_array_omegar():
    """
    Element omegar ftype=real(dp) pytype=float
    
    
    Defined at lr_dav_variables.fpp line 75
    
    """
    global omegar
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_tddfpt.f90wrap_lr_dav_variables__array__omegar(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        omegar = _arrays[array_handle]
    else:
        omegar = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_tddfpt.f90wrap_lr_dav_variables__array__omegar)
        _arrays[array_handle] = omegar
    return omegar

def set_array_omegar(omegar):
    globals()['omegar'][...] = omegar


_array_initialisers = [get_array_vc_couple, get_array_eign_value_order, \
    get_array_energy_dif_order, get_array_ploted, get_array_kill_left, \
    get_array_kill_right, get_array_vec_b, get_array_svec_b, \
    get_array_left_full, get_array_right_full, get_array_left_res, \
    get_array_right_res, get_array_vecwork, get_array_left2, get_array_right2, \
    get_array_m_c, get_array_m_d, get_array_m, get_array_ground_state, \
    get_array_c_vec_b, get_array_d_vec_b, get_array_fx, get_array_fy, \
    get_array_fxr, get_array_fyr, get_array_work, get_array_left_m, \
    get_array_right_m, get_array_eign_value, get_array_m_shadow_avatar, \
    get_array_inner_matrix, get_array_tr_energy, get_array_energy_dif, \
    get_array_contribute, get_array_chi_dav, get_array_total_chi, \
    get_array_norm_f, get_array_omegal, get_array_omegar]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "lr_dav_variables".')

for func in _dt_array_initialisers:
    func()
