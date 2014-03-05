from kuroko import Bot, timer


class MyBot(Bot):

    @timer(5)
    def echo_pong(self):
        print("pong")


bot = MyBot()
bot.start()
