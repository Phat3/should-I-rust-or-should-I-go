#!/bin/bash
#
# This script reads the configuration file and it spawn a new container for each client

LOCAL_DIR=$(pwd)
DATACENTER_LIST_FILE="./server/config.csv"

tmux new-session -s challenge -n editor -d
tmux set-option -g mouse on 

for line in $(cat ./server/config.csv)
do
    DATACENTER_ID=$(echo $line | cut -d, -f 1)
    L_PORT=$(echo $line | cut -d, -f 3)
    # DATACENTER_NAME=$(echo $line | cut -d, -f 4)
    CONTROLLER_PORT=$(echo $line | cut -d, -f 6)
    tmux split-window -t challenge
    tmux send-keys -t challenge:0.$DATACENTER_ID "workon should_i_rust" C-m
    tmux send-keys -t challenge:0.$DATACENTER_ID "python ./server/src/main.py $DATACENTER_ID $L_PORT $CONTROLLER_PORT $DATACENTER_LIST_FILE" C-m
    tmux select-layout tiled
done

tmux select-pane -t challenge:0.0
tmux attach -t challenge