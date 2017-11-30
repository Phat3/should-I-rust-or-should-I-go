#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

RO_DIR = "/home/phate/repos/should-I-rust-or-should-I-go/service/service/ro"


STUB_EXAMPLE = """
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
    stub = []
    while True:
        line = raw_input()
        if line == "EOF":
            stub.append("\n")
            break
        stub.append(line)
    stub = "\n".join(stub)
    compile_service(stub)

def compile_service(stub):
    print "Try to compile the service..."
    with open("src/glue.s", "w") as glue:
        glue.write(stub)
    # proc = subprocess.Popen(["make"], stdout=subprocess.PIPE)
    # print proc.stdout.read()
    error_code = subprocess.call(["make"])
    if error_code != 0:
        print "The submitted stub is incorrect..."
        sys.stdout.flush()
        subprocess.call(["make", "clean"])
        os.remove("src/glue.s")
        return
    print stub
    sys.stdout.flush()
    # execute_new_commander()

# def executre_new_commander():


if __name__ == "__main__":
    main()