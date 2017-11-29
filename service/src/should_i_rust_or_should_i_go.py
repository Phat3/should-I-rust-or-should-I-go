#!/usr/bin/env python2.7
import os
import sys
import subprocess

STATIC_LIB_PATH = "./libhello.a"
LAUNCHER_PATH  = "./rustgo.a"
TRAMPOLINE_PATH = "../rw/hello.s"

def main():
    print "Hi! Welcome to our note storage service"
    print "Want to (R)ead or (W)"
    sys.stdout.flush() # Note the flush calls!
    stub = raw_input()
    compile_service(stub)

def compile_service(stub):
    print "Try to compile the service..."
    proc = subprocess.Popen(["make", "--directory", "/home/phate/repos/should-I-rust-or-should-I-go/service/service/ro/"], stdout=subprocess.PIPE)
    print proc.stdout.read()
    sys.stdout.flush()
    print stub
    sys.stdout.flush()

if __name__ == "__main__":
    main()
