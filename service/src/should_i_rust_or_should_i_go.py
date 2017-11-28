#!/usr/bin/env python2.7
import os
import sys

# This service stores notes with a name and a password.
# More or less the same as the C one, see that for more comments :)


def main():
    print "Hi! Welcome to our note storage service"
    print "Want to (R)ead or (W)rite a note?"
    sys.stdout.flush() # Note the flush calls!

    stub = raw_input()
    compile_service(stub)

def compile_service(stub):
    print "Try to compile the service..."
    sys.stdout.flush()
    print stub


if __name__ == "__main__":
    main()
