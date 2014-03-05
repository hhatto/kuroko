import os
from kuroko import Bot, watch

basepath = os.path.dirname(os.path.abspath(__file__))

class MyBot(Bot):

    @watch(basepath, patterns=['*.txt'], recursive=True)
    def echo_pong(self, event):
        print(event, "change [%s]" % event.src_path)


bot = MyBot()
bot.start()
