"""
File storing all the application configuration
"""
import os
import csv
import logging

LOGGER = logging.getLogger("paxos.server")

# Dictionary holding the configuration for the client
APP_CONFIG = {
    # Unique ID for the client (probably just an integer...)
    "DATACENTER_ID" : 0,
    # Local listening port for the client
    "L_PORT" : None,
    # Dictionary that holds the relationship between
    # { CLIENT_ID : (IP_ADDRESS, PORT) }
    "DATACENTER_ROUTING_TABLE" : {},
    # Threshold for heartbeats (in seconds)
    "HEARTBEAT_THRESHOLD" : 0.5,
}

def fill_app_config(args):
    """
    Tis method configures the client according to the settings passed to the container
    :return Bool : True if the configiuration succeed, False otherwise
    """
    with open(args.DATACENTER_LIST_FILE) as csvf:
        datacenter_list = list(csv.reader(csvf, delimiter=","))
    
        APP_CONFIG["L_PORT"] = args.L_PORT 
        APP_CONFIG["R_PORT"] = args.CONTROLLER_PORT
        APP_CONFIG["DATACENTER_ID"] = args.DATACENTER_ID 

        # in order to avoid livelock we use different timeout for each server
        # based on its ID
        APP_CONFIG["HEARTBEAT_THRESHOLD"] += 0.2*APP_CONFIG["DATACENTER_ID"]

        for row in datacenter_list:
            APP_CONFIG["DATACENTER_ROUTING_TABLE"][str(row[0])] = ("127.0.0.1", int(row[2]))
