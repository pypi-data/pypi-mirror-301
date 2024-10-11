"""
Module scatter_mod


Defined at scatter_mod.fpp lines 20-222

"""
from __future__ import print_function, absolute_import, division
import libqepy_fftxlib
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def cgather_sym(self, f_in, f_out):
    """
    cgather_sym(self, f_in, f_out)
    
    
    Defined at scatter_mod.fpp lines 138-157
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    
    -----------------------------------------------------------------------
     ... gather complex data for symmetrization(used in phonon code)
     ... Differs from gather_grid because mpi_allgatherv is used instead
     ... of mpi_gatherv - all data is gathered on ALL processors
     ... COMPLEX*16  f_in  = distributed variable(nrxx)
     ... COMPLEX*16  f_out = gathered variable(nr1x*nr2x*nr3x)
    """
    libqepy_fftxlib.f90wrap_scatter_mod__cgather_sym(dfftp=self._handle, f_in=f_in, \
        f_out=f_out)

def cgather_sym_many(self, f_in, f_out, nbnd, nbnd_proc, start_nbnd_proc):
    """
    cgather_sym_many(self, f_in, f_out, nbnd, nbnd_proc, start_nbnd_proc)
    
    
    Defined at scatter_mod.fpp lines 162-187
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    nbnd : int
    nbnd_proc : int array
    start_nbnd_proc : int array
    
    -----------------------------------------------------------------------
     ... Written by A. Dal Corso
     ... This routine generalizes cgather_sym, receiveng nbnd complex
     ... distributed functions and collecting nbnd_proc(dfftp%mype+1)
     ... functions in each processor.
     ... start_nbnd_proc(dfftp%mype+1), says where the data for each processor
     ... start in the distributed variable
     ... COMPLEX*16  f_in  = distributed variable(nrxx,nbnd)
     ... COMPLEX*16 f_out = gathered variable(nr1x*nr2x*nr3x,nbnd_proc(dfftp%mype+1))
    """
    libqepy_fftxlib.f90wrap_scatter_mod__cgather_sym_many(dfftp=self._handle, \
        f_in=f_in, f_out=f_out, nbnd=nbnd, nbnd_proc=nbnd_proc, \
        start_nbnd_proc=start_nbnd_proc)

def cscatter_sym_many(self, f_in, f_out, target_ibnd, nbnd, nbnd_proc, \
    start_nbnd_proc):
    """
    cscatter_sym_many(self, f_in, f_out, target_ibnd, nbnd, nbnd_proc, \
        start_nbnd_proc)
    
    
    Defined at scatter_mod.fpp lines 192-220
    
    Parameters
    ----------
    dfftp : Fft_Type_Descriptor
    f_in : complex array
    f_out : complex array
    target_ibnd : int
    nbnd : int
    nbnd_proc : int array
    start_nbnd_proc : int array
    
    ----------------------------------------------------------------------------
     ... Written by A. Dal Corso
     ... generalizes cscatter_sym. It assumes that each processor has
     ... a certain number of bands(nbnd_proc(dfftp%mype+1)). The processor
     ... that has target_ibnd scatters it to all the other processors
     ... that receive a distributed part of the target function.
     ... start_nbnd_proc(dfftp%mype+1) is used to identify the processor
     ... that has the required band
     ... COMPLEX*16 f_in = gathered variable(nr1x*nr2x*nr3x, nbnd_proc(dfftp%mype+1) \
         )
     ... COMPLEX*16  f_out = distributed variable(nrxx)
    """
    libqepy_fftxlib.f90wrap_scatter_mod__cscatter_sym_many(dfftp=self._handle, \
        f_in=f_in, f_out=f_out, target_ibnd=target_ibnd, nbnd=nbnd, \
        nbnd_proc=nbnd_proc, start_nbnd_proc=start_nbnd_proc)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "scatter_mod".')

for func in _dt_array_initialisers:
    func()
