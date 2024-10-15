import time
from os import stat
from os.path import realpath
from signal import signal as bind
from sys import argv, exit

from kalib.descriptors import cache
from kalib.logging import Logging

Logger = Logging.Default
NeedRestart = False


@cache
def get_selfpath():
    return realpath(argv[0])


def get_mtime():
    return stat(get_selfpath()).st_mtime


@cache
def quit_at(*, func=exit, signal=None, errno=137, **kw):

    def signal_handler(signum, frame):
        global NeedRestart
        NeedRestart = True
        Logger.warning(f'{signal=} received, mark restart as needed')

    if signal:
        bind(signal, signal_handler)

    initial_stamp = get_mtime()
    def on_change(*, sleep=0.0):

        if NeedRestart and signal:
            Logger.warning(f'{signal=} received, quit..')
            func(errno)
            return False

        elif initial_stamp != (ctime := get_mtime()):
            file = get_selfpath()
            Logger.warning(
                f'{file=} updated {time.time() - ctime:.2f} seconds ago, quit..')
            func(errno)
            return False

        if sleep := (sleep or kw.get('sleep', 0.0)):
            time.sleep(sleep)
        return True
    return on_change
