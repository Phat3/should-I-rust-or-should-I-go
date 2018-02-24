"""
Wrapper class that lists every command available for the datacenter
"""
import logging
from datetime import datetime
from threading import Thread
from config import APP_CONFIG
import network

LOGGER = logging.getLogger("paxos.server")

class Command(Thread):
    """
    Wrapper class for commands exposed by the client
    """
    def __init__(self, resource_manager):
        Thread.__init__(self)
        self.resource_manager = resource_manager

class PingAll(Command):
    """
    DEBUG method : just ping the other clients to see if they are up
    """
    def __init__(self, resource_manager):
        Command.__init__(self, resource_manager)

    def run(self):
        for (addr, port) in APP_CONFIG["DATACENTER_ROUTING_TABLE"]:
            LOGGER.debug("Pinging %s:%d", addr, port)
            data = network.send_data(addr, port, 'Hello from %s' % APP_CONFIG["DATACENTER_ID"])
            LOGGER.debug(data)

class StartElection(Command):
    """
    DEBUG method: force the starting of a new leader election
    """
    def __init__(self, resource_manager, send_prepare_callback):
        Command.__init__(self, resource_manager)
        self.send_prepare_callback = send_prepare_callback

    def run(self):
        LOGGER.info("Starting Election process")
        ballot_number = self.resource_manager.increment_ballot_num()
        self.resource_manager.reset_prepare_acks_received()
        self.resource_manager.put_request_into_queue(("ELECTION", None, (APP_CONFIG["DATACENTER_ID"])))
        LOGGER.info("Sending PREPARE with ballot number : %r", ballot_number)
        self.send_prepare_callback(self.resource_manager, ballot_number)

class Buy(Command):
    """
    Buy stuff from UCSB ticket system
    """
    def __init__(self, resource_manager, amount, uniqid,
                 send_prepare_callback, send_accept_callback):
        Command.__init__(self, resource_manager)
        self.amount = amount
        self.uniqid = uniqid
        self.send_prepare_callback = send_prepare_callback
        self.send_accept_callback = send_accept_callback

    def run(self):
        if self.resource_manager.is_command_in_log(self.uniqid):
            LOGGER.info("Duplicete command (%s)!", self.uniqid)
            return
        if self.amount > self.resource_manager.tickets_left():
            LOGGER.info("No more ticket left")
            return
        ballot_number = self.resource_manager.increment_ballot_num()
        self.resource_manager.reset_prepare_acks_received()
        LOGGER.info("Starting Buy process")
        # if we have already received a number of nomoreaccept greater than
        # the majority of servers in the cluster we can skip the accept phase
        if self.resource_manager.get_nomoreaccept_tracker() >= self.resource_manager.get_majority_threshold():
            # 1 - Propose the received value from the client
            self.resource_manager.set_accepted_val(("BUY", self.uniqid,
                                                    self.amount))
            LOGGER.info("It is possible to skip the prepare phase...")
            LOGGER.info("Sending ACCEPT for ballot num : %r and accepted value %r",
                        self.resource_manager.get_current_ballot_num(),
                        self.resource_manager.get_accepted_val())
            # 2 - Append it to the log
            self.resource_manager.insert_entry_in_log_at_index(
                self.resource_manager.get_accepted_val(),
                None
            )
            self.resource_manager.pp_log()
            # 3 - Send ACCEPT message
            self.send_accept_callback(self.resource_manager,
                                      self.resource_manager.get_current_ballot_num(),
                                      len(self.resource_manager.get_log()) -1,
                                      self.resource_manager.get_accepted_val())
        # Otherwise let's run the prepare phase first
        else:
            self.resource_manager.put_request_into_queue(("BUY", self.uniqid,
                                                          self.amount))
            LOGGER.info("Sending PREPARE with ballot number : %r", ballot_number)
            self.send_prepare_callback(self.resource_manager, ballot_number)

