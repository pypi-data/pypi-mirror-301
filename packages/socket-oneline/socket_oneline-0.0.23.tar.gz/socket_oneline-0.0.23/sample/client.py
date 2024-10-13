from sample.svc import svc
from socket_oneline import OnelineClient


# --------------------
## sample Client that wraps the OnelineClient
class Client:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to Oneline Client
        self._client = OnelineClient()

    # --------------------
    ## initialize the OnelineClient and connect to the server
    #
    # @return None
    def init(self):
        svc.log.info(f'client      : started version:v{self._client.version}')

        self._client.ip_address = svc.ip_address
        self._client.ip_port = svc.ip_port
        self._client.logger = svc.log
        self._client.verbose = svc.verbose
        if not self._client.init():
            svc.log.info('ERR failed to set params')
            return

        self._client.connect()

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        self._client.disconnect()
        self._client = None

    # --------------------
    @property
    def is_connected(self):
        return self._client.connected

    # --------------------
    ## ping the Server
    #
    # @return the response (should be 'pong')
    def ping(self):
        return self.send_recv('ping')

    # --------------------
    ## send a command to the Server, wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd):
        self.send(cmd)
        rsp = self.recv()
        return rsp

    # --------------------
    ## send a cmd01 command to the Server
    #
    # @return the response (should be 'ack')
    def cmd01(self):
        return self.send_recv('cmd01')

    # --------------------
    ## send a disconnect ocmmand to the Server
    #
    # @return None
    def disconnect(self):
        self.send('disconnect')

    # --------------------
    ## send a shutdown command to the Server
    #
    # @return None
    def shutdown(self):
        self.send('shutdown')

    # --------------------
    ## send a command to the Server
    #
    # @param cmd  the command to send
    # @return None
    def send(self, cmd):
        svc.log.info(f'client      : tx: {cmd}')
        self._client.send(cmd)

    # --------------------
    ## wait for a response from the Server
    #
    # @return the response
    def recv(self):
        rsp = self._client.recv()
        svc.log.info(f'client      : rx: {rsp}')
        return rsp
