#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import subprocess

def _clean_custom():
    try:
        #subprocess.call(["make", "clean"], shell=True)
        shutil.rmtree("./build")
        os.remove("src/glue_custom.s")
    except:
        print "problems"
        sys.stdout.flush()
        pass

def _execute_custom():
    try:
        proc = subprocess.Popen(["./build/commander", "custom"], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "DONE!"
    except:
        print "ERROR!"
    sys.stdout.flush()
    _clean_custom()

def _compile_custom(stub):
    with open("src/glue_custom.s", "w") as glue:
        glue.write(stub)
    DNULL = open(os.devnull, "w")
    error_code = subprocess.call(["make"], stdout=DNULL, stderr=subprocess.STDOUT)
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
