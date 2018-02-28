#!/bin/bash

socat tcp-l:7777,reuseaddr,fork exec:"./oracle.py"
