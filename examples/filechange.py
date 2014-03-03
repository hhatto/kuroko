import os
import okonomi

basepath = os.path.dirname(os.path.abspath(__file__))

class MyBot(okonomi.Bot):

    @okonomi.watch(basepath, patterns=['*.txt'], recursive=True)
    def echo_pong(self, event):
        print(event, "change [%s]" % event.src_path)


bot = MyBot()
bot.start()
