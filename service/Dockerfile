FROM ubuntu:18.04

RUN apt update

WORKDIR /root/
# ------------- Install dependencies --------------
# 
# This is very flexible... you can:
# 
# 1 - Install dependencies from a  package manager
RUN apt install -y python python-pip build-essential vim wget socat clang
# 2 - Install dependencies from a custom url
RUN wget -O go.tar.gz https://dl.google.com/go/go1.9.2.linux-amd64.tar.gz  && tar xzvf go.tar.gz
# 3 - Set environment variables
ENV PATH=/root/go/bin:$PATH
# etc....

WORKDIR /root/service

# COPY ./service ./

CMD cd ./rw && socat tcp-l:6666,reuseaddr,fork exec:"../ro/should_i_rust_or_should_i_go.py"
