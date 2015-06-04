#=======================================================================
# machine.py
#=======================================================================

from pydgin.storage import RegisterFile

#-----------------------------------------------------------------------
# State
#-----------------------------------------------------------------------
class State(object):
#    _virtualizable_ = ['pc', 'ncycles', 'N', 'Z', 'C', 'V']

    def __init__(self, memory, debug, reset_addr=0x0, **args):
        self.pc       = reset_addr
        self.rf       = RegisterFile(constant_zero=False, num_regs=64)
        self.mem      = memory

        self.running   = True
        self.debug     = debug
        self.rf.debug  = debug
        self.mem.debug = debug

        self.AN  = 0b0
        self.AZ  = 0b0
        self.AC  = 0b0
        self.AV  = 0b0
        self.AVS = 0b0
        self.BN  = 0b0
        self.BZ  = 0b0

        # other registers
        self.pc = 0b0
        self.status   = 0
        self.ncycles  = 0
        self.stats_en = False

        # marks if should be running, syscall_exit sets it false
        self.running = True

    def set_register(self, index, value):
        self.rf[index] = value

    def fetch_pc( self ):
        return self.pc
