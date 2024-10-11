"""
Module command_line_options


Defined at command_line_options.fpp lines 13-252

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_command_line(input_command_line=None):
    """
    get_command_line([input_command_line])
    
    
    Defined at command_line_options.fpp lines 46-178
    
    Parameters
    ----------
    input_command_line : str
    
    """
    libqepy_modules.f90wrap_command_line_options__get_command_line(input_command_line=input_command_line)

def my_iargc(input_command_line):
    """
    my_iargc = my_iargc(input_command_line)
    
    
    Defined at command_line_options.fpp lines 181-195
    
    Parameters
    ----------
    input_command_line : str
    
    Returns
    -------
    my_iargc : int
    
    """
    my_iargc = \
        libqepy_modules.f90wrap_command_line_options__my_iargc(input_command_line=input_command_line)
    return my_iargc

def my_getarg(input_command_line, narg):
    """
    arg = my_getarg(input_command_line, narg)
    
    
    Defined at command_line_options.fpp lines 198-223
    
    Parameters
    ----------
    input_command_line : str
    narg : int
    
    Returns
    -------
    arg : str
    
    """
    arg = \
        libqepy_modules.f90wrap_command_line_options__my_getarg(input_command_line=input_command_line, \
        narg=narg)
    return arg

def set_command_line(nimage=None, npool=None, ntg=None, nmany=None, nyfft=None, \
    nband=None, ndiag=None, pencil_decomposition=None):
    """
    set_command_line([nimage, npool, ntg, nmany, nyfft, nband, ndiag, \
        pencil_decomposition])
    
    
    Defined at command_line_options.fpp lines 225-250
    
    Parameters
    ----------
    nimage : int
    npool : int
    ntg : int
    nmany : int
    nyfft : int
    nband : int
    ndiag : int
    pencil_decomposition : bool
    
    """
    libqepy_modules.f90wrap_command_line_options__set_command_line(nimage=nimage, \
        npool=npool, ntg=ntg, nmany=nmany, nyfft=nyfft, nband=nband, ndiag=ndiag, \
        pencil_decomposition=pencil_decomposition)

def get_nargs():
    """
    Element nargs ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 29
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__nargs()

def set_nargs(nargs):
    libqepy_modules.f90wrap_command_line_options__set__nargs(nargs)

def get_nimage_():
    """
    Element nimage_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 31
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__nimage_()

def set_nimage_(nimage_):
    libqepy_modules.f90wrap_command_line_options__set__nimage_(nimage_)

def get_nband_():
    """
    Element nband_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 31
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__nband_()

def set_nband_(nband_):
    libqepy_modules.f90wrap_command_line_options__set__nband_(nband_)

def get_nyfft_():
    """
    Element nyfft_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 31
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__nyfft_()

def set_nyfft_(nyfft_):
    libqepy_modules.f90wrap_command_line_options__set__nyfft_(nyfft_)

def get_nmany_():
    """
    Element nmany_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 31
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__nmany_()

def set_nmany_(nmany_):
    libqepy_modules.f90wrap_command_line_options__set__nmany_(nmany_)

def get_npool_():
    """
    Element npool_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 34
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__npool_()

def set_npool_(npool_):
    libqepy_modules.f90wrap_command_line_options__set__npool_(npool_)

def get_ndiag_():
    """
    Element ndiag_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 34
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__ndiag_()

def set_ndiag_(ndiag_):
    libqepy_modules.f90wrap_command_line_options__set__ndiag_(ndiag_)

def get_ntg_():
    """
    Element ntg_ ftype=integer  pytype=int
    
    
    Defined at command_line_options.fpp line 34
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__ntg_()

def set_ntg_(ntg_):
    libqepy_modules.f90wrap_command_line_options__set__ntg_(ntg_)

def get_pencil_decomposition_():
    """
    Element pencil_decomposition_ ftype=logical pytype=bool
    
    
    Defined at command_line_options.fpp line 36
    
    """
    return \
        libqepy_modules.f90wrap_command_line_options__get__pencil_decomposition_()

def set_pencil_decomposition_(pencil_decomposition_):
    libqepy_modules.f90wrap_command_line_options__set__pencil_decomposition_(pencil_decomposition_)

def get_rmm_with_paro_():
    """
    Element rmm_with_paro_ ftype=logical pytype=bool
    
    
    Defined at command_line_options.fpp line 36
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__rmm_with_paro_()

def set_rmm_with_paro_(rmm_with_paro_):
    libqepy_modules.f90wrap_command_line_options__set__rmm_with_paro_(rmm_with_paro_)

def get_library_init():
    """
    Element library_init ftype=logical pytype=bool
    
    
    Defined at command_line_options.fpp line 38
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__library_init()

def set_library_init(library_init):
    libqepy_modules.f90wrap_command_line_options__set__library_init(library_init)

def get_input_file_():
    """
    Element input_file_ ftype=character(len=256) pytype=str
    
    
    Defined at command_line_options.fpp line 40
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__input_file_()

def set_input_file_(input_file_):
    libqepy_modules.f90wrap_command_line_options__set__input_file_(input_file_)

def get_command_line_():
    """
    Element command_line ftype=character(len=512) pytype=str
    
    
    Defined at command_line_options.fpp line 42
    
    """
    return libqepy_modules.f90wrap_command_line_options__get__command_line()

def set_command_line_(command_line):
    libqepy_modules.f90wrap_command_line_options__set__command_line(command_line)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "command_line_options".')

for func in _dt_array_initialisers:
    func()
