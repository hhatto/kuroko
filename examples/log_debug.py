from kuroko import Bot, timer


class MyBot(Bot):

    @timer(5)
    def echo_pong(self):
        print("pong")
        self.log.info("pong")


bot = MyBot(debug=True)
bot.start()
