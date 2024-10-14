"""
python binding for raspsim, a cycle-accurate x86 simulator based on PTLsim
"""
from __future__ import annotations
import typing
__all__ = ['Address', 'BoundsException', 'BreakpointException', 'CoprocOverrunException', 'Core', 'DebugException', 'DivideException', 'DoubleFaultException', 'FPUException', 'FPUNotAvailException', 'GPFaultException', 'InvalidOpcodeException', 'InvalidTSSException', 'MachineCheckException', 'Memory', 'NMIException', 'OverflowException', 'PageFaultException', 'Prot', 'RaspsimException', 'RegisterFile', 'SSEException', 'SegNotPresentException', 'SpuriousIntException', 'StackFaultException', 'UnalignedException', 'XMMRegister', 'getProtFromELFSegment']
class Address:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __add__(self, offset: int) -> Address:
        """
        Add an offset to the address
        """
    def __eq__(self, other: Address) -> bool:
        """
        Check if two addresses are equal
        """
    def __ge__(self, other: Address) -> bool:
        """
        Check if the address is greater than or equal to another address
        """
    def __gt__(self, other: Address) -> bool:
        """
        Check if the address is greater than another address
        """
    def __hash__(self) -> int:
        ...
    def __int__(self) -> int:
        """
        Get the address as an integer
        """
    def __le__(self, other: Address) -> bool:
        """
        Check if the address is less than or equal to another address
        """
    def __lt__(self, other: Address) -> bool:
        """
        Check if the address is less than another address
        """
    def __ne__(self, other: Address) -> bool:
        """
        Check if two addresses are not equal
        """
    def __sub__(self, offset: int) -> Address:
        """
        Subtract an offset from the address
        """
    def read(self, size: int = 1) -> bytes:
        """
        Read data from the address
        """
    def write(self, value: bytes) -> None:
        """
        Write data to the address
        """
class BoundsException(Exception):
    pass
class BreakpointException(Exception):
    pass
class CoprocOverrunException(Exception):
    pass
