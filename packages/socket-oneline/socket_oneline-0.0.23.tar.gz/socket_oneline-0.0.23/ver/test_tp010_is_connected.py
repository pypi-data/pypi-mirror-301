import sys
import time
import unittest

from medver_pytest import pth

from ver.core.ver_client import VerClient
from ver.core.ver_server import VerServer
from ver.core.ver_services import VerServices
from tools.xplat_utils.os_specific import OsSpecific


# -------------------
class TestTp010IsConnected(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        VerServices.logger = None
        VerServices.verbose = True

    # -------------------
    def setUp(self):
        print('')
        self._callback_called = False
        self._callback_cmd = None
        self._callback_invalid = False
        VerServices.server = VerServer()

    # -------------------
    def tearDown(self):
        # VerServices.server.term()
        VerServices.client.term()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_tp010(self):
        pth.proto.protocol('tp-010', 'connect and then server exits')

        # initially disconnected
        pth.proto.step('check if client is connected before server is started')
        VerServices.client = VerClient()
        pth.ver.verify_false(VerServices.client.is_connected)

        pth.proto.step('start server')
        VerServices.server.init()
        pth.ver.verify_false(VerServices.client.is_connected)

        pth.proto.step('verify server is running')
        pth.ver.verify(VerServices.server.ols.is_running, reqids='SRS-001')
        pth.ver.verify_false(VerServices.client.is_connected)

        pth.proto.step('start client')
        VerServices.client.init()
        pth.ver.verify_true(VerServices.client.olc.connected, reqids='SRS-011')
        pth.ver.verify_true(VerServices.client.is_connected)

        pth.proto.step('set the callback function')
        VerServices.server.ols.callback = self._server_callback

        # normal command works
        rsp = VerServices.client.cmd01()
        pth.ver.verify_equal('ut_rsp', rsp, reqids=['SRS-008', 'SRS-015'])
        pth.ver.verify_true(self._callback_called, reqids=['SRS-008', 'SRS-013'])
        pth.ver.verify_equal('cmd01', self._callback_cmd, reqids='SRS-008')
        pth.ver.verify_false(self._callback_invalid, reqids='SRS-007')
        pth.ver.verify_true(VerServices.client.is_connected)

        self._callback_called = False
        self._callback_cmd = None
        self._callback_invalid = False
        VerServices.client.cmd_exit()
        sys.stdout.flush()

        OsSpecific.init()
        if OsSpecific.os_name == 'macos':
            # gets a BrokenPipeError; could not get ConnectionResetError
            # only needs one send_recv() and then a second send()
            VerServices.client.send_recv('ping')
            VerServices.client.send('ping')
        else:  # ubuntu
            # requires 1.6s to get ConnectionResetError
            # requires 1.7s or longer to get BrokenPipeError
            time.sleep(1.7500)
            VerServices.client.send('ping')
            # requires 2 pings
            VerServices.client.send('ping')
        sys.stdout.flush()

        pth.ver.verify_false(VerServices.client.is_connected)

    # --------------------
    # this is run in the server's thread
    def _server_callback(self, cmd, is_invalid):
        sys.stdout.flush()

        self._callback_called = True
        self._callback_cmd = cmd
        self._callback_invalid = is_invalid
        if cmd == 'cmdexit':
            sys.stdout.flush()
            VerServices.server.term()
            # no response
        else:
            VerServices.server.ols.send('ut_rsp')
