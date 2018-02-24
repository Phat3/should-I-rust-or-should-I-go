#!/bin/bash

docker-up
docker build -t dist_sys_paxos_server ./server/
docker build -t dist_sys_paxos_client ./client/