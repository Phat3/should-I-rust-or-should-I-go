#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

from pwn import *

CUSTOM_STUB ="""TEXT ·trampoline(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX // Load the argument before messing with SP
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ADDQ $256, SP      // Rollback SP to reuse this function's frame
    ANDQ $~15, SP      // Align the stack to 16-bytes
    CALL AX
    MOVQ BX, SP        // Restore SP
    MOVQ AX, ret+8(FP) // Place the return value on the stack
    RET


TEXT ·call_get_flag(SB), 0, $256-8
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ANDQ $~15, SP      // Align the stack to 16-bytes
    ADDQ $32, SP
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
    MOVQ BX, SP        // Restore SP
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

    p.recvuntil("3 - Custom command")
    p.sendline("3")

    p.recvuntil("Submit stub")
    p.send(payload + "EOF\n")

    print p.recvuntil("DONE!")
    print p.recvuntil("3 - Custom command")
    p.close()


if __name__ == "__main__":
    print sys.argv
    print get_flag("127.0.0.1", 6666, "AAAABBBB", "CCCCDDDD")
