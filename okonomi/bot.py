import time
from multiprocessing import Process
import logbook
from crontab import CronTab


class Bot(object):

    """Okonomi Bot Object"""

    funcs = []

    def __init__(self, daemonize=False, debug=False):
        self.daemonize = daemonize
        self.procs = []
        logging_level = logbook.INFO if not debug else logbook.DEBUG
        self.log = logbook.Logger('okonomi', logging_level)

    def _register(self, func, options):
        self.log.debug('register func: @%s.%s' % (func.__name__, options['callback'].__name__))
        self.procs.append(Process(target=func, args=(options, )))

    def exe_timer(self, options):
        callback = options['callback']
        while True:
            callback(self)
            time.sleep(options['interval'])

    @classmethod
    def timer(self, interval=1):
        def _timer(func):
            self.funcs.append({'function': 'exe_timer', 'options': {'interval': interval, 'callback': func}})
        return _timer

    def exe_crontab(self, options):
        callback = options['callback']
        entry = CronTab(options['schedule'])
        while True:
            time.sleep(entry.next())
            callback(self)

    @classmethod
    def crontab(self, schedule='* * * * *'):
        def _timer(func):
            self.funcs.append({'function': 'exe_crontab', 'options': {'schedule': schedule, 'callback': func}})
        return _timer

    def start(self):
        self.log.debug("start bot...")
        for func in self.funcs:
            self._register(getattr(self, func['function']), options=func['options'])
        for proc in self.procs:
            proc.start()
        try:
            # TODO: busy loop, now
            while True:
                self.log.debug("busy loop")
                time.sleep(1)
        except KeyboardInterrupt:
            for proc in self.procs:
                if proc.is_alive():
                    proc.terminate()
            for proc in self.procs:
                proc.join()
            print("Goodby")


timer = Bot.timer
crontab = Bot.crontab
