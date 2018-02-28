#!/usr/bin/env python

import sys
from subprocess import *
import binascii

def decrypt_rsa(ciphertext):
    p = Popen(['/usr/bin/openssl','rsautl','-decrypt','-inkey','./keys/key.pem'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    plaintext, err = p.communicate(input=ciphertext)
    return plaintext if not err else err

def encrypt_rsa(plaintext):
    p = Popen(['/usr/bin/openssl','rsautl','-encrypt', '-pubin','-inkey','./keys/public.pem','-raw'], stdout=PIPE, stdin=PIPE, stderr=PIPE)  
    cipherstream, err = p.communicate(input=plaintext)
    return cipherstream if not err else err


def main():
    print "Start service"
    sys.stdout.flush()
    ciphertext = binascii.unhexlify(raw_input())
    plaintext = decrypt_rsa(ciphertext)
    print plaintext
    sys.stdout.flush()

if __name__ == "__main__":
    main()