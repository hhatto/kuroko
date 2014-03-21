import time
import functools
from multiprocessing import Process, Queue
import logbook
from crontab import CronTab
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class _ProxyEventHandler(PatternMatchingEventHandler):

    def _set_queue(self, queue):
        self.passing_queue = queue

    def on_any_event(self, event):
        """passing all event to callback function"""
        self.passing_queue.put(event)


class Bot(object):

    """Kuroko Bot Object"""

    funcs = []

    def __init__(self, daemonize=False, debug=False):
        self.daemonize = daemonize  # TODO: not implementation
        self.procs = []
        logging_level = logbook.INFO if not debug else logbook.DEBUG
        # Logging Object for Bot Object
        self._ = logbook.Logger('[kuroko system]', logging_level)
        # Logging Object for User definition functions
        self.log = logbook.Logger('[kuroko user]', logging_level)

    def _register(self, func, options):
        self._.debug('register func: @%s.%s' % (func.__name__, options['callback'].__name__))
        self.procs.append(Process(target=func, args=(options, )))

    def exe_timer(self, options):
        callback = options['callback']
        while True:
            callback(self)
            time.sleep(options['interval'])

    @classmethod
    def timer(self, obj=None, *args, **kwargs):
        if callable(obj):
            # not exist arg
            func = obj
            def _timer(interval=60):
                self.funcs.append({'function': 'exe_timer',
                                   'options': {'interval': interval, 'callback': func}})
            return _timer()
        else:
            # exist arg(s)
            _args = [obj] + list(args)
            def _timer(func):
                def _inner_timer(self, interval=60):
                    self.funcs.append({'function': 'exe_timer',
                                       'options': {'interval': interval, 'callback': func}})
                return _inner_timer(self, *_args, **kwargs)
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
            self.funcs.append({'function': 'exe_crontab',
                               'options': {'schedule': schedule, 'callback': func}})
        return _timer

    def exe_watch(self, options):
        callback = options['callback']
        path = options['path']
        ev = _ProxyEventHandler(options['patterns'], options['ignore_patterns'],
                                options['ignore_directories'], options['case_sensitive'])
        passing_queue = Queue()
        ev._set_queue(passing_queue)
        observer = Observer()
        observer.schedule(ev, path, options['recursive'])
        observer.start()
        try:
            while True:
                event = passing_queue.get()
                callback(self, event)
        except:
            observer.stop()

    @classmethod
    def watch(self, obj=None, *args, **kwargs):
        if callable(obj):
            # not exist arg
            func = obj
            @functools.wraps(obj)
            def _watch():
                self.funcs.append({'function': 'exe_watch',
                                   'options': {'path': '.', 'callback': func, 'patterns': ['*'],
                                               'ignore_patterns': None, 'ignore_directories': None,
                                               'recursive': False, 'case_sensitive': False}})
            return _watch()
        else:
            # exist arg(s)
            _args = [obj] + list(args)
            def _watch(func):
                def _inner_watch(self, path='.', patterns=['*'], ignore_patterns=None, ignore_directories=None, recursive=True, case_sensitive=False):
                    self.funcs.append({'function': 'exe_watch',
                                       'options': {'path': path, 'callback': func, 'patterns': patterns,
                                                   'ignore_patterns': ignore_patterns,
                                                   'ignore_directories': ignore_directories,
                                                   'recursive': recursive,
                                                   'case_sensitive': case_sensitive}})
                return _inner_watch(self, *_args, **kwargs)
            return _watch

    def start(self):
        self._.info("start bot...")
        for func in self.funcs:
            self._register(getattr(self, func['function']), options=func['options'])
        for proc in self.procs:
            proc.start()
        try:
            # TODO: busy loop, now
            while True:
                self._.debug("busy loop")
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
watch = Bot.watch
