from revelation.storage import is_local_address

from pydgin.utils import intmask


def load_program(elf, mem, coreids, alignment=0, ext_base=0x8e000000,
                 ext_size=32):
    """Copy the contents of an ELF file into individual cores.
    The 'elf' argument should be the result of a call to
    pydgin.elf.elf_reader().
    """
    sections   = elf.get_sections()
    entrypoint = -1
    for coreid in coreids:
        coreid_mask = coreid << 20
        for section in sections:
            if is_local_address(section.addr):
                start_addr = coreid_mask | section.addr
            else:
                start_addr = section.addr
            for index, data in enumerate(section.data):
                mem.write(start_addr + index, 1, ord(data), quiet=True)
            if section.name == '.text':
                entrypoint = intmask(section.addr)
            if section.name == '.data':
                mem.data_section = section.addr
    assert entrypoint >= 0
    return
