#=======================================================================
# machine.py
#=======================================================================

from pydgin.storage import RegisterFile

RESET_ADDR = 0x58

#-----------------------------------------------------------------------
# State
#-----------------------------------------------------------------------
class State(object):
    _virtualizable_ = ['pc', 'num_insts', 'AN', 'AZ', 'AC', 'AV',
                       'AVS', 'BN', 'BIS', 'BUS', 'BVS', 'BZ']

    def __init__(self, memory, debug, reset_addr=RESET_ADDR):
        self.pc       = reset_addr
        self.rf       = RegisterFile(constant_zero=False, num_regs=107)
        self.mem      = memory

        self.running   = True   # Set False by bkpt instructions.
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
        self.BIS = 0b0
        self.BUS = 0b0
        self.BV  = 0b0
        self.BVS = 0b0

        # Other registers
        self.status = 0
        self.num_insts = 0
        self.stats_en = False

    def set_register(self, index, value):
        self.rf[index] = value

    def fetch_pc( self ):
        return self.pc
