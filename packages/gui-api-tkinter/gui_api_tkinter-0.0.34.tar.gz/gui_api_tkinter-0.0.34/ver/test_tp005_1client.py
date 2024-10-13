import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp005(unittest.TestCase):
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
        svc.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp005(self):
        pth.proto.protocol('tp-005', 'check only 1 client can connect to the App server')
        pth.proto.add_objective('check that one and only one client can connect to the GUI API server')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{svc.th.version}')

        pth.proto.step('start gui')
        svc.helper.start_process()
        pth.ver.verify_true(svc.helper.gui_process.is_alive())
        pth.ver.verify_false(svc.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        ok = svc.th.connect()
        pth.ver.verify_true(ok, reqids=['SRS-002'])
        pth.ver.verify_true(svc.th.is_connected())

        pth.proto.step('attempt 2nd connection to GUI App server, should fail')
        ok = svc.th.connect()
        pth.ver.verify_false(ok, reqids=['SRS-002'])
        pth.ver.verify_true(svc.th.is_connected())

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
