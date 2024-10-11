"""
Module qepy_common


Defined at qepy_common.fpp lines 5-309

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy
from qepy_pw.fft_types import fft_type_descriptor
from qepy_pw.scf import scf_type

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy_pw.input_base")
class input_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=input_base)
    
    
    Defined at qepy_common.fpp lines 19-28
    
    """
    def __init__(self, handle=None):
        """
        self = Input_Base()
        
        
        Defined at qepy_common.fpp lines 19-28
        
        
        Returns
        -------
        this : Input_Base
        	Object to be constructed
        
        
        Automatically generated constructor for input_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pw.f90wrap_qepy_common__input_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Input_Base
        
        
        Defined at qepy_common.fpp lines 19-28
        
        Parameters
        ----------
        this : Input_Base
        	Object to be destructed
        
        
        Automatically generated destructor for input_base
        """
        if self._alloc:
            libqepy_pw.f90wrap_qepy_common__input_base_finalise(this=self._handle)
    
    @property
    def my_world_comm(self):
        """
        Element my_world_comm ftype=integer             pytype=int
        
        
        Defined at qepy_common.fpp line 20
        
        """
        return libqepy_pw.f90wrap_input_base__get__my_world_comm(self._handle)
    
    @my_world_comm.setter
    def my_world_comm(self, my_world_comm):
        libqepy_pw.f90wrap_input_base__set__my_world_comm(self._handle, my_world_comm)
    
    @property
    def start_images(self):
        """
        Element start_images ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 21
        
        """
        return libqepy_pw.f90wrap_input_base__get__start_images(self._handle)
    
    @start_images.setter
    def start_images(self, start_images):
        libqepy_pw.f90wrap_input_base__set__start_images(self._handle, start_images)
    
    @property
    def filename(self):
        """
        Element filename ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 22
        
        """
        return libqepy_pw.f90wrap_input_base__get__filename(self._handle)
    
    @filename.setter
    def filename(self, filename):
        libqepy_pw.f90wrap_input_base__set__filename(self._handle, filename)
    
    @property
    def code(self):
        """
        Element code ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 23
        
        """
        return libqepy_pw.f90wrap_input_base__get__code(self._handle)
    
    @code.setter
    def code(self, code):
        libqepy_pw.f90wrap_input_base__set__code(self._handle, code)
    
    @property
    def tmp_dir(self):
        """
        Element tmp_dir ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 24
        
        """
        return libqepy_pw.f90wrap_input_base__get__tmp_dir(self._handle)
    
    @tmp_dir.setter
    def tmp_dir(self, tmp_dir):
        libqepy_pw.f90wrap_input_base__set__tmp_dir(self._handle, tmp_dir)
    
    @property
    def wfc_dir(self):
        """
        Element wfc_dir ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 25
        
        """
        return libqepy_pw.f90wrap_input_base__get__wfc_dir(self._handle)
    
    @wfc_dir.setter
    def wfc_dir(self, wfc_dir):
        libqepy_pw.f90wrap_input_base__set__wfc_dir(self._handle, wfc_dir)
    
    @property
    def prefix(self):
        """
        Element prefix ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 26
        
        """
        return libqepy_pw.f90wrap_input_base__get__prefix(self._handle)
    
    @prefix.setter
    def prefix(self, prefix):
        libqepy_pw.f90wrap_input_base__set__prefix(self._handle, prefix)
    
    @property
    def needwf(self):
        """
        Element needwf ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 28
        
        """
        return libqepy_pw.f90wrap_input_base__get__needwf(self._handle)
    
    @needwf.setter
    def needwf(self, needwf):
        libqepy_pw.f90wrap_input_base__set__needwf(self._handle, needwf)
    
    def __str__(self):
        ret = ['<input_base>{\n']
        ret.append('    my_world_comm : ')
        ret.append(repr(self.my_world_comm))
        ret.append(',\n    start_images : ')
        ret.append(repr(self.start_images))
        ret.append(',\n    filename : ')
        ret.append(repr(self.filename))
        ret.append(',\n    code : ')
        ret.append(repr(self.code))
        ret.append(',\n    tmp_dir : ')
        ret.append(repr(self.tmp_dir))
        ret.append(',\n    wfc_dir : ')
        ret.append(repr(self.wfc_dir))
        ret.append(',\n    prefix : ')
        ret.append(repr(self.prefix))
        ret.append(',\n    needwf : ')
        ret.append(repr(self.needwf))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy_pw.tddft_base")
