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


Okonomi?
========
Okonomi is Soul Food in Osaka City!
Okonomiyaki_ is official name.

.. _Okonomiyaki: http://en.wikipedia.org/wiki/Okonomiyaki

