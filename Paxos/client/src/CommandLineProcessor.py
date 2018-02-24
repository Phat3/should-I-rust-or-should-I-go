"""
Class that manages input from command line
"""

import cmd
import uuid
import sys
import re
from config import APP_CONFIG
from CommandHandler import Ping, PingAll, StartElection, Show, Buy, ConfigChange, \
                           Activate, Deactivate

class CommandLineProcessor(cmd.Cmd):
    """
    Class that manages the command line of
    the client
    """
    intro = "Client for UCSB ticketing kiosk"

    menu = """
    Commands Available:

        1 - show:

        2 - buy [numOfTickets]:

        3 - quit:
    """

    def __init__(self, connection_handler_thread):
        cmd.Cmd.__init__(self)
        self.connection_handler_thread = connection_handler_thread
        self.prompt = "client %s >> " % APP_CONFIG["CLIENT_ID"]
        self.regex_valid_ip = re.compile(r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b')

    def default(self, line):
        print "ERROR : undefined command %s" % line

    def do_EOF(self, line):
        """
        Quit the client upon ctrl+d
        """
        return self.do_quit(line)

    def postloop(self):
        print

    def do_quit(self, line):
        """
        Quit the client
        """
        print "Stopping"
        self.connection_handler_thread.stop()
        print "Bye!"
        sys.exit(0)
        return True

    def do_menu(self, line):
        """
        Show the menu of the application
        """
        print self.menu

    def do_show(self, line):
        """
        Execute show command
        """
        command = Show()
        command.run()

    def do_buy(self, num_of_tickets):
        """
        Execute show command
        """
        try:
            uniqid = str(uuid.uuid4())
            print "Executing BUY %d (%s)...." % (int(num_of_tickets), uniqid)
            command = Buy(int(num_of_tickets),
                          APP_CONFIG["R_HOST"],
                          APP_CONFIG["R_PORT"],
                          uniqid)
            command.run()
        except ValueError:
            print "Please provide a valid number of tickets"

    def do_ping(self, line):
        """
        Ping the datacenter relative to this client
        """
        command = Ping()
        command.run()

    def do_pingall(self, line):
        """
        Ping all datacenters
        """
        command = PingAll()
        command.run()

    def do_election(self, line):
        """
        Force the start of a new election
        with this being initiated by the corresponding
        Datacenter of this client
        """
        command = StartElection(APP_CONFIG["R_HOST"],
                                APP_CONFIG["R_PORT"],
                                str(uuid.uuid4()))
        command.run()

    def do_config(self, line):
        """
        Issue command in order to change the cluster configuration
        """
        try:
            cmd_type, server_id, ip_addr, port = line.split(" ")
            if cmd_type not in ["add", "remove"]:
                print "allowed types are add or remove only"
            # TODO : insert valid regex for ipv4
            # elif re.match(self.regex_valid_ip, ip_addr) is None:
                # print "The ip address format is not valid"
            else:
                uniqid = str(uuid.uuid4())
                print "Executing CONFIG %s (%s, %d) (%s)...." % (cmd_type,
                                                                ip_addr,
                                                                int(port),
                                                                uniqid)
                command = ConfigChange(
                    cmd_type.upper(),
                    server_id,
                    ip_addr,
                    int(port),
                    APP_CONFIG["R_HOST"],
                    APP_CONFIG["R_PORT"],
                    uniqid
                )
                command.run()
        except ValueError:
            print "Please provide a valid port number and/or a valid server_id (int)"

    def do_activate(self, line):
        """
        Simulate the activation of a new server in the cluster
        """
        command = Activate()
        command.run()

    def do_deactivate(self, line):
        """
        Simulate the activation of a new server in the cluster
        """
        command = Deactivate()
        command.run()
