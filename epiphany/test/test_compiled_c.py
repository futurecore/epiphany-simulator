from epiphany.sim import Epiphany
from epiphany.test.machine import StateChecker

import os.path
import pytest

elf_dir = os.path.join('epiphany', 'test', 'c')


@pytest.mark.parametrize('elf_file,expected',
                         [('hello.elf',           'Hello, world!\n'),
                          pytest.mark.skip(('fib_print.elf',       '10946')),
                          pytest.mark.skip(('read_file.elf',       'Hello, world!')),
                          ('selfmod.elf',         'Hello\nWorld\n'),
                          ('selfmod2.elf',        'Hello\nWorld\n'),
                          ('user_interrupt1.elf', ('User interrupt 1.\n'
                                                   'User interrupt 2.\n'
                                                   'User interrupt 3.\n'
                                                   'User interrupt 4.\n'
                                                   'Another user interrupt.\n')),
                          pytest.mark.skip(('user_interrupt2.elf',
                           ('main:    trigger user interrupt with swi\n'
                            'user_isr:  begin\n'
                            'user_isr:  before float overflow\n'
                            'exception_isr:  begin\n'
                            'exception_isr:  trigger user interrupt with swi.\n'
                            'exception_isr:  end\n'
                            'user_isr:  begin\n'
                            'user_isr:  again, will not trigger float exception\n'
                            'user_isr:  end\n'
                            'user_isr:  after float overflow\n'
                            'user_isr:  end\n'))),
                         ])
def test_compiled_c_with_output(elf_file, expected, capfd):
    """Test an ELF file that has been compiled from a C function.
    This test checks text printed to STDOUT.
    """
    elf_filename = os.path.join(elf_dir, elf_file)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 100000
        epiphany.run()
        assert not epiphany.state.running
        out, err = capfd.readouterr()
        assert err == ''
        assert expected in out


@pytest.mark.parametrize('elf_file,expected',
                         [('fib_return.elf', StateChecker(rf0=10946)),
                          ('exit5.elf',      StateChecker(rf0=5)),
                          ('setilat.elf',    StateChecker(rf20=0xaaaaaaaa, rf21=0x5555, rfILATST=0xaaaaffff)),
                          ('clearilat.elf',  StateChecker(rf20=0xaaaaaaaa, rf21=0x5555, rfILATCL=0xaaaaffff)),
                         ])
def test_compiled_c_with_return(elf_file, expected):
    """Test an ELF file that has been compiled from a C function.
    This test checks the state of the simulator after exit.
    """
    elf_filename = os.path.join(elf_dir, elf_file)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 10000
        epiphany.run()
        expected.check(epiphany.state)
        assert not epiphany.state.running


@pytest.mark.parametrize('elf_file,expected', [('nothing.elf',   236),
                                               ('fib.elf',       441),
                                              ])
def test_compiled_c(elf_file, expected, capsys):
    """Test an ELF file that has been compiled from a C function.
    This test checks that the correct number of instructions have been executed.
    """
    elf_filename = os.path.join(elf_dir, elf_file)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 10000
        epiphany.run()
        out, err = capsys.readouterr()
        expected_text = 'Instructions Executed = ' + str(expected)
        assert expected_text in out
        assert err == ''
        assert not epiphany.state.running