class tddft_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=tddft_base)
    
    
    Defined at qepy_common.fpp lines 31-40
    
    """
    def __init__(self, handle=None):
        """
        self = Tddft_Base()
        
        
        Defined at qepy_common.fpp lines 31-40
        
        
        Returns
        -------
        this : Tddft_Base
        	Object to be constructed
        
        
        Automatically generated constructor for tddft_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pw.f90wrap_qepy_common__tddft_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Tddft_Base
        
        
        Defined at qepy_common.fpp lines 31-40
        
        Parameters
        ----------
        this : Tddft_Base
        	Object to be destructed
        
        
        Automatically generated destructor for tddft_base
        """
        if self._alloc:
            libqepy_pw.f90wrap_qepy_common__tddft_base_finalise(this=self._handle)
    
    def free(self):
        """
        free__binding__tddft_base(self)
        
        
        Defined at qepy_common.fpp lines 186-192
        
        Parameters
        ----------
        obj : unknown
        
        """
        libqepy_pw.f90wrap_qepy_common__free__binding__tddft_base(obj=self._handle)
    
    @property
    def initial(self):
        """
        Element initial ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 32
        
        """
        return libqepy_pw.f90wrap_tddft_base__get__initial(self._handle)
    
    @initial.setter
    def initial(self, initial):
        libqepy_pw.f90wrap_tddft_base__set__initial(self._handle, initial)
    
    @property
    def finish(self):
        """
        Element finish ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 33
        
        """
        return libqepy_pw.f90wrap_tddft_base__get__finish(self._handle)
    
    @finish.setter
    def finish(self, finish):
        libqepy_pw.f90wrap_tddft_base__set__finish(self._handle, finish)
    
    @property
    def istep(self):
        """
        Element istep ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 34
        
        """
        return libqepy_pw.f90wrap_tddft_base__get__istep(self._handle)
    
    @istep.setter
    def istep(self, istep):
        libqepy_pw.f90wrap_tddft_base__set__istep(self._handle, istep)
    
    @property
    def nstep(self):
        """
        Element nstep ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 35
        
        """
        return libqepy_pw.f90wrap_tddft_base__get__nstep(self._handle)
    
    @nstep.setter
    def nstep(self, nstep):
        libqepy_pw.f90wrap_tddft_base__set__nstep(self._handle, nstep)
    
    @property
    def iterative(self):
        """
        Element iterative ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 36
        
        """
        return libqepy_pw.f90wrap_tddft_base__get__iterative(self._handle)
    
    @iterative.setter
    def iterative(self, iterative):
        libqepy_pw.f90wrap_tddft_base__set__iterative(self._handle, iterative)
    
    @property
    def dipole(self):
        """
        Element dipole ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 37
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_tddft_base__array__dipole(self._handle)
        if array_handle in self._arrays:
            dipole = self._arrays[array_handle]
        else:
            dipole = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_tddft_base__array__dipole)
            self._arrays[array_handle] = dipole
        return dipole
    
    @dipole.setter
    def dipole(self, dipole):
        self.dipole[...] = dipole
    
    def __str__(self):
        ret = ['<tddft_base>{\n']
        ret.append('    initial : ')
        ret.append(repr(self.initial))
        ret.append(',\n    finish : ')
        ret.append(repr(self.finish))
        ret.append(',\n    istep : ')
        ret.append(repr(self.istep))
        ret.append(',\n    nstep : ')
        ret.append(repr(self.nstep))
        ret.append(',\n    iterative : ')
        ret.append(repr(self.iterative))
        ret.append(',\n    dipole : ')
        ret.append(repr(self.dipole))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy_pw.energies_base")