class Core:
    """
    A class to interact with the simulator
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, logfile: str = '/dev/null') -> None:
        """
        Create a new Raspsim instance
        """
    def __str__(self) -> str:
        """
        Get the string representation of the current state of the simulator
        """
    def disableSSE(self) -> None:
        """
        Disable SSE
        """
    def disableX87(self) -> None:
        """
        Disable X87
        """
    def enablePerfectCache(self) -> None:
        """
        Enable perfect cache
        """
    def enableStaticBranchPrediction(self) -> None:
        """
        Enable static branch prediction
        """
    def memmap(self, start: int, prot: Prot, length: int = 0, data: bytes = b'') -> Address:
        """
        Map a range of memory to the virtual address space of the simulator.
        
        Maps data from `data` into memory and fills the rest with zeros if `length` is greater than the size of `data`. If `length` is 0, the size of `data` will be used as length.
        """
    def run(self, ninstr: int = 18446744073709551615) -> None:
        """
        Run the simulator for a number of instructions
        """
    @property
    def cycles(self) -> int:
        """
        Get the number of cycles
        """
    @property
    def instructions(self) -> int:
        """
        Get the number of instructions
        """
    @property
    def memimg(self) -> Memory:
        """
        Get a memory image object
        """
    @property
    def registers(self) -> RegisterFile:
        """
        Get the register file
        """
class DebugException(Exception):
    pass
class DivideException(Exception):
    pass
class DoubleFaultException(Exception):
    pass
class FPUException(Exception):
    pass
class FPUNotAvailException(Exception):
    pass
class GPFaultException(Exception):
    pass
class InvalidOpcodeException(Exception):
    pass
class InvalidTSSException(Exception):
    pass
class MachineCheckException(Exception):
    pass
class Memory:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, slice: slice) -> bytes:
        """
        Get a slice of memory
        """
    def __setitem__(self, slice: slice, data: bytes) -> None:
        """
        Set a slice of memory
        """
class NMIException(Exception):
    pass
class OverflowException(Exception):
    pass
class PageFaultException(Exception):
    pass
class Prot:
    """
    Members:
    
      READ
    
      WRITE
    
      EXEC
    
      NONE
    
      RW
    
      RX
    
      RWX
    """
    EXEC: typing.ClassVar[Prot]  # value = <Prot.EXEC: 4>
    NONE: typing.ClassVar[Prot]  # value = <Prot.NONE: 0>
    READ: typing.ClassVar[Prot]  # value = <Prot.READ: 1>
    RW: typing.ClassVar[Prot]  # value = <Prot.RW: 3>
    RWX: typing.ClassVar[Prot]  # value = <Prot.RWX: 7>
    RX: typing.ClassVar[Prot]  # value = <Prot.RX: 5>
    WRITE: typing.ClassVar[Prot]  # value = <Prot.WRITE: 2>
    __members__: typing.ClassVar[dict[str, Prot]]  # value = {'READ': <Prot.READ: 1>, 'WRITE': <Prot.WRITE: 2>, 'EXEC': <Prot.EXEC: 4>, 'NONE': <Prot.NONE: 0>, 'RW': <Prot.RW: 3>, 'RX': <Prot.RX: 5>, 'RWX': <Prot.RWX: 7>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __and__(self, arg0: Prot) -> bool:
        """
        Check if a protection flag is set
        """
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, arg0: Prot) -> Prot:
        """
        Combine two protection flags
        """
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class RaspsimException(Exception):
    pass
class RegisterFile:
    """
    A class to access the registers of the virtual CPU
    """
    ah: int
    al: int
    ax: int
    bh: int
    bl: int
    bp: int
    bx: int
    ch: int
    cl: int
    cx: int
    dh: int
    di: int
    dl: int
    dx: int
    eax: int
    ebp: int
    ebx: int
    ecx: int
    edi: int
    edx: int
    esi: int
    esp: int
    r10: int
    r11: int
    r12: int
    r13: int
    r14: int
    r15: int
    r8: int
    r9: int
    rax: int
    rbp: int
    rbx: int
    rcx: int
    rdi: int
    rdx: int
    rip: int
    rsi: int
    rsp: int
    si: int
    sp: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, regname: str) -> int:
        """
        Get the value of a register
        """
    def __setitem__(self, regname: str, value: int) -> None:
        """
        Set the value of a register
        """
    @property
    def xmm0(self) -> XMMRegister:
        ...
    @property
    def xmm1(self) -> XMMRegister:
        ...
    @property
    def xmm10(self) -> XMMRegister:
        ...
    @property
    def xmm11(self) -> XMMRegister:
        ...
    @property
    def xmm12(self) -> XMMRegister:
        ...
    @property
    def xmm13(self) -> XMMRegister:
        ...
    @property
    def xmm2(self) -> XMMRegister:
        ...
    @property
    def xmm3(self) -> XMMRegister:
        ...
    @property
    def xmm4(self) -> XMMRegister:
        ...
    @property
    def xmm5(self) -> XMMRegister:
        ...
    @property
    def xmm6(self) -> XMMRegister:
        ...
    @property
    def xmm7(self) -> XMMRegister:
        ...
    @property
    def xmm8(self) -> XMMRegister:
        ...
    @property
    def xmm9(self) -> XMMRegister:
        ...
class SSEException(Exception):
    pass
class SegNotPresentException(Exception):
    pass
class SpuriousIntException(Exception):
    pass
class StackFaultException(Exception):
    pass
class UnalignedException(Exception):
    pass
class XMMRegister:
    """
    A class to access the XMM registers of the virtual CPU
    """
    chars: tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]
    pd: tuple[float, float]
    ps: tuple[float, float, float, float]
    sd: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def ss(self) -> float:
        ...
    @ss.setter
    def ss(self) -> float:
        ...
def getProtFromELFSegment(flags: int) -> Prot:
    """
    Get the protection as Raspsim Prot from ELF segment flags
    """
