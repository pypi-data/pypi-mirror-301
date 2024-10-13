import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp012(unittest.TestCase):

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
    def test_tp012(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-012', 'check "cbox_select" function')
        pth.proto.add_objective('check that cbox_select() correctly sets option in a Combobox widget')
        pth.proto.add_objective('check that cbox_select() respond with accurate nak json objects')
        pth.proto.add_objective('check that cbox_select_on() correctly sets option in a Combobox widget')
        pth.proto.add_objective('check that cbox_select_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that cbox_select_at() correctly sets option in a Combobox widget')
        pth.proto.add_objective('check that cbox_select_at() respond with accurate nak json objects')
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

        pth.proto.step('check initial Combobox widget information')
        widget_path = ['window1', 'page1_frame', 'button_frame', 'combobox1']
        item = svc.th.search(widget_path)
        pth.ver.verify_equal('TCombobox', item['class'])
        pth.ver.verify_equal('combobox1', item['name'], reqids=['SRS-120'])
        pth.ver.verify_equal('', item['value'], reqids='SRS-120')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-120')

        # === combobox_set_on
        opt_id = 'combobox_opt1'
        pth.proto.step('set option on the Combobox widget')
        item = svc.th.search(widget_path)
        svc.th.combobox_set_on(item, opt_id)

        pth.proto.step('verify the contents of the combobox widget have changed to "combobox_opt1"')
        svc.th.get_screen()
        item = svc.th.search(widget_path)
        pth.ver.verify_equal('combobox_opt1', item['value'], reqids=['SRS-121', 'SRS-122'])

        # === combobox_set()
        opt_id = 'combobox_opt2'
        pth.proto.step('combobox_set() on combobox1 using search path')
        ack_nak = svc.th.combobox_set(widget_path, opt_id)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the combobox widget have changed to "combobox_opt2"')
        svc.th.get_screen()
        item = svc.th.search(widget_path)
        pth.ver.verify_equal('combobox_opt2', item['value'], reqids=['SRS-121', 'SRS-122'])

        # === combobox_set_at()
        pth.proto.step('combobox_set_at() on combobox1 using raw x, y coordinates')
        combobox = svc.th.search(widget_path)
        x = int((combobox['coordinates']['x1'] + combobox['coordinates']['x2']) / 2)
        y = int((combobox['coordinates']['y1'] + combobox['coordinates']['y2']) / 2)
        ack_nak = svc.th.combobox_set_at(x, y, 'combobox_opt3')
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the selected option is "combobox_opt3"')
        svc.th.get_screen()
        item = svc.th.search(widget_path)
        pth.ver.verify_equal('combobox_opt3', item['value'], reqids=['SRS-121', 'SRS-122'])

        # === combobox_set_on()
        pth.proto.step('combobox_set_on() with None item')
        ack_nak = svc.th.combobox_set_on(None, 3)
        pth.ver.verify_equal('combobox_set_on', ack_nak['rsp'], reqids=['SRS-124'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-124'])
        pth.ver.verify_equal('combobox set item is None', ack_nak['reason'], reqids=['SRS-124'])

        pth.proto.step('combobox_set_on() with missing coordinates')
        ack_nak = svc.th.combobox_set_on({}, 'h')
        pth.ver.verify_equal('combobox_set_on', ack_nak['rsp'], reqids=['SRS-124'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-124'])
        pth.ver.verify_equal('combobox set item missing coordinates values', ack_nak['reason'], reqids=['SRS-124'])

        pth.proto.step('combobox_set_on() with None opt_id')
        ack_nak = svc.th.combobox_set_on(item, None)
        pth.ver.verify_equal('combobox_set_on', ack_nak['rsp'], reqids=['SRS-124'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-124'])
        pth.ver.verify_equal('combobox set opt_id is None', ack_nak['reason'], reqids=['SRS-124'])

        pth.proto.step('combobox_set_on() with empty opt_id')
        ack_nak = svc.th.combobox_set_on(item, 0)
        pth.ver.verify_equal('combobox_set_on', ack_nak['rsp'], reqids=['SRS-124'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-124'])
        pth.ver.verify_equal('combobox set opt_id is empty', ack_nak['reason'], reqids=['SRS-124'])

        # === combobox_set()
        pth.proto.step('combobox_set() with None path')
        ack_nak = svc.th.combobox_set(None, 1)
        pth.ver.verify_equal('combobox_set', ack_nak['rsp'], reqids=['SRS-123'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-123'])
        pth.ver.verify_equal('combobox set path is None', ack_nak['reason'], reqids=['SRS-123'])

        pth.proto.step('combobox_set() with empty path')
        ack_nak = svc.th.combobox_set([], 2)
        pth.ver.verify_equal('combobox_set', ack_nak['rsp'], reqids=['SRS-123'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-123'])
        pth.ver.verify_equal('combobox set path is empty', ack_nak['reason'], reqids=['SRS-123'])

        pth.proto.step('combobox_set() with unknown path')
        ack_nak = svc.th.combobox_set(['windowx1'], [3])
        pth.ver.verify_equal('combobox_set', ack_nak['rsp'], reqids=['SRS-123'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-123'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-123'])

        pth.proto.step('combobox_set() with None opt_id')
        ack_nak = svc.th.combobox_set(['window1'], None)
        pth.ver.verify_equal('combobox_set', ack_nak['rsp'], reqids=['SRS-123'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-123'])
        pth.ver.verify_equal('combobox set opt_id is None', ack_nak['reason'], reqids=['SRS-123'])

        pth.proto.step('combobox_set() with empty opt_id')
        ack_nak = svc.th.combobox_set(['window1'], [])
        pth.ver.verify_equal('combobox_set', ack_nak['rsp'], reqids=['SRS-123'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-123'])
        pth.ver.verify_equal('combobox set opt_id is empty', ack_nak['reason'], reqids=['SRS-123'])

        # === combobox_set_at()
        pth.proto.step('combobox_set_at() with bad x coordinate')
        ack_nak = svc.th.combobox_set_at(1.23, 10, 1)
        pth.ver.verify_equal('combobox_set_at', ack_nak['rsp'], reqids=['SRS-125'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-125'])
        pth.ver.verify_equal('combobox set x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-125'])

        pth.proto.step('combobox_set_at() with bad y coordinate')
        ack_nak = svc.th.combobox_set_at(10, 1.23, 2)
        pth.ver.verify_equal('combobox_set_at', ack_nak['rsp'], reqids=['SRS-125'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-125'])
        pth.ver.verify_equal('combobox set y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-125'])

        pth.proto.step('combobox_set_at() with None opt_id')
        ack_nak = svc.th.combobox_set_at(10, 20, None)
        pth.ver.verify_equal('combobox_set_at', ack_nak['rsp'], reqids=['SRS-125'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-125'])
        pth.ver.verify_equal('combobox set opt_id is None', ack_nak['reason'], reqids=['SRS-125'])

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
