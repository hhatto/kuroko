Kuroko
=======
Minimalistic Python Bot Framework


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
5sec interval task execution

.. code-block:: python

    import kuroko

    class MyBot(kuroko.Bot):

        @kuroko.timer(5)
        def echo_pong(self):
            print("pong")

    bot = MyBot()
    bot.start()

crontab like task execution

.. code-block:: python

    class MyBot(kuroko.Bot):

        @kuroko.crontab('*/5 * * * *')
        def echo_pong(self):
            print("pong")

watchdog_ thin wrapper

.. code-block:: python

    class MyBot(kuroko.Bot):

        @kuroko.watch
        def echo_pong(self, event):
            print("pong", event)

        @kuroko.watch(patterns=['*.py'])
        def echo_ping(self, event):
            print("ping", event)


.. _watchdog: https://pypi.python.org/pypi/watchdog

License
-------
MIT
