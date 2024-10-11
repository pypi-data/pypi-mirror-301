"""
Module mp_global


Defined at mp_global.fpp lines 13-130

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_startup(my_world_comm=None, start_images=None, images_only=None):
    """
    mp_startup([my_world_comm, start_images, images_only])
    
    
    Defined at mp_global.fpp lines 46-111
    
    Parameters
    ----------
    my_world_comm : int
    start_images : bool
    images_only : bool
    
    -----------------------------------------------------------------------
     This wrapper subroutine initializes all parallelization levels.
     If option with_images=.true., processes are organized into images,
     each performing a quasi-indipendent calculation, such as a point
     in configuration space(NEB) or a phonon irrep(PHonon).
     Within each image processes are further subdivided into various
     groups and parallelization levels.
      IMPORTANT NOTICE 1: since the command line is read here, it may be
                          convenient to call it in serial execution as well
      IMPORTANT NOTICE 2: most parallelization levels are initialized here
                          but at least some will be moved to a later stage
      SPECIAL CASE: command-line options "-ntg" and "-nyfft", introduced to
                    improve scaling, coexist and are in part interchangeable.
                    If task groups are available, -ntg is faster than -nyfft
                    because it communicates larger data chuncks less frequently
                    Sometimes task groups are not available as for instance
                    when metagga is used or realus or for conjugate gradient.
                    For those cases, -nyfft can be used instead.
                    You may specify one or another: the same value will be set
                    for both ntg and nyfft. These variables are kept separated
                    to help understanding which operation belong to task groups
                    or to nyfft, allowing to differenciate them if need arises.
    """
    libqepy_modules.f90wrap_mp_global__mp_startup(my_world_comm=my_world_comm, \
        start_images=start_images, images_only=images_only)

def mp_global_end():
    """
    mp_global_end()
    
    
    Defined at mp_global.fpp lines 115-129
    
    
    -----------------------------------------------------------------------
    """
    libqepy_modules.f90wrap_mp_global__mp_global_end()

def get_nproc_file():
    """
    Element nproc_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 35
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nproc_file()

def set_nproc_file(nproc_file):
    libqepy_modules.f90wrap_mp_global__set__nproc_file(nproc_file)

def get_nproc_image_file():
    """
    Element nproc_image_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 36
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nproc_image_file()

def set_nproc_image_file(nproc_image_file):
    libqepy_modules.f90wrap_mp_global__set__nproc_image_file(nproc_image_file)

def get_nproc_pool_file():
    """
    Element nproc_pool_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 37
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nproc_pool_file()

def set_nproc_pool_file(nproc_pool_file):
    libqepy_modules.f90wrap_mp_global__set__nproc_pool_file(nproc_pool_file)

def get_nproc_ortho_file():
    """
    Element nproc_ortho_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 38
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nproc_ortho_file()

def set_nproc_ortho_file(nproc_ortho_file):
    libqepy_modules.f90wrap_mp_global__set__nproc_ortho_file(nproc_ortho_file)

def get_nproc_bgrp_file():
    """
    Element nproc_bgrp_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 39
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nproc_bgrp_file()

def set_nproc_bgrp_file(nproc_bgrp_file):
    libqepy_modules.f90wrap_mp_global__set__nproc_bgrp_file(nproc_bgrp_file)

def get_ntask_groups_file():
    """
    Element ntask_groups_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 40
    
    """
    return libqepy_modules.f90wrap_mp_global__get__ntask_groups_file()

def set_ntask_groups_file(ntask_groups_file):
    libqepy_modules.f90wrap_mp_global__set__ntask_groups_file(ntask_groups_file)

def get_nyfft_file():
    """
    Element nyfft_file ftype=integer  pytype=int
    
    
    Defined at mp_global.fpp line 41
    
    """
    return libqepy_modules.f90wrap_mp_global__get__nyfft_file()

def set_nyfft_file(nyfft_file):
    libqepy_modules.f90wrap_mp_global__set__nyfft_file(nyfft_file)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_global".')

for func in _dt_array_initialisers:
    func()
