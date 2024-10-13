import unittest

from medver_pytest import pth

from ver.core.ver_client import VerClient
from ver.core.ver_server import VerServer
from ver.core.ver_services import VerServices
from ver.helpers.helper import Helper


# -------------------
class TestTp009Reconnect(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        VerServices.logger = None
        VerServices.verbose = True

    # -------------------
    def setUp(self):
        print('')
        VerServices.server = VerServer()

    # -------------------
    def tearDown(self):
        VerServices.server.term()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_tp009(self):
        pth.proto.protocol('tp-009', 'connect a client, attempt to reconnect with the same client')

        pth.proto.step('start server')
        VerServices.server.init()

        pth.proto.step('verify server is running')
        pth.ver.verify(VerServices.server.ols.is_running, reqids='SRS-001')

        pth.proto.step('start client')
        client = VerClient()
        client.init()
        pth.ver.verify_true(client.olc.connected, reqids='SRS-011')

        pth.proto.step('verify ping works on client')
        rsp = client.ping()
        pth.ver.verify_equal('pong', rsp, reqids='SRS-004')

        pth.proto.step('verify server is still running')
        pth.ver.verify_true(VerServices.server.ols.is_running, reqids='SRS-006')

        pth.proto.step('client attempt to reconnect')
        client.init()
        pth.ver.verify_true(client.olc.connected, reqids='SRS-011')

        pth.proto.step('verify ping still works on client')
        rsp = client.ping()
        pth.ver.verify_equal('pong', rsp, reqids='SRS-004')

        pth.proto.step('verify server is still running')
        pth.ver.verify_true(VerServices.server.ols.is_running, reqids='SRS-006')

        pth.proto.step('client requests shutdown')
        client.shutdown()

        # server should be stopped
        Helper.wait_until_stopped(5)
        pth.ver.verify_false(VerServices.server.ols.is_running, reqids='SRS-006')

        client.term()
