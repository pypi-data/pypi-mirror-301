import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp006(unittest.TestCase):

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
    def test_tp006(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-006', 'check information for various widgets')
        pth.proto.add_objective('check informaion for root window is accurate')
        pth.proto.add_objective('check informaion for Frame widgets is accurate')
        pth.proto.add_objective('check informaion for Button widgets is accurate')
        pth.proto.add_objective('check informaion for Label widgets is accurate')
        pth.proto.add_objective('check informaion for Entry widgets is accurate')
        pth.proto.add_objective('check informaion for Radiobutton widgets is accurate')
        pth.proto.add_objective('check informaion for Listbox widgets is accurate')
        pth.proto.add_objective('check informaion for Combobox widgets is accurate')
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

        pth.proto.step('check window information')
        item = svc.th.search(['window1'])
        pth.ver.verify_equal('Tk', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('window1', item['name'], reqids=['SRS-040', 'SRS-043'])
        pth.ver.verify_equal('Ver Version: Ver v1.2.3', item['title'], reqids='SRS-043')
        prefix = item['geometry'][0:7]
        pth.ver.verify_equal('400x300', prefix, reqids='SRS-043')

        pth.proto.step('check frame information')
        item = svc.th.search(['window1', 'page1_frame'])
        pth.ver.verify_equal('Frame', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('page1_frame', item['name'], reqids=['SRS-044', 'SRS-041'])
        pth.ver.verify_equal('<unknown>', item['value'], reqids='SRS-044')
        pth.ver.verify_equal('<unknown>', item['state'], reqids='SRS-044')

        pth.proto.step('check button information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'button1'])
        pth.ver.verify_equal('Button', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('button1', item['name'], reqids=['SRS-070', 'SRS-041'])
        pth.ver.verify_equal('press me!', item['value'], reqids='SRS-070')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-070')

        pth.proto.step('check label information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'label1'])
        pth.ver.verify_equal('Label', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('label1', item['name'], reqids=['SRS-080', 'SRS-041'])
        pth.ver.verify_equal('state: 0', item['value'], reqids='SRS-080')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-080')

        pth.proto.step('check entry information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'entry1'])
        pth.ver.verify_equal('Entry', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('entry1', item['name'], reqids=['SRS-090', 'SRS-041'])
        pth.ver.verify_equal('', item['value'], reqids='SRS-090')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-090')

        pth.proto.step('check radiobutton information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'rb1'])
        pth.ver.verify_equal('Radiobutton', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('rb1', item['name'], reqids=['SRS-090', 'SRS-041'])
        pth.ver.verify_equal('option1', item['value'], reqids='SRS-090')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-090')

        pth.proto.step('check listbox information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'listbox1'])
        pth.ver.verify_equal('Listbox', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('listbox1', item['name'], reqids=['SRS-110', 'SRS-041'])
        pth.ver.verify_equal(['lbox_item1', 'lbox_item2', 'lbox_item3', 'lbox_item4'],
                             item['value'], reqids='SRS-110')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-110')

        pth.proto.step('check combobox information')
        item = svc.th.search(['window1', 'page1_frame', 'button_frame', 'combobox1'])
        pth.ver.verify_equal('TCombobox', item['class'], reqids='SRS-042')
        pth.ver.verify_equal('combobox1', item['name'], reqids=['SRS-120', 'SRS-041'])
        pth.ver.verify_equal('', item['value'], reqids='SRS-120')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-120')

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
