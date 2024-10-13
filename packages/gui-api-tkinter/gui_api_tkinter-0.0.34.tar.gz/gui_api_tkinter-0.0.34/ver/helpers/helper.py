import sys
import time

from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from tools.xplat_utils.utils_logger import UtilsLogger as logger
from ver.helpers import svc
from ver.helpers.cmd_runner import CmdRunner


# --------------------
class Helper:

    # --------------------
    def __init__(self):
        self.gui_process = None

        self.button1_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        self.label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']

        # menu paths
        self.menu_later_path = ('File', 'later')
        self.submenu_nested1 = ('File', 'Nestedf1', 'nestedf111')
        self.submenu_nested2 = ('File', 'Nestedf1', 'nestedf112')
        self.submenu_nested3 = ('File', 'Nestedf1', 'nestedf113')  # should be disabled
        self.menu_file_exit_path = ('File', 'Exit')
        self.menu_clear_path = ('Other', 'Clear')

    # --------------------
    def init(self):
        from ver.helpers.logger_stdout import Logger
        svc.logger = Logger()
        svc.th = GuiApiHarness()
        svc.th.init()
        # uncomment to get logging
        # svc.th.init(svc.logger)

    # --------------------
    def term(self):
        svc.th.term()

    # --------------------
    def init_each_test(self, ptobj):
        logger.line('')
        svc.pytself = ptobj

    # --------------------
    def term_each_test(self):
        self.kill_process()
        svc.pytself.assertFalse(self.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {svc.logger.lines}')

    # --------------------
    def start_process(self, args=''):
        # logger_args = ''
        # uncomment to get server/gui_api logging to out/ver_logger.txt
        logger_args = '--logger file'

        svc.logger.info(f'start_process: {args} {logger_args}')
        self.gui_process = CmdRunner()
        cmd = ''
        if sys.platform == 'win32':
            cmd = 'bash '
        cmd += f'ver/do_gui.sh {args} {logger_args}'
        self.gui_process.start_task_bg('gui', cmd, working_dir='.')
        # show it off for a bit
        time.sleep(1)

    # --------------------
    def kill_process(self):
        svc.logger.info('kill_process')
        self.gui_process.finish()

    # --------------------
    def clean_shutdown(self):
        svc.th.get_screen()
        # do a clean exit of the GUI using File | Exit
        self.click_file_exit_menuitem()
        time.sleep(0.500)
        svc.th.term()

    # --------------------
    @property
    def label1_text(self):
        item = svc.th.search(self.label1_path)
        return item['value']

    # --------------------
    def click_button1(self):
        svc.th.click_left(self.button1_path)

    # --------------------
    def click_clear_menuitem(self):
        svc.th.menu_click(self.menu_clear_path)

    # --------------------
    def click_file_exit_menuitem(self):
        svc.th.menu_click(self.menu_file_exit_path)

    # --------------------
    def click_later_menuitem(self):
        svc.th.menu_click(self.menu_later_path)

    # --------------------
    def click_nested1_menuitem(self):
        svc.th.menu_click(self.submenu_nested1)

    # --------------------
    def click_nested2_menuitem(self):
        svc.th.menu_click(self.submenu_nested2)

    # --------------------
    ## get some menu info
    #
    # @return None
    def getinfo(self):
        cmd = {
            'cmd': 'getinfo',
        }
        ack_nak = svc.th.send_recv(cmd)
        return ack_nak