class ConfigChange(Command):
    """
    Change cluster config
    """
    def __init__(self, resource_manager, cmd_type, server_id, ip_addr, port, uniqid,
                 send_prepare_callback, send_accept_callback):
        Command.__init__(self, resource_manager)
        self.cmd_type = cmd_type
        self.server_id = server_id
        self.ip_addr = ip_addr
        self.port = port
        self.uniqid = uniqid
        self.send_prepare_callback = send_prepare_callback
        self.send_accept_callback = send_accept_callback

    def run(self):
        if self.resource_manager.is_command_in_log(self.uniqid):
            LOGGER.info("Duplicate command (%s)!", self.uniqid)
            return
        ballot_number = self.resource_manager.increment_ballot_num()
        self.resource_manager.reset_prepare_acks_received()
        LOGGER.info("Starting CONFIG CHANGE process")
        # if we have already received a number of nomoreaccept greater than
        # the majority of servers in the cluster we can skip the accept phase
        if self.resource_manager.get_nomoreaccept_tracker() > \
           self.resource_manager.get_majority_threshold():
            # 1 - Propose the received value from the client
            self.resource_manager.set_accepted_val(("CONFIG", self.uniqid,
                                                    (self.cmd_type, self.server_id, self.ip_addr, self.port)))
            LOGGER.info("It is possible to skip the prepare phase...")
            LOGGER.info("Sending ACCEPT for ballot num : %r and accepted value %r",
                        self.resource_manager.get_current_ballot_num(),
                        self.resource_manager.get_accepted_val())
            # 2 - Append it to the log
            self.resource_manager.insert_entry_in_log_at_index(
                self.resource_manager.get_accepted_val(),
                None
            )
            self.resource_manager.pp_log()
            # 3 - Send ACCEPT message
            self.send_accept_callback(self.resource_manager,
                                      self.resource_manager.get_current_ballot_num(),
                                      len(self.resource_manager.get_log()) -1,
                                      self.resource_manager.get_accepted_val())
        # Otherwise let's run the prepare phase first
        else:
            self.resource_manager.put_request_into_queue(("CONFIG", self.uniqid,
                                                          (self.cmd_type, self.server_id, self.ip_addr, self.port)))
            LOGGER.info("Sending PREPARE with ballot number : %r", ballot_number)
            self.send_prepare_callback(self.resource_manager, ballot_number)

