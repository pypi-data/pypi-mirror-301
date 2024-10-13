import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp004(unittest.TestCase):
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
    def test_tp004(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-004', 'check "search" with various invalid paths')
        pth.proto.add_objective('check that search respond with accurate nak JSON objects')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{svc.th.version}')

        pth.proto.step('start gui')
        svc.helper.start_process()
        pth.ver.verify_true(svc.helper.gui_process.is_alive())
        pth.ver.verify_false(svc.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        svc.th.connect()
        pth.ver.verify_true(svc.th.is_connected())

        # no get_screen at this point
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        pth.ver.verify_none(svc.th.content)
        pth.ver.verify_none(svc.th._search_content(svc.th.content, button_path, 0))  # pylint: disable=protected-access

        pth.proto.step('with no get_screen, search using a valid path')
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-024'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-024'])
        pth.ver.verify_equal('content is None', item['reason'], reqids=['SRS-024'])
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('get page content')
        svc.th.get_screen()
        pth.ver.verify_gt(len(svc.th.content), 0)

        pth.proto.step('search using a valid path to button1')
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        item = svc.th.search(button_path)
        pth.ver.verify_equal('press me!', item['value'])
        pth.ver.verify_true(svc.th.exists(button_path))

        pth.proto.step('check if 1st item in path is not found')
        button_path = ['windowx', 'page1_frame', 'button_frame', 'button1']
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('check if middle item in path is not found')
        button_path = ['window1', 'pagex_frame', 'page']
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])
        pth.ver.verify_false(svc.th.exists(button_path))
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('check if last item in path is not found')
        button_path = ['window1', 'page_frame', 'pagex']
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('check if path is an empty list')
        button_path = []
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is empty', item['reason'], reqids=['SRS-025'])
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('check if search path list is None')
        button_path = None
        item = svc.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is None', item['reason'], reqids=['SRS-025'])
        pth.ver.verify_false(svc.th.exists(button_path))

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
