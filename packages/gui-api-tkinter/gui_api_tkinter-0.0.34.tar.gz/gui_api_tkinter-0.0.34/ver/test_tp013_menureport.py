import time
import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp013(unittest.TestCase):

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
    def test_tp013(self):  # pylint: disable=too-many-statements
        pth.proto.protocol('tp-013', 'check menu_report functions')
        pth.proto.add_objective('check that menu_click() invokes menu items at various menu levels')
        pth.proto.add_objective('check that menu_click() responds with accurate nak json objects')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{svc.th.version}')

        pth.proto.step('start gui')
        svc.helper.start_process()
        time.sleep(0.001)  # not needed but keeps time import
        pth.ver.verify_true(svc.helper.gui_process.is_alive())
        pth.ver.verify_false(svc.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        svc.th.connect()
        pth.ver.verify_true(svc.th.is_connected())

        pth.proto.step('check menu_report with missing content')
        paths = svc.th.menu_report()
        pth.ver.verify_none(paths)

        pth.proto.step('get menu_state with missing content')
        rsp = svc.th.menu_item(svc.helper.submenu_nested2)
        pth.ver.verify_equal('nak', rsp['value'])
        pth.ver.verify_equal('content is None', rsp['reason'])

        pth.proto.step('get page content')
        svc.th.get_screen()
        pth.ver.verify_gt(len(svc.th.content), 0)

        pth.proto.step('get menu_report with screen content')

        # uncomment to get current screen content
        # import json
        # print(f'DBG {json.dumps(svc.th.content, indent=4)}')

        # uncomment to print menu_paths to stdout
        # for path, info in svc.th.menu_paths.items():
        #     svc.logger.info(f'DBG report: {path} {info}')

        paths = svc.th.menu_report()
        pth.ver.verify_equal(10, len(paths))
        pth.ver.verify_equal(('File', 'later'), paths[0])
        pth.ver.verify_equal(('File', 'Nestedf1', 'nestedf111'), paths[1])
        pth.ver.verify_equal(('File', 'Nestedf1', 'nestedf112'), paths[2])
        pth.ver.verify_equal(('File', 'Nestedf1', 'nestedf113'), paths[3])
        pth.ver.verify_equal(('File', 'Nestedf2', 'nestedf221'), paths[4])
        pth.ver.verify_equal(('File', 'Nestedf2', 'nestedf222'), paths[5])
        pth.ver.verify_equal(('File', 'Nestedf2', 'nestedf223'), paths[6])
        pth.ver.verify_equal(('File', 'Exit'), paths[7])
        pth.ver.verify_equal(('Other', 'Clear'), paths[8])
        pth.ver.verify_equal(('Other2',), paths[9])

        pth.proto.step('get menu_state with screen content')

        item = svc.th.menu_item(svc.helper.submenu_nested2)
        pth.ver.verify_equal('nestedf112', item['label'])
        pth.ver.verify_equal('normal', item['state'])

        item = svc.th.menu_item(svc.helper.submenu_nested3)
        pth.ver.verify_equal('nestedf113', item['label'])
        pth.ver.verify_equal('disabled', item['state'])

        # note: a single item tuple requires the trailing "," to be evaluated
        # as a tuple. A single item list can be also be used.
        item = svc.th.menu_item(['Other2'])
        pth.ver.verify_equal('Other2', item['label'])
        pth.ver.verify_equal('normal', item['state'])

        # list converted to a tuple
        item = svc.th.menu_item(['File', 'later'])
        pth.ver.verify_equal('later', item['label'])
        pth.ver.verify_equal('normal', item['state'])

        # invalid menu_path
        rsp = svc.th.menu_item([])
        pth.ver.verify_equal('nak', rsp['value'])
        pth.ver.verify_equal('menu path is empty', rsp['reason'])

        rsp = svc.th.menu_item(None)
        pth.ver.verify_equal('nak', rsp['value'])
        pth.ver.verify_equal('menu path is None', rsp['reason'])

        rsp = svc.th.menu_item(('bad path'))
        pth.ver.verify_equal('nak', rsp['value'])
        pth.ver.verify_equal('menu path is not found', rsp['reason'])

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected())
