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
    p = subprocess.Popen(["cd ../ro && make"], stdout=subprocess.PIPE)
    print p.stdout.readline()
    sys.stdout.flush()
    print stub
    sys.stdout.flush()

if __name__ == "__main__":
    main()
