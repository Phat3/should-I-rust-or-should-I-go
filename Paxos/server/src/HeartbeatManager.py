"""
Class sthat manages the hartbeat process when we are leaders
"""

import time
import logging
from datetime import datetime
from threading import Thread
from config import APP_CONFIG
from network import send_heartbeat, send_prepare
from CommandHandler import StartElection

LOGGER = logging.getLogger("paxos.server")

class HeartbeatManager(Thread):
    """
    If we are the current leader we need to send an
    'Heartbeat' to every other servewr every T seconds
    """
    def __init__(self, resource_manager):
        Thread.__init__(self)
        self.resource_manager = resource_manager

    def run(self):
        while True:
            time.sleep(1)
            prev_leader = self.resource_manager.get_leader_id()
            # we should sleep at most for the minimun threshold possible
            time_diff = (datetime.now() - self.resource_manager.last_heartbeat_from_leader_ts).total_seconds()
            # We need to send an heartbeat in two cases:
            #   - we are the current leader
            #   - the time threshold expired since we heard from the
            #     last heartbeat from the previous leader
            if self.resource_manager.am_i_the_leader() and not self.resource_manager.is_idle():
                send_heartbeat(self.resource_manager)
            elif time_diff > 1 and not self.resource_manager.is_idle():
                # start election
                time.sleep(APP_CONFIG["HEARTBEAT_THRESHOLD"]*2)
                if self.resource_manager.get_leader_id() == prev_leader:
                    command = StartElection(self.resource_manager, send_prepare)
                    command.run()
            time.sleep(0.5)
