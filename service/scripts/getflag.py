#!/usr/bin/env python
# -*- coding: utf-8 -*
import socket
import sys

from pwn import *

CUSTOM_STUB ="""TEXT ·custom(SB), 0, $256-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $32, SP
    MOVQ $%s, 0(SP)
    MOVQ $%s, 4(SP)
    MOVQ $%s, 8(SP)
    MOVQ $%s, 12(SP)
    MOVQ $%s, 16(SP)
    MOVQ $%d, DI
    MOVQ SP, SI
    MOVQ $20, DX
    CALL get_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
"""

def get_flag(ip, port, flag_id, token):
    # We read that note, knowing the password (in other words, we're benign traffic)
    # Whatever the patch, this must still work!

    payload = CUSTOM_STUB % (hex(unpack(token[:4])), hex(unpack(token[4:8])),
                             hex(unpack(token[8:12])), hex(unpack(token[12:16])), hex(unpack(token[16:])),
                             flag_id)
    print payload

    p = remote(ip, port)

    p.recvuntil("4 - Debug interface", timeout=2)
    p.sendline("4")

    p.recvuntil("Submit stub", timeout=2)
    p.send(payload + "EOF\n")

    print p.recvuntil("DONE!", timeout=2)
    print p.recvuntil("4 - Debug interface")
    p.close()


if __name__ == "__main__":
    print get_flag("127.0.0.1", 6666, 1454620416, "TkvUMJBjBiWC7V1AWqfY")
