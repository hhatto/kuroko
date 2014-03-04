import okonomi


class MyBot(okonomi.Bot):

    @okonomi.watch
    def echo_pong(self, event):
        print(event, "change [%s]" % event.src_path)


bot = MyBot()
bot.start()
