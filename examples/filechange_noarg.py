from kuroko import Bot, watch


class MyBot(Bot):

    @watch
    def echo_pong(self, event):
        print(event, "change [%s]" % event.src_path)


bot = MyBot()
bot.start()
