"""
File that exposes all the 'critical' resources of the application
"""

import threading
import logging
from datetime import datetime
from config import APP_CONFIG

LOGGER = logging.getLogger("paxos.server")

# Since we have only one instance of the class
# ResourceManager we can lock in this silly way...
def synchronized(func):
    """
    Decorator that locks the method class wise!
    (E. g. if we have two object of the same class only one
    object at a time can access a method)
    """
    func.__lock__ = threading.RLock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func

class ResourceManager(object):
    """
    Class that manages all the critical resources of the client
    """
    def __init__(self):
        """
        Initialize the resources at the starting point of the application
        """
        # delay between config change and setting new majority
        self.alpha = 2
        # local log of this datacenter
        self.log = []
        # keep track of the known to be chosen entries
        self.know_to_be_chosen_tracker = []
        # latest ballot number in phase 1
        self.current_ballot_num = 0 + int(APP_CONFIG["DATACENTER_ID"])*0.1
        # latest ballot number accepted in phase 2
        self.accepted_ballot_num = 0
        # latest accept value
        self.accepted_val = None
        # ack received within the election phase
        self.prepare_acks_received = []
        # Track the ballot numbers already acked by a majority
        self.acked_ballot = []
        # ack received within the acceptance phase
        self.accept_acks_received = {}
        # Keep track of the current leader
        # At tehe beginning we don't know who he is
        self.leader_id = None
        # Keep track of the timestamp of the last heartbeat
        # heard from the leader
        self.last_heartbeat_from_leader_ts = datetime.now()
        # queue of requests that has to be processed
        self.request_queue = []
        # keeps track of the nomoreaccept flag received
        self.nomoreaccept_tracker = 0
        # Total tickets for game
        self.total_tickets = 1000


    @synchronized
    def get_log(self):
        """
        return the current log
        """
        return self.log

    @synchronized
    def get_current_ballot_num(self):
        """
        return the current ballot number
        """
        return self.current_ballot_num

    @synchronized
    def get_accepted_ballot_num(self):
        """
        return the accepted ballot number
        """
        return self.accepted_ballot_num

    @synchronized
    def get_accepted_val(self):
        """
        return the current ballot number
        """
        return self.accepted_val

    @synchronized
    def get_prepare_acks_received(self):
        """
        return the current prepare ack list
        """
        return self.prepare_acks_received

    @synchronized
    def get_accept_acks_received(self, log_index):
        """
        return the current accept ack list
        """
        return self.accept_acks_received[str(log_index)]

    @synchronized
    def get_request_from_queue(self, ballot_number):
        """
        return the current requessts queue
        """
        return self.request_queue[ballot_number]

    @synchronized
    def get_leader_id(self):
        """
        return the current leader id
        """
        return self.leader_id

    @synchronized
    def get_first_not_chosen_entry_idx(self):
        """
        Get the first index thath is not known to be chosen in the log
        """
        try:
            return next(idx for idx, is_chosen in enumerate(self.know_to_be_chosen_tracker) if \
                        not is_chosen)
        except StopIteration:
            return None

    @synchronized
    def get_log_entry_at_index(self, idx):
        """
        Return the log entry atr index idx
        """
        return self.log[idx]

    @synchronized
    def get_nomoreaccept_tracker(self):
        """
        Return the number of nomoreaccept received since
        the server become leader
        """
        return self.nomoreaccept_tracker

    @synchronized
    def set_current_ballot_num(self, ballot_num):
        """
        Set the current ballot number to the one passed as parameter
        """
        self.current_ballot_num = ballot_num

    @synchronized
    def set_accepted_ballot_num(self, ballot_num):
        """
        Set the accepted ballot number to the one passed as parameter
        """
        self.accepted_ballot_num = ballot_num

    @synchronized
    def set_accepted_val(self, accepted_val):
        """
        Set the current accepted_val to the one passed as parameter
        """
        self.accepted_val = accepted_val

    @synchronized
    def set_leader_id(self, dc_id):
        """
        Set the current leader id to the one received
        """
        self.leader_id = dc_id

    @synchronized
    def set_last_heartbeat_ts(self, ts):
        """
        Set the  the timestamp of the heartbeat
        """
        self.last_heartbeat_from_leader_ts = ts

    @synchronized
    def increment_ballot_num(self):
        """
        Increment the current ballot number upon the start
        a new leader election
        """
        self.current_ballot_num += 1
        return self.current_ballot_num

    @synchronized
    def put_request_into_queue(self, req):
        """
        insert the request received from client into the queue
        """
        self.request_queue = [req] + self.request_queue

    @synchronized
    def pop_request_from_queue(self):
        """
        Return ther oldest request in the queue
        """
        return self.request_queue.pop()

    @synchronized
    def insert_entry_in_log_at_index(self, entry, index=None):
        """
        Add the entry in the log at the position indicated by the index
        """
        # if we don't provide index just append the entry at the end
        if index is None:
            self.log.append(entry)
            self.know_to_be_chosen_tracker.append(False)
        # extends the log to suit the new entry if it is too short
        elif len(self.log) <= index:
            self.log = self.log + [None]*(index - len(self.log)) + [entry]
            self.know_to_be_chosen_tracker = self.know_to_be_chosen_tracker + \
                                             [False]*(index - len(self.know_to_be_chosen_tracker)+1)
        else:
            self.log[index] = entry
            self.know_to_be_chosen_tracker[index] = False

    @synchronized
    def reset_prepare_acks_received(self):
        """
        Reset the list of ack received within the election
        """
        self.prepare_acks_received = []

    @synchronized
    def append_prepare_ack(self, sender_dc_id, received_ballot_num,
                           received_accepted_num, received_accepted_val):
        """
        Append the received ack to the list of received acks
        """
        ack = [sender_dc_id, received_ballot_num, received_accepted_num, received_accepted_val]
        self.prepare_acks_received.append(ack)

    @synchronized
    def reset_accept_acks_received(self, log_index):
        """
        Reset the list of ack received within the election
        """
        self.accept_acks_received[str(log_index)] = []

    @synchronized
    def append_accept_ack(self, log_index, received_ballot_num):
        """
        Append the received ack to the list of received acks
        """
        if str(log_index) not in self.accept_acks_received.keys():
            self.accept_acks_received[str(log_index)] = [received_ballot_num]
        else:
            self.accept_acks_received[str(log_index)].append(received_ballot_num)

    @synchronized
    def mark_entry_as_chosen(self, log_entry):
        """
        Mark the entry in the log as chosen
        """
        self.know_to_be_chosen_tracker[log_entry] = True

    @synchronized
    def get_highest_ballot_num_received(self):
        """
        Return the highest ballot num received for the prepare phase
        """
        return max([b for (_, _, b, _) in self.prepare_acks_received])

    @synchronized
    def get_val_with_highest_ballot_num(self):
        """
        Return the value withb the highest accepted ballot number
        in the sequence of the ack received
        """
        max_accepted_val = 0
        result = None
        for (_, _, b, val) in self.prepare_acks_received:
            if b > max_accepted_val:
                result = val
        return result

    @synchronized
    def am_i_the_leader(self):
        """
        Check if we are the current leader of the cluster
        """
        return APP_CONFIG["DATACENTER_ID"] == self.leader_id

    @synchronized
    def pp_log(self):
        """
        Pretty print the status of the log
        """
        print "\n--------------------------------------"
        print "Len log:", len(self.log)
        print self.log
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Len Tracker:", len(self.know_to_be_chosen_tracker)
        print self.know_to_be_chosen_tracker
        print "--------------------------------------\n"

    @synchronized
    def increment_nomoreaccept_tracker(self):
        """
        Increment the number of nomoreaccept received
        """
        self.nomoreaccept_tracker += 1

    @synchronized
    def tickets_left(self):
        """
        Return the number of tickets remaining (100 - tickets sold so far)
        """
        buy_entries = [entry for entry in self.log if entry[0] == "BUY"]
        return self.total_tickets - sum([amount for _, _, (amount) in buy_entries])

    @synchronized
    def add_client(self, client_id, addr, port):
        """
        Add client to datacenter routing table
        """
        APP_CONFIG["DATACENTER_ROUTING_TABLE"][client_id] = (int(addr), int(port))

    @synchronized
    def remove_client(self, client_id):
        """
        Remove client client to datacenter routing table
        """
        try:
            del APP_CONFIG["DATACENTER_ROUTING_TABLE"][client_id]
        except KeyError:
            pass

    @synchronized
    def is_entry_committed(self, log_index):
        """
        Return true if the selected entry is known to be chosen
        """
        return self.know_to_be_chosen_tracker[log_index]

    @synchronized
    def is_command_in_log(self, uniqid):
        """
        Check if the uniqid od the command is already present in the log
        """
        return uniqid in [ids for _, ids, _ in self.log]

    @synchronized
    def mark_ballot_as_acked(self, ballot_num):
        """
        Mark the ballot number as acked by a majority
        """
        self.acked_ballot.append(ballot_num)

    @synchronized
    def is_ballot_acked(self, ballot_num):
        """
        Check if  teh ballot number was already acked by a majority
        """
        return ballot_num in self.acked_ballot

    @synchronized
    def is_config_to_update(self):
        """
        Return true if we have to update the configuration of the cluster
        """
        if len(self.log) - self.alpha < 0:
            return False
        # first_known_to_be_chosen_idx = self.get_first_not_chosen_entry_idx()
        # if first_known_to_be_chosen_idx is None:
        return self.log[-self.alpha][0] == "CONFIG"
        # elif first_known_to_be_chosen_idx - self.alpha >= 0:
        #     return self.log[(first_known_to_be_chosen_idx - self.alpha)][0] == "CONFIG"
        # return False

    @synchronized
    def update_config(self):
        """
        Update the routing table of the server upon configuration change

        ASSUMPTIONS :
            - the id we are trying to remove is considered to be always present
              inside the routing table
            - No collisions on the server ids
        """
        cmd_type, server_id, ip_addr, port = self.log[-self.alpha][2]
        if cmd_type == "ADD":
            LOGGER.info("We need to add this server %d, %s:%d", server_id, ip_addr, port)
            APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(server_id)] = (ip_addr, port)
        else:
            LOGGER.info("We need to remove this server %d %s:%d", server_id, ip_addr, port)
            del APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(server_id)]
            if server_id == APP_CONFIG["DATACENTER_ID"]:
                APP_CONFIG["IDLE"] = True
        return self.log[-self.alpha]

    @synchronized
    def get_routing_table_items(self):
        """
        We need to ensure mutual exclusion also on the routing table now that
        can be modified... Here is the wrong place to do it but still...
        """
        return APP_CONFIG["DATACENTER_ROUTING_TABLE"].items()

    @synchronized
    def get_routing_table_element(self, server_id):
        """
        We need to ensure mutual exclusion also on the routing table now that
        can be modified... Here is the wrong place to do it but still...
        """
        return APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(server_id)]

    @synchronized
    def get_majority_threshold(self):
        """
        Get the number of servers that forms a majority
        """
        return len(APP_CONFIG["DATACENTER_ROUTING_TABLE"]) / 2

    @synchronized
    def get_uncertain_entries_idxs(self):
        """
        Get entries that are not known to be chosen
        """
        uncertain_entries = []
        for idx, val in enumerate(self.know_to_be_chosen_tracker):
            if not val:
                uncertain_entries.append(idx)
        return uncertain_entries

    @synchronized
    def get_uncertain_entries_requested(self, uncertain_entries_idxs):
        """
        Get entries requested by an acceptor
        """
        uncertain_entries = []
        for idx in uncertain_entries_idxs:
            uncertain_entries.append(self.log[idx])
        return uncertain_entries

    @synchronized
    def get_last_committed_entry_idx(self):
        """
        Return the last index of a known entry
        """
        last_index = 0
        for idx, val in enumerate(self.know_to_be_chosen_tracker):
            if val:
                last_index = idx
        return last_index

    @synchronized
    def get_log_after_idx_requested(self, idx):
        """
        Return the log from the idx requested till the end
        """
        if idx == 0:
            return self.log
        return self.log[idx+1:]

    @synchronized
    def consolidate_log(self, uncertain_entries_fix, log_received):
        """
        Append entries known to be chosen in log and fix the uncertain one
        """
        for idx, val in enumerate(self.know_to_be_chosen_tracker):
            if not val:
                self.log[idx] = uncertain_entries_fix.pop()
                self.know_to_be_chosen_tracker[idx] = True
                self.execute_command(self.log[idx])
        for val in log_received:
            self.execute_command(val)
        self.log = self.log + log_received
        self.know_to_be_chosen_tracker += [True]*len(log_received)

    def execute_command(self, command):
        """
        Execute the command in the state machine
        """
        cmd_str, _, params = command
        if cmd_str == "CONFIG":
            cmd_type, server_id, ip_addr, port = params
            if cmd_type == "ADD":
                LOGGER.info("We need to add this server %d, %s:%d", server_id, ip_addr, port)
                APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(server_id)] = (ip_addr, port)
            else:
                LOGGER.info("We need to remove this server %d %s:%d", server_id, ip_addr, port)
                del APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(server_id)]
        print APP_CONFIG["DATACENTER_ROUTING_TABLE"]

    def update_routing_table(self, routing_table):
        APP_CONFIG["DATACENTER_ROUTING_TABLE"] = routing_table

    def is_idle(self):
        return APP_CONFIG["IDLE"]

    def turn_on(self):
        APP_CONFIG["IDLE"] = False
