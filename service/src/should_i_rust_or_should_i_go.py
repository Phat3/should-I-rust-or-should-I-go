#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import subprocess

RO_DIR = "/home/phate/repos/should-I-rust-or-should-I-go/service/service/ro"
CUSTOM_STUB ="""TEXT ·trampoline(SB), 0, $256-16
    MOVQ f_ptr+0(FP), AX // Load the argument before messing with SP
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ADDQ $256, SP      // Rollback SP to reuse this function's frame
    ANDQ $~15, SP      // Align the stack to 16-bytes
    CALL AX
    MOVQ BX, SP        // Restore SP
    MOVQ AX, ret+8(FP) // Place the return value on the stack
    RET


TEXT ·call_get_flag(SB), 0, $256-8
    MOVQ SP, BX        // Save SP in a callee-saved registry
    ANDQ $~15, SP      // Align the stack to 16-bytes
    ADDQ $32, SP
    MOVQ $0x41414141, 0(SP)
    MOVQ $0x42424242, 4(SP)
    MOVQ $0x43434343, 8(SP)
    MOVQ $0x44444444, 12(SP)
    MOVQ SP, DI
    MOVQ $8, SI
    MOVQ SP, DX
    ADDQ $8, DX
    MOVQ $8, CX
    CALL get_detonation_code(SB)
    MOVQ BX, SP        // Restore SP
    RET
"""

def _clean_custom():
    try:
        #subprocess.call(["make", "clean"], shell=True)
        shutil.rmtree("./build")
        os.remove("src/glue.s")
    except:
        print "problems"
        sys.stdout.flush()
        pass

def _execute_custom():
    try:
        proc = subprocess.Popen(["./build/commander", "custom"], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "DONE!"
        sys.stdout.flush()
    except:
        print "ERROR!"
        sys.stdout.flush()
    _clean_custom()

def _compile_custom(stub):
    print "Try to compile the service..."
    sys.stdout.flush()
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
    print proc.stdout.read()
    sys.stdout.flush()
    with open("src/glue.s", "w") as glue:
        glue.write(stub)
    print "Dropped"
    sys.stdout.flush()
    error_code = subprocess.call(["make"], shell=True)
    if error_code != 0:
        print "The submitted stub is incorrect..."
        sys.stdout.flush()
        _clean_custom()
    else:
        _execute_custom()

def execute_custom():
    print "Submit stub"
    sys.stdout.flush()
    stub = []
    while True:
        line = raw_input()
        if line == "EOF":
            stub.append("\n")
            break
        stub.append(line)
    stub = "\n".join(stub)
    _compile_custom(stub)

def execute_choice(choice):
    if choice == "1":
        print "Execute option 1..."
        sys.stdout.flush()
    elif choice == "2":
        print "Execute option 2..."
        sys.stdout.flush()
    elif choice == "3":
        print "Execute option 3..."
        sys.stdout.flush()
        execute_custom()
    else:
        print "I don't know what that is!"
        sys.stdout.flush()
    show_menu()

def show_menu():
    print "1 - option 1"
    print "2 - Get detonation code"
    print "3 - Custom command"
    sys.stdout.flush()
    choice = raw_input()
    execute_choice(choice)

def main():
    print "Hi! Welcome to our note storage service"
    print "Want to (R)ead or (W)"
    sys.stdout.flush() # Note the flush calls!
    show_menu()


if __name__ == "__main__":
    main()
