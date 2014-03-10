from kuroko import Bot, timer
from datetime import datetime

class MyBot(Bot):

    @timer
    def echo_pong(self):
        print(datetime.now(), "pong")


bot = MyBot()
bot.start()