class energies_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=energies_base)
    
    
    Defined at qepy_common.fpp lines 43-83
    
    """
    def __init__(self, handle=None):
        """
        self = Energies_Base()
        
        
        Defined at qepy_common.fpp lines 43-83
        
        
        Returns
        -------
        this : Energies_Base
        	Object to be constructed
        
        
        Automatically generated constructor for energies_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pw.f90wrap_qepy_common__energies_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Energies_Base
        
        
        Defined at qepy_common.fpp lines 43-83
        
        Parameters
        ----------
        this : Energies_Base
        	Object to be destructed
        
        
        Automatically generated destructor for energies_base
        """
        if self._alloc:
            libqepy_pw.f90wrap_qepy_common__energies_base_finalise(this=self._handle)
    
    def reset(self, value):
        """
        reset__binding__energies_base(self, value)
        
        
        Defined at qepy_common.fpp lines 229-260
        
        Parameters
        ----------
        obj : unknown
        value : float
        
        """
        libqepy_pw.f90wrap_qepy_common__reset__binding__energies_base(obj=self._handle, \
            value=value)
    
    @property
    def etot(self):
        """
        Element etot ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 44
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etot(self._handle)
    
    @etot.setter
    def etot(self, etot):
        libqepy_pw.f90wrap_energies_base__set__etot(self._handle, etot)
    
    @property
    def ek(self):
        """
        Element ek ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 45
        
        """
        return libqepy_pw.f90wrap_energies_base__get__ek(self._handle)
    
    @ek.setter
    def ek(self, ek):
        libqepy_pw.f90wrap_energies_base__set__ek(self._handle, ek)
    
    @property
    def eloc(self):
        """
        Element eloc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 46
        
        """
        return libqepy_pw.f90wrap_energies_base__get__eloc(self._handle)
    
    @eloc.setter
    def eloc(self, eloc):
        libqepy_pw.f90wrap_energies_base__set__eloc(self._handle, eloc)
    
    @property
    def enl(self):
        """
        Element enl ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 47
        
        """
        return libqepy_pw.f90wrap_energies_base__get__enl(self._handle)
    
    @enl.setter
    def enl(self, enl):
        libqepy_pw.f90wrap_energies_base__set__enl(self._handle, enl)
    
    @property
    def ewld(self):
        """
        Element ewld ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 48
        
        """
        return libqepy_pw.f90wrap_energies_base__get__ewld(self._handle)
    
    @ewld.setter
    def ewld(self, ewld):
        libqepy_pw.f90wrap_energies_base__set__ewld(self._handle, ewld)
    
    @property
    def exc(self):
        """
        Element exc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 49
        
        """
        return libqepy_pw.f90wrap_energies_base__get__exc(self._handle)
    
    @exc.setter
    def exc(self, exc):
        libqepy_pw.f90wrap_energies_base__set__exc(self._handle, exc)
    
    @property
    def ehart(self):
        """
        Element ehart ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 50
        
        """
        return libqepy_pw.f90wrap_energies_base__get__ehart(self._handle)
    
    @ehart.setter
    def ehart(self, ehart):
        libqepy_pw.f90wrap_energies_base__set__ehart(self._handle, ehart)
    
    @property
    def fock2(self):
        """
        Element fock2 ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 51
        
        """
        return libqepy_pw.f90wrap_energies_base__get__fock2(self._handle)
    
    @fock2.setter
    def fock2(self, fock2):
        libqepy_pw.f90wrap_energies_base__set__fock2(self._handle, fock2)
    
    @property
    def demet(self):
        """
        Element demet ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 52
        
        """
        return libqepy_pw.f90wrap_energies_base__get__demet(self._handle)
    
    @demet.setter
    def demet(self, demet):
        libqepy_pw.f90wrap_energies_base__set__demet(self._handle, demet)
    
    @property
    def elondon(self):
        """
        Element elondon ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 53
        
        """
        return libqepy_pw.f90wrap_energies_base__get__elondon(self._handle)
    
    @elondon.setter
    def elondon(self, elondon):
        libqepy_pw.f90wrap_energies_base__set__elondon(self._handle, elondon)
    
    @property
    def edftd3(self):
        """
        Element edftd3 ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 54
        
        """
        return libqepy_pw.f90wrap_energies_base__get__edftd3(self._handle)
    
    @edftd3.setter
    def edftd3(self, edftd3):
        libqepy_pw.f90wrap_energies_base__set__edftd3(self._handle, edftd3)
    
    @property
    def exdm(self):
        """
        Element exdm ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 55
        
        """
        return libqepy_pw.f90wrap_energies_base__get__exdm(self._handle)
    
    @exdm.setter
    def exdm(self, exdm):
        libqepy_pw.f90wrap_energies_base__set__exdm(self._handle, exdm)
    
    @property
    def etsvdw(self):
        """
        Element etsvdw ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 56
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etsvdw(self._handle)
    
    @etsvdw.setter
    def etsvdw(self, etsvdw):
        libqepy_pw.f90wrap_energies_base__set__etsvdw(self._handle, etsvdw)
    
    @property
    def eext(self):
        """
        Element eext ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 57
        
        """
        return libqepy_pw.f90wrap_energies_base__get__eext(self._handle)
    
    @eext.setter
    def eext(self, eext):
        libqepy_pw.f90wrap_energies_base__set__eext(self._handle, eext)
    
    @property
    def etotefield(self):
        """
        Element etotefield ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 58
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etotefield(self._handle)
    
    @etotefield.setter
    def etotefield(self, etotefield):
        libqepy_pw.f90wrap_energies_base__set__etotefield(self._handle, etotefield)
    
    @property
    def etotgatefield(self):
        """
        Element etotgatefield ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 59
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etotgatefield(self._handle)
    
    @etotgatefield.setter
    def etotgatefield(self, etotgatefield):
        libqepy_pw.f90wrap_energies_base__set__etotgatefield(self._handle, \
            etotgatefield)
    
    @property
    def eth(self):
        """
        Element eth ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 60
        
        """
        return libqepy_pw.f90wrap_energies_base__get__eth(self._handle)
    
    @eth.setter
    def eth(self, eth):
        libqepy_pw.f90wrap_energies_base__set__eth(self._handle, eth)
    
    @property
    def en_el(self):
        """
        Element en_el ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 61
        
        """
        return libqepy_pw.f90wrap_energies_base__get__en_el(self._handle)
    
    @en_el.setter
    def en_el(self, en_el):
        libqepy_pw.f90wrap_energies_base__set__en_el(self._handle, en_el)
    
    @property
    def epaw(self):
        """
        Element epaw ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 62
        
        """
        return libqepy_pw.f90wrap_energies_base__get__epaw(self._handle)
    
    @epaw.setter
    def epaw(self, epaw):
        libqepy_pw.f90wrap_energies_base__set__epaw(self._handle, epaw)
    
    @property
    def egrand(self):
        """
        Element egrand ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 63
        
        """
        return libqepy_pw.f90wrap_energies_base__get__egrand(self._handle)
    
    @egrand.setter
    def egrand(self, egrand):
        libqepy_pw.f90wrap_energies_base__set__egrand(self._handle, egrand)
    
    @property
    def ept(self):
        """
        Element ept ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 64
        
        """
        return libqepy_pw.f90wrap_energies_base__get__ept(self._handle)
    
    @ept.setter
    def ept(self, ept):
        libqepy_pw.f90wrap_energies_base__set__ept(self._handle, ept)
    
    @property
    def esol(self):
        """
        Element esol ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 65
        
        """
        return libqepy_pw.f90wrap_energies_base__get__esol(self._handle)
    
    @esol.setter
    def esol(self, esol):
        libqepy_pw.f90wrap_energies_base__set__esol(self._handle, esol)
    
    @property
    def evsol(self):
        """
        Element evsol ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 66
        
        """
        return libqepy_pw.f90wrap_energies_base__get__evsol(self._handle)
    
    @evsol.setter
    def evsol(self, evsol):
        libqepy_pw.f90wrap_energies_base__set__evsol(self._handle, evsol)
    
    @property
    def esic(self):
        """
        Element esic ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 67
        
        """
        return libqepy_pw.f90wrap_energies_base__get__esic(self._handle)
    
    @esic.setter
    def esic(self, esic):
        libqepy_pw.f90wrap_energies_base__set__esic(self._handle, esic)
    
    @property
    def esci(self):
        """
        Element esci ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 68
        
        """
        return libqepy_pw.f90wrap_energies_base__get__esci(self._handle)
    
    @esci.setter
    def esci(self, esci):
        libqepy_pw.f90wrap_energies_base__set__esci(self._handle, esci)
    
    @property
    def extene(self):
        """
        Element extene ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 70
        
        """
        return libqepy_pw.f90wrap_energies_base__get__extene(self._handle)
    
    @extene.setter
    def extene(self, extene):
        libqepy_pw.f90wrap_energies_base__set__extene(self._handle, extene)
    
    @property
    def ehf(self):
        """
        Element ehf ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 71
        
        """
        return libqepy_pw.f90wrap_energies_base__get__ehf(self._handle)
    
    @ehf.setter
    def ehf(self, ehf):
        libqepy_pw.f90wrap_energies_base__set__ehf(self._handle, ehf)
    
    @property
    def etxc(self):
        """
        Element etxc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 73
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etxc(self._handle)
    
    @etxc.setter
    def etxc(self, etxc):
        libqepy_pw.f90wrap_energies_base__set__etxc(self._handle, etxc)
    
    @property
    def etxcc(self):
        """
        Element etxcc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 74
        
        """
        return libqepy_pw.f90wrap_energies_base__get__etxcc(self._handle)
    
    @etxcc.setter
    def etxcc(self, etxcc):
        libqepy_pw.f90wrap_energies_base__set__etxcc(self._handle, etxcc)
    
    @property
    def paw_ehart_ae(self):
        """
        Element paw_ehart_ae ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 75
        
        """
        return libqepy_pw.f90wrap_energies_base__get__paw_ehart_ae(self._handle)
    
    @paw_ehart_ae.setter
    def paw_ehart_ae(self, paw_ehart_ae):
        libqepy_pw.f90wrap_energies_base__set__paw_ehart_ae(self._handle, paw_ehart_ae)
    
    @property
    def paw_ehart_ps(self):
        """
        Element paw_ehart_ps ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 76
        
        """
        return libqepy_pw.f90wrap_energies_base__get__paw_ehart_ps(self._handle)
    
    @paw_ehart_ps.setter
    def paw_ehart_ps(self, paw_ehart_ps):
        libqepy_pw.f90wrap_energies_base__set__paw_ehart_ps(self._handle, paw_ehart_ps)
    
    @property
    def paw_exc_ae(self):
        """
        Element paw_exc_ae ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 77
        
        """
        return libqepy_pw.f90wrap_energies_base__get__paw_exc_ae(self._handle)
    
    @paw_exc_ae.setter
    def paw_exc_ae(self, paw_exc_ae):
        libqepy_pw.f90wrap_energies_base__set__paw_exc_ae(self._handle, paw_exc_ae)
    
    @property
    def paw_exc_ps(self):
        """
        Element paw_exc_ps ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 78
        
        """
        return libqepy_pw.f90wrap_energies_base__get__paw_exc_ps(self._handle)
    
    @paw_exc_ps.setter
    def paw_exc_ps(self, paw_exc_ps):
        libqepy_pw.f90wrap_energies_base__set__paw_exc_ps(self._handle, paw_exc_ps)
    
    def __str__(self):
        ret = ['<energies_base>{\n']
        ret.append('    etot : ')
        ret.append(repr(self.etot))
        ret.append(',\n    ek : ')
        ret.append(repr(self.ek))
        ret.append(',\n    eloc : ')
        ret.append(repr(self.eloc))
        ret.append(',\n    enl : ')
        ret.append(repr(self.enl))
        ret.append(',\n    ewld : ')
        ret.append(repr(self.ewld))
        ret.append(',\n    exc : ')
        ret.append(repr(self.exc))
        ret.append(',\n    ehart : ')
        ret.append(repr(self.ehart))
        ret.append(',\n    fock2 : ')
        ret.append(repr(self.fock2))
        ret.append(',\n    demet : ')
        ret.append(repr(self.demet))
        ret.append(',\n    elondon : ')
        ret.append(repr(self.elondon))
        ret.append(',\n    edftd3 : ')
        ret.append(repr(self.edftd3))
        ret.append(',\n    exdm : ')
        ret.append(repr(self.exdm))
        ret.append(',\n    etsvdw : ')
        ret.append(repr(self.etsvdw))
        ret.append(',\n    eext : ')
        ret.append(repr(self.eext))
        ret.append(',\n    etotefield : ')
        ret.append(repr(self.etotefield))
        ret.append(',\n    etotgatefield : ')
        ret.append(repr(self.etotgatefield))
        ret.append(',\n    eth : ')
        ret.append(repr(self.eth))
        ret.append(',\n    en_el : ')
        ret.append(repr(self.en_el))
        ret.append(',\n    epaw : ')
        ret.append(repr(self.epaw))
        ret.append(',\n    egrand : ')
        ret.append(repr(self.egrand))
        ret.append(',\n    ept : ')
        ret.append(repr(self.ept))
        ret.append(',\n    esol : ')
        ret.append(repr(self.esol))
        ret.append(',\n    evsol : ')
        ret.append(repr(self.evsol))
        ret.append(',\n    esic : ')
        ret.append(repr(self.esic))
        ret.append(',\n    esci : ')
        ret.append(repr(self.esci))
        ret.append(',\n    extene : ')
        ret.append(repr(self.extene))
        ret.append(',\n    ehf : ')
        ret.append(repr(self.ehf))
        ret.append(',\n    etxc : ')
        ret.append(repr(self.etxc))
        ret.append(',\n    etxcc : ')
        ret.append(repr(self.etxcc))
        ret.append(',\n    paw_ehart_ae : ')
        ret.append(repr(self.paw_ehart_ae))
        ret.append(',\n    paw_ehart_ps : ')
        ret.append(repr(self.paw_ehart_ps))
        ret.append(',\n    paw_exc_ae : ')
        ret.append(repr(self.paw_exc_ae))
        ret.append(',\n    paw_exc_ps : ')
        ret.append(repr(self.paw_exc_ps))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy_pw.embed_base")
