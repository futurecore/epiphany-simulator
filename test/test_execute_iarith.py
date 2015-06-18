from pydgin.utils import trim_32

from epiphany.instruction import Instruction
from epiphany.isa import decode
from epiphany.test.machine import StateChecker, new_state

import opcode_factory
import pytest


def test_add_register_arguments():
    instr = Instruction(opcode_factory.add32(rd=2, rn=1, rm=0), '')
    assert instr.rd == 2
    assert instr.rn == 1
    assert instr.rm == 0
    instr = Instruction(opcode_factory.add32(rd=10, rn=9, rm=8), '')
    assert instr.rd == 2 + 8
    assert instr.rn == 1 + 8
    assert instr.rm == 0 + 8


@pytest.mark.parametrize('factory,expected',
                         [(opcode_factory.add32, dict(AZ=0, rf2=92)),
                          (opcode_factory.sub32, dict(AZ=0, AN=0, rf2=2)),
                         ])
def test_execute_add32sub32(factory, expected):
    state = new_state(rf0=45, rf1=47)
    instr = factory(rd=2, rn=1, rm=0)
    name, executefn = decode(instr)
    executefn(state, Instruction(instr, None))
    expected_state = StateChecker(pc=4, **expected)
    expected_state.check(state)


@pytest.mark.parametrize('factory,expected',
                         [(opcode_factory.add16, dict(AZ=0, rf2=7)),
                          (opcode_factory.sub16, dict(AZ=0, AN=0, rf2=3)),
                         ])
def test_execute_add16sub16(factory, expected):
    state = new_state(rf0=2, rf1=5)
    instr = factory(rd=2, rn=1, rm=0)
    name, executefn = decode(instr)
    executefn(state, Instruction(instr, None))
    expected_state = StateChecker(pc=2, **expected)
    expected_state.check(state)



@pytest.mark.parametrize('opcode,imm,expected',
                         [(opcode_factory.add32_immediate, 0b01010101010,
                           dict(AZ=0, rf1=(0b01010101010 + 5))),
                          (opcode_factory.sub32_immediate, 0b01010101010,
                           dict(AZ=0, AN=1, AC=1, rf1=trim_32(5 - 0b01010101010))),
                          (opcode_factory.sub32_immediate, 0b00000000101,
                           dict(AZ=1, AN=0, AC=0, rf1=0)),
                         ])
def test_execute_arith32_immediate(opcode, imm, expected):
    state = new_state(rf0=5)
    instr = opcode(rd=1, rn=0, imm=imm)
    name, executefn = decode(instr)
    executefn(state, Instruction(instr, None))
    expected_state = StateChecker(pc=4, **expected)
    expected_state.check(state)


def test_sub32_immediate_argument():
    instr = Instruction(opcode_factory.sub32_immediate(rd=1, rn=0, imm=0b01010101010), '')
    assert instr.rd == 1
    assert instr.rn == 0
    assert instr.imm11 == 0b01010101010


@pytest.mark.parametrize('is16bit,imm,expected_pc',
                         [(False, 0b01111111,  254),
                          (True,  0b011111111, 510)])
def test_execute_bcond(is16bit, imm, expected_pc):
    state = new_state(AZ=1, pc=0)
    instr = opcode_factory.bcond16(condition=0b0000, imm=imm)
    name, executefn = decode(instr)
    executefn(state, Instruction(instr, None))
    expected_state = StateChecker(pc=expected_pc, AZ=1)
    expected_state.check(state)
