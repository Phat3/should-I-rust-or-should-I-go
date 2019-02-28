FROM ubuntu:18.04

RUN apt update

WORKDIR /root/
# ------------- Install system dependencies --------------
#
# This is very flexible... you can:
#
# 1 - Install dependencies from a  package manager
# 2 - Install dependencies from a custom url
# 3 - Set environment variables
# etc...
RUN apt install -y \
    python \
    python-pip \
    build-essential \
    vim \
    wget \
    socat \
    clang
# ------------- Creating unprivileged user for the challenge -------------
#
# After installing all the dependencies that need root privilege we need to define an
# unprivileged user that runs the challenge itself. In this way when the challenge gets exploited
# the attacker cannot mess with system files inside the container
RUN useradd -ms /bin/bash chall
USER chall
WORKDIR /home/chall

# ------------- Install local dependencies --------------
RUN wget -O go.tar.gz https://dl.google.com/go/go1.9.2.linux-amd64.tar.gz  && tar xzvf go.tar.gz
ENV PATH=/home/chall/go/bin:$PATH

# ------------- Spawn the challenge --------------
WORKDIR /home/chall/service

CMD cd ./rw && socat tcp-l:6666,reuseaddr,fork exec:"../ro/should_i_rust_or_should_i_go.py"
