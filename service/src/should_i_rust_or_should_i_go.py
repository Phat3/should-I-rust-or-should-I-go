#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# I realy want spaghetti today for lunch...

import os
import shutil
import sys
import subprocess

def _restore_commander():
    if not os.path.isfile("commander"):
        shutil.copy("../ro/commander", ".")

def _clean_custom(tmp_folder):
    try:
        shutil.rmtree(tmp_folder)
    except:
        pass
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

def execute_show_info():
    try:
        proc = subprocess.Popen(["./commander", "check_core"], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "Here you go Einstein..."
    except:
        print "ERROR!"
    sys.stdout.flush()

def execute_set_variable_yield():
    print "Insert the new value"
    sys.stdout.flush()
    value = raw_input()
    try:
        proc = subprocess.Popen(["./commander", "set_variable_yield", value], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "Whoa relax!"
    except:
        print "ERROR!"
    sys.stdout.flush()

def execute_set_dt_amount():
    print "Insert percentage"
    sys.stdout.flush()
    value = raw_input()
    try:
        proc = subprocess.Popen(["./commander", "set_dt_amount", value], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "God damn!"
    except:
        print "ERROR!"
    sys.stdout.flush()

def execute_defuse():
    print "Insert code ID"
    sys.stdout.flush()
    code_id = raw_input()
    print "Insert password"
    sys.stdout.flush()
    passwd = raw_input()
    try:
        proc = subprocess.Popen(["./commander", "defuse", code_id, passwd], stdout=subprocess.PIPE)
        print proc.stdout.read()
    except:
        print "ERROR!"
    sys.stdout.flush()

def execute_toggle_eni():
    try:
        proc = subprocess.Popen(["./commander", "toggle_eni"], stdout=subprocess.PIPE)
        print proc.stdout.read()
        print "I hope you know what you are doing..."
    except:
        print "ERROR!"
    sys.stdout.flush()

def execute_choice(choice):
    _restore_commander()
    if choice == "1":
        execute_show_info()
    elif choice == "2":
        execute_set_variable_yield()
    elif choice == "3":
        execute_set_dt_amount()
    elif choice == "4":
        execute_toggle_eni()
    elif choice == "5":
        execute_defuse()
    elif choice == "6":
        execute_custom()
    else:
        print "W-W-What is that supposed to mean"
        sys.stdout.flush()
    show_menu()

def show_menu():
    try:
        print
        print "------------ Rick 'O bomb menu ------------"
        print "1 - Show info"
        print "2 - Set variable yield"
        print "3 - Set Deuterium / Tritium amount"
        print "4 - Toggle External Neutron Initiator"
        print "5 - Defuse bomb"
        print "6 - Debug interface"
        sys.stdout.flush()
        choice = raw_input()
        execute_choice(choice)
    except EOFError:
        print "Aaand it's gone..."

def main():
    print "Uh, hi everybody. I'm Rick"
    print "Listen, I'm sending this message to you from another dimension:"
    print "yesterday night I blacked out and I planted this neutrino bomb in the center of the earth,"
    print "you have until 3pm to try to defuse it otherwise the entire galaxy is gonna blow up."
    print
    print "I would defuse the bomb myself but here's just one problem, one little hang-up."
    print "The dimension I am now is so advanced, that they had also halted the aging process,"
    print "and everyone here is young, and they have been forever. I'm the only old person here."
    print "It is like I'm some sort of, you know, celebrity, walking around."
    print "I-I'm fascinating to them. There are a lot of attractive women here,"
    print "and they they they they all want time with me."
    print "I had a lot of fun with a lot of young ladies, but I spent so much time here and"
    print "my interdimensional portal device it's got no charge left."
    print "It's as good as garbage now! So I'm stuck here!"
    print
    print "I think I left a way to defuse it without knowing the detonation code but y-y-you know what"
    print "happen when I drink, I become insecure and I want to be liked by others so I wrote this challenge"
    print "following the same principle applied by Nolan in his movie inception:"
    print "write something confusing and stupid so it will become everyone's favorite."
    print
    print "There could be other errors in this application because, you know, most of the time"
    print "science is more art than science!"
    print
    print "Have fun I guess... I have to go back to business ;-)"
    print
    print "Wubba lubba dub dub!"
    sys.stdout.flush() # Note the flush calls!
    show_menu()

if __name__ == "__main__":
    main()
