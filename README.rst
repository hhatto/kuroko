Okonomi
=======
Minimalistic Python Bot Framework


Requirements
============
- Python2.7+
- Logbook

Installation
============

::

    pip install okonomi


Usage
=====
5sec interval task execution

.. code-block:: python

    import okonomi

    class MyBot(okonomi.Bot):

        @okonomi.timer(5)
        def echo_pong(self):
            print("pong")

    bot = MyBot()
    bot.start()

crontab like task execution

.. code-block:: python

    class MyBot(okonomi.Bot):

        @okonomi.crontab('*/5 * * * *')
        def echo_pong(self):
            print("pong")

watchdog_ thin wrapper

.. code-block:: python

    class MyBot(okonomi.Bot):

        @okonomi.watch
        def echo_pong(self, event):
            print("pong", event)

        @okonomi.watch(patterns=['*.py'])
        def echo_ping(self, event):
            print("ping", event)


.. _watchdog: https://pypi.python.org/pypi/watchdog


Okonomi?
========
Okonomi is Soul Food in Osaka City!
Okonomiyaki_ is official name.

.. _Okonomiyaki: http://en.wikipedia.org/wiki/Okonomiyaki

