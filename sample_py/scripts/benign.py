import random
import string
import socket
import sys

from pwn import *

# To create random strings
POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase


def generate_new_flag():
    import string, random
    FLAG_POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase
    new_flag = ''.join(random.choice(FLAG_POSSIBILITIES) for x in range(13))
    return "FLG" + new_flag


def benign(ip, port):
    # There should be some other benign traffic to your service.
    # It helps determine if the service is functional or not, and makes it
    # harder to fingerprint flag-related traffic.
    #
    # In this case, I was lazy and I'm just creating a dummy note.

    note_id = random.randint(0,4294967295) # Well, hopefully should not collide
    password = ''.join(random.choice(POSSIBILITIES) for x in range(20))
    content = generate_new_flag()

    p = remote(ip, port)
    p.recvuntil("Hi! Welcome to our note storage service")
    p.recvuntil("Want to (R)ead or (W)rite a note?")
    p.sendline("W")
    p.recvuntil("Please type: note_id password content")
    p.recvuntil("The note_id is an number. No extra whitespace!")
    p.sendline("{} {} {}".format(note_id, password, content))
    p.recvuntil("Your note is safe with us! Bye!")
    p.close()

    while True: # Safety over all :D
        wrong_password = ''.join(random.choice(POSSIBILITIES) for x in range(20))
        if wrong_password != password: break
    p = remote(ip, port)
    p.recvuntil("Hi! Welcome to our note storage service")
    p.recvuntil("Want to (R)ead or (W)rite a note?")
    p.sendline("R")
    p.recvuntil("Please type: note_id password");
    p.sendline("{} {}".format(note_id, wrong_password))
    p.recvuntil("Wrong password!")
    p.close()

    p = remote(ip, port)
    p.recvuntil("Hi! Welcome to our note storage service")
    p.recvuntil("Want to (R)ead or (W)rite a note?")
    p.sendline("R")
    p.recvuntil("Please type: note_id password")
    p.sendline("{} {}".format(note_id, password))
    p.recvuntil("Note content: ")
    retrieved_content = p.recvuntil("\n").strip()
    assert content == retrieved_content
    p.close()

    # Nothing to return, if we got here without exceptions we assume that everything worked :)


if __name__ == "__main__":
    benign("127.0.0.1", 6666)
