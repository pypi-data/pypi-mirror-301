import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp011(unittest.TestCase):

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
    def test_tp011(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-011', 'check "lbox_select" function')
        pth.proto.add_objective('check that lbox_select() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select() respond with accurate nak json objects')
        pth.proto.add_objective('check that lbox_select_on() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that lbox_select_at() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select_at() respond with accurate nak json objects')
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

        pth.proto.step('get page content')
        svc.th.get_screen()
        pth.ver.verify_gt(len(svc.th.content), 0)

        # uncomment for debug
        # print(f'DBG {json.dumps(svc.th.content, indent=4)}')

        pth.proto.step('check initial Listbox widget information')
        lbox_path = ['window1', 'page1_frame', 'button_frame', 'listbox1']
        item = svc.th.search(lbox_path)
        pth.ver.verify_equal('Listbox', item['class'])
        pth.ver.verify_equal('listbox1', item['name'], reqids=['SRS-110'])
        pth.ver.verify_equal(['lbox_item1', 'lbox_item2', 'lbox_item3', 'lbox_item4'],
                             item['value'], reqids='SRS-110')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-110')

        label3_path = ['window1', 'page1_frame', 'button_frame', 'label3']

        # === lbox_select_on
        opt_id = 1  # lbox_item2
        pth.proto.step('select an option on the Listbox widget')
        item = svc.th.search(lbox_path)
        svc.th.lbox_select_on(item, opt_id)

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item2"')
        svc.th.get_screen()
        label3 = svc.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item2', label3['value'], reqids=['SRS-111', 'SRS-112'])

        opt_id = [2]  # lbox_item3
        pth.proto.step('select another option on the Listbox widget')
        item = svc.th.search(lbox_path)
        svc.th.lbox_select_on(item, opt_id)

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item3"')
        svc.th.get_screen()
        label3 = svc.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item3', label3['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select()
        opt_id = 3  # lbox_item4
        pth.proto.step('lbox_select() on lbox1 using search path')
        ack_nak = svc.th.lbox_select(lbox_path, opt_id)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item4"')
        svc.th.get_screen()
        label3 = svc.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item4', label3['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select_at()
        pth.proto.step('lbox_select_at() on lbox1 using raw x, y coordinates')
        lbox = svc.th.search(lbox_path)
        x = int((lbox['coordinates']['x1'] + lbox['coordinates']['x2']) / 2)
        y = int((lbox['coordinates']['y1'] + lbox['coordinates']['y2']) / 2)
        ack_nak = svc.th.lbox_select_at(x, y, 1)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the selected option is "lbox_item2"')
        svc.th.get_screen()
        item = svc.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item2', item['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select_on()
        pth.proto.step('lbox_select_on() with None item')
        ack_nak = svc.th.lbox_select_on(None, 3)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select item is None', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with missing coordinates')
        ack_nak = svc.th.lbox_select_on({}, 'h')
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select item missing coordinates values', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with None opt_ids')
        ack_nak = svc.th.lbox_select_on(item, None)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with empty opt_ids')
        ack_nak = svc.th.lbox_select_on(item, 0)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select opt_ids is empty', ack_nak['reason'], reqids=['SRS-114'])

        # === lbox_select()
        pth.proto.step('lbox_select() with None path')
        ack_nak = svc.th.lbox_select(None, 1)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select path is None', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with empty path')
        ack_nak = svc.th.lbox_select([], 2)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select path is empty', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with unknown path')
        ack_nak = svc.th.lbox_select(['windowx1'], [3])
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with None opt_ids')
        ack_nak = svc.th.lbox_select(['window1'], None)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with empty opt_ids')
        ack_nak = svc.th.lbox_select(['window1'], [])
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select opt_ids is empty', ack_nak['reason'], reqids=['SRS-113'])

        # === lbox_select_at()
        pth.proto.step('lbox_select_at() with bad x coordinate')
        ack_nak = svc.th.lbox_select_at(1.23, 10, 1)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('lbox_select_at() with bad y coordinate')
        ack_nak = svc.th.lbox_select_at(10, 1.23, 2)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('lbox_select_at() with None opt_ids')
        ack_nak = svc.th.lbox_select_at(10, 20, None)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
