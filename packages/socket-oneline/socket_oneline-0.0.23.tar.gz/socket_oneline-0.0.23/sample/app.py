import os
import time

from sample.client import Client
from sample.common.cmd_runner import CmdRunner


# --------------------
## sample App to set up a background process to run the OnelineServer and
# to run the OnelineClient locally
class App:
    # --------------------
    ## constructor
    def __init__(self):
        ## when done indicates all done with the bg process
        self._finished = False

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        # TODO handle Ctrl-C
        # TODO check if server came down cleanly or threw excp
        crunner = CmdRunner()
        path = os.path.join('sample', 'server_main.py')
        cmd = f'python -u {path}'
        crunner.run_process('server', cmd)
        time.sleep(0.5)

    # --------------------
    ## run the client for various scenarios
    #
    # @return None
    def run(self):
        # server is up, talk to it with a client
        client = Client()
        client.init()
        # confirm the server is up and working
        client.ping()
        # send a known cmd, expect 'ack' in return
        client.cmd01()
        # send an unknown cmd, expect 'nak' in return
        client.send_recv('junk')
        # let the server know we're about to disconnect
        client.disconnect()
        client.term()

        # create a new client
        client = Client()
        client.init()
        client.ping()
        # tell server to exit, stop the process
        client.shutdown()
        client.term()

        self._finished = True
