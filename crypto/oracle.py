#!/usr/bin/env python

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
    plaintext = '\x00\x02\x09\xad\x82\x9f\xfb\x3a\x98\xb9\x1a\x1b\xe5\x3c\x6d\x61' + \
                '\x88\x45\x6f\x19\x2e\x85\x0c\x9d\x23\x89\x98\xa3\x95\x58\x74\x21\x86\x97\x04' + \
                '\x3f\x5a\x11\xb4\x93\x6e\xfd\x3f\xbe\xc0\x0b\xed\x3c\x10\x03\x19\x99\x13\x9c' + \
                '\x04\x4a\x79\xbb\x94\x75\xcb\x50\xc7\x2f\xd5\xd8\x6e\x38\xd3\xc5\x6c\xab\x5d' + \
                '\x19\x45\xb9\x31\xd4\x63\xd9\x58\x6c\x05\x29\xa2\xc8\xca\x8b\xb3\x17\x6a\xba' + \
                '\x6d\x3e\x32\xde\xeb\xe0\xbc\xa2\x20\x22\x86\x58\x2a\x08\x93\x33\xf7\xca\x7b' + \
                '\x40\x70\xf2\x72\x00\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21'
    cipherstream = encrypt_rsa(plaintext)
    plaintext = decrypt_rsa(cipherstream)
    print plaintext


if __name__ == "__main__":
    main()