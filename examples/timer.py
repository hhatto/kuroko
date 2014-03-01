import okonomi


class MyBot(okonomi.Bot):

    @okonomi.timer(5)
    def echo_pong(self):
        print("pong")


bot = MyBot()
bot.start()
