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
example of 5sec interval task

.. code-block:: python

    import okonomi

    class MyBot(okonomi.Bot):

        @okonomi.timer(5)
        def echo_pong(self):
            print("pong")

    bot = MyBot()
    bot.start()


Okonomi?
========
Okonomi is Japanese Soul Food!
Okonomi-yaki is official name.
