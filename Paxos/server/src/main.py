"""
Simple class that models the client
"""

import sys
import logging
import argparse
from config import fill_app_config, APP_CONFIG
from network import ConnectionHandler
from ResourceManager import ResourceManager
from HeartbeatManager import HeartbeatManager

FORMAT = "%(levelname)s --- %(message)s"
logging.basicConfig(format=FORMAT)

LOGGER = logging.getLogger("paxos.server")
LOGGER.setLevel(logging.DEBUG)

def main():
    """
    Start the client
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("DATACENTER_ID", help="ID of the datacenter", type=int)
    parser.add_argument("L_PORT", help="Local port where the datacenter listen", type=int)
    parser.add_argument("CONTROLLER_PORT", help="Port exposed by the controller", type=int)
    parser.add_argument("DATACENTER_LIST_FILE", help="Path to the config file holding the configurations for datacenters")
    fill_app_config(parser.parse_args())

    resource_manager = ResourceManager()
    LOGGER.debug("DATACENTER ID: %s", APP_CONFIG["DATACENTER_ID"])
    LOGGER.debug("DATACENTER :%d", APP_CONFIG["L_PORT"])
    LOGGER.debug("CONTROLLER :%d", APP_CONFIG["R_PORT"])
    LOGGER.debug("DATACENTER ROUTING TABLE %r", APP_CONFIG["DATACENTER_ROUTING_TABLE"])
    # LOGGER.debug("DATACENTER active %r", APP_CONFIG["ACTIVE"])
    # LOGGER.debug("DATACENTER idle %r", APP_CONFIG["IDLE"])
    connection_handler_thread = ConnectionHandler(resource_manager)
    connection_handler_thread.start()
    heartbeat_manager_thread = HeartbeatManager(resource_manager)
    heartbeat_manager_thread.start()


if __name__ == '__main__':
    main()