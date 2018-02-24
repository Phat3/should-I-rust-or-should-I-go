"""
Wrapper class that lists every command available for the client
"""
import logging
import json
from threading import Thread
from config import APP_CONFIG
import network

LOGGER = logging.getLogger("paxos.client")

class Command(Thread):
    """
    Wrapper class for commands exposed by the client
    """
    def __init__(self):
        Thread.__init__(self)

class Ping(Command):
    """
    DEBUG method : just ping the correspondent datacenter
    """
    def __init__(self):
        Command.__init__(self)

    def run(self):
        LOGGER.debug("Pinging %s:%d", APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"])
        data = network.send_data(APP_CONFIG["R_HOST"],
                                 APP_CONFIG["R_PORT"], {
                                     "CMD" : "PINGREQ",
                                     "DATA" : "Hello from %s" % APP_CONFIG["CLIENT_ID"]
                                 })
        LOGGER.debug(data)

class PingAll(Command):
    """
    DEBUG method : just ping the other clients to see if they are up
    """
    def __init__(self):
        Command.__init__(self)

    def run(self):
        for (addr, port) in APP_CONFIG["DATACENTER_ROUTING_TABLE"].values():
            LOGGER.debug("Pinging %s:%d", addr, port)
            data = network.send_data(addr, port, {
                "CMD" : "PINGREQ",
                "DATA" : "Hello from %s" % APP_CONFIG["CLIENT_ID"]
            })
            LOGGER.debug(data)

class StartElection(Command):
    """
    DEBUG :  force the election process to start
    """
    def __init__(self, r_host, r_port, uniqid):
        Command.__init__(self)
        self.r_host = r_host
        self.r_port = r_port
        self.uniqid = uniqid

    def run(self):
        network.send_data_async(self.r_host, self.r_port, {
            "CMD" : "START_ELECTION",
            "UNIQID" : self.uniqid
        })

class Show(Command):
    """
    Show the current status of the datacenter
    """
    def __init__(self):
        Command.__init__(self)

    def run(self):
        data = network.send_data(APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"], {
            "CMD" : "SHOW"
        })
        try:
            formatted_data = json.loads(data)
            print "Current Leader: %r" % formatted_data["CURRENT_LEADER"]
            print 
            print "Tickets left: %r" % formatted_data["NUM_TICKETS"]
            print 
            for entry in formatted_data["CURRENT_LOG"]:
                print entry
        except:
            print "Ops something went wrong..."

class Activate(Command):
    """
    'Activate' the related server
    """
    def __init__(self):
        Command.__init__(self)

    def run(self):
        network.send_data_async(APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"], {
            "CMD" : "ACTIVATE"
        })

class Deactivate(Command):
    """
    'Crash' the related server
    """
    def __init__(self):
        Command.__init__(self)

    def run(self):
        network.send_data_async(APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"], {
            "CMD" : "DEACTIVATE"
        })

class Buy(Command):
    """
    Called when buy operation is performed
    """
    def __init__(self, amount, r_host, r_port, uniqid):
        Command.__init__(self)
        self.amount = amount
        self.r_host = r_host
        self.r_port = r_port
        self.uniqid = uniqid

    def run(self):
        network.send_data_async(self.r_host, self.r_port, {
            "CMD" : "BUY",
            "AMOUNT" : self.amount,
            "UNIQID" : self.uniqid
        })

class ConfigChange(Command):
    """
    Called when CONFIG operation is performed
    """
    def __init__(self, cmd_type, server_id, ip_addr, port, r_host, r_port, uniqid):
        Command.__init__(self)
        self.cmd_type = cmd_type
        self.server_id = server_id
        self.ip_addr = ip_addr
        self.port = port
        self.r_host = r_host
        self.r_port = r_port
        self.uniqid = uniqid

    def run(self):
        network.send_data_async(self.r_host, self.r_port, {
            "CMD" : "CONFIG",
            "TYPE" : self.cmd_type,
            "SERVER_ID" : self.server_id,
            "IP_ADDR" : self.ip_addr,
            "PORT" : self.port,
            "UNIQID" : self.uniqid
        })
