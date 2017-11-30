#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

stub = """
TEXT ·trampoline(SB), 0, $2048
    MOVQ SP, BX 
    ADDQ $2048, SP
    ANDQ $~15, SP
    CALL hello(SB)
    MOVQ BX, SP
    RET
"""
def main():
    print "Hi! Welcome to our note storage service"
    print "Want to (R)ead or (W)"
    sys.stdout.flush() # Note the flush calls!
    compile_service(stub)

def compile_service(stub):
    print "Try to compile the service..."
    with open("./src/glue.s", "w") as glue:
        glue.write(stub)
    proc = subprocess.Popen(["make"], stdout=subprocess.PIPE)
    print proc.stdout.read()
    sys.stdout.flush()
    print stub
    sys.stdout.flush()

if __name__ == "__main__":
    main()
