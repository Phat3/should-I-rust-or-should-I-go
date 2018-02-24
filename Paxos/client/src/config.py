"""
File storing all the application configuration
"""
import os
import logging
import csv

LOGGER = logging.getLogger("paxos.client")

# Dictionary holding the configuration for the client
APP_CONFIG = {
    # Unique ID for the client (probably just an integer...)
    "CLIENT_ID" : 0,
    
    # L_HOST : Local host where the client is running
    "L_HOST" : "",
    # L_PORT : Local listening port for the client
    "L_PORT" : None,
    # R_HOST : Ip of the datacentere relative to this client
    "R_HOST" : "",
    # R_PORT : port of the datacentere relative to this client
    "R_PORT" : None,
    # Dictionary that holds the relationship between
    # { CLIENT_ID : (IP_ADDRESS, PORT) }
    "DATACENTER_ROUTING_TABLE" : [],
}

def fill_app_config(index=0):
    """
    Tis method configures the client according to the settings passed to the container
    :return Bool : True if the configiuration succeed, False otherwise
    """
    DATACENTER_LIST_FILE = "./config.csv"
    with open(DATACENTER_LIST_FILE) as csvf:
        datacenter_list = list(csv.reader(csvf, delimiter=","))
    
        if "L_HOST" not in os.environ.keys():
            APP_CONFIG["L_HOST"] = datacenter_list[index][4]
        else:
            APP_CONFIG["L_HOST"] = os.environ["L_HOST"]
        
        if "L_PORT" not in os.environ.keys():
            APP_CONFIG["L_PORT"] = int(datacenter_list[index][5])
        else:
            APP_CONFIG["L_PORT"] = int(os.environ["L_PORT"])
        
        if "R_HOST" not in os.environ.keys():
            APP_CONFIG["R_HOST"] = datacenter_list[index][1]
        else:
            APP_CONFIG["R_HOST"] = os.environ["R_HOST"]

        if "R_PORT" not in os.environ.keys():
            APP_CONFIG["R_PORT"] = int(datacenter_list[index][2])
        else:
            APP_CONFIG["R_PORT"] = int(os.environ["R_PORT"])
        
        if "CLIENT_ID" not in os.environ.keys():
            APP_CONFIG["CLIENT_ID"] = int(datacenter_list[index][0])
        else:
            APP_CONFIG["CLIENT_ID"] = int(os.environ["CLIENT_ID"])
        
        if not os.path.exists(DATACENTER_LIST_FILE):
            LOGGER.error("Datacenter list not found")
            return False
                    
    return True
