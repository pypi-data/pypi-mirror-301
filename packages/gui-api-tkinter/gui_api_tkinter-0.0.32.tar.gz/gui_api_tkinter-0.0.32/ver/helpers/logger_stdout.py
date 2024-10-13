import math
import sys
import time


# --------------------
## logger instance
class Logger:
    # --------------------
    ## initialize
    def __init__(self):
        ## holds count of the last time a flush was done
        self._flush_count = 0
        ## holds the last time a full DTS was written to the log
        self._start_time = 0

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        pass

    # --------------------
    ## write the message to stdout and save to the array for later processing
    #
    # @param msg  the message to log
    # @return None
    def info(self, msg):
        self._log('INFO', msg)

    # --------------------
    ## log a line
    #
    # @param tag    what kind of log line is it
    # @param msg    the text of the log line
    # @return None
    def _log(self, tag, msg):
        elapsed = time.time() - self._start_time
        if self._start_time == 0 or elapsed > 3600:
            self._start_time = time.time()
            ms_str = str(math.modf(self._start_time)[0])[2:5]
            tstr = time.strftime("%H:%M:%S.", time.localtime(self._start_time)) + ms_str
            dts = time.strftime("%Y/%m/%d", time.localtime(self._start_time))
            print(f'{tstr} {tag:<4} DTS on {dts}')
            elapsed = time.time() - self._start_time

        ms_str = str(math.modf(elapsed)[0])[2:5]
        tstr = time.strftime('%M:%S.', time.localtime(elapsed)) + ms_str
        print(f'{tstr} {tag} {msg}')

        self._flush_count += 1
        if self._flush_count > 5:
            self.flush()

    # --------------------
    ## flush the log
    #
    # @return None
    def flush(self):
        sys.stdout.flush()
