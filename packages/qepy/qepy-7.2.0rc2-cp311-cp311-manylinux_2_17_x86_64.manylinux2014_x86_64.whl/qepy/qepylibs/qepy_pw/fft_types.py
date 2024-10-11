"""
Module fft_types


Defined at ../fftxlib/fft_types.fpp lines 14-866

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy_pw.fft_type_descriptor")
class fft_type_descriptor(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=fft_type_descriptor)
    
    
    Defined at ../fftxlib/fft_types.fpp lines 25-131
    
    """
    def __init__(self, at, bg, gcutm, comm, fft_fact=None, nyfft=None, handle=None):
        """
        self = Fft_Type_Descriptor(at, bg, gcutm, comm[, fft_fact, nyfft])
        
        
        Defined at ../fftxlib/fft_types.fpp lines 140-211
        
        Parameters
        ----------
        at : float array
        bg : float array
        gcutm : float
        comm : int
        fft_fact : int array
        nyfft : int
        
        Returns
        -------
        desc : Fft_Type_Descriptor
        
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pw.f90wrap_fft_types__fft_type_allocate(at=at, bg=bg, \
            gcutm=gcutm, comm=comm, fft_fact=fft_fact, nyfft=nyfft)
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Fft_Type_Descriptor
        
        
        Defined at ../fftxlib/fft_types.fpp lines 213-259
        
        Parameters
        ----------
        desc : Fft_Type_Descriptor
        
        """
        if self._alloc:
            libqepy_pw.f90wrap_fft_types__fft_type_deallocate(desc=self._handle)
    
    @property
    def nr1(self):
        """
        Element nr1 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 29
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr1(self._handle)
    
    @nr1.setter
    def nr1(self, nr1):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr1(self._handle, nr1)
    
    @property
    def nr2(self):
        """
        Element nr2 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 30
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr2(self._handle)
    
    @nr2.setter
    def nr2(self, nr2):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr2(self._handle, nr2)
    
    @property
    def nr3(self):
        """
        Element nr3 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 31
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr3(self._handle)
    
    @nr3.setter
    def nr3(self, nr3):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr3(self._handle, nr3)
    
    @property
    def nr1x(self):
        """
        Element nr1x ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 32
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr1x(self._handle)
    
    @nr1x.setter
    def nr1x(self, nr1x):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr1x(self._handle, nr1x)
    
    @property
    def nr2x(self):
        """
        Element nr2x ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 33
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr2x(self._handle)
    
    @nr2x.setter
    def nr2x(self, nr2x):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr2x(self._handle, nr2x)
    
    @property
    def nr3x(self):
        """
        Element nr3x ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 34
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr3x(self._handle)
    
    @nr3x.setter
    def nr3x(self, nr3x):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr3x(self._handle, nr3x)
    
    @property
    def lpara(self):
        """
        Element lpara ftype=logical pytype=bool
        
        
        Defined at ../fftxlib/fft_types.fpp line 46
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__lpara(self._handle)
    
    @lpara.setter
    def lpara(self, lpara):
        libqepy_pw.f90wrap_fft_type_descriptor__set__lpara(self._handle, lpara)
    
    @property
    def lgamma(self):
        """
        Element lgamma ftype=logical pytype=bool
        
        
        Defined at ../fftxlib/fft_types.fpp line 47
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__lgamma(self._handle)
    
    @lgamma.setter
    def lgamma(self, lgamma):
        libqepy_pw.f90wrap_fft_type_descriptor__set__lgamma(self._handle, lgamma)
    
    @property
    def root(self):
        """
        Element root ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 48
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__root(self._handle)
    
    @root.setter
    def root(self, root):
        libqepy_pw.f90wrap_fft_type_descriptor__set__root(self._handle, root)
    
    @property
    def comm(self):
        """
        Element comm ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 49
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__comm(self._handle)
    
    @comm.setter
    def comm(self, comm):
        libqepy_pw.f90wrap_fft_type_descriptor__set__comm(self._handle, comm)
    
    @property
    def comm2(self):
        """
        Element comm2 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 50
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__comm2(self._handle)
    
    @comm2.setter
    def comm2(self, comm2):
        libqepy_pw.f90wrap_fft_type_descriptor__set__comm2(self._handle, comm2)
    
    @property
    def comm3(self):
        """
        Element comm3 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 51
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__comm3(self._handle)
    
    @comm3.setter
    def comm3(self, comm3):
        libqepy_pw.f90wrap_fft_type_descriptor__set__comm3(self._handle, comm3)
    
    @property
    def nproc(self):
        """
        Element nproc ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 52
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nproc(self._handle)
    
    @nproc.setter
    def nproc(self, nproc):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nproc(self._handle, nproc)
    
    @property
    def nproc2(self):
        """
        Element nproc2 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 53
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nproc2(self._handle)
    
    @nproc2.setter
    def nproc2(self, nproc2):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nproc2(self._handle, nproc2)
    
    @property
    def nproc3(self):
        """
        Element nproc3 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 54
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nproc3(self._handle)
    
    @nproc3.setter
    def nproc3(self, nproc3):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nproc3(self._handle, nproc3)
    
    @property
    def mype(self):
        """
        Element mype ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 55
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__mype(self._handle)
    
    @mype.setter
    def mype(self, mype):
        libqepy_pw.f90wrap_fft_type_descriptor__set__mype(self._handle, mype)
    
    @property
    def mype2(self):
        """
        Element mype2 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 56
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__mype2(self._handle)
    
    @mype2.setter
    def mype2(self, mype2):
        libqepy_pw.f90wrap_fft_type_descriptor__set__mype2(self._handle, mype2)
    
    @property
    def mype3(self):
        """
        Element mype3 ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 57
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__mype3(self._handle)
    
    @mype3.setter
    def mype3(self, mype3):
        libqepy_pw.f90wrap_fft_type_descriptor__set__mype3(self._handle, mype3)
    
    @property
    def iproc(self):
        """
        Element iproc ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 58
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iproc(self._handle)
        if array_handle in self._arrays:
            iproc = self._arrays[array_handle]
        else:
            iproc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iproc)
            self._arrays[array_handle] = iproc
        return iproc
    
    @iproc.setter
    def iproc(self, iproc):
        self.iproc[...] = iproc
    
    @property
    def iproc2(self):
        """
        Element iproc2 ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 58
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iproc2(self._handle)
        if array_handle in self._arrays:
            iproc2 = self._arrays[array_handle]
        else:
            iproc2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iproc2)
            self._arrays[array_handle] = iproc2
        return iproc2
    
    @iproc2.setter
    def iproc2(self, iproc2):
        self.iproc2[...] = iproc2
    
    @property
    def iproc3(self):
        """
        Element iproc3 ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 58
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iproc3(self._handle)
        if array_handle in self._arrays:
            iproc3 = self._arrays[array_handle]
        else:
            iproc3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iproc3)
            self._arrays[array_handle] = iproc3
        return iproc3
    
    @iproc3.setter
    def iproc3(self, iproc3):
        self.iproc3[...] = iproc3
    
    @property
    def my_nr3p(self):
        """
        Element my_nr3p ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 62
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__my_nr3p(self._handle)
    
    @my_nr3p.setter
    def my_nr3p(self, my_nr3p):
        libqepy_pw.f90wrap_fft_type_descriptor__set__my_nr3p(self._handle, my_nr3p)
    
    @property
    def my_nr2p(self):
        """
        Element my_nr2p ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 63
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__my_nr2p(self._handle)
    
    @my_nr2p.setter
    def my_nr2p(self, my_nr2p):
        libqepy_pw.f90wrap_fft_type_descriptor__set__my_nr2p(self._handle, my_nr2p)
    
    @property
    def my_i0r3p(self):
        """
        Element my_i0r3p ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 64
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__my_i0r3p(self._handle)
    
    @my_i0r3p.setter
    def my_i0r3p(self, my_i0r3p):
        libqepy_pw.f90wrap_fft_type_descriptor__set__my_i0r3p(self._handle, my_i0r3p)
    
    @property
    def my_i0r2p(self):
        """
        Element my_i0r2p ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 65
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__my_i0r2p(self._handle)
    
    @my_i0r2p.setter
    def my_i0r2p(self, my_i0r2p):
        libqepy_pw.f90wrap_fft_type_descriptor__set__my_i0r2p(self._handle, my_i0r2p)
    
    @property
    def nr3p(self):
        """
        Element nr3p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 66
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr3p(self._handle)
        if array_handle in self._arrays:
            nr3p = self._arrays[array_handle]
        else:
            nr3p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr3p)
            self._arrays[array_handle] = nr3p
        return nr3p
    
    @nr3p.setter
    def nr3p(self, nr3p):
        self.nr3p[...] = nr3p
    
    @property
    def nr3p_offset(self):
        """
        Element nr3p_offset ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 67
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr3p_offset(self._handle)
        if array_handle in self._arrays:
            nr3p_offset = self._arrays[array_handle]
        else:
            nr3p_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr3p_offset)
            self._arrays[array_handle] = nr3p_offset
        return nr3p_offset
    
    @nr3p_offset.setter
    def nr3p_offset(self, nr3p_offset):
        self.nr3p_offset[...] = nr3p_offset
    
    @property
    def nr2p(self):
        """
        Element nr2p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 68
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr2p(self._handle)
        if array_handle in self._arrays:
            nr2p = self._arrays[array_handle]
        else:
            nr2p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr2p)
            self._arrays[array_handle] = nr2p
        return nr2p
    
    @nr2p.setter
    def nr2p(self, nr2p):
        self.nr2p[...] = nr2p
    
    @property
    def nr2p_offset(self):
        """
        Element nr2p_offset ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 69
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr2p_offset(self._handle)
        if array_handle in self._arrays:
            nr2p_offset = self._arrays[array_handle]
        else:
            nr2p_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr2p_offset)
            self._arrays[array_handle] = nr2p_offset
        return nr2p_offset
    
    @nr2p_offset.setter
    def nr2p_offset(self, nr2p_offset):
        self.nr2p_offset[...] = nr2p_offset
    
    @property
    def nr1p(self):
        """
        Element nr1p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 70
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr1p(self._handle)
        if array_handle in self._arrays:
            nr1p = self._arrays[array_handle]
        else:
            nr1p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr1p)
            self._arrays[array_handle] = nr1p
        return nr1p
    
    @nr1p.setter
    def nr1p(self, nr1p):
        self.nr1p[...] = nr1p
    
    @property
    def nr1w(self):
        """
        Element nr1w ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 71
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w(self._handle)
        if array_handle in self._arrays:
            nr1w = self._arrays[array_handle]
        else:
            nr1w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w)
            self._arrays[array_handle] = nr1w
        return nr1w
    
    @nr1w.setter
    def nr1w(self, nr1w):
        self.nr1w[...] = nr1w
    
    @property
    def nr1w_tg(self):
        """
        Element nr1w_tg ftype=integer               pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 72
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nr1w_tg(self._handle)
    
    @nr1w_tg.setter
    def nr1w_tg(self, nr1w_tg):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nr1w_tg(self._handle, nr1w_tg)
    
    @property
    def i0r3p(self):
        """
        Element i0r3p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 73
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__i0r3p(self._handle)
        if array_handle in self._arrays:
            i0r3p = self._arrays[array_handle]
        else:
            i0r3p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__i0r3p)
            self._arrays[array_handle] = i0r3p
        return i0r3p
    
    @i0r3p.setter
    def i0r3p(self, i0r3p):
        self.i0r3p[...] = i0r3p
    
    @property
    def i0r2p(self):
        """
        Element i0r2p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 74
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__i0r2p(self._handle)
        if array_handle in self._arrays:
            i0r2p = self._arrays[array_handle]
        else:
            i0r2p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__i0r2p)
            self._arrays[array_handle] = i0r2p
        return i0r2p
    
    @i0r2p.setter
    def i0r2p(self, i0r2p):
        self.i0r2p[...] = i0r2p
    
    @property
    def ir1p(self):
        """
        Element ir1p ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 75
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1p(self._handle)
        if array_handle in self._arrays:
            ir1p = self._arrays[array_handle]
        else:
            ir1p = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1p)
            self._arrays[array_handle] = ir1p
        return ir1p
    
    @ir1p.setter
    def ir1p(self, ir1p):
        self.ir1p[...] = ir1p
    
    @property
    def indp(self):
        """
        Element indp ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 76
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indp(self._handle)
        if array_handle in self._arrays:
            indp = self._arrays[array_handle]
        else:
            indp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indp)
            self._arrays[array_handle] = indp
        return indp
    
    @indp.setter
    def indp(self, indp):
        self.indp[...] = indp
    
    @property
    def ir1w(self):
        """
        Element ir1w ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 77
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w(self._handle)
        if array_handle in self._arrays:
            ir1w = self._arrays[array_handle]
        else:
            ir1w = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w)
            self._arrays[array_handle] = ir1w
        return ir1w
    
    @ir1w.setter
    def ir1w(self, ir1w):
        self.ir1w[...] = ir1w
    
    @property
    def indw(self):
        """
        Element indw ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 78
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indw(self._handle)
        if array_handle in self._arrays:
            indw = self._arrays[array_handle]
        else:
            indw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indw)
            self._arrays[array_handle] = indw
        return indw
    
    @indw.setter
    def indw(self, indw):
        self.indw[...] = indw
    
    @property
    def ir1w_tg(self):
        """
        Element ir1w_tg ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 79
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_tg(self._handle)
        if array_handle in self._arrays:
            ir1w_tg = self._arrays[array_handle]
        else:
            ir1w_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_tg)
            self._arrays[array_handle] = ir1w_tg
        return ir1w_tg
    
    @ir1w_tg.setter
    def ir1w_tg(self, ir1w_tg):
        self.ir1w_tg[...] = ir1w_tg
    
    @property
    def indw_tg(self):
        """
        Element indw_tg ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 80
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indw_tg(self._handle)
        if array_handle in self._arrays:
            indw_tg = self._arrays[array_handle]
        else:
            indw_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indw_tg)
            self._arrays[array_handle] = indw_tg
        return indw_tg
    
    @indw_tg.setter
    def indw_tg(self, indw_tg):
        self.indw_tg[...] = indw_tg
    
    @property
    def ir1p_d(self):
        """
        Element ir1p_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 81
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1p_d(self._handle)
        if array_handle in self._arrays:
            ir1p_d = self._arrays[array_handle]
        else:
            ir1p_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1p_d)
            self._arrays[array_handle] = ir1p_d
        return ir1p_d
    
    @ir1p_d.setter
    def ir1p_d(self, ir1p_d):
        self.ir1p_d[...] = ir1p_d
    
    @property
    def ir1w_d(self):
        """
        Element ir1w_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 81
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_d(self._handle)
        if array_handle in self._arrays:
            ir1w_d = self._arrays[array_handle]
        else:
            ir1w_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_d)
            self._arrays[array_handle] = ir1w_d
        return ir1w_d
    
    @ir1w_d.setter
    def ir1w_d(self, ir1w_d):
        self.ir1w_d[...] = ir1w_d
    
    @property
    def ir1w_tg_d(self):
        """
        Element ir1w_tg_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 81
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_tg_d(self._handle)
        if array_handle in self._arrays:
            ir1w_tg_d = self._arrays[array_handle]
        else:
            ir1w_tg_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ir1w_tg_d)
            self._arrays[array_handle] = ir1w_tg_d
        return ir1w_tg_d
    
    @ir1w_tg_d.setter
    def ir1w_tg_d(self, ir1w_tg_d):
        self.ir1w_tg_d[...] = ir1w_tg_d
    
    @property
    def indp_d(self):
        """
        Element indp_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 82
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indp_d(self._handle)
        if array_handle in self._arrays:
            indp_d = self._arrays[array_handle]
        else:
            indp_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indp_d)
            self._arrays[array_handle] = indp_d
        return indp_d
    
    @indp_d.setter
    def indp_d(self, indp_d):
        self.indp_d[...] = indp_d
    
    @property
    def indw_d(self):
        """
        Element indw_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 82
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indw_d(self._handle)
        if array_handle in self._arrays:
            indw_d = self._arrays[array_handle]
        else:
            indw_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indw_d)
            self._arrays[array_handle] = indw_d
        return indw_d
    
    @indw_d.setter
    def indw_d(self, indw_d):
        self.indw_d[...] = indw_d
    
    @property
    def indw_tg_d(self):
        """
        Element indw_tg_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 82
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__indw_tg_d(self._handle)
        if array_handle in self._arrays:
            indw_tg_d = self._arrays[array_handle]
        else:
            indw_tg_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__indw_tg_d)
            self._arrays[array_handle] = indw_tg_d
        return indw_tg_d
    
    @indw_tg_d.setter
    def indw_tg_d(self, indw_tg_d):
        self.indw_tg_d[...] = indw_tg_d
    
    @property
    def nr1p_d(self):
        """
        Element nr1p_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 83
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr1p_d(self._handle)
        if array_handle in self._arrays:
            nr1p_d = self._arrays[array_handle]
        else:
            nr1p_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr1p_d)
            self._arrays[array_handle] = nr1p_d
        return nr1p_d
    
    @nr1p_d.setter
    def nr1p_d(self, nr1p_d):
        self.nr1p_d[...] = nr1p_d
    
    @property
    def nr1w_d(self):
        """
        Element nr1w_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 83
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w_d(self._handle)
        if array_handle in self._arrays:
            nr1w_d = self._arrays[array_handle]
        else:
            nr1w_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w_d)
            self._arrays[array_handle] = nr1w_d
        return nr1w_d
    
    @nr1w_d.setter
    def nr1w_d(self, nr1w_d):
        self.nr1w_d[...] = nr1w_d
    
    @property
    def nr1w_tg_d(self):
        """
        Element nr1w_tg_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 83
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w_tg_d(self._handle)
        if array_handle in self._arrays:
            nr1w_tg_d = self._arrays[array_handle]
        else:
            nr1w_tg_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nr1w_tg_d)
            self._arrays[array_handle] = nr1w_tg_d
        return nr1w_tg_d
    
    @nr1w_tg_d.setter
    def nr1w_tg_d(self, nr1w_tg_d):
        self.nr1w_tg_d[...] = nr1w_tg_d
    
    @property
    def nst(self):
        """
        Element nst ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 84
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nst(self._handle)
    
    @nst.setter
    def nst(self, nst):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nst(self._handle, nst)
    
    @property
    def nsp(self):
        """
        Element nsp ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 85
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nsp(self._handle)
        if array_handle in self._arrays:
            nsp = self._arrays[array_handle]
        else:
            nsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nsp)
            self._arrays[array_handle] = nsp
        return nsp
    
    @nsp.setter
    def nsp(self, nsp):
        self.nsp[...] = nsp
    
    @property
    def nsp_offset(self):
        """
        Element nsp_offset ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 87
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nsp_offset(self._handle)
        if array_handle in self._arrays:
            nsp_offset = self._arrays[array_handle]
        else:
            nsp_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nsp_offset)
            self._arrays[array_handle] = nsp_offset
        return nsp_offset
    
    @nsp_offset.setter
    def nsp_offset(self, nsp_offset):
        self.nsp_offset[...] = nsp_offset
    
    @property
    def nsw(self):
        """
        Element nsw ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 88
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nsw(self._handle)
        if array_handle in self._arrays:
            nsw = self._arrays[array_handle]
        else:
            nsw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nsw)
            self._arrays[array_handle] = nsw
        return nsw
    
    @nsw.setter
    def nsw(self, nsw):
        self.nsw[...] = nsw
    
    @property
    def nsw_offset(self):
        """
        Element nsw_offset ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 89
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nsw_offset(self._handle)
        if array_handle in self._arrays:
            nsw_offset = self._arrays[array_handle]
        else:
            nsw_offset = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nsw_offset)
            self._arrays[array_handle] = nsw_offset
        return nsw_offset
    
    @nsw_offset.setter
    def nsw_offset(self, nsw_offset):
        self.nsw_offset[...] = nsw_offset
    
    @property
    def nsw_tg(self):
        """
        Element nsw_tg ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 90
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nsw_tg(self._handle)
        if array_handle in self._arrays:
            nsw_tg = self._arrays[array_handle]
        else:
            nsw_tg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nsw_tg)
            self._arrays[array_handle] = nsw_tg
        return nsw_tg
    
    @nsw_tg.setter
    def nsw_tg(self, nsw_tg):
        self.nsw_tg[...] = nsw_tg
    
    @property
    def ngl(self):
        """
        Element ngl ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 91
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ngl(self._handle)
        if array_handle in self._arrays:
            ngl = self._arrays[array_handle]
        else:
            ngl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ngl)
            self._arrays[array_handle] = ngl
        return ngl
    
    @ngl.setter
    def ngl(self, ngl):
        self.ngl[...] = ngl
    
    @property
    def nwl(self):
        """
        Element nwl ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 92
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nwl(self._handle)
        if array_handle in self._arrays:
            nwl = self._arrays[array_handle]
        else:
            nwl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nwl)
            self._arrays[array_handle] = nwl
        return nwl
    
    @nwl.setter
    def nwl(self, nwl):
        self.nwl[...] = nwl
    
    @property
    def ngm(self):
        """
        Element ngm ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 93
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__ngm(self._handle)
    
    @ngm.setter
    def ngm(self, ngm):
        libqepy_pw.f90wrap_fft_type_descriptor__set__ngm(self._handle, ngm)
    
    @property
    def ngw(self):
        """
        Element ngw ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 97
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__ngw(self._handle)
    
    @ngw.setter
    def ngw(self, ngw):
        libqepy_pw.f90wrap_fft_type_descriptor__set__ngw(self._handle, ngw)
    
    @property
    def iplp(self):
        """
        Element iplp ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 101
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iplp(self._handle)
        if array_handle in self._arrays:
            iplp = self._arrays[array_handle]
        else:
            iplp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iplp)
            self._arrays[array_handle] = iplp
        return iplp
    
    @iplp.setter
    def iplp(self, iplp):
        self.iplp[...] = iplp
    
    @property
    def iplw(self):
        """
        Element iplw ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 102
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iplw(self._handle)
        if array_handle in self._arrays:
            iplw = self._arrays[array_handle]
        else:
            iplw = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iplw)
            self._arrays[array_handle] = iplw
        return iplw
    
    @iplw.setter
    def iplw(self, iplw):
        self.iplw[...] = iplw
    
    @property
    def nnp(self):
        """
        Element nnp ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 103
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nnp(self._handle)
    
    @nnp.setter
    def nnp(self, nnp):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nnp(self._handle, nnp)
    
    @property
    def nnr(self):
        """
        Element nnr ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 104
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nnr(self._handle)
    
    @nnr.setter
    def nnr(self, nnr):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nnr(self._handle, nnr)
    
    @property
    def nnr_tg(self):
        """
        Element nnr_tg ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 108
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__nnr_tg(self._handle)
    
    @nnr_tg.setter
    def nnr_tg(self, nnr_tg):
        libqepy_pw.f90wrap_fft_type_descriptor__set__nnr_tg(self._handle, nnr_tg)
    
    @property
    def iss(self):
        """
        Element iss ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 109
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__iss(self._handle)
        if array_handle in self._arrays:
            iss = self._arrays[array_handle]
        else:
            iss = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__iss)
            self._arrays[array_handle] = iss
        return iss
    
    @iss.setter
    def iss(self, iss):
        self.iss[...] = iss
    
    @property
    def isind(self):
        """
        Element isind ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 110
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__isind(self._handle)
        if array_handle in self._arrays:
            isind = self._arrays[array_handle]
        else:
            isind = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__isind)
            self._arrays[array_handle] = isind
        return isind
    
    @isind.setter
    def isind(self, isind):
        self.isind[...] = isind
    
    @property
    def ismap(self):
        """
        Element ismap ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 111
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ismap(self._handle)
        if array_handle in self._arrays:
            ismap = self._arrays[array_handle]
        else:
            ismap = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ismap)
            self._arrays[array_handle] = ismap
        return ismap
    
    @ismap.setter
    def ismap(self, ismap):
        self.ismap[...] = ismap
    
    @property
    def ismap_d(self):
        """
        Element ismap_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 112
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__ismap_d(self._handle)
        if array_handle in self._arrays:
            ismap_d = self._arrays[array_handle]
        else:
            ismap_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__ismap_d)
            self._arrays[array_handle] = ismap_d
        return ismap_d
    
    @ismap_d.setter
    def ismap_d(self, ismap_d):
        self.ismap_d[...] = ismap_d
    
    @property
    def nl(self):
        """
        Element nl ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 113
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nl(self._handle)
        if array_handle in self._arrays:
            nl = self._arrays[array_handle]
        else:
            nl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nl)
            self._arrays[array_handle] = nl
        return nl
    
    @nl.setter
    def nl(self, nl):
        self.nl[...] = nl
    
    @property
    def nlm(self):
        """
        Element nlm ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 114
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nlm(self._handle)
        if array_handle in self._arrays:
            nlm = self._arrays[array_handle]
        else:
            nlm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nlm)
            self._arrays[array_handle] = nlm
        return nlm
    
    @nlm.setter
    def nlm(self, nlm):
        self.nlm[...] = nlm
    
    @property
    def nl_d(self):
        """
        Element nl_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 115
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nl_d(self._handle)
        if array_handle in self._arrays:
            nl_d = self._arrays[array_handle]
        else:
            nl_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nl_d)
            self._arrays[array_handle] = nl_d
        return nl_d
    
    @nl_d.setter
    def nl_d(self, nl_d):
        self.nl_d[...] = nl_d
    
    @property
    def nlm_d(self):
        """
        Element nlm_d ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 116
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__nlm_d(self._handle)
        if array_handle in self._arrays:
            nlm_d = self._arrays[array_handle]
        else:
            nlm_d = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__nlm_d)
            self._arrays[array_handle] = nlm_d
        return nlm_d
    
    @nlm_d.setter
    def nlm_d(self, nlm_d):
        self.nlm_d[...] = nlm_d
    
    @property
    def tg_snd(self):
        """
        Element tg_snd ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 119
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__tg_snd(self._handle)
        if array_handle in self._arrays:
            tg_snd = self._arrays[array_handle]
        else:
            tg_snd = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__tg_snd)
            self._arrays[array_handle] = tg_snd
        return tg_snd
    
    @tg_snd.setter
    def tg_snd(self, tg_snd):
        self.tg_snd[...] = tg_snd
    
    @property
    def tg_rcv(self):
        """
        Element tg_rcv ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 120
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__tg_rcv(self._handle)
        if array_handle in self._arrays:
            tg_rcv = self._arrays[array_handle]
        else:
            tg_rcv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__tg_rcv)
            self._arrays[array_handle] = tg_rcv
        return tg_rcv
    
    @tg_rcv.setter
    def tg_rcv(self, tg_rcv):
        self.tg_rcv[...] = tg_rcv
    
    @property
    def tg_sdsp(self):
        """
        Element tg_sdsp ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 121
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__tg_sdsp(self._handle)
        if array_handle in self._arrays:
            tg_sdsp = self._arrays[array_handle]
        else:
            tg_sdsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__tg_sdsp)
            self._arrays[array_handle] = tg_sdsp
        return tg_sdsp
    
    @tg_sdsp.setter
    def tg_sdsp(self, tg_sdsp):
        self.tg_sdsp[...] = tg_sdsp
    
    @property
    def tg_rdsp(self):
        """
        Element tg_rdsp ftype=integer pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 122
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__tg_rdsp(self._handle)
        if array_handle in self._arrays:
            tg_rdsp = self._arrays[array_handle]
        else:
            tg_rdsp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__tg_rdsp)
            self._arrays[array_handle] = tg_rdsp
        return tg_rdsp
    
    @tg_rdsp.setter
    def tg_rdsp(self, tg_rdsp):
        self.tg_rdsp[...] = tg_rdsp
    
    @property
    def has_task_groups(self):
        """
        Element has_task_groups ftype=logical pytype=bool
        
        
        Defined at ../fftxlib/fft_types.fpp line 124
        
        """
        return \
            libqepy_pw.f90wrap_fft_type_descriptor__get__has_task_groups(self._handle)
    
    @has_task_groups.setter
    def has_task_groups(self, has_task_groups):
        libqepy_pw.f90wrap_fft_type_descriptor__set__has_task_groups(self._handle, \
            has_task_groups)
    
    @property
    def use_pencil_decomposition(self):
        """
        Element use_pencil_decomposition ftype=logical pytype=bool
        
        
        Defined at ../fftxlib/fft_types.fpp line 125
        
        """
        return \
            libqepy_pw.f90wrap_fft_type_descriptor__get__use_pencil_decomposition(self._handle)
    
    @use_pencil_decomposition.setter
    def use_pencil_decomposition(self, use_pencil_decomposition):
        libqepy_pw.f90wrap_fft_type_descriptor__set__use_pencil_decomposition(self._handle, \
            use_pencil_decomposition)
    
    @property
    def rho_clock_label(self):
        """
        Element rho_clock_label ftype=character(len=12) pytype=str
        
        
        Defined at ../fftxlib/fft_types.fpp line 127
        
        """
        return \
            libqepy_pw.f90wrap_fft_type_descriptor__get__rho_clock_label(self._handle)
    
    @rho_clock_label.setter
    def rho_clock_label(self, rho_clock_label):
        libqepy_pw.f90wrap_fft_type_descriptor__set__rho_clock_label(self._handle, \
            rho_clock_label)
    
    @property
    def wave_clock_label(self):
        """
        Element wave_clock_label ftype=character(len=12) pytype=str
        
        
        Defined at ../fftxlib/fft_types.fpp line 128
        
        """
        return \
            libqepy_pw.f90wrap_fft_type_descriptor__get__wave_clock_label(self._handle)
    
    @wave_clock_label.setter
    def wave_clock_label(self, wave_clock_label):
        libqepy_pw.f90wrap_fft_type_descriptor__set__wave_clock_label(self._handle, \
            wave_clock_label)
    
    @property
    def grid_id(self):
        """
        Element grid_id ftype=integer  pytype=int
        
        
        Defined at ../fftxlib/fft_types.fpp line 129
        
        """
        return libqepy_pw.f90wrap_fft_type_descriptor__get__grid_id(self._handle)
    
    @grid_id.setter
    def grid_id(self, grid_id):
        libqepy_pw.f90wrap_fft_type_descriptor__set__grid_id(self._handle, grid_id)
    
    @property
    def aux(self):
        """
        Element aux ftype=complex(dp) pytype=complex
        
        
        Defined at ../fftxlib/fft_types.fpp line 131
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_fft_type_descriptor__array__aux(self._handle)
        if array_handle in self._arrays:
            aux = self._arrays[array_handle]
        else:
            aux = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_fft_type_descriptor__array__aux)
            self._arrays[array_handle] = aux
        return aux
    
    @aux.setter
    def aux(self, aux):
        self.aux[...] = aux
    
    def __str__(self):
        ret = ['<fft_type_descriptor>{\n']
        ret.append('    nr1 : ')
        ret.append(repr(self.nr1))
        ret.append(',\n    nr2 : ')
        ret.append(repr(self.nr2))
        ret.append(',\n    nr3 : ')
        ret.append(repr(self.nr3))
        ret.append(',\n    nr1x : ')
        ret.append(repr(self.nr1x))
        ret.append(',\n    nr2x : ')
        ret.append(repr(self.nr2x))
        ret.append(',\n    nr3x : ')
        ret.append(repr(self.nr3x))
        ret.append(',\n    lpara : ')
        ret.append(repr(self.lpara))
        ret.append(',\n    lgamma : ')
        ret.append(repr(self.lgamma))
        ret.append(',\n    root : ')
        ret.append(repr(self.root))
        ret.append(',\n    comm : ')
        ret.append(repr(self.comm))
        ret.append(',\n    comm2 : ')
        ret.append(repr(self.comm2))
        ret.append(',\n    comm3 : ')
        ret.append(repr(self.comm3))
        ret.append(',\n    nproc : ')
        ret.append(repr(self.nproc))
        ret.append(',\n    nproc2 : ')
        ret.append(repr(self.nproc2))
        ret.append(',\n    nproc3 : ')
        ret.append(repr(self.nproc3))
        ret.append(',\n    mype : ')
        ret.append(repr(self.mype))
        ret.append(',\n    mype2 : ')
        ret.append(repr(self.mype2))
        ret.append(',\n    mype3 : ')
        ret.append(repr(self.mype3))
        ret.append(',\n    iproc : ')
        ret.append(repr(self.iproc))
        ret.append(',\n    iproc2 : ')
        ret.append(repr(self.iproc2))
        ret.append(',\n    iproc3 : ')
        ret.append(repr(self.iproc3))
        ret.append(',\n    my_nr3p : ')
        ret.append(repr(self.my_nr3p))
        ret.append(',\n    my_nr2p : ')
        ret.append(repr(self.my_nr2p))
        ret.append(',\n    my_i0r3p : ')
        ret.append(repr(self.my_i0r3p))
        ret.append(',\n    my_i0r2p : ')
        ret.append(repr(self.my_i0r2p))
        ret.append(',\n    nr3p : ')
        ret.append(repr(self.nr3p))
        ret.append(',\n    nr3p_offset : ')
        ret.append(repr(self.nr3p_offset))
        ret.append(',\n    nr2p : ')
        ret.append(repr(self.nr2p))
        ret.append(',\n    nr2p_offset : ')
        ret.append(repr(self.nr2p_offset))
        ret.append(',\n    nr1p : ')
        ret.append(repr(self.nr1p))
        ret.append(',\n    nr1w : ')
        ret.append(repr(self.nr1w))
        ret.append(',\n    nr1w_tg : ')
        ret.append(repr(self.nr1w_tg))
        ret.append(',\n    i0r3p : ')
        ret.append(repr(self.i0r3p))
        ret.append(',\n    i0r2p : ')
        ret.append(repr(self.i0r2p))
        ret.append(',\n    ir1p : ')
        ret.append(repr(self.ir1p))
        ret.append(',\n    indp : ')
        ret.append(repr(self.indp))
        ret.append(',\n    ir1w : ')
        ret.append(repr(self.ir1w))
        ret.append(',\n    indw : ')
        ret.append(repr(self.indw))
        ret.append(',\n    ir1w_tg : ')
        ret.append(repr(self.ir1w_tg))
        ret.append(',\n    indw_tg : ')
        ret.append(repr(self.indw_tg))
        ret.append(',\n    ir1p_d : ')
        ret.append(repr(self.ir1p_d))
        ret.append(',\n    ir1w_d : ')
        ret.append(repr(self.ir1w_d))
        ret.append(',\n    ir1w_tg_d : ')
        ret.append(repr(self.ir1w_tg_d))
        ret.append(',\n    indp_d : ')
        ret.append(repr(self.indp_d))
        ret.append(',\n    indw_d : ')
        ret.append(repr(self.indw_d))
        ret.append(',\n    indw_tg_d : ')
        ret.append(repr(self.indw_tg_d))
        ret.append(',\n    nr1p_d : ')
        ret.append(repr(self.nr1p_d))
        ret.append(',\n    nr1w_d : ')
        ret.append(repr(self.nr1w_d))
        ret.append(',\n    nr1w_tg_d : ')
        ret.append(repr(self.nr1w_tg_d))
        ret.append(',\n    nst : ')
        ret.append(repr(self.nst))
        ret.append(',\n    nsp : ')
        ret.append(repr(self.nsp))
        ret.append(',\n    nsp_offset : ')
        ret.append(repr(self.nsp_offset))
        ret.append(',\n    nsw : ')
        ret.append(repr(self.nsw))
        ret.append(',\n    nsw_offset : ')
        ret.append(repr(self.nsw_offset))
        ret.append(',\n    nsw_tg : ')
        ret.append(repr(self.nsw_tg))
        ret.append(',\n    ngl : ')
        ret.append(repr(self.ngl))
        ret.append(',\n    nwl : ')
        ret.append(repr(self.nwl))
        ret.append(',\n    ngm : ')
        ret.append(repr(self.ngm))
        ret.append(',\n    ngw : ')
        ret.append(repr(self.ngw))
        ret.append(',\n    iplp : ')
        ret.append(repr(self.iplp))
        ret.append(',\n    iplw : ')
        ret.append(repr(self.iplw))
        ret.append(',\n    nnp : ')
        ret.append(repr(self.nnp))
        ret.append(',\n    nnr : ')
        ret.append(repr(self.nnr))
        ret.append(',\n    nnr_tg : ')
        ret.append(repr(self.nnr_tg))
        ret.append(',\n    iss : ')
        ret.append(repr(self.iss))
        ret.append(',\n    isind : ')
        ret.append(repr(self.isind))
        ret.append(',\n    ismap : ')
        ret.append(repr(self.ismap))
        ret.append(',\n    ismap_d : ')
        ret.append(repr(self.ismap_d))
        ret.append(',\n    nl : ')
        ret.append(repr(self.nl))
        ret.append(',\n    nlm : ')
        ret.append(repr(self.nlm))
        ret.append(',\n    nl_d : ')
        ret.append(repr(self.nl_d))
        ret.append(',\n    nlm_d : ')
        ret.append(repr(self.nlm_d))
        ret.append(',\n    tg_snd : ')
        ret.append(repr(self.tg_snd))
        ret.append(',\n    tg_rcv : ')
        ret.append(repr(self.tg_rcv))
        ret.append(',\n    tg_sdsp : ')
        ret.append(repr(self.tg_sdsp))
        ret.append(',\n    tg_rdsp : ')
        ret.append(repr(self.tg_rdsp))
        ret.append(',\n    has_task_groups : ')
        ret.append(repr(self.has_task_groups))
        ret.append(',\n    use_pencil_decomposition : ')
        ret.append(repr(self.use_pencil_decomposition))
        ret.append(',\n    rho_clock_label : ')
        ret.append(repr(self.rho_clock_label))
        ret.append(',\n    wave_clock_label : ')
        ret.append(repr(self.wave_clock_label))
        ret.append(',\n    grid_id : ')
        ret.append(repr(self.grid_id))
        ret.append(',\n    aux : ')
        ret.append(repr(self.aux))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def fft_stick_index(self, i, j):
    """
    fft_stick_index = fft_stick_index(self, i, j)
    
    
    Defined at ../fftxlib/fft_types.fpp lines 819-830
    
    Parameters
    ----------
    desc : Fft_Type_Descriptor
    i : int
    j : int
    
    Returns
    -------
    fft_stick_index : int
    
    """
    fft_stick_index = \
        libqepy_pw.f90wrap_fft_types__fft_stick_index(desc=self._handle, i=i, j=j)
    return fft_stick_index

def fft_index_to_3d(ir, dfft):
    """
    i, j, k, offrange = fft_index_to_3d(ir, dfft)
    
    
    Defined at ../fftxlib/fft_types.fpp lines 833-864
    
    Parameters
    ----------
    ir : int
    dfft : Fft_Type_Descriptor
    
    Returns
    -------
    i : int
    j : int
    k : int
    offrange : bool
    
    """
    i, j, k, offrange = libqepy_pw.f90wrap_fft_types__fft_index_to_3d(ir=ir, \
        dfft=dfft._handle)
    return i, j, k, offrange


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "fft_types".')

for func in _dt_array_initialisers:
    func()