class ProcessPrepare(Command):
    """
    Process the receive of a PREPARE message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id,
                 received_ballot_num, send_prepare_ack_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.received_ballot_num = received_ballot_num
        self.send_prepare_ack_callback = send_prepare_ack_callback

    def run(self):
        if self.received_ballot_num > self.resource_manager.get_current_ballot_num():
            LOGGER.info("Received valid PREPARE from DC : %d", self.sender_dc_id)
            first_not_chosen_entry = self.resource_manager.get_first_not_chosen_entry_idx()
            self.resource_manager.set_current_ballot_num(self.received_ballot_num)
            self.send_prepare_ack_callback(self.resource_manager,
                                           self.sender_dc_id,
                                           self.received_ballot_num,
                                           self.resource_manager.get_accepted_ballot_num(),
                                           self.resource_manager.get_accepted_val(),
                                           False if first_not_chosen_entry else True)

class ProcessPrepareAck(Command):
    """
    Process the acknowledgement of receiving a PREPARE message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id,
                 received_ballot_num, received_accepted_ballot_num,
                 received_accepted_val, nomoreaccept_flag,
                 send_accept_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.received_ballot_num = received_ballot_num
        self.received_accepted_ballot_num = received_accepted_ballot_num
        self.received_accepted_val = received_accepted_val
        self.send_accept_callback = send_accept_callback
        self.nomoreaccept_flag = nomoreaccept_flag

    def run(self):
        self.resource_manager.append_prepare_ack(self.sender_dc_id,
                                                 self.received_ballot_num,
                                                 self.received_accepted_ballot_num,
                                                 self.received_accepted_val)
        # Increment the number of nomoreaccept received if the flag is set
        if self.nomoreaccept_flag:
            self.resource_manager.increment_nomoreaccept_tracker()
        if len(self.resource_manager.get_prepare_acks_received()) >= \
           self.resource_manager.get_majority_threshold() and \
           not self.resource_manager.is_ballot_acked(self.received_ballot_num):
            LOGGER.info("Majority confirmed PREPARE")
            self.resource_manager.mark_ballot_as_acked(
                self.resource_manager.get_current_ballot_num())
            # get the maximum accepted val saw during this round of election if any
            are_all_accepted_values_none = all(val is None \
                                               for (_, _, _, val) in \
                                               self.resource_manager.get_prepare_acks_received())
            first_not_chosen_entry = self.resource_manager.get_first_not_chosen_entry_idx()
            # If we received something from someone else we need to propose that
            # value first
            if not are_all_accepted_values_none:
                highest_ballot_num = self.resource_manager.get_highest_ballot_num_received()
                if highest_ballot_num > self.resource_manager.get_current_ballot_num():
                    self.resource_manager.set_accepted_val(
                        self.resource_manager.get_val_with_highest_ballot_num())
                else:
                    entry = self.resource_manager.pop_request_from_queue()
                    self.resource_manager.set_accepted_val(entry)

            #  Otherwise we can be in two cases:
            #   - We need to propose an entry that is still not known to be chosen
            #   - We need to propose a request in the queue
            else:
                if first_not_chosen_entry is not None:
                    log_entry = self.resource_manager.get_log_entry_at_index(first_not_chosen_entry)
                    # CASE 1.1 : We have an entry that is not chosen yet
                    if log_entry is not None:
                        # we need to propose the not chosen entry first
                        self.resource_manager.set_accepted_val(log_entry)
                    # CASE 2.1 : We have a "hole" int the log (i. e. 2 different entries
                    #            to be chosen but spreaded away)
                    else:
                        entry = self.resource_manager.pop_request_from_queue()
                        self.resource_manager.set_accepted_val(entry)
                # CASE 2.2 : Everything is know to be chosen and we just need to append
                #            the new entry tot the log and propose it
                else:
                    entry = self.resource_manager.pop_request_from_queue()
                    self.resource_manager.set_accepted_val(entry)
            # insert inside the log
            # this work even if first_not_chosen_entry is none
            # because if it's none it will be appendend at the end
            self.resource_manager.insert_entry_in_log_at_index(
                self.resource_manager.get_accepted_val(),
                first_not_chosen_entry
            )
            self.resource_manager.pp_log()
            # we already hear from a majority so the next received ack does
            # not interest us
            self.resource_manager.reset_prepare_acks_received()
            LOGGER.info("Sending ACCEPT for ballot num : %r and accepted value %r",
                        self.resource_manager.get_current_ballot_num(),
                        self.resource_manager.get_accepted_val())
            self.send_accept_callback(self.resource_manager,
                                      self.resource_manager.get_current_ballot_num(),
                                      len(self.resource_manager.get_log()) -1 if first_not_chosen_entry is None else first_not_chosen_entry,
                                      self.resource_manager.get_accepted_val())

