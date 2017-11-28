import random
import string
import socket
import sys

from pwn import *

# To create random strings
POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase

def set_flag(ip, port, flag):
    # We create a new note with the flag as content
    note_id = str(random.randint(0,4294967295)) # Well, hopefully should not collide
    password = ''.join(random.choice(POSSIBILITIES) for x in range(20))
    content = flag

    # Interaction with the service
    # Try to be robust, services will not always answer immediately

    p = remote(ip, port)

    p.recvuntil("Hi! Welcome to our note storage service")
    p.recvuntil("Want to (R)ead or (W)rite a note?")

    p.sendline("W")

    p.recvuntil("Please type: note_id password content")
    p.recvuntil("The note_id is an number. No extra whitespace!")
    p.sendline("{} {} {}".format(note_id, password, content))

    p.recvuntil("Your note is safe with us! Bye!")
    p.close()

    return {
            'FLAG_ID': note_id, # Unique id for each flag
            'TOKEN': password,  # benign (get_flag) will know this, exploits will not
            }


if __name__ == "__main__":
    print set_flag("127.0.0.1", 6666, sys.argv[1] if len(sys.argv)>1 else "FLG1234567890")
