"""
Wrapper class that implements and manages the network functions
"""

import socket
import logging
from threading import Thread
import json
from config import APP_CONFIG
from CommandHandler import ProcessPrepare, ProcessPrepareAck, \
                           ProcessAccept, ProcessHeartbeat, ProcessAcceptAck, \
                           Buy, ProcessConfirm, ConfigChange, \
                           ProcessLogRequest, ProcessLogUpdate, ProcessWakeUp

LOGGER = logging.getLogger("paxos.server")

class ConnectionHandler(Thread):
    """
    Setup and run the connection handler in a separate thread
    """
    def __init__(self, resource_manager):
        Thread.__init__(self)
        self.active = True
        self.resource_manager = resource_manager

    def run(self):
        """
        Setup the connections handler
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", APP_CONFIG["L_PORT"]))
        sock.listen(1)
        LOGGER.debug("Listening on port %s", APP_CONFIG["L_PORT"])
        while self.active:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            try:
                formatted_data = json.loads(data)
                # DEBUG
                if formatted_data["CMD"] == "PINGREQ":
                    # {CMD : PINGREQ }
                    conn.sendall("DATACENTER %d is ALIVE!" % APP_CONFIG["DATACENTER_ID"])
                # DEBUG
                if formatted_data["CMD"] == "PREPARE":
                    # {CMD : PREPARE, "DC_ID" : DC_ID, "BALLOT_NUM" : BALLOT_NUM }
                    command = ProcessPrepare(self.resource_manager,
                                                int(formatted_data["DC_ID"]),
                                                float(formatted_data["BALLOT_NUM"]),
                                                send_prepare_ack)
                    command.run()
                if formatted_data["CMD"] == "PREPAREACK":
                    # {CMD : PREPAREACK, "DC_ID" : DC_ID, "BALLOT_NUM" : BALLOT_NUM,
                    #  ACCEPTED_BALLOT_NUM : ACCEPTED_BALLOT_NUM, ACCEPTED_VAL : ACCEPTED_VAL }
                    command = ProcessPrepareAck(self.resource_manager,
                                                int(formatted_data["DC_ID"]),
                                                float(formatted_data["BALLOT_NUM"]),
                                                float(formatted_data["ACCEPTED_BALLOT_NUM"]),
                                                formatted_data["ACCEPTED_VAL"],
                                                int(formatted_data["NOMOREACCEPT"]),
                                                send_accept)
                    command.run()
                if formatted_data["CMD"] == "ACCEPT":
                    # {CMD : ACCEPT, DC_ID : DC_ID, ACCEPTED_VAL : ACCEPTED_VAL, UNIQID : uniqid }
                    command = ProcessAccept(self.resource_manager,
                                            int(formatted_data["DC_ID"]),
                                            float(formatted_data["BALLOT_NUM"]),
                                            int(formatted_data["LOG_INDEX"]),
                                            formatted_data["ACCEPTED_VAL"],
                                            send_accept_ack_to_leader)
                    command.run()

                if formatted_data["CMD"] == "HEARTBEAT":
                    # {CMD : HEARTBEAT, DC_ID : DC_ID}
                    command = ProcessHeartbeat(self.resource_manager,
                                                int(formatted_data["DC_ID"]),
                                                send_log_request)
                    command.run()
                if formatted_data["CMD"] == "SHOW":
                    conn.sendall(json.dumps({
                        "CURRENT_LEADER" : self.resource_manager.get_leader_id(),
                        "NUM_TICKETS" : self.resource_manager.tickets_left(),
                        "CURRENT_LOG" : self.resource_manager.get_log()}))

                if formatted_data["CMD"] == "ACCEPT_ACK":
                    # {CMD : ACCEPT_ACK, DC_ID : DC_ID, BALLOT_NUM : BALLOT_NUM}
                    command = ProcessAcceptAck(self.resource_manager,
                                                int(formatted_data["DC_ID"]),
                                                float(formatted_data["BALLOT_NUM"]),
                                                int(formatted_data["LOG_INDEX"]),
                                                send_confirm,
                                                send_wake_up)
                    command.run()
                if formatted_data["CMD"] == "BUY":
                    # {CMD : BUY, DC_ID : DC_ID, AMOUNT: AMOUNT}
                    if self.resource_manager.am_i_the_leader():
                        command = Buy(self.resource_manager,
                                        int(formatted_data["AMOUNT"]),
                                        formatted_data["UNIQID"],
                                        send_prepare,
                                        send_accept)
                        command.run()
                    else:
                        send_redirect(self.resource_manager,
                                        self.resource_manager.get_leader_id(),
                                        formatted_data["CMD"],
                                        formatted_data["UNIQID"],
                                        int(formatted_data["AMOUNT"]))
                if formatted_data["CMD"] == "CONFIG":
                    # {CMD : BUY, DC_ID : DC_ID, AMOUNT: AMOUNT}
                    if self.resource_manager.am_i_the_leader():
                        command = ConfigChange(self.resource_manager,
                                                formatted_data["TYPE"],
                                                int(formatted_data["SERVER_ID"]),
                                                formatted_data["IP_ADDR"],
                                                int(formatted_data["PORT"]),
                                                formatted_data["UNIQID"],
                                                send_prepare,
                                                send_accept)
                        command.run()
                    else:
                        params = [formatted_data["TYPE"], formatted_data["SERVER_ID"],
                                    formatted_data["IP_ADDR"], formatted_data["PORT"]]
                        send_redirect(self.resource_manager,
                                        self.resource_manager.get_leader_id(),
                                        formatted_data["CMD"],
                                        formatted_data["UNIQID"],
                                        params)

                    if formatted_data["CMD"] == "CONFIRM":
                        command = ProcessConfirm(self.resource_manager,
                                                 formatted_data["ACCEPTED_VAL"],
                                                 int(formatted_data["LOG_INDEX"]))
                        command.run()

                    if formatted_data["CMD"] == "LOG_REQUEST":
                        command = ProcessLogRequest(self.resource_manager,
                                                    int(formatted_data["DC_ID"]),
                                                    [int(idx) for idx in formatted_data["UNCERTAIN_IDXS"]],
                                                    int(formatted_data["LAST_COMMITTED_IDX"]),
                                                    send_log_update)
                        command.run()

                    if formatted_data["CMD"] == "LOG_UPDATE":
                        command = ProcessLogUpdate(self.resource_manager,
                                                   formatted_data["UNCERTAIN_ENTRIES"],
                                                   formatted_data["PARTIAL_LOG"])
                        command.run()

                    if formatted_data["CMD"] == "WAKE_UP":
                        command = ProcessWakeUp(self.resource_manager,
                                                int(formatted_data["DC_ID"]),
                                                formatted_data["ROUTING_TABLE"],
                                                send_wake_up)
                        command.run()

            except ValueError as exc:
                print"Exception triggered"
                print exc
                print data
                pass

            conn.close()

    def stop(self):
        """
        Stops the connection handler
        """
        self.active = False
        
# ------ NETWORK CALLBACKS -------

def send_prepare(res_manager, ballot_num):
    """
    Send prepare request to all
    Phase 1 : Prepare candidate ---> everyone else

    :param ballot_num : current ballot number
    """
    for idx, (addr, port) in res_manager.get_routing_table_items():
        # This message is sent only from the leader...
        # don't send it to ourself
        if int(idx) != APP_CONFIG["DATACENTER_ID"]:
            send_data_async(addr, port, {
                "CMD" : "PREPARE",
                "DC_ID" : APP_CONFIG["DATACENTER_ID"],
                "BALLOT_NUM" : ballot_num
            })

def send_prepare_ack(res_manager, sender_id, ballot_num, accepted_ballot_num, accepted_val,
                     nomoreaccept):
    """
    Send ack to upon receiving a PREPARE message that
    satisfy the condition of the PAXOS algorithm
    """
    dc_addr, dc_port = res_manager.get_routing_table_element(sender_id)
    send_data_async(dc_addr, dc_port, {
        "CMD" : "PREPAREACK",
        "DC_ID" : APP_CONFIG["DATACENTER_ID"],
        "BALLOT_NUM" : ballot_num,
        "ACCEPTED_BALLOT_NUM" : accepted_ballot_num,
        "ACCEPTED_VAL" : accepted_val,
        "NOMOREACCEPT" : nomoreaccept
    })

def send_accept(res_manager, ballot_num, log_index, accepted_val):
    """
    Send ACCEPT to all

    Phase 2: Leader ---> everyone else
    """
    for idx, (addr, port) in res_manager.get_routing_table_items():
        # This message is sent only from the leader...
        # don't send it to ourself
        if int(idx) != APP_CONFIG["DATACENTER_ID"]:
            send_data_async(addr, port, {
                "CMD" : "ACCEPT",
                "DC_ID" : APP_CONFIG["DATACENTER_ID"],
                "BALLOT_NUM" : ballot_num,
                "LOG_INDEX" : log_index,
                "ACCEPTED_VAL" : accepted_val
            })

def send_accept_ack_to_leader(res_manager, sender_id, ballot_num, log_index):
    """
    Send ACCEPT to the leader
    """
    if sender_id != APP_CONFIG["DATACENTER_ID"]:
        leader_addr, leader_port = res_manager.get_routing_table_element(sender_id)
        send_data_async(leader_addr, leader_port, {
            "CMD" : "ACCEPT_ACK",
            "DC_ID" : APP_CONFIG["DATACENTER_ID"],
            "BALLOT_NUM" : ballot_num,
            "LOG_INDEX" : log_index,
        })

def send_heartbeat(res_manager):
    """
    Send heartbeat to everyone else with my id
    """
    for idx, (addr, port) in res_manager.get_routing_table_items():
        if int(idx) != APP_CONFIG["DATACENTER_ID"]:
            send_data_async(addr, port, {
                "CMD" : "HEARTBEAT",
                "DC_ID" : APP_CONFIG["DATACENTER_ID"],
            })

def send_redirect(res_manager, leader_id, prev_cmd, uniqid, params):
    """
    Redirect the client to the correct leader
    """
    leader_host, leader_port = res_manager.get_routing_table_element(leader_id)
    send_data_async(APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"], {
        "CMD" : "REDIRECT",
        "PREV_CMD" : prev_cmd,
        "LEADER_HOST" : leader_host,
        "LEADER_PORT" : leader_port,
        "UNIQID" : uniqid,
        "PARAMS" : params
    })

def send_confirm(res_manager, accepted_val, log_index):
    """
    Send commit confirm to everyone
    """
    for idx, (addr, port) in res_manager.get_routing_table_items():
        if int(idx) != APP_CONFIG["DATACENTER_ID"]:
            send_data_async(addr, port, {
                "CMD" : "CONFIRM",
                "ACCEPTED_VAL" : accepted_val,
                "LOG_INDEX" : log_index,
            })

def send_log_request(res_manager, leader_id, uncertain_entries_idxs,
                     last_committed_entry_idx):
    """
    Send LOG_REQUEST to leader
    """
    leader_host, leader_port = res_manager.get_routing_table_element(leader_id)
    send_data_async(leader_host, leader_port, {
        "CMD" : "LOG_REQUEST",
        "DC_ID" : APP_CONFIG["DATACENTER_ID"],
        "UNCERTAIN_IDXS" : uncertain_entries_idxs,
        "LAST_COMMITTED_IDX" : last_committed_entry_idx
    })

def send_log_update(res_manager, sender_id, uncertain_entries,
                    partial_log):
    """
    Send LOG_REQUEST to leader
    """
    leader_host, leader_port = res_manager.get_routing_table_element(sender_id)
    send_data_async(leader_host, leader_port, {
        "CMD" : "LOG_UPDATE",
        "DC_ID" : APP_CONFIG["DATACENTER_ID"],
        "UNCERTAIN_ENTRIES" : uncertain_entries,
        "PARTIAL_LOG" : partial_log
    })

def send_wake_up(res_manager, sender_id):
    """
    Send LOG_REQUEST to leader
    """
    leader_host, leader_port = res_manager.get_routing_table_element(sender_id)
    send_data_async(leader_host, leader_port, {
        "CMD" : "WAKE_UP",
        "DC_ID" : APP_CONFIG["DATACENTER_ID"],
        "ROUTING_TABLE" : res_manager.get_routing_table_items()
    })

# ------ NETWORK UTILITIES-------

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
    data = sock.recv(1024)
    sock.close()
    return data


def send_data_async(addr, port, data_to_send):
    """
    Send data to addr using a socket and DO NOT WAIT for the response
    :param addr: address of the client we want to contect (only port)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        sock.connect((addr, port))
        if not isinstance(data_to_send, basestring):
            data_to_send = json.dumps(data_to_send)
        sock.sendall(data_to_send)
        sock.close()
    except:
        print 
        pass
