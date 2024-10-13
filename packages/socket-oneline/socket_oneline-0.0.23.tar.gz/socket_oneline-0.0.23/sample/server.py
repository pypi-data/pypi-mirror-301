import time

from sample.svc import svc
from socket_oneline.lib.oneline_server import OnelineServer


# --------------------
## sample Server that wraps the OnelineServer
class Server:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._server = OnelineServer()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        svc.log.info(f'server      : started version:v{self._server.version}')

        self._server.callback = self._callback
        self._server.ip_address = svc.ip_address
        self._server.ip_port = svc.ip_port
        self._server.logger = svc.log
        self._server.verbose = svc.verbose
        if not self._server.start():
            svc.log.info('ERR failed to set params')

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## wait until the server stops running i.e. it is shutdown
    #
    # @return None
    def wait_until_done(self):
        while self._server.is_running:
            time.sleep(0.5)

    # --------------------
    ## callback function used by OnelineServer to handle incoming commands
    #
    # @param cmd         the incoming command from the client
    # @param is_invalid  indicates if the command was invalid
    # @return None
    def _callback(self, cmd, is_invalid):
        svc.log.info(f'server      : callback: cmd="{cmd}" is_invalid={is_invalid}')
        if cmd == 'cmd01':
            self._server.send('ack')
        else:
            # unknown command, let client know
            self._server.send('nak - unknown cmd')
