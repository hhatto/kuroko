from kuroko import Bot, crontab


class MyBot(Bot):

    @crontab('*/2 * * * *')
    def echo_pong(self):
        print("pong")


bot = MyBot()
bot.start()
