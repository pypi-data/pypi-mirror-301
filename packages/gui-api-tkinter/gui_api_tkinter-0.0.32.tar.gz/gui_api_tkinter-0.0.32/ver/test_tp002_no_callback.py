import unittest

from medver_pytest import pth

from gui_api_tkinter.lib.constants import Constants
from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp002(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        svc.helper = Helper()
        svc.helper.init()

    # -------------------
    def setUp(self):
        svc.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        svc.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        svc.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp002(self):
        pth.proto.protocol('tp-002', 'no callback defined, check for nak')
        pth.proto.add_objective('check that built-in functions work when callback funciton not defined')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        # use alternate access to version
        pth.proto.set_dut_version(f'v{Constants.version}')

        pth.proto.step('start gui')
        # don't define callback
        svc.helper.start_process('--no-callback')
        pth.ver.verify_true(svc.helper.gui_process.is_alive())
        pth.ver.verify_false(svc.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        svc.th.connect()
        pth.ver.verify_true(svc.th.is_connected())

        pth.proto.step('send invalid "cmd02" command')
        cmd = {
            'cmd': 'cmd02',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = svc.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'nak', reqids='SRS-011')
        pth.ver.verify_equal(rsp['reason'], 'unknown command', reqids='SRS-011')

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
