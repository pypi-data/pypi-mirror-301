"""
Module int_global_variables


Defined at path_interpolation.fpp lines 13-31

"""
from __future__ import print_function, absolute_import, division
import libqepy_neb
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_n():
    """
    Element n ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 19
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__n()

def set_n(n):
    libqepy_neb.f90wrap_int_global_variables__set__n(n)

def get_dim():
    """
    Element dim ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 19
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__dim()

def set_dim(dim):
    libqepy_neb.f90wrap_int_global_variables__set__dim(dim)

def get_old_num_of_images():
    """
    Element old_num_of_images ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 20
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__old_num_of_images()

def set_old_num_of_images(old_num_of_images):
    libqepy_neb.f90wrap_int_global_variables__set__old_num_of_images(old_num_of_images)

def get_new_num_of_images():
    """
    Element new_num_of_images ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 20
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__new_num_of_images()

def set_new_num_of_images(new_num_of_images):
    libqepy_neb.f90wrap_int_global_variables__set__new_num_of_images(new_num_of_images)

def get_first_image():
    """
    Element first_image ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 21
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__first_image()

def set_first_image(first_image):
    libqepy_neb.f90wrap_int_global_variables__set__first_image(first_image)

def get_last_image():
    """
    Element last_image ftype=integer                       pytype=int
    
    
    Defined at path_interpolation.fpp line 21
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__last_image()

def set_last_image(last_image):
    libqepy_neb.f90wrap_int_global_variables__set__last_image(last_image)

def get_array_old_pos():
    """
    Element old_pos ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 22
    
    """
    global old_pos
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__old_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        old_pos = _arrays[array_handle]
    else:
        old_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__old_pos)
        _arrays[array_handle] = old_pos
    return old_pos

def set_array_old_pos(old_pos):
    globals()['old_pos'][...] = old_pos

def get_array_new_pos():
    """
    Element new_pos ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 22
    
    """
    global new_pos
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__new_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        new_pos = _arrays[array_handle]
    else:
        new_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__new_pos)
        _arrays[array_handle] = new_pos
    return new_pos

def set_array_new_pos(new_pos):
    globals()['new_pos'][...] = new_pos

def get_array_old_pes_gradient():
    """
    Element old_pes_gradient ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 23
    
    """
    global old_pes_gradient
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__old_pes_gradient(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        old_pes_gradient = _arrays[array_handle]
    else:
        old_pes_gradient = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__old_pes_gradient)
        _arrays[array_handle] = old_pes_gradient
    return old_pes_gradient

def set_array_old_pes_gradient(old_pes_gradient):
    globals()['old_pes_gradient'][...] = old_pes_gradient

def get_array_new_pes_gradient():
    """
    Element new_pes_gradient ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 23
    
    """
    global new_pes_gradient
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__new_pes_gradient(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        new_pes_gradient = _arrays[array_handle]
    else:
        new_pes_gradient = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__new_pes_gradient)
        _arrays[array_handle] = new_pes_gradient
    return new_pes_gradient

def set_array_new_pes_gradient(new_pes_gradient):
    globals()['new_pes_gradient'][...] = new_pes_gradient

def get_array_fix_atom():
    """
    Element fix_atom ftype=integer pytype=int
    
    
    Defined at path_interpolation.fpp line 24
    
    """
    global fix_atom
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__fix_atom(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fix_atom = _arrays[array_handle]
    else:
        fix_atom = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__fix_atom)
        _arrays[array_handle] = fix_atom
    return fix_atom

def set_array_fix_atom(fix_atom):
    globals()['fix_atom'][...] = fix_atom

def get_array_old_v():
    """
    Element old_v ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 25
    
    """
    global old_v
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__old_v(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        old_v = _arrays[array_handle]
    else:
        old_v = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__old_v)
        _arrays[array_handle] = old_v
    return old_v

def set_array_old_v(old_v):
    globals()['old_v'][...] = old_v

def get_array_new_v():
    """
    Element new_v ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 25
    
    """
    global new_v
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__new_v(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        new_v = _arrays[array_handle]
    else:
        new_v = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__new_v)
        _arrays[array_handle] = new_v
    return new_v

