Kuroko
=======
.. image:: https://travis-ci.org/hhatto/kuroko.svg?branch=master
    :target: https://travis-ci.org/hhatto/kuroko

Minimalistic Python Task Executor Framework


Requirements
============
- Python2.7+
- Logbook_
- crontab_
- watchdog_

.. _Logbook: https://pypi.python.org/pypi/Logbook
.. _crontab: https://pypi.python.org/pypi/crontab


Installation
============

::

    pip install kuroko


Usage
=====
examples

5sec interval task execution
----------------------------

.. code-block:: python

    import kuroko

    class MyBot(kuroko.Bot):

        @kuroko.timer(5)
        def echo_pong(self):
            print("pong")

    bot = MyBot()
    bot.start()

crontab like task execution
---------------------------

.. code-block:: python

    class MyBot(kuroko.Bot):

        @kuroko.crontab('*/5 * * * *')
        def echo_pong(self):
            print("pong")

watchdog_ thin wrapper
----------------------

.. code-block:: python

    class MyBot(kuroko.Bot):

        @kuroko.watch
        def echo_pong(self, event):
            print("pong", event)

        @kuroko.watch(patterns=['*.py'])
        def echo_ping(self, event):
            print("ping", event)


.. _watchdog: https://pypi.python.org/pypi/watchdog

logging
-------

.. code-block:: python

    class MyBot(kuroko.Bot):

        @kuroko.crontab('*/5 * * * *')
        def echo_pong(self):
            self.log.info("app logging")


Restart & Stop task
-------------------
send a SIGUSR1 when you want to restart the all tasks,
send a SIGHUP when you want to stop the all tasks.


TODO
====
- [ ] support multi-thread model
- [ ] colorize logging
- [ ] statistics web frontend
- [ ] terminal like interface


License
=======
MIT
