"""
Simple class that models the client
"""

import sys
import logging
from config import fill_app_config, APP_CONFIG
from network import ConnectionHandler
from CommandLineProcessor import CommandLineProcessor

FORMAT = "%(levelname)s --- %(message)s"
logging.basicConfig(format=FORMAT)

LOGGER = logging.getLogger("paxos.client")
LOGGER.setLevel(logging.DEBUG)

def main():
    """
    Start the client
    """
    # Use commandline to launch specific client
    if len(sys.argv) > 1:
        is_configured = fill_app_config(sys.argv[1])
    else:
        is_configured = fill_app_config()
    if not is_configured:
        sys.exit(-1)
    LOGGER.debug("CLIENT ID: %s", APP_CONFIG["CLIENT_ID"])
    LOGGER.debug("CLIENT %s:%d", APP_CONFIG["L_HOST"], APP_CONFIG["L_PORT"])
    LOGGER.debug("DATACENTER %s:%d", APP_CONFIG["R_HOST"], APP_CONFIG["R_PORT"])
    LOGGER.debug("DATACENTER ROUTING TABLE %r", APP_CONFIG["DATACENTER_ROUTING_TABLE"])
    connection_handler_thread = ConnectionHandler()
    connection_handler_thread.start()
    command_line_processor = CommandLineProcessor(connection_handler_thread)
    command_line_processor.cmdloop("Starting command prompt")
    #sys.exit()

if __name__ == '__main__':
    main()