class embed_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=embed_base)
    
    
    Defined at qepy_common.fpp lines 86-123
    
    """
    def __init__(self, handle=None):
        """
        self = Embed_Base()
        
        
        Defined at qepy_common.fpp lines 86-123
        
        
        Returns
        -------
        this : Embed_Base
        	Object to be constructed
        
        
        Automatically generated constructor for embed_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = libqepy_pw.f90wrap_qepy_common__embed_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Embed_Base
        
        
        Defined at qepy_common.fpp lines 86-123
        
        Parameters
        ----------
        this : Embed_Base
        	Object to be destructed
        
        
        Automatically generated destructor for embed_base
        """
        if self._alloc:
            libqepy_pw.f90wrap_qepy_common__embed_base_finalise(this=self._handle)
    
    def allocate_extpot(self):
        """
        allocate_extpot__binding__embed_base(self)
        
        
        Defined at qepy_common.fpp lines 195-209
        
        Parameters
        ----------
        embed : unknown
        
        """
        libqepy_pw.f90wrap_qepy_common__allocate_extpot__binding__embed_base(embed=self._handle)
    
    def allocate_extforces(self):
        """
        allocate_extforces__binding__embed_base(self)
        
        
        Defined at qepy_common.fpp lines 212-226
        
        Parameters
        ----------
        embed : unknown
        
        """
        libqepy_pw.f90wrap_qepy_common__allocate_extforces__binding__embed_base(embed=self._handle)
    
    def free(self):
        """
        free__binding__embed_base(self)
        
        
        Defined at qepy_common.fpp lines 175-183
        
        Parameters
        ----------
        obj : unknown
        
        """
        libqepy_pw.f90wrap_qepy_common__free__binding__embed_base(obj=self._handle)
    
    @property
    def input(self):
        """
        Element input ftype=type(input_base) pytype=Input_Base
        
        
        Defined at qepy_common.fpp line 87
        
        """
        input_handle = libqepy_pw.f90wrap_embed_base__get__input(self._handle)
        if tuple(input_handle) in self._objs:
            input = self._objs[tuple(input_handle)]
        else:
            input = input_base.from_handle(input_handle)
            self._objs[tuple(input_handle)] = input
        return input
    
    @input.setter
    def input(self, input):
        input = input._handle
        libqepy_pw.f90wrap_embed_base__set__input(self._handle, input)
    
    @property
    def tddft(self):
        """
        Element tddft ftype=type(tddft_base) pytype=Tddft_Base
        
        
        Defined at qepy_common.fpp line 88
        
        """
        tddft_handle = libqepy_pw.f90wrap_embed_base__get__tddft(self._handle)
        if tuple(tddft_handle) in self._objs:
            tddft = self._objs[tuple(tddft_handle)]
        else:
            tddft = tddft_base.from_handle(tddft_handle)
            self._objs[tuple(tddft_handle)] = tddft
        return tddft
    
    @tddft.setter
    def tddft(self, tddft):
        tddft = tddft._handle
        libqepy_pw.f90wrap_embed_base__set__tddft(self._handle, tddft)
    
    @property
    def energies(self):
        """
        Element energies ftype=type(energies_base) pytype=Energies_Base
        
        
        Defined at qepy_common.fpp line 89
        
        """
        energies_handle = libqepy_pw.f90wrap_embed_base__get__energies(self._handle)
        if tuple(energies_handle) in self._objs:
            energies = self._objs[tuple(energies_handle)]
        else:
            energies = energies_base.from_handle(energies_handle)
            self._objs[tuple(energies_handle)] = energies
        return energies
    
    @energies.setter
    def energies(self, energies):
        energies = energies._handle
        libqepy_pw.f90wrap_embed_base__set__energies(self._handle, energies)
    
    @property
    def task(self):
        """
        Element task ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 90
        
        """
        return libqepy_pw.f90wrap_embed_base__get__task(self._handle)
    
    @task.setter
    def task(self, task):
        libqepy_pw.f90wrap_embed_base__set__task(self._handle, task)
    
    @property
    def extpot(self):
        """
        Element extpot ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 91
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_embed_base__array__extpot(self._handle)
        if array_handle in self._arrays:
            extpot = self._arrays[array_handle]
        else:
            extpot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_embed_base__array__extpot)
            self._arrays[array_handle] = extpot
        return extpot
    
    @extpot.setter
    def extpot(self, extpot):
        self.extpot[...] = extpot
    
    @property
    def extene(self):
        """
        Element extene ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 92
        
        """
        return libqepy_pw.f90wrap_embed_base__get__extene(self._handle)
    
    @extene.setter
    def extene(self, extene):
        libqepy_pw.f90wrap_embed_base__set__extene(self._handle, extene)
    
    @property
    def exttype(self):
        """
        Element exttype ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 93
        
        """
        return libqepy_pw.f90wrap_embed_base__get__exttype(self._handle)
    
    @exttype.setter
    def exttype(self, exttype):
        libqepy_pw.f90wrap_embed_base__set__exttype(self._handle, exttype)
    
    @property
    def extforces(self):
        """
        Element extforces ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 94
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_embed_base__array__extforces(self._handle)
        if array_handle in self._arrays:
            extforces = self._arrays[array_handle]
        else:
            extforces = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_embed_base__array__extforces)
            self._arrays[array_handle] = extforces
        return extforces
    
    @extforces.setter
    def extforces(self, extforces):
        self.extforces[...] = extforces
    
    @property
    def extstress(self):
        """
        Element extstress ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 95
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            libqepy_pw.f90wrap_embed_base__array__extstress(self._handle)
        if array_handle in self._arrays:
            extstress = self._arrays[array_handle]
        else:
            extstress = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    libqepy_pw.f90wrap_embed_base__array__extstress)
            self._arrays[array_handle] = extstress
        return extstress
    
    @extstress.setter
    def extstress(self, extstress):
        self.extstress[...] = extstress
    
    @property
    def initial(self):
        """
        Element initial ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 96
        
        """
        return libqepy_pw.f90wrap_embed_base__get__initial(self._handle)
    
    @initial.setter
    def initial(self, initial):
        libqepy_pw.f90wrap_embed_base__set__initial(self._handle, initial)
    
    @property
    def finish(self):
        """
        Element finish ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 97
        
        """
        return libqepy_pw.f90wrap_embed_base__get__finish(self._handle)
    
    @finish.setter
    def finish(self, finish):
        libqepy_pw.f90wrap_embed_base__set__finish(self._handle, finish)
    
    @property
    def mix_coef(self):
        """
        Element mix_coef ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 98
        
        """
        return libqepy_pw.f90wrap_embed_base__get__mix_coef(self._handle)
    
    @mix_coef.setter
    def mix_coef(self, mix_coef):
        libqepy_pw.f90wrap_embed_base__set__mix_coef(self._handle, mix_coef)
    
    @property
    def etotal(self):
        """
        Element etotal ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 99
        
        """
        return libqepy_pw.f90wrap_embed_base__get__etotal(self._handle)
    
    @etotal.setter
    def etotal(self, etotal):
        libqepy_pw.f90wrap_embed_base__set__etotal(self._handle, etotal)
    
    @property
    def dnorm(self):
        """
        Element dnorm ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 100
        
        """
        return libqepy_pw.f90wrap_embed_base__get__dnorm(self._handle)
    
    @dnorm.setter
    def dnorm(self, dnorm):
        libqepy_pw.f90wrap_embed_base__set__dnorm(self._handle, dnorm)
    
    @property
    def lewald(self):
        """
        Element lewald ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 101
        
        """
        return libqepy_pw.f90wrap_embed_base__get__lewald(self._handle)
    
    @lewald.setter
    def lewald(self, lewald):
        libqepy_pw.f90wrap_embed_base__set__lewald(self._handle, lewald)
    
    @property
    def nlpp(self):
        """
        Element nlpp ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 102
        
        """
        return libqepy_pw.f90wrap_embed_base__get__nlpp(self._handle)
    
    @nlpp.setter
    def nlpp(self, nlpp):
        libqepy_pw.f90wrap_embed_base__set__nlpp(self._handle, nlpp)
    
    @property
    def diag_conv(self):
        """
        Element diag_conv ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 103
        
        """
        return libqepy_pw.f90wrap_embed_base__get__diag_conv(self._handle)
    
    @diag_conv.setter
    def diag_conv(self, diag_conv):
        libqepy_pw.f90wrap_embed_base__set__diag_conv(self._handle, diag_conv)
    
    @property
    def ldescf(self):
        """
        Element ldescf ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 104
        
        """
        return libqepy_pw.f90wrap_embed_base__get__ldescf(self._handle)
    
    @ldescf.setter
    def ldescf(self, ldescf):
        libqepy_pw.f90wrap_embed_base__set__ldescf(self._handle, ldescf)
    
    @property
    def iterative(self):
        """
        Element iterative ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 106
        
        """
        return libqepy_pw.f90wrap_embed_base__get__iterative(self._handle)
    
    @iterative.setter
    def iterative(self, iterative):
        libqepy_pw.f90wrap_embed_base__set__iterative(self._handle, iterative)
    
    @property
    def lmovecell(self):
        """
        Element lmovecell ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 108
        
        """
        return libqepy_pw.f90wrap_embed_base__get__lmovecell(self._handle)
    
    @lmovecell.setter
    def lmovecell(self, lmovecell):
        libqepy_pw.f90wrap_embed_base__set__lmovecell(self._handle, lmovecell)
    
    @property
    def dfftp(self):
        """
        Element dfftp ftype=type(fft_type_descriptor) pytype=Fft_Type_Descriptor
        
        
        Defined at qepy_common.fpp line 114
        
        """
        dfftp_handle = libqepy_pw.f90wrap_embed_base__get__dfftp(self._handle)
        if tuple(dfftp_handle) in self._objs:
            dfftp = self._objs[tuple(dfftp_handle)]
        else:
            dfftp = fft_type_descriptor.from_handle(dfftp_handle)
            self._objs[tuple(dfftp_handle)] = dfftp
        return dfftp
    
    @dfftp.setter
    def dfftp(self, dfftp):
        dfftp = dfftp._handle
        libqepy_pw.f90wrap_embed_base__set__dfftp(self._handle, dfftp)
    
    @property
    def dffts(self):
        """
        Element dffts ftype=type(fft_type_descriptor) pytype=Fft_Type_Descriptor
        
        
        Defined at qepy_common.fpp line 115
        
        """
        dffts_handle = libqepy_pw.f90wrap_embed_base__get__dffts(self._handle)
        if tuple(dffts_handle) in self._objs:
            dffts = self._objs[tuple(dffts_handle)]
        else:
            dffts = fft_type_descriptor.from_handle(dffts_handle)
            self._objs[tuple(dffts_handle)] = dffts
        return dffts
    
    @dffts.setter
    def dffts(self, dffts):
        dffts = dffts._handle
        libqepy_pw.f90wrap_embed_base__set__dffts(self._handle, dffts)
    
    @property
    def rho(self):
        """
        Element rho ftype=type(scf_type) pytype=Scf_Type
        
        
        Defined at qepy_common.fpp line 116
        
        """
        rho_handle = libqepy_pw.f90wrap_embed_base__get__rho(self._handle)
        if tuple(rho_handle) in self._objs:
            rho = self._objs[tuple(rho_handle)]
        else:
            rho = scf_type.from_handle(rho_handle)
            self._objs[tuple(rho_handle)] = rho
        return rho
    
    @rho.setter
    def rho(self, rho):
        rho = rho._handle
        libqepy_pw.f90wrap_embed_base__set__rho(self._handle, rho)
    
    @property
    def v(self):
        """
        Element v ftype=type(scf_type) pytype=Scf_Type
        
        
        Defined at qepy_common.fpp line 117
        
        """
        v_handle = libqepy_pw.f90wrap_embed_base__get__v(self._handle)
        if tuple(v_handle) in self._objs:
            v = self._objs[tuple(v_handle)]
        else:
            v = scf_type.from_handle(v_handle)
            self._objs[tuple(v_handle)] = v
        return v
    
    @v.setter
    def v(self, v):
        v = v._handle
        libqepy_pw.f90wrap_embed_base__set__v(self._handle, v)
    
    @property
    def vnew(self):
        """
        Element vnew ftype=type(scf_type) pytype=Scf_Type
        
        
        Defined at qepy_common.fpp line 118
        
        """
        vnew_handle = libqepy_pw.f90wrap_embed_base__get__vnew(self._handle)
        if tuple(vnew_handle) in self._objs:
            vnew = self._objs[tuple(vnew_handle)]
        else:
            vnew = scf_type.from_handle(vnew_handle)
            self._objs[tuple(vnew_handle)] = vnew
        return vnew
    
    @vnew.setter
    def vnew(self, vnew):
        vnew = vnew._handle
        libqepy_pw.f90wrap_embed_base__set__vnew(self._handle, vnew)
    
    def __str__(self):
        ret = ['<embed_base>{\n']
        ret.append('    input : ')
        ret.append(repr(self.input))
        ret.append(',\n    tddft : ')
        ret.append(repr(self.tddft))
        ret.append(',\n    energies : ')
        ret.append(repr(self.energies))
        ret.append(',\n    task : ')
        ret.append(repr(self.task))
        ret.append(',\n    extpot : ')
        ret.append(repr(self.extpot))
        ret.append(',\n    extene : ')
        ret.append(repr(self.extene))
        ret.append(',\n    exttype : ')
        ret.append(repr(self.exttype))
        ret.append(',\n    extforces : ')
        ret.append(repr(self.extforces))
        ret.append(',\n    extstress : ')
        ret.append(repr(self.extstress))
        ret.append(',\n    initial : ')
        ret.append(repr(self.initial))
        ret.append(',\n    finish : ')
        ret.append(repr(self.finish))
        ret.append(',\n    mix_coef : ')
        ret.append(repr(self.mix_coef))
        ret.append(',\n    etotal : ')
        ret.append(repr(self.etotal))
        ret.append(',\n    dnorm : ')
        ret.append(repr(self.dnorm))
        ret.append(',\n    lewald : ')
        ret.append(repr(self.lewald))
        ret.append(',\n    nlpp : ')
        ret.append(repr(self.nlpp))
        ret.append(',\n    diag_conv : ')
        ret.append(repr(self.diag_conv))
        ret.append(',\n    ldescf : ')
        ret.append(repr(self.ldescf))
        ret.append(',\n    iterative : ')
        ret.append(repr(self.iterative))
        ret.append(',\n    lmovecell : ')
        ret.append(repr(self.lmovecell))
        ret.append(',\n    dfftp : ')
        ret.append(repr(self.dfftp))
        ret.append(',\n    dffts : ')
        ret.append(repr(self.dffts))
        ret.append(',\n    rho : ')
        ret.append(repr(self.rho))
        ret.append(',\n    v : ')
        ret.append(repr(self.v))
        ret.append(',\n    vnew : ')
        ret.append(repr(self.vnew))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def set_embed(self):
    """
    set_embed(self)
    
    
    Defined at qepy_common.fpp lines 137-147
    
    Parameters
    ----------
    obj : Embed_Base
    
    """
    libqepy_pw.f90wrap_qepy_common__set_embed(obj=self._handle)

def get_is_mpi():
    """
    Element is_mpi ftype=logical pytype=bool
    
    
    Defined at qepy_common.fpp line 16
    
    """
    return libqepy_pw.f90wrap_qepy_common__get__is_mpi()

def set_is_mpi(is_mpi):
    libqepy_pw.f90wrap_qepy_common__set__is_mpi(is_mpi)

def get_is_openmp():
    """
    Element is_openmp ftype=logical pytype=bool
    
    
    Defined at qepy_common.fpp line 17
    
    """
    return libqepy_pw.f90wrap_qepy_common__get__is_openmp()

def set_is_openmp(is_openmp):
    libqepy_pw.f90wrap_qepy_common__set__is_openmp(is_openmp)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qepy_common".')

for func in _dt_array_initialisers:
    func()
