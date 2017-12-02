#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

from pwn import *

CUSTOM_STUB ="""TEXT ·custom(SB), 0, $256-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $32, SP
    MOVQ $0x%s, 0(SP)
    MOVQ $0x%s, 4(SP)
    MOVQ $0x%s, 8(SP)
    MOVQ $0x%s, 12(SP)
    MOVQ SP, DI
    MOVQ $8, SI
    MOVQ SP, DX
    ADDQ $8, DX
    MOVQ $8, CX
    CALL get_detonation_code(SB)
    MOVQ BX, SP
    RET
"""

def get_flag(ip, port, flag_id, token):
    # We read that note, knowing the password (in other words, we're benign traffic)
    # Whatever the patch, this must still work!
    code_1 = flag_id.encode("hex")
    code_2 = token.encode("hex")

    payload = CUSTOM_STUB % (code_1[:8], code_1[8:],
                             code_2[:8], code_2[8:])

    p = remote(ip, port)

    p.recvuntil("3 - Custom command", timeout=2)
    p.sendline("3")

    p.recvuntil("Submit stub", timeout=2)
    p.send(payload + "EOF\n")

    print p.recvuntil("DONE!", timeout=2)
    print p.recvuntil("3 - Custom command")
    p.close()


if __name__ == "__main__":
    print get_flag("127.0.0.1", 6666, "AAAABBBB", "CCCCDDDD")
