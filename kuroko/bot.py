import signal
import time
import functools
from multiprocessing import Process, Queue
import logbook
from crontab import CronTab
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class _ProxyEventHandler(PatternMatchingEventHandler):

    """watchdog event handler"""

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
        self.procs = {}
        self.restart_flag = False
        self.terminate_flag = False
        logging_level = logbook.INFO if not debug else logbook.DEBUG
        # Logging Object for Bot Object
        self._ = logbook.Logger('[kuroko system]', logging_level)
        # Logging Object for User definition functions
        self.log = logbook.Logger('[kuroko user]', logging_level)
        signal.signal(signal.SIGUSR1, self._reload_signal_handler)
        signal.signal(signal.SIGHUP, self._stop_signal_handler)

    def _reload_signal_handler(self, signum, frame):
        self._.debug("realod all task")
        self.restart_flag = True

    def _stop_signal_handler(self, signum, frame):
        self._.debug("stop all task")
        self.terminate_flag = True

    def _register(self, func, options):
        self._.debug('register func: @%s.%s' % (func.__name__, options['callback'].__name__))
        p = Process(target=func, name=options['callback'].__name__, args=(options, ))
        self.procs[options['callback'].__name__] = {'procobj': p, 'function': func, 'options': options}
        return p

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
        # FIXME: change to offset not used implementation
        # problem of callback function twice time when process died.
        old_sleep_time = entry.next()
        while True:
            sleep_time = entry.next()
            if sleep_time > old_sleep_time:
                callback(self)
            old_sleep_time = sleep_time
            time.sleep(1)

    @classmethod
    def crontab(self, schedule='* * * * *'):
        def _crontab(func):
            self.funcs.append({'function': 'exe_crontab',
                               'options': {'schedule': schedule, 'callback': func}})
        return _crontab

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

    def _check_proc(self, autorestart=True):
        """alive monitoring"""
        restart_proc_name = []
        for procname, proc in self.procs.items():
            if not proc['procobj'].is_alive():
                self._.warn("'%s' func not alive" % procname)
                if autorestart:
                    restart_proc_name.append(procname)
        for procname in restart_proc_name:
            p = self._register(getattr(self, self.procs[procname]['function'].__name__), options=self.procs[procname]['options'])
            self._.warn("'%s' func restart" % p.name)
            p.start()

    def start(self):
        """Bot start method"""
        self._.info("start bot...")
        for func in self.funcs:
            self._register(getattr(self, func['function']), options=func['options'])
        for proc in self.procs.values():
            proc['procobj'].start()
        try:
            # TODO: busy loop, now
            while True:
                self._.debug("busy loop")
                if self.restart_flag or self.terminate_flag:
                    for proc in self.procs.values():
                        print("start", proc['procobj'], proc['procobj'].is_alive())
                        if proc['procobj'].is_alive():
                            self._.debug("terminate")
                            proc['procobj'].terminate()
                        print("end", proc['procobj'], proc['procobj'].is_alive())
                if self.restart_flag:
                    self._check_proc(self)
                    self.restart_flag = False
                if self.terminate_flag:
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            for proc in self.procs.values():
                if proc['procobj'].is_alive():
                    proc['procobj'].terminate()
            for proc in self.procs.values():
                proc['procobj'].join()
            print("Goodby")


timer = Bot.timer
crontab = Bot.crontab
watch = Bot.watch