class ProcessAccept(Command):
    """
    Process the receive of a ACCEPT message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id,
                 received_accepted_ballot_num,
                 received_log_index,
                 received_accepted_val, send_accept_ack_to_leader_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.received_accepted_ballot_num = received_accepted_ballot_num
        self.received_log_index = received_log_index
        self.received_accepted_val = received_accepted_val
        self.send_accept_ack_to_leader_callback = send_accept_ack_to_leader_callback

    def run(self):
        LOGGER.debug("RECEIVED BALLOT NUMBER %r FROM %r", self.received_accepted_ballot_num, self.sender_dc_id)
        LOGGER.debug("MY BALLOT NUMBER IS %r", self.resource_manager.get_current_ballot_num())
        if self.received_accepted_ballot_num >= self.resource_manager.get_current_ballot_num():
            self.resource_manager.set_accepted_ballot_num(self.received_accepted_ballot_num)
            self.resource_manager.set_current_ballot_num(self.received_accepted_ballot_num)
            self.resource_manager.set_accepted_val(self.received_accepted_val)
            # Put the accepted value in the log
            # Not committed yet
            self.resource_manager.insert_entry_in_log_at_index(
                self.received_accepted_val,
                self.received_log_index)
            self.resource_manager.pp_log()
        LOGGER.info("Sending ACCEPT_ACK to leader for ballot num %r",
                    self.resource_manager.get_current_ballot_num())
        self.send_accept_ack_to_leader_callback(self.resource_manager,
                                                self.sender_dc_id,
                                                self.resource_manager.get_current_ballot_num(),
                                                self.received_log_index)


class ProcessAcceptAck(Command):
    """
    Process the receive of a ACCEPT_ACK message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id,
                 received_accepted_ballot_num, received_log_index,
                 send_confirm_callback,
                 send_wake_up_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.received_accepted_ballot_num = received_accepted_ballot_num
        self.received_log_index = received_log_index
        self.send_confirm_callback = send_confirm_callback
        self.send_wake_up_callback = send_wake_up_callback

    def run(self):
        # We need to distinguish acks based on the log index proposed
        self.resource_manager.append_accept_ack(
            self.received_log_index,
            self.received_accepted_ballot_num)
        # we can put >= because the leader itself has already voted
        if len(self.resource_manager.get_accept_acks_received(self.received_log_index)) >= \
           self.resource_manager.get_majority_threshold() and \
           not self.resource_manager.is_entry_committed(self.received_log_index):
            LOGGER.info("Majority confirmed ACCEPT")
            max_ballot_number_returned = max(self.resource_manager.get_accept_acks_received(
                self.received_log_index
            ))
            # get the maximum accepted val saw during this round of election if any
            if self.resource_manager.get_current_ballot_num() >= max_ballot_number_returned:
                LOGGER.info("Value Committed!!")
                # result leader election
                # Other operations such as BUY, Config
                #else:
                self.resource_manager.mark_entry_as_chosen(self.received_log_index)
                self.resource_manager.pp_log()
                self.send_confirm_callback(
                    self.resource_manager,
                    self.resource_manager.get_accepted_val(),
                    self.received_log_index)
                if self.resource_manager.is_config_to_update():
                    LOGGER.info("Upfdate config...")
                    new_config = self.resource_manager.update_config()
                    if new_config[0][2] == "ADD":
                        _, _, (_, server_id, _, _) = new_config
                        self.send_wake_up_callback(self.resource_manager, server_id)
                # TODO: Should this command be commited in the log as well?
                if self.resource_manager.get_accepted_val()[0] == "ELECTION":
                    LOGGER.info("ELECTED LEADER!!!")
                    self.resource_manager.set_leader_id(APP_CONFIG["DATACENTER_ID"])
            else:
                # TODO: What happen to a rejected value??
                LOGGER.info("Value rejected because my ballot number (%r) is less then this one %r",
                            self.resource_manager.get_current_ballot_num(),
                            max_ballot_number_returned)
            # we already hear from a majority so the next received ack does
            # not interest us
            self.resource_manager.reset_accept_acks_received(self.received_log_index)

class ProcessConfirm(Command):
    """
    Process the CONFIRM message
    """
    def __init__(self, resource_manager, received_accepted_val, received_log_index):
        Command.__init__(self, resource_manager)
        self.received_accepted_val = received_accepted_val
        self.received_log_index = received_log_index

    def run(self):
        LOGGER.info("Value Committed!!")
        self.resource_manager.set_accepted_val(None)
        # WE should insert the committed valu here (if it's already present
        # it's fine to overwrite it) because it can happen that an accepor hasn't
        # received the log entry yet
        self.resource_manager.insert_entry_in_log_at_index(
            self.received_accepted_val,
            self.received_log_index
        )
        self.resource_manager.mark_entry_as_chosen(self.received_log_index)
        if self.resource_manager.is_config_to_update():
            LOGGER.info("Upfdate config...")
            self.resource_manager.update_config()
        if self.received_accepted_val[0] == "ELECTION":
            self.resource_manager.set_leader_id(self.received_accepted_val[2])
        self.resource_manager.pp_log()


