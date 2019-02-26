FROM ubuntu:18.04

RUN apt update

WORKDIR /root/service

# Install dependencies
# RUN 

ADD service/ro ./

CMD cd service/rw && socat tcp-l:6666,reuseaddr,fork exec:"../ro/should_i_rust_or_should_i_go.py"