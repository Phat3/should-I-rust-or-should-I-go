#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import string
import random
from pwn import *

POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase

def benign(ip, port):

    code_id = str(random.randint(0, 4294967295)) # Well, hopefully should not collide
    passwd = ''.join(random.choice(POSSIBILITIES) for x in range(20))

    p = remote(ip, port)
    p.recvuntil("6 - Debug interface", timeout=2)
    p.sendline("1")
    content = p.recvuntil("Here you go Einstein...", timeout=2)
    p.close()
    if 'Einstein' not in content:
        return False

    p = remote(ip, port)
    p.recvuntil("6 - Debug interface", timeout=2)
    p.sendline("2")
    p.recvuntil("Insert the new value", timeout=2)
    p.sendline(str(random.randint(1, 9999999)))
    content = p.recvuntil("Whoa relax!", timeout=2)
    p.close()
    if 'relax' not in content:
        return False

    p = remote(ip, port)
    p.recvuntil("6 - Debug interface", timeout=2)
    p.sendline("3")
    p.recvuntil("Insert percentage", timeout=2)
    p.sendline(str(random.randint(1, 9999999)))
    content = p.recvuntil("God damn!", timeout=2)
    p.close()
    if 'damn!' not in content:
        return False

    p = remote(ip, port)
    p.recvuntil("6 - Debug interface", timeout=2)
    p.sendline("4")
    content = p.recvuntil("I hope you know what you are doing...", timeout=2)
    p.close()
    if 'doing...' not in content:
        return False

    p = remote(ip, port)
    p.recvuntil("6 - Debug interface", timeout=2)
    p.sendline("5")
    p.recvuntil("Insert code ID", timeout=2)
    p.sendline(code_id)
    p.recvuntil("Insert password", timeout=2)
    p.sendline(passwd)
    content = p.recvuntil("Don't even trip dawg", timeout=2)
    p.close()
    if 'dawg' not in content:
        return False

    return True

if __name__ == "__main__":
    if not benign("127.0.0.1", 6666):
        raise Exception
