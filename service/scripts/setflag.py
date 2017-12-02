#!/usr/bin/env python
# -*- coding: utf-8 -*

import random
import string
import socket
import sys

from pwn import *

# To create random strings
POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase

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
    CALL set_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
"""

def set_flag(ip, port, flag):
    # We create a new note with the flag as content
    note_id = random.randint(0,4294967295) # Well, hopefully should not collide
    password = ''.join(random.choice(POSSIBILITIES) for x in range(20))
    content = flag

    # Interaction with the service
    # Try to be robust, services will not always answer immediately
    '''
    payload = CUSTOM_STUB % (password[:8], password[8:16],
                             password[16:24], password[24:32], password[32:],
                             note_id)
    '''
    payload = CUSTOM_STUB % (hex(unpack(password[:4])), hex(unpack(password[4:8])),
                             hex(unpack(password[8:12])), hex(unpack(password[12:16])), hex(unpack(password[16:])),
                             note_id)

    print payload

    p = remote(ip, port)

    p.recvuntil("3 - Custom command", timeout=2)
    p.sendline("3")

    p.recvuntil("Submit stub", timeout=2)
    p.send(payload + "EOF\n")

    print p.recvuntil("DONE!", timeout=2)
    print p.recvuntil("3 - Custom command")
    p.close()

    result = {
            'FLAG_ID': note_id, # Unique id for each flag
            'TOKEN': password  # benign (get_flag) will know this, exploits will not
            }

    print result


if __name__ == "__main__":
    print set_flag("127.0.0.1", 6666, sys.argv[1] if len(sys.argv)>1 else "FLG1234567890")