def set_array_new_v(new_v):
    globals()['new_v'][...] = new_v

def get_array_d_r():
    """
    Element d_r ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 26
    
    """
    global d_r
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__d_r(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d_r = _arrays[array_handle]
    else:
        d_r = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__d_r)
        _arrays[array_handle] = d_r
    return d_r

def set_array_d_r(d_r):
    globals()['d_r'][...] = d_r

def get_array_a():
    """
    Element a ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 27
    
    """
    global a
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__a(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        a = _arrays[array_handle]
    else:
        a = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__a)
        _arrays[array_handle] = a
    return a

def set_array_a(a):
    globals()['a'][...] = a

def get_array_b():
    """
    Element b ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 27
    
    """
    global b
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__b(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        b = _arrays[array_handle]
    else:
        b = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__b)
        _arrays[array_handle] = b
    return b

def set_array_b(b):
    globals()['b'][...] = b

def get_array_c():
    """
    Element c ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 27
    
    """
    global c
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__c(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        c = _arrays[array_handle]
    else:
        c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__c)
        _arrays[array_handle] = c
    return c

def set_array_c(c):
    globals()['c'][...] = c

def get_array_d():
    """
    Element d ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 27
    
    """
    global d
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__d(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d = _arrays[array_handle]
    else:
        d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__d)
        _arrays[array_handle] = d
    return d

def set_array_d(d):
    globals()['d'][...] = d

def get_array_f():
    """
    Element f ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 27
    
    """
    global f
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__f(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        f = _arrays[array_handle]
    else:
        f = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__f)
        _arrays[array_handle] = f
    return f

def set_array_f(f):
    globals()['f'][...] = f

def get_array_old_mesh():
    """
    Element old_mesh ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 28
    
    """
    global old_mesh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__old_mesh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        old_mesh = _arrays[array_handle]
    else:
        old_mesh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__old_mesh)
        _arrays[array_handle] = old_mesh
    return old_mesh

def set_array_old_mesh(old_mesh):
    globals()['old_mesh'][...] = old_mesh

def get_array_new_mesh():
    """
    Element new_mesh ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 28
    
    """
    global new_mesh
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__new_mesh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        new_mesh = _arrays[array_handle]
    else:
        new_mesh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__new_mesh)
        _arrays[array_handle] = new_mesh
    return new_mesh

def set_array_new_mesh(new_mesh):
    globals()['new_mesh'][...] = new_mesh

def get_array_tangent():
    """
    Element tangent ftype=real(dp) pytype=float
    
    
    Defined at path_interpolation.fpp line 29
    
    """
    global tangent
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_neb.f90wrap_int_global_variables__array__tangent(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tangent = _arrays[array_handle]
    else:
        tangent = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_neb.f90wrap_int_global_variables__array__tangent)
        _arrays[array_handle] = tangent
    return tangent

def set_array_tangent(tangent):
    globals()['tangent'][...] = tangent

def get_old_restart_file():
    """
    Element old_restart_file ftype=character(len=256) pytype=str
    
    
    Defined at path_interpolation.fpp line 30
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__old_restart_file()

def set_old_restart_file(old_restart_file):
    libqepy_neb.f90wrap_int_global_variables__set__old_restart_file(old_restart_file)

def get_new_restart_file():
    """
    Element new_restart_file ftype=character(len=256) pytype=str
    
    
    Defined at path_interpolation.fpp line 30
    
    """
    return libqepy_neb.f90wrap_int_global_variables__get__new_restart_file()

def set_new_restart_file(new_restart_file):
    libqepy_neb.f90wrap_int_global_variables__set__new_restart_file(new_restart_file)


_array_initialisers = [get_array_old_pos, get_array_new_pos, \
    get_array_old_pes_gradient, get_array_new_pes_gradient, get_array_fix_atom, \
    get_array_old_v, get_array_new_v, get_array_d_r, get_array_a, get_array_b, \
    get_array_c, get_array_d, get_array_f, get_array_old_mesh, \
    get_array_new_mesh, get_array_tangent]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "int_global_variables".')

for func in _dt_array_initialisers:
    func()
