import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp003(unittest.TestCase):
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
    def test_tp003(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-003', 'check "click_left_at" with an invalid values')
        pth.proto.add_objective('check that click_left_at() respond with accurate nak json objects')
        pth.proto.add_objective('check that click_left_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that click_left() respond with accurate nak json objects')
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

        pth.proto.step('get page content and confirm initial state is "state: 0"')
        svc.th.get_screen()
        pth.ver.verify_gt(len(svc.th.content), 0)
        label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']
        label1 = svc.th.search(label1_path)
        pth.ver.verify_equal('state: 0', label1['value'], reqids=['SRS-051'])

        pth.proto.step('search using a valid path to button1')
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        button = svc.th.search(button_path)
        pth.ver.verify_equal('press me!', button['value'])

        # === click_left_on()
        pth.proto.step('click_left_on() on button1 using item returned from search')
        ack_nak = svc.th.click_left_on(button)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 1"')
        svc.th.get_screen()
        label1 = svc.th.search(label1_path)
        pth.ver.verify_equal('state: 1', label1['value'], reqids=['SRS-051'])

        # === click_left()
        pth.proto.step('click_left() on button1 using search path')
        ack_nak = svc.th.click_left(button_path)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 0"')
        svc.th.get_screen()
        label1 = svc.th.search(label1_path)
        pth.ver.verify_equal('state: 0', label1['value'], reqids=['SRS-051'])

        # === click_left_at()
        pth.proto.step('click_left_at() on button1 using raw x, y coordinates')
        button = svc.th.search(button_path)
        x = int((button['coordinates']['x1'] + button['coordinates']['x2']) / 2)
        y = int((button['coordinates']['y1'] + button['coordinates']['y2']) / 2)
        ack_nak = svc.th.click_left_at(x, y)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 1"')
        svc.th.get_screen()
        label1 = svc.th.search(label1_path)
        pth.ver.verify_equal('state: 1', label1['value'], reqids=['SRS-051'])

        # === click_left_on()
        pth.proto.step('click_left_on() with None item')
        ack_nak = svc.th.click_left_on(None)
        pth.ver.verify_equal('click_left_on', ack_nak['rsp'], reqids=['SRS-053'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-053'])
        pth.ver.verify_equal('click item is None', ack_nak['reason'], reqids=['SRS-053'])

        pth.proto.step('click_left_on() with missing coordinates')
        ack_nak = svc.th.click_left_on({})
        pth.ver.verify_equal('click_left_on', ack_nak['rsp'], reqids=['SRS-053'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-053'])
        pth.ver.verify_equal('click item missing coordinates values', ack_nak['reason'], reqids=['SRS-053'])

        # === click_left()
        pth.proto.step('click_left() with None path')
        ack_nak = svc.th.click_left(None)
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('click path is None', ack_nak['reason'], reqids=['SRS-052'])

        pth.proto.step('click_left() with empty path')
        ack_nak = svc.th.click_left([])
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('click path is empty', ack_nak['reason'], reqids=['SRS-052'])

        pth.proto.step('click_left() with unknown path')
        ack_nak = svc.th.click_left(['windowx1'])
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-052'])

        # === click_left_at()
        pth.proto.step('click_left_at() with bad x coordinate')
        ack_nak = svc.th.click_left_at(1.23, 10)
        pth.ver.verify_equal('click_left_at', ack_nak['rsp'], reqids=['SRS-054'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-054'])
        pth.ver.verify_equal('click x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-054'])

        pth.proto.step('click_left_at() with bad y coordinate')
        ack_nak = svc.th.click_left_at(10, 1.23)
        pth.ver.verify_equal('click_left_at', ack_nak['rsp'], reqids=['SRS-054'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-054'])
        pth.ver.verify_equal('click y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-054'])

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
