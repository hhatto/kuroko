import okonomi


class MyBot(okonomi.Bot):

    @okonomi.crontab('*/2 * * * *')
    def echo_pong(self):
        print("pong")


bot = MyBot()
bot.start()
