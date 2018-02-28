#!/bin/bash

socat tcp-l:6666,reuseaddr,fork exec:"./oracle.py"
