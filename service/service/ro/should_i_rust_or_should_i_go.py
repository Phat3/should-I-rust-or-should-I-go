#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# I realy want spaghetti today for lunch...

import os
import shutil
import sys
import subprocess
import traceback

def _clean_custom(tmp_folder):
    try:
        shutil.rmtree(tmp_folder)
    except:
        print "problems"
        sys.stdout.flush()
    return

def _execute_custom(tmp_folder):
    try:
        proc = subprocess.Popen([(tmp_folder + "/build/commander"), "custom"], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "DONE!"
    except:
        print "ERROR!"
    sys.stdout.flush()
    return _clean_custom(tmp_folder)

def _compile_custom(tmp_folder, stub):
    with open(tmp_folder + "/src/glue_custom.s", "w") as glue:
        glue.write(stub)
    DNULL = open(os.devnull, "w")
    error_code = subprocess.call(["make", "-C", tmp_folder], stdout=DNULL, stderr=subprocess.STDOUT)
    if error_code != 0:
        print "The submitted stub is incorrect..."
        sys.stdout.flush()
        return _clean_custom(tmp_folder)
    else:
        return _execute_custom(tmp_folder)

def _copy_src_files(stub):
    team_name = "team"
    try:
        if os.path.isdir(team_name):
            shutil.rmtree(team_name)
        shutil.copytree("../ro/commander_files", team_name)
    except:
        print "Error during copy of source files"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        return
    return _compile_custom(team_name, stub)


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
    return _copy_src_files(stub)

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
    elif choice == "4":
        print "Execute option 4..."
        sys.stdout.flush()
        execute_custom()
    else:
        print "I don't know what that is!"
        sys.stdout.flush()
    show_menu()

def show_menu():
    try:
        print "1 - option 1"
        print "2 - option 2"
        print "3 - option 3"
        print "4 - Debug interface"
        sys.stdout.flush()
        choice = raw_input()
        execute_choice(choice)
    except EOFError:
        print "Aaand it's gone..."

def main():
    print "Hi! Welcome to our note storage service"
    print "Want to (R)ead or (W)"
    sys.stdout.flush() # Note the flush calls!
    show_menu()

if __name__ == "__main__":
    main()
