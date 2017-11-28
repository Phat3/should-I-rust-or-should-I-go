import socket
import sys

from pwn import *

def get_flag(ip, port, flag_id, token):
    # We read that note, knowing the password (in other words, we're benign traffic)
    # Whatever the patch, this must still work!
    note_id = flag_id
    password = token

    # Interaction with the service
    # Try to be robust, services will not always answer immediately
    p = remote(ip, port)

    p.recvuntil("Hi! Welcome to our note storage service")
    p.recvuntil("Want to (R)ead or (W)rite a note?")

    p.sendline("R")

    p.recvuntil("Please type: note_id password")
    p.sendline("{} {}".format(note_id, password))

    p.recvuntil("Note content: ")
    content = p.recvuntil("\n").strip()
    p.close()

    return { 'FLAG': content }


if __name__ == "__main__":
    print get_flag("127.0.0.1", 6666, sys.argv[1], sys.argv[2])