class ProcessHeartbeat(Command):
    """
    Process the receive of a HEARTBEAT message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id, send_request_log_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.send_request_log_callback = send_request_log_callback

    def run(self):
        # LOGGER.debug("Received HEARTBEAT from DC : %d", self.sender_dc_id)
        # if we receive an heartbeat from someone that has an ID
        # greater than us we need to update our leader
        self.resource_manager.set_leader_id(self.sender_dc_id)
        self.resource_manager.set_last_heartbeat_ts(datetime.now())
        if self.resource_manager.is_idle():
            self.resource_manager.turn_on()
            LOGGER.info("I'm not in IDLE anymore")
            LOGGER.info("Requesting Log...")
            self.send_request_log_callback(self.resource_manager,
                                           self.resource_manager.get_leader_id(),
                                           self.resource_manager.get_uncertain_entries_idxs(),
                                           self.resource_manager.get_last_committed_entry_idx())

class ProcessWakeUp(Command):
    """
    Process the receive of a HEARTBEAT message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id, received_routing_table,
                 send_request_log_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.received_routing_table = received_routing_table
        self.send_request_log_callback = send_request_log_callback

    def run(self):
        # LOGGER.debug("Received HEARTBEAT from DC : %d", self.sender_dc_id)
        # if we receive an heartbeat from someone that has an ID
        # greater than us we need to update our leader
        self.resource_manager.set_leader_id(self.sender_dc_id)
        self.resource_manager.set_last_heartbeat_ts(datetime.now())
        self.resource_manager.update_routing_table(self.received_routing_table) 
        if self.resource_manager.is_idle():
            self.resource_manager.turn_on()
            LOGGER.info("I'm not in IDLE anymore")
            LOGGER.info("Requesting Log...")
            self.send_request_log_callback(self.resource_manager,
                                           self.resource_manager.get_leader_id(),
                                           self.resource_manager.get_uncertain_entries_idxs(),
                                           self.resource_manager.get_last_committed_entry_idx())

class ProcessLogRequest(Command):
    """
    Process the receive of a LOG_REQUEST message from another datacenter
    """
    def __init__(self, resource_manager, sender_dc_id,
                 uncertain_entries_received_idxs, last_committed_entry_idx,
                 send_log_update_callback):
        Command.__init__(self, resource_manager)
        self.sender_dc_id = sender_dc_id
        self.uncertain_entries_received_idxs = uncertain_entries_received_idxs
        self.last_committed_entry_idx = last_committed_entry_idx
        self.send_log_update_callback = send_log_update_callback

    def run(self):
        LOGGER.info("LOG_REQUEST received")
        uncertain_entries_received = self.resource_manager.get_uncertain_entries_requested(self.uncertain_entries_received_idxs)
        partial_log = self.resource_manager.get_log_after_idx_requested(self.last_committed_entry_idx)
        self.send_log_update_callback(self.resource_manager,
                                      self.sender_dc_id,
                                      uncertain_entries_received,
                                      partial_log)

class ProcessLogUpdate(Command):
    """
    Process the receive of a LOG_UPDATE message from another datacenter
    """
    def __init__(self, resource_manager,
                 uncertain_entries_received, log_received):
        Command.__init__(self, resource_manager)
        self.uncertain_entries_received = uncertain_entries_received
        self.log_received = log_received

    def run(self):
        LOGGER.info("LOG_UPDATE received")
        self.resource_manager.consolidate_log(self.uncertain_entries_received,
                                              self.log_received)
        self.resource_manager.pp_log()


# MULTI PAXOS
#
# [X] - Each prepare and accept needs an additional argument (index of the log)
#      Figure out which log entry to use
#      We have to know which entry are chosen (majority accepted the value)
#       - Find lowest entry not know to be chosen
#       - If first index not available (another entry not known to be choisen) we need to
#         propose first that value
# [X] - Use leader to reduce conflicts
#      LAMPORT SOLUTION :
#           1 - Server with higher ID act as leader
#           2 - Each server sends heartbet to every other servers every T secoonds
#           3 - If a server hasn't received heartbeat form a server with higher ID in 2T seconds
#               then he becomes the leader
#           4 - Clients get redirected to the leader
# [X] - Ensure full replication:
#     We need to ensure 2 thinghs:
#           1 - Full replication of the log on EVERY server and not just on a majority of them
#               SOLUTION : we have to keep trying sending the ACCEPT RPC (in background)
#                          until we hear from EVERY server!
#           2 - Inform all servers about CHOSEN entries
#               SOLUTION : mark the entries know to be chosen with
#                          accepted_proposasl[log_entry] = MAX_INT
#                          AND
#                          keep track of the first unchosen index
#                          (piggyback this information on every ACCEPT)
# [X] - CLient protocol
# [X] - Configuration changes
# [X] - ELiminating prepares
#     - The acceptor when it receives a proposal it looks into his own
#       log and if it hasn't any other entry after the proposed one he sends
#       back a NOMOREACCEPTED message to the leader
#     - If the acceptor respond with NOMOREACCEPTED the leader can avoid to send
#       prepares to that acceptor again
#     - if teh leader receive NOMOREACCEPTED form a majority of acceptors it will not
#       send again any PREPARE rpc
