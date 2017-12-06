#!/usr/bin/env python
# -*- coding: utf-8 -*

import random
import string
import sys

from pwn import *

# To create random strings
POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase

# I was in a hurry and I didn't want to write a single function
# that creates the token and the flag at the same time
CUSTOM_STUB_TOKEN = """TEXT ·custom(SB), 0, $256-8
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
    CALL set_token(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
"""

CUSTOM_STUB_FLAG = """TEXT ·custom(SB), 0, $256-8
    MOVQ SP, BX
    ANDQ $~15, SP
    SUBQ $32, SP
    MOVQ $%s, 0(SP)
    MOVQ $%s, 4(SP)
    MOVQ $%s, 8(SP)
    MOVQ $%s, 12(SP)
    MOVQ $%d, DI
    MOVQ SP, SI
    MOVQ $13, DX
    CALL set_detonation_code(SB)
    MOVQ BX, SP
    MOVQ AX, ret+8(FP)
    RET
"""

def set_flag(ip, port, flag):
    # We create a new note with the flag as content
    note_id = random.randint(0, 4294967295) # Well, hopefully should not collide
    password = ''.join(random.choice(POSSIBILITIES) for x in range(20))
    content = flag
    # Create stub that creates the file containing the token
    payload_token = CUSTOM_STUB_TOKEN % (hex(unpack(password[:4])), hex(unpack(password[4:8])),
                                         hex(unpack(password[8:12])), hex(unpack(password[12:16])),
                                         hex(unpack(password[16:])),
                                         note_id)

    # Create stub that creates the file containing the flag
    payload_flag = CUSTOM_STUB_FLAG % (hex(unpack(content[:4])), hex(unpack(content[4:8])),
                                       hex(unpack(content[8:12])), hex(u8(content[12:])),
                                       note_id)
    p = remote(ip, port)

    # Try to create the token
    p.recvuntil("4 - Degug interface", timeout=2)
    p.sendline("4")

    p.recvuntil("Submit stub", timeout=2)
    p.send(payload_token + "EOF\n")

    response = p.recvuntil("DONE!", timeout=2)
    # if error return False
    if not "successfully wrote to file" in response:
        return False

    # Try to create the flag
    p.recvuntil("4 - Debug interface", timeout=2)
    p.sendline("4")

    p.recvuntil("Submit stub", timeout=2)
    p.send(payload_flag + "EOF\n")

    response = p.recvuntil("DONE!", timeout=2)
    p.close()
    # if error return False
    if not "successfully wrote to file" in response:
        return False
    # If everything worked correctly return the result
    result = {
        'FLAG_ID': note_id, # Unique id for each flag
        'TOKEN': password  # benign (get_flag) will know this, exploits will not
    }
    return result

if __name__ == "__main__":
    print set_flag("127.0.0.1", 6666, sys.argv[1] if len(sys.argv) > 1 else "FLG1234567890")
