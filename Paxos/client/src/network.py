"""
Wrapper class that implements and manages the network functions
"""

import socket
from threading import Thread
import json
import logging
from config import APP_CONFIG
from CommandHandler import PingAll, StartElection, Buy, ConfigChange

LOGGER = logging.getLogger("paxos.client")

class ConnectionHandler(Thread):
    """
    Setup and run the connection handler in a separate thread
    """
    def __init__(self):
        Thread.__init__(self)
        self.active = True

    def run(self):
        """
        Setup the connections handler
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", APP_CONFIG["L_PORT"]))
        sock.listen(1)
        while self.active:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            conn.close()
            try:
                formatted_data = json.loads(data)
                if formatted_data["CMD"] == "STOP":
                    LOGGER.debug("BYE!")
                    self.stop()
                if formatted_data["CMD"] == "PING":
                    # {CMD : PING }
                    command = PingAll()
                    command.start()

                if formatted_data["CMD"] == "REDIRECT":
                    # {CMD : REDIRECT, LEADER_HOST : LEADER_HOST, LEADER_PORT : LEADER_PORT }
                    if formatted_data["PREV_CMD"] == "CONFIG":
                        cmd_type, server_id, ip_addr, port = formatted_data["PARAMS"]
                        command = ConfigChange(cmd_type,
                                               server_id,
                                               ip_addr,
                                               int(port),
                                               formatted_data["LEADER_HOST"],
                                               int(formatted_data["LEADER_PORT"]),
                                               formatted_data["UNIQID"])
                    else:
                        command = Buy(formatted_data["PARAMS"],
                                      formatted_data["LEADER_HOST"],
                                      int(formatted_data["LEADER_PORT"]),
                                      formatted_data["UNIQID"])
                    command.start()
                
            except ValueError as exc:
                print exc
                print data
                pass

    def stop(self):
        """
        Stops the connection handler
        """
        self.active = False

def send_data(addr, port, data_to_send):
    """
    Send data to addr using a socket and WAIT for the response
    :param addr: address of the client we want to contect (only port)
    :rerturn data: data received as response
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    if not isinstance(data_to_send, basestring):
        data_to_send = json.dumps(data_to_send)
    sock.sendall(data_to_send)
    data = ""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    sock.close()
    return data


def send_data_async(addr, port, data_to_send):
    """
    Send data to addr using a socket and DO NOT WAIT for the response
    :param addr: address of the client we want to contect (only port)
    """
    #time.sleep(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    if not isinstance(data_to_send, basestring):
        data_to_send = json.dumps(data_to_send)
    sock.sendall(data_to_send)
    sock.close()
